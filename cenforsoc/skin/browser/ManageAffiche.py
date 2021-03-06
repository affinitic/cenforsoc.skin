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
from interfaces import IManageAffiche
#from collective.captcha.browser.captcha import Captcha


class ManageAffiche(BrowserView):
    implements(IManageAffiche)

    def getAllAffiches(self):
        """
        table
        recuperation de toutes les affiches
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        AfficheTable = wrapper.getMapper('affiche')
        query = session.query(AfficheTable)
        query = query.order_by(AfficheTable.affiche_inventaire)
        allAffiches = query.all()
        return allAffiches

    def getAfficheByPk(self, affichePk):
        """
        table
        recuperation d'une affiche selon sa pk
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        AfficheTable = wrapper.getMapper('affiche')
        query = session.query(AfficheTable)
        query = query.filter(AfficheTable.affiche_pk == affichePk)
        affiche = query.one()
        return affiche

    def getAfficheByLeffeSearch(self, searchString):
        """
        table pg affiche
        recuperation d'une affiche via le livesearch
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        AfficheTable = wrapper.getMapper('affiche')
        query = session.query(AfficheTable)
        query = query.filter(or_(AfficheTable.affiche_titre.ilike("%%%s%%" % searchString),
                                 or_(AfficheTable.affiche_auteur.ilike("%%%s%%" % searchString),
                                     AfficheTable.affiche_descriptif.ilike("%%%s%%" % searchString),
                                     AfficheTable.affiche_mot_cle.ilike("%%%s%%" % searchString))))
        query = query.order_by(AfficheTable.affiche_titre)
        affiche = ["%s" % (elem.affiche_titre) for elem in query.all()]
        return affiche

    def getAllAffichesByLettre(self, lettre):
        """
        recuperation de tous les affiches commencant par la lettre
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        AfficheTable = wrapper.getMapper('affiche')
        query = session.query(AfficheTable)
        query = query.filter(AfficheTable.affiche_titre.like("%%%s%%" % lettre))
        query = query.order_by(AfficheTable.affiche_titre)
        allAffiches = query.all()
        return allAffiches

    def getSearchingAffiche(self, affichePk=None, searchingLetter=None):
        """
        table pg affiche
        recuperation d'une affiche selon la pk
        la pk peut arriver via le form en hidden ou via un lien construit,
         (cas du listing de resultat de moteur de recherche)
        je teste si la pk arrive par param, si pas je prends celle du form
        """
        fields = self.request.form
        afficheTitre = fields.get('afficheTitre')
        if not affichePk:
            affichePk = fields.get('affiche_pk')

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        AfficheTable = wrapper.getMapper('affiche')
        query = session.query(AfficheTable)
        if afficheTitre:
            query = query.filter(AfficheTable.affiche_titre == afficheTitre)
        if affichePk:
            query = query.filter(AfficheTable.affiche_pk == affichePk)
        if searchingLetter:
            query = query.filter(AfficheTable.affiche_titre.ilike("%%%s" % searchingLetter))
        allAffiches = query.all()
        return allAffiches

    def insertAffiche(self):
        """
        table pg affiche
        ajout d'un item affiche sans image
        """
        fields = self.context.REQUEST
        afficheTitre = getattr(fields, 'afficheTitre', None)
        afficheNumInventaire = getattr(fields, 'afficheNumInventaire', None)
        afficheAuteur = getattr(fields, 'afficheAuteur')
        afficheIllustrateur = getattr(fields, 'afficheIllustrateur', None)
        afficheLieuEdition = getattr(fields, 'afficheLieuEdition', None)
        afficheEditeur = getattr(fields, 'afficheEditeur')
        afficheDateEdition = getattr(fields, 'afficheDateEdition', None)
        afficheColoration = getattr(fields, 'afficheColoration', None)
        afficheFormat = getattr(fields, 'afficheFormat')
        afficheNbreExemplaire = getattr(fields, 'afficheNbreExemplaire')
        afficheMotCle = getattr(fields, 'afficheMotCle')
        afficheDescriptif = getattr(fields, 'afficheDescriptif')
        afficheHistorique = getattr(fields, 'afficheHistorique')
        afficheCommanditaire = getattr(fields, 'afficheCommanditaire')
        afficheSerie = getattr(fields, 'afficheSerie')
        
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        insertAffiche = wrapper.getMapper('affiche')
        newEntry = insertAffiche(affiche_titre = afficheTitre, \
                                 affiche_inventaire = afficheNumInventaire, \
                                 affiche_auteur = afficheAuteur, \
                                 affiche_illustrateur = afficheIllustrateur, \
                                 affiche_lieu_edition = afficheLieuEdition, \
                                 affiche_editeur = afficheEditeur, \
                                 affiche_date_edition = afficheDateEdition, \
                                 affiche_coloration = afficheColoration, \
                                 affiche_format = afficheFormat, \
                                 affiche_nbre_exemplaire = afficheNbreExemplaire, \
                                 affiche_mot_cle = afficheMotCle, \
                                 affiche_descriptif = afficheDescriptif, \
                                 affiche_historique = afficheHistorique, \
                                 affiche_commanditaire = afficheCommanditaire, \
                                 affiche_serie = afficheSerie)
        session.add(newEntry)
        session.flush()
        session.refresh(newEntry)
        affichePk = newEntry.affiche_pk

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"L'affiche a été correctement enregistrée !"
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/gestion-de-la-base/les-affiches/admin-decrire-une-affiche?affichePk=%s" % (portalUrl, affichePk)
        self.request.response.redirect(url)
        return ''

    def updateAffiche(self):
        """
        table
        mise a jour d'un item affiche
        """
        fields = self.context.REQUEST

        affichePk = getattr(fields, 'affichePk')
        afficheTitre = getattr(fields, 'afficheTitre', None)
        afficheNumInventaire = getattr(fields, 'afficheNumInventaire', None)
        afficheAuteur = getattr(fields, 'afficheAuteur')
        afficheIllustrateur = getattr(fields, 'afficheIllustrateur', None)
        afficheLieuEdition = getattr(fields, 'afficheLieuEdition', None)
        afficheEditeur = getattr(fields, 'afficheEditeur')
        afficheDateEdition = getattr(fields, 'afficheDateEdition', None)
        afficheColoration = getattr(fields, 'afficheColoration', None)
        afficheFormat = getattr(fields, 'afficheFormat')
        afficheNbreExemplaire = getattr(fields, 'afficheNbreExemplaire')
        afficheMotCle = getattr(fields, 'afficheMotCle')
        afficheDescriptif = getattr(fields, 'afficheDescriptif')
        afficheHistorique = getattr(fields, 'afficheHistorique')
        afficheCommanditaire = getattr(fields, 'afficheCommanditaire')
        afficheSerie = getattr(fields, 'afficheSerie')

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        updateAfficheTable = wrapper.getMapper('affiche')
        query = session.query(updateAfficheTable)
        query = query.filter(updateAfficheTable.affiche_pk == affichePk)
        affiches = query.all()
        for affiche in affiches:
            affiche.affiche_titre = unicode(afficheTitre, 'utf-8')
            affiche.affiche_inventaire = unicode(afficheNumInventaire, 'utf-8')
            affiche.affiche_auteur = unicode(afficheAuteur, 'utf-8')
            affiche.affiche_illustrateur = unicode(afficheIllustrateur, 'utf-8')
            affiche.affiche_lieu_edition = unicode(afficheLieuEdition, 'utf-8')
            affiche.affiche_editeur = unicode(afficheEditeur, 'utf-8')
            affiche.affiche_date_edition = unicode(afficheDateEdition, 'utf-8')
            affiche.affiche_coloration = unicode(afficheColoration, 'utf-8')
            affiche.affiche_format = unicode(afficheFormat, 'utf-8')
            affiche.affiche_nbre_exemplaire = unicode(afficheNbreExemplaire, 'utf-8')
            affiche.affiche_mot_cle = unicode(afficheMotCle, 'utf-8')
            affiche.affiche_descriptif = unicode(afficheDescriptif, 'utf-8')
            affiche.affiche_historique = unicode(afficheHistorique, 'utf-8')
            affiche.affiche_commanditaire = unicode(afficheCommanditaire, 'utf-8')
            affiche.affiche_serie = unicode(afficheSerie, 'utf-8')

        session.flush()

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"L'affiche a bien été modifié !"
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/gestion-de-la-base/les-affiches/admin-decrire-une-affiche?affichePk=%s" % (portalUrl, affichePk)
        self.request.response.redirect(url)
        return ''

    def listAfficheInLocalFs(self):
        """
        """
        apef = getattr(self.context, 'plone')
        lfs = getattr(apef, 'affiche_cenforsoc')
        listeAffiches = lfs.fileValues()
        affiches = []
        for i in range(len(listeAffiches)):
            affiches.append(listeAffiches[i].id)
        return affiches

    def insertAfficheToLocalFs(self, for_id, fileUpload):
        """
        ajout d'un fichier dans le localfs
        comme  catalogue pdf de l'operateur
        """
        afficheFolderXXXXXXXXXXXXXXXXXXXXXXXXXXXXX = getattr(self.context, 'rof-questionnaire')
        lfs = getattr(rof, 'rof_pdf')
        filename, ext = os.path.splitext(fileUpload.filename)
        normalized_filename = normalizeString(filename, encoding='utf-8')
        filepath = '%s%s' % (normalized_filename, ext)
        lfs.manage_upload(fileUpload, id=filepath)

        return ''

    def deleteAfficheFromLocalFS(self, \
                                 fileName, \
                                 for_id=None):
        """
        suppression du fichier dans le localfs
        comme  catalogue pdf de l'operateur
        suppression dans la table link_organisme_formation
        """
        #suppression dans le localfs
        rof = getattr(self.context, 'rof-questionnaire')
        lfs = getattr(rof, 'rof_pdf')
        lfs.manage_delObjects(ids=fileName)

        #suppression dans la table link_organisme_catalogue
        wrapper = getSAWrapper('apef')
        session = wrapper.session
        deleteCatalogue = wrapper.getMapper('link_organisme_catalogue')
        query = session.query(deleteCatalogue)
        query = query.filter(deleteCatalogue.c.for_catalogue == fileName)
        newEntries = query.all()
        for newEntry in newEntries:
            session.delete(newEntry)
        session.flush()

        if for_id:
            cible = "%s/rof-questionnaire/operateur-gerer-catalogue-pdf" % self.context.portal_url()
        else:
            cible = "%s/rof-questionnaire/accueil" % self.context.portal_url()
        self.context.REQUEST.RESPONSE.redirect(cible)
        return ''

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
