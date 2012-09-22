# -*- coding: utf-8 -*-

#import datetime
#import time
#import random
#from sqlalchemy import select, func
#from mailer import Mailer
#from LocalFS import LocalFS
from Products.Five import BrowserView
from zope.interface import implements
from z3c.sqlalchemy import getSAWrapper
#from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
#from Products.CMFPlone.utils import normalizeString
#from Products.CMFCore.utils import getToolByName
#from Products.CMFPlone import PloneMessageFactory as _
#from Products.AddRemoveWidget.AddRemoveWidget import AddRemoveWidget
#from Products.Archetypes.atapi import LinesField
#from Products.Archetypes.Renderer import renderer
#from Products.Archetypes.atapi import BaseContent
from interfaces import IManageLivre
#from collective.captcha.browser.captcha import Captcha


class ManageLivre(BrowserView):
    implements(IManageLivre)

    def getAllLivres(self):
        """
        recuperation de tous les périodiques
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        LivreTable = wrapper.getMapper('Livre')
        query = session.query(LivreTable)
        query = query.order_by(LivreTable.per_titre)
        allLivres = query.all()
        return allLivres

    def getLivreByPk(self, LivrePk):
        """
        recuperation d'un Livre selon sa pk
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        LivreTable = wrapper.getMapper('Livre')
        query = session.query(LivreTable)
        query = query.filter(LivreTable.per_pk == LivrePk)
        Livre = query.one()
        return Livre

    def getAllLivresByLettre(self, lettre):
        """
        recuperation de tous les périodiques commencant par la lettre
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        LivreTable = wrapper.getMapper('Livre')
        query = session.query(LivreTable)
        query = query.filter(LivreTable.per_titre.like("%s" % lettre))
        query = query.order_by(LivreTable.per_titre)
        allLivres = query.all()
        return allLivres


    def getLivreByLeffeSearch(self, searchString):
        """
        table pg Livre
        recuperation d'un Livre via le lightsearch
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        LivreTable = wrapper.getMapper('Livre')
        query = session.query(LivreTable)
        query = query.filter(LivreTable.per_titre.ilike("%%%s%%" % searchString))
        Livre = ["%s" % (elem.per_titre) for elem in query.all()]
        return Livre

    def getSearchingLivre(self, LivrePk=None):
        """
        table pg Livre
        recuperation du Livre selon la pk
        la pk peut arriver via le form en hidden ou via un lien construit,
         (cas du listing de resultat de moteur de recherche)
        je teste si la pk arrive par param, si pas je prends celle du form
        """
        fields = self.request.form
        LivreTitre = fields.get('LivreTitre')
        if not LivrePk:
            LivrePk = fields.get('Livre_pk')

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        LivreTable = wrapper.getMapper('Livre')
        query = session.query(LivreTable)
        if LivreTitre:
            query = query.filter(LivreTable.per_titre == LivreTitre)
        if LivrePk:
            query = query.filter(LivreTable.per_pk == LivrePk)
        allLivres = query.all()
        return allLivres

    def addLivre(self):
        """
        ajout d'un item Livre
        """
        fields = self.context.REQUEST
        LivreTitre = getattr(fields, 'LivreTitre')
        LivreDescription = getattr(fields, 'LivreDescription', None)

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        insertLivre = wrapper.getMapper('Livre')
        newEntry = insertLivre(per_titre=LivreTitre, \
                                    per_description=LivreDescription)
        session.save(newEntry)
        session.flush()
        #cible = "%s/ajouter-un-Livre" % (self.context.portal_url(), )
        #self.context.REQUEST.RESPONSE.redirect(cible)

    def updateLivre(self):
        """
        mise a jour d'un item Livre
        """
        fields = self.context.REQUEST
        LivrePk = getattr(fields, 'LivrePk')
        LivreTitre = getattr(fields, 'LivreTitre', None)
        LivreDescription = getattr(fields, 'LivreDescription', None)

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        updateLivreTable = wrapper.getMapper('Livre')
        query = session.query(updateLivreTable)
        query = query.filter(updateLivreTable.per_pk == LivrePk)
        Livres = query.all()
        for Livre in Livres:
            Livre.per_titre = unicode(LivreTitre, 'utf-8')
            Livre.per_description = unicode(LivreDescription, 'utf-8')

        session.flush()
        #cible = "%s/gestion-de-la-base/les-Livres" % (self.context.portal_url(), )
        #self.context.REQUEST.RESPONSE.redirect(cible)

    def deleteLivre(self):
        """
        table pg Livre
        suppression des Livres
        """
        fields = self.context.REQUEST
        LivrePk = getattr(fields, 'LivrePk')

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        deleteLivreTable = wrapper.getMapper('Livre')
        query = session.query(deleteLivreTable)
        query = query.filter(deleteLivreTable.per_pk == LivrePk)
        allLivres = query.all()
        for LivrePk in allLivres:
            session.delete(LivrePk)
        session.flush()
        #cible = "%s/gestion-de-la-base/les-Livres" % (self.context.portal_url(), )
        #self.context.REQUEST.RESPONSE.redirect(cible)


    def gestionLivre(self):
        """
        insertion ou update d'un Livre
        """
        fields = self.context.REQUEST
        operation = getattr(fields, 'operation')

        if operation == "insert":
            self.addLivre()
            return {'status': 1}

        if operation == "update":
            self.updateLivre()
            return {'status': 2}

        if operation == "delete":
            self.deleteLivre()
            return {'status': 3}
