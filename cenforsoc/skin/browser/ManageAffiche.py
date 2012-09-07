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
from interfaces import IManageAffiche
#from collective.captcha.browser.captcha import Captcha


class ManageAffiche(BrowserView):
    implements(IManageAffiche)

    def getAllAffiches(self):
        """
        recuperation de toutes les affiches
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        afficheTable = wrapper.getMapper('affiche')
        query = session.query(afficheTable)
        query = query.order_by(afficheTable.affiche_titre)
        allAffiches = query.all()
        return allAffiches

    def getAfficheByPk(self, affichePk):
        """
        recuperation d'une affiche selon sa pk
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        afficheTable = wrapper.getMapper('affiche')
        query = session.query(afficheTable)
        query = query.filter(afficheTable.affiche_pk == affichePk)
        affiche = query.one()
        return affiche

    def addAffiche(self):
        """
        ajout d'un item affiche
        """
        fields = self.context.REQUEST
        afficheTitre = getattr(fields, 'afficheTitre')
        afficheDescription = getattr(fields, 'afficheDescription', None)

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        insertAffiche = wrapper.getMapper('affiche')
        newEntry = insertAffiche(affiche_titre=afficheTitre, \
                                 affiche_description=afficheDescription)
        session.save(newEntry)
        session.flush()
        cible = "%s/creation-d-une-affiche" % (self.context.portal_url(), )
        self.context.REQUEST.RESPONSE.redirect(cible)

    def updateAffiche(self):
        """
        mise a jour d'un item affiche
        """
        fields = self.context.REQUEST
        affichePk = getattr(fields, 'affichePk')
        afficheTitre = getattr(fields, 'afficheTitre', None)
        afficheDescription = getattr(fields, 'afficheDescription', None)

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        updateAfficheTable = wrapper.getMapper('affiche')
        query = session.query(updateAfficheTable)
        query = query.filter(updateAfficheTable.affiche_pk == affichePk)
        affiches = query.all()
        for affiche in affiches:
            affiche.affiche_titre = unicode(afficheTitre, 'utf-8')
            affiche.affiche_description = unicode(afficheDescription, 'utf-8')

        session.flush()
        cible = "%s/creation-d-une-affiche" % (self.context.portal_url(), )
        self.context.REQUEST.RESPONSE.redirect(cible)

    def gestionAffiche(self):
        """
        insertion ou update d'une affiche
        """
        fields = self.context.REQUEST
        operation = getattr(fields, 'operation')

        if operation == "insert":
            self.addAffiche()

        if operation == "update":
            self.updateAffiche()
