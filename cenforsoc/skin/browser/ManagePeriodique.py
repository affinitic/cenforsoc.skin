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
from Products.CMFCore.utils import getToolByName
# #from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
#from Products.CMFPlone.utils import normalizeString
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
        PeriodiqueTable = wrapper.getMapper('periodique')
        query = session.query(PeriodiqueTable)
        query = query.order_by(PeriodiqueTable.per_titre)
        allPeriodiques = query.all()
        return allPeriodiques

    def getPeriodiqueByPk(self, periodiquePk):
        """
        recuperation d'un periodique selon sa pk
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        PeriodiqueTable = wrapper.getMapper('periodique')
        query = session.query(PeriodiqueTable)
        query = query.filter(PeriodiqueTable.per_pk == periodiquePk)
        periodique = query.one()
        return periodique

    def getAllPeriodiquesByLettre(self, lettre):
        """
        recuperation de tous les périodiques commencant par la lettre
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        PeriodiqueTable = wrapper.getMapper('periodique')
        query = session.query(PeriodiqueTable)
        query = query.filter(PeriodiqueTable.per_titre.like("%%%s%%" % lettre))
        query = query.order_by(PeriodiqueTable.per_titre)
        allPeriodiques = query.all()
        return allPeriodiques

    def getPeriodiqueByLeffeSearch(self, searchString):
        """
        table pg periodique
        recuperation d'un periodique via le livesearch
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        PeriodiqueTable = wrapper.getMapper('periodique')
        query = session.query(PeriodiqueTable)
        query = query.filter(PeriodiqueTable.per_titre.ilike("%%%s%%" % searchString))
        query = query.order_by(PeriodiqueTable.per_titre)
        periodique = ["%s" % (elem.per_titre) for elem in query.all()]
        return periodique

    def getSearchingPeriodique(self, periodiquePk=None, searchingLetter=None):
        """
        table pg periodique
        recuperation du periodique selon la pk
        la pk peut arriver via le form en hidden ou via un lien construit,
         (cas du listing de resultat de moteur de recherche)
        je teste si la pk arrive par param, si pas je prends celle du form
        """
        fields = self.request.form
        periodiqueTitre = fields.get('periodiqueTitre')
        if not periodiquePk:
            periodiquePk = fields.get('periodique_pk')

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        PeriodiqueTable = wrapper.getMapper('periodique')
        query = session.query(PeriodiqueTable)
        if periodiqueTitre:
            query = query.filter(PeriodiqueTable.per_titre == periodiqueTitre)
        if periodiquePk:
            query = query.filter(PeriodiqueTable.per_pk == periodiquePk)
        if searchingLetter:
            query = query.filter(PeriodiqueTable.per_titre.ilike("%%%s" % searchingLetter))
        allPeriodiques = query.all()
        return allPeriodiques

    def findPeriodique(self, periodiquePk=None):
        """
        Renvoie un periodique après une Leffe search ou une sélection par pk
        """
        if periodiquePk is None:
            fields = self.request.form
            periodiqueTitre = fields.get('periodiqueTitre', None)
            if periodiqueTitre is not None:
                # Leffe searched cahier de charge
                wrapper = getSAWrapper('cenforsoc')
                session = wrapper.session
                PeriodiqueTable = wrapper.getMapper('periodique')
                query = session.query(PeriodiqueTable)
                query = query.filter(PeriodiqueTable.per_titre == periodiqueTitre)
                periodique = query.one()
                return periodique
            else:
                return None
        else:
            return self.getPeriodiqueByPk(periodiquePk)

    def insertPeriodique(self):
        """
        ajout d'un item periodique
        """
        fields = self.context.REQUEST
        periodiqueTitre = getattr(fields, 'periodiqueTitre')
        periodiqueDescription = getattr(fields, 'periodiqueDescription', None)

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        insertPeriodique = wrapper.getMapper('periodique')
        newEntry = insertPeriodique(per_titre=periodiqueTitre,
                                    per_description=periodiqueDescription)
        session.add(newEntry)
        session.flush()

        session.refresh(newEntry)
        periodiquePk = newEntry.per_pk

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Vos informations ont été enregistrées !"
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/gestion-de-la-base/les-periodiques/admin-decrire-un-periodique?periodiquePk=%s" % (portalUrl, periodiquePk)
        self.request.response.redirect(url)
        return ''

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
        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Vos informations ont été modifiées !"
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/gestion-de-la-base/les-periodiques/admin-decrire-un-periodique?periodiquePk=%s" % (portalUrl, periodiquePk)
        self.request.response.redirect(url)
        return ''

    def deletePeriodique(self):
        """
        table pg periodique
        suppression des periodiques
        """
        fields = self.context.REQUEST
        periodiquePk = getattr(fields, 'periodiquePk')

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        deletePeriodiqueTable = wrapper.getMapper('periodique')
        query = session.query(deletePeriodiqueTable)
        query = query.filter(deletePeriodiqueTable.per_pk == periodiquePk)
        allPeriodiques = query.all()
        for periodiquePk in allPeriodiques:
            session.delete(periodiquePk)
        session.flush()

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Le périodique a été supprimé !"
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/gestion-de-la-base/les-periodiques/" % (portalUrl, )
        self.request.response.redirect(url)
        return ''

    def gestionPeriodique(self):
        """
        insertion ou update d'un periodique
        """
        fields = self.context.REQUEST
        operation = getattr(fields, 'operation')

        if operation == "insert":
            self.addPeriodique()
            return {'status': 1}

        if operation == "update":
            self.updatePeriodique()
            return {'status': 2}

        if operation == "delete":
            self.deletePeriodique()
            return {'status': 3}
