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
from interfaces import IManageFormation
#from collective.captcha.browser.captcha import Captcha


class ManageFormation(BrowserView):
    implements(IManageFormation)

    def getAllFormations(self):
        """
        table pg formation
        recuperation de toutes les formations
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        FormationTable = wrapper.getMapper('formation')
        query = session.query(FormationTable)
        query = query.order_by(FormationTable.form_titre)
        allFormations = query.all()
        return allFormations

    def getFormationByPk(self, formationPk):
        """
        table pg formation
        recuperation d'une formation selon sa pk
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        FormationTable = wrapper.getMapper('formation')
        query = session.query(FormationTable)
        query = query.filter(FormationTable.for_pk == formationPk)
        formation = query.one()
        return formation

    def getFormationOpen(self):
        """
        table pg formation
        recuperation d'une formation selon son état ouverte
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        FormationTable = wrapper.getMapper('formation')
        query = session.query(FormationTable)
        query = query.filter(FormationTable.form_etat == 'ouvert')
        formationsOpen = query.all()
        return formationsOpen

    def getFormationByLeffeSearch(self, searchString):
        """
        table pg formation
        recuperation d'une formation via le livesearch
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        FormationTable = wrapper.getMapper('formation')
        query = session.query(FormationTable)
        query = query.filter(FormationTable.for_titre.ilike("%%%s%%" % searchString))
        formation = ["%s" % (elem.for_titre) for elem in query.all()]
        return formation

    def insertAuteur(self):
        """
        table pg auteur
        ajout d'un item Auteur
        """
        fields = self.request.form

        auteurNom = fields.get('auteurNom', None)
        auteurPrenom = fields.get('auteurPrenom', None)
        
        auteurNom = unicode(auteurNom, 'utf-8')
        auteurPrenom = unicode(auteurPrenom, 'utf-8')

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
        fields = self.request.form
        
        auteurPk = fields.get('auteurPk', None)
        auteurNom = fields.get('auteurNom', None)
        auteurPrenom = fields.get('auteurPrenom', None)

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

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"L'auteur %s %s a bien été modifié !" % (auteurNom, auteurPrenom)
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/documentation/auteur/auteur" % (portalUrl)
        self.request.response.redirect(url)
        return ''
        
    def gestionFormation(self):
        """
        insertion ou update d'une formation
        """
        fields = self.context.REQUEST
        operation = getattr(fields, 'operation')

        if operation == "insert":
            self.insertFormation()

        if operation == "update":
            self.updateFormation()
