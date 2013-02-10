# -*- coding: utf-8 -*-

#import datetime
#import time
#import random
from sqlalchemy import or_
#from mailer import Mailer
#from LocalFS import LocalFS
from Products.Five import BrowserView
from zope.interface import implements
from z3c.sqlalchemy import getSAWrapper
#from Products.CMFPlone.utils import normalizeString
#from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
#from Products.CMFPlone.utils import normalizeString
from Products.CMFCore.utils import getToolByName
#from Products.CMFPlone import PloneMessageFactory as _
#from Products.AddRemoveWidget.AddRemoveWidget import AddRemoveWidget
#from Products.Archetypes.atapi import LinesField
#from Products.Archetypes.Renderer import renderer
#from Products.Archetypes.atapi import BaseContent
from interfaces import IManageAuteur
#from collective.captcha.browser.captcha import Captcha


class ManageAuteur(BrowserView):
    implements(IManageAuteur)

    def getAllAuteurs(self):
        """
        table pg auteur
        recuperation de toutes les auteurs
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        AuteurTable = wrapper.getMapper('auteur')
        query = session.query(AuteurTable)
        query = query.order_by(AuteurTable.auteur_nom)
        allAuteurs = query.all()
        return allAuteurs

    def getAuteurByPk(self, auteurPk):
        """
        table pg auteur
        recuperation d'une auteur selon sa pk
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        AuteurTable = wrapper.getMapper('auteur')
        query = session.query(AuteurTable)
        query = query.filter(AuteurTable.auteur_pk == auteurPk)
        auteur = query.one()
        return auteur

    def getAuteurByLeffeSearch(self, searchString):
        """
        table pg auteur
        recuperation d'une Auteur via le livesearch
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        AuteurTable = wrapper.getMapper('auteur')
        query = session.query(AuteurTable)
        query = query.filter(or_(AuteurTable.auteur_nom.ilike("%%%s%%" % searchString),
                                 or_(AuteurTable.auteur_prenom.ilike("%%%s%%" % searchString))))
        auteur = ["%s" % (elem.auteur_nom) for elem in query.all()]
        return auteur

    def getSearchingAuteur(self, auteurPk=None, searchingLetter=None):
        """
        table pg auteur
        recuperation d'un auteur selon la pk
        la pk peut arriver via le form en hidden ou via un lien construit,
         (cas du listing de resultat de moteur de recherche)
        je teste si la pk arrive par param, si pas je prends celle du form
        """
        fields = self.request.form
        auteurNom = fields.get('auteurNom')
        if not auteurPk:
            auteurPk = fields.get('auteur_pk')

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        AuteurTable = wrapper.getMapper('Auteur')
        query = session.query(AuteurTable)
        if auteurNom:
            query = query.filter(AuteurTable.auteur_nom == auteurNom)
        if auteurPk:
            query = query.filter(AuteurTable.auteur_pk == auteurPk)
        if searchingLetter:
            query = query.filter(AuteurTable.auteur_nom.ilike("%%%s" % searchingLetter))
        allAuteurs = query.all()
        return allAuteurs

    def insertAuteur(self):
        """
        table pg auteur
        ajout d'un item Auteur
        """
        fields = self.request.form

        auteurNom = fields.get('auteurNom', None)
        auteurPrenom = fields.get('auteurPrenom', None)

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        insertAuteur = wrapper.getMapper('auteur')
        newEntry = insertAuteur(auteur_nom=auteurNom, \
                                auteur_prenom=auteurPrenom)
        session.add(newEntry)
        session.flush()
        session.refresh(newEntry)
        auteurPk = newEntry.auteur_pk

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Le nouvel auteur %s %s a bien été enregistré !" % (auteurNom, auteurPrenom)
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/documentation/auteur/ajouter-un-auteur" % (portalUrl)
        self.request.response.redirect(url)
        return ''

    def updateAuteur(self):
        """
        table pg auteur
        mise a jour d'un item auteur
        """
        fields = self.context.REQUEST
        auteurPk = getattr(fields, 'auteurPk')
        auteurNom = getattr(fields, 'auteurNom', None)
        auteurPrenom = getattr(fields, 'auteurPrenom', None)

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        updateAuteurTable = wrapper.getMapper('auteur')
        query = session.query(updateAuteurTable)
        query = query.filter(updateAuteurTable.auteur_pk == auteurPk)
        auteurs = query.all()
        for auteur in auteurs:
            auteur.auteur_nom = unicode(auteurNom, 'utf-8')
            auteur.auteur_prenom = unicode(auteurPrenom, 'utf-8')

        session.flush()
        cible = "%s/creation-d-un-auteur" % (self.context.portal_url(), )
        self.context.REQUEST.RESPONSE.redirect(cible)

    def gestionAuteur(self):
        """
        insertion ou update d'un auteur
        """
        fields = self.context.REQUEST
        operation = getattr(fields, 'operation')

        if operation == "insert":
            self.insertAuteur()

        if operation == "update":
            self.updateAuteur()
