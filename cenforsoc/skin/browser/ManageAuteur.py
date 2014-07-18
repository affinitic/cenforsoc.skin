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
        query = query.order_by(AuteurTable.auteur_nom)
        auteur = ["%s, %s - %s" % ((elem.auteur_nom).upper(), elem.auteur_prenom, (elem.auteur_pk)) for elem in query.all()]
        return auteur

    def getAuteurPkByAuteurNom(self, livrePk, auteurNom=None):
        """
        table pg auteur
        recuperation de la pk d'un auteur selon leur nom
        à partir de la table livre
        """
        if not auteurNom:
            return''
        else:
            nom = auteurNom.split(', ')
            auteurNom = nom[0]
            print auteurNom
            if len(nom) > 1:
                auteurPrenom = nom[1]
            else:
                auteurPrenom = None
            wrapper = getSAWrapper('cenforsoc')
            session = wrapper.session
            AuteurTable = wrapper.getMapper('auteur')
            query = session.query(AuteurTable)

            if auteurNom:
                query = query.filter(AuteurTable.auteur_nom == auteurNom)
                if auteurPrenom:
                    query = query.filter(AuteurTable.auteur_prenom == auteurPrenom)
                auteur = query.one()
                auteurPk = auteur.auteur_pk
                return (livrePk, auteurPk)

    def getAuteurByLivrePk(self, livrePk, sortieListe=None):
        """
        table pg link_livre_auteur
        recuperation des auteur selon la pk d'un livre
        permet de retourner :
            toutes les infos auteur
            selon sortieListe :
                une chaine formatée des auteurNom (nom, prenom - nom, prenom)
                une liste des pk des auteur d'un livre
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        LinkLivreAuteurTable = wrapper.getMapper('link_livre_auteur')
        query = session.query(LinkLivreAuteurTable)
        query = query.filter(LinkLivreAuteurTable.livre_fk == livrePk)
        auteurs = query.all()

        if sortieListe == 'listeAuteurFormatee':
            auteursLivre = ""
            compteur = 0
            nbrAuteurs = len(auteurs)
            if nbrAuteurs > 0:
                for auteur in auteurs:
                    compteur = compteur + 1
                    auteurNom = auteur.auteurs.auteur_nom
                    auteurPrenom = auteur.auteurs.auteur_prenom or ''
                    auteursLivre = auteursLivre + auteurNom.upper() + ', ' + auteurPrenom
                    if compteur < nbrAuteurs:
                        auteursLivre = auteursLivre + (' - ')
                return auteursLivre
        if sortieListe == 'cle':
            auteursPk = []
            compteur = 0
            nbrAuteurs = len(auteurs)
            if nbrAuteurs > 0:
                for auteur in auteurs:
                    compteur = compteur + 1
                    auteursPk.append(auteur.auteurs.auteur_pk)
                return auteursPk

        else:
            return auteurs

    def getSearchingAuteur(self, auteurPk=None):
        """
        table pg auteur
        recuperation d'un auteur selon la pk
        la pk peut arriver via le form en hidden ou via un lien construit,
         (cas du listing de resultat de moteur de recherche)
        je teste si la pk arrive par param, si pas je prends celle du form
        """
        fields = self.request.form
        auteurNom = fields.get('auteurNom', None)

        if not auteurPk:
            auteurPk = fields.get('auteur_pk')

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        AuteurTable = wrapper.getMapper('auteur')
        query = session.query(AuteurTable)
        if auteurNom:
            auteurNom = auteurNom.split(',')
            auteurNom = auteurNom[0]
            auteurNom = auteurNom.decode('utf-8')
            auteurNom = auteurNom.capitalize()
            query = query.filter(AuteurTable.auteur_nom == auteurNom)
        if auteurPk:
            query = query.filter(AuteurTable.auteur_pk == auteurPk)
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

        auteurNom = unicode(auteurNom, 'utf-8')
        auteurPrenom = unicode(auteurPrenom, 'utf-8')

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        insertAuteur = wrapper.getMapper('auteur')
        newEntry = insertAuteur(auteur_nom=auteurNom,
                                auteur_prenom=auteurPrenom)
        session.add(newEntry)
        session.flush()
        session.refresh(newEntry)
        auteurPk = newEntry.auteur_pk

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Le nouvel auteur %s %s a bien été enregistré !" % (auteurNom, auteurPrenom)
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/gestion-de-la-base/les-auteurs/admin-decrire-un-auteur?auteurPk=%s" % (portalUrl, auteurPk)
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
        url = "%s/gestion-de-la-base/les-auteurs/admin-decrire-un-auteur?auteurPk=%s" % (portalUrl, auteurPk)
        self.request.response.redirect(url)
        return ''

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
