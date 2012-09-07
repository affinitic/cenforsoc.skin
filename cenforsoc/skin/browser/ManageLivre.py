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
        recuperation de tous les livres
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        livreTable = wrapper.getMapper('livre')
        query = session.query(livreTable)
        query = query.order_by(livreTable.liv_titre)
        allLivres = query.all()
        return allLivres

    def getLivreByPk(self, livrePk):
        """
        recuperation d'un livre selon sa pk
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        livreTable = wrapper.getMapper('livre')
        query = session.query(livreTable)
        query = query.filter(livreTable.liv_pk == livrePk)
        livre = query.one()
        return livre

    def addLivre(self):
        """
        ajout d'un item livre
        """
        fields = self.context.REQUEST
        livreTitre = getattr(fields, 'livreTitre')
        livreDescription = getattr(fields, 'livreDescription', None)

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        insertLivre = wrapper.getMapper('livre')
        newEntry = insertLivre(liv_titre=livreTitre, \
                               liv_description=livreDescription)
        session.save(newEntry)
        session.flush()
        cible = "%s/creation-d-un-livre" % (self.context.portal_url(), )
        self.context.REQUEST.RESPONSE.redirect(cible)

    def updateLivre(self):
        """
        mise a jour d'un item livre
        """
        fields = self.context.REQUEST
        livrePk = getattr(fields, 'livrePk')
        livreTitre = getattr(fields, 'livreTitre', None)
        livreDescription = getattr(fields, 'livreDescription', None)

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        updateLivreTable = wrapper.getMapper('livre')
        query = session.query(updateLivreTable)
        query = query.filter(updateLivreTable.liv_pk == livrePk)
        livres = query.all()
        for livre in livres:
            livre.liv_titre = unicode(livreTitre, 'utf-8')
            livre.liv_description = unicode(livreDescription, 'utf-8')

        session.flush()
        cible = "%s/creation-d-un-livre" % (self.context.portal_url(), )
        self.context.REQUEST.RESPONSE.redirect(cible)

    def gestionLivre(self):
        """
        insertion ou update d'un livre
        """
        fields = self.context.REQUEST
        operation = getattr(fields, 'operation')

        if operation == "insert":
            self.addLivre()

        if operation == "update":
            self.updateLivre()
