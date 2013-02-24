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
        query = query.filter(FormationTable.form_pk == formationPk)
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

    def insertFormation(self):
        """
        table pg formation
        ajout d'un item formation
        """
        fields = self.request.form

        formationTitre = fields.get('formationTitre', None)
        formationDuree = fields.get('formationDuree', None)
        formationDateDebut = fields.get('formationDateDebut', None)
        formationDescription = fields.get('formationDescription', None)
        formationNiveauRequis = fields.get('formationNiveauRequis', None)
        formationEtat = fields.get('formationEtat', None)

        formationTitre = unicode(formationTitre, 'utf-8')
        formationDescription = unicode(formationDescription, 'utf-8')
        formationNiveauRequis = unicode(formationNiveauRequis, 'utf-8')

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        insertAuteur = wrapper.getMapper('formation')
        newEntry = insertAuteur(form_titre=formationTitre, \
                                form_duree=formationDuree, \
                                form_date_deb=formationDateDebut, \
                                form_description=formationDescription, \
                                form_niveau_requis=formationNiveauRequis, \
                                form_etat=formationEtat)
        session.add(newEntry)
        session.flush()
        session.refresh(newEntry)
        formationPk = newEntry.for_pk

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"La nouvelle formation %s  a bien été enregistrée !" % (formationTitre)
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/formation/ajouter-une-formation" % (portalUrl)
        self.request.response.redirect(url)
        return ''

    def updateFormation(self):
        """
        table pg auteur
        mise a jour d'un item auteur
        """
        fields = self.request.form
        
        formationPk = fields.get('formationPk', None)
        formationTitre = fields.get('formationTitre', None)
        formationDuree = fields.get('formationDuree', None)
        formationDateDebut = fields.get('formationDateDebut', None)
        formationDescription = fields.get('formationDescription', None)
        formationNiveauRequis = fields.get('formationNiveauRequis', None)
        formationEtat = fields.get('formationEtat', None)

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        updateFormationTable = wrapper.getMapper('formation')
        query = session.query(updateFormationTable)
        query = query.filter(updateFormationTable.form_pk == formationPk)
        formations = query.all()
        for formation in formations:
            formation.form_titre = unicode(formationTitre, 'utf-8')
            formation.form_duree = unicode(formationDuree, 'utf-8')
            formation.form_date_deb = unicode(formationDateDebut, 'utf-8')
            formation.form_description = unicode(formationDescription, 'utf-8')
            formation.form_niveau_requis = unicode(formationNiveauRequis, 'utf-8')
            formation.form_etat = unicode(formationEtat, 'utf-8')

        session.flush()

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"La formation %s a bien été modifiée !" % (formationTitre)
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/formations/" % (portalUrl)
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
