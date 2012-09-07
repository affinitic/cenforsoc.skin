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
from interfaces import IManagePeriodique
#from collective.captcha.browser.captcha import Captcha


class ManagePeriodique(BrowserView):
    implements(IManagePeriodique)

    def getAllPeriodiques(self):
        """
        recuperation de tous les périodiques
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        periodiqueTable = wrapper.getMapper('periodique')
        query = session.query(periodiqueTable)
        query = query.order_by(periodiqueTable.per_titre)
        allPeriodiques = query.all()
        return allPeriodiques

    def getPeriodiqueByPk(self, periodiquePk):
        """
        recuperation d'un periodique selon sa pk
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        periodiqueTable = wrapper.getMapper('periodique')
        query = session.query(periodiqueTable)
        query = query.filter(periodiqueTable.per_pk == periodiquePk)
        periodique = query.one()
        return periodique

    def addPeriodique(self):
        """
        ajout d'un item periodique
        """
        fields = self.context.REQUEST
        periodiqueTitre = getattr(fields, 'periodiqueTitre')
        periodiqueDescription = getattr(fields, 'periodiqueDescription', None)

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        insertPeriodique = wrapper.getMapper('periodique')
        newEntry = insertPeriodique(per_titre=periodiqueTitre, \
                                    per_description=periodiqueDescription)
        session.save(newEntry)
        session.flush()
        cible = "%s/creation-d-un-periodique" % (self.context.portal_url(), )
        self.context.REQUEST.RESPONSE.redirect(cible)

    def updatePeriodique(self):
        """
        mise a jour d'un item periodique
        """
        fields = self.context.REQUEST
        periodiquePk = getattr(fields, 'periodiquePk')
        periodiqueTitre = getattr(fields, 'periodiqueTitre', None)
        periodiqueDescription = getattr(fields, 'periodiqueDescription', None)

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        updatePeriodiqueTable = wrapper.getMapper('periodique')
        query = session.query(updatePeriodiqueTable)
        query = query.filter(updatePeriodiqueTable.per_pk == periodiquePk)
        periodiques = query.all()
        for periodique in periodiques:
            periodique.per_titre = unicode(periodiqueTitre, 'utf-8')
            periodique.per_description = unicode(periodiqueDescription, 'utf-8')

        session.flush()
        cible = "%s/creation-d-un-periodique" % (self.context.portal_url(), )
        self.context.REQUEST.RESPONSE.redirect(cible)

    def gestionPeriodique(self):
        """
        insertion ou update d'un periodique
        """
        fields = self.context.REQUEST
        operation = getattr(fields, 'operation')

        if operation == "insert":
            self.addPeriodique()

        if operation == "update":
            self.updatePeriodique()
