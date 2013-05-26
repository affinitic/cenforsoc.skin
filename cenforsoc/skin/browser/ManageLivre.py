# -*- coding: utf-8 -*-

#import datetime
#import time
#import random
#from sqlalchemy import select, func, distinct
#from mailer import Mailer
#from LocalFS import LocalFS
from Products.Five import BrowserView
from zope.interface import implements
from z3c.sqlalchemy import getSAWrapper
#from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
#from Products.CMFPlone.utils import normalizeString
from Products.CMFCore.utils import getToolByName
#from Products.CMFPlone import PloneMessageFactory as _
#from Products.AddRemoveWidget.AddRemoveWidget import AddRemoveWidget
#from Products.Archetypes.atapi import LinesField
#from Products.Archetypes.Renderer import renderer
#from Products.Archetypes.atapi import BaseContent
from interfaces import IManageLivre
#from collective.captcha.browser.captcha import Captcha


class ManageLivre(BrowserView):
    implements(IManageLivre)

    def getAllAuteurs(self):
        """
        recuperation de tous les auteurs
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        LivreTable = wrapper.getMapper('auteur')
        query = session.query(LivreTable)
        allAuteurs = query
        return allAuteurs

    def getAuteurByLivrePk(self, LivrePk):
        """
        table pg link_livre_auteur
        recuperation des auteur selon la pk d'un livre
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        LinkLivreAuteurTable = wrapper.getMapper('link_livre_auteur')
        query = session.query(LinkLivreAuteurTable)
        query = query.filter(LinkLivreAuteurTable.livre_fk == LivrePk)
        livre = query.all()
        return livre

    def insertAuteurLivre(self):
        """
        table pg link_livre_auteur
        3 auteurs possible pour un livre
        recuperer les auteurs depuis le livesearch,
        check si plusieurs noms et separation des pk
        insertion des nouvelles donnees
        """
        fields = self.request.form
        livrePk = fields.get('livrePk', None)
        auteurNom = fields.get('auteurNom', None)

        auteurPk = []
        for nom in auteurNom:
            if len(nom) > 0:
                b = nom.split('- ')
                auteurPk.append(int(b[1]))

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        LinkLivreAuteurTable = wrapper.getMapper('link_livre_auteur')
        for pk in auteurPk:
            newEntry = LinkLivreAuteurTable(livre_fk=livrePk,
                                            auteur_fk=pk)
            session.add(newEntry)
        session.flush()

    def deleteAuteurLivre(self):
        """
        table pg link_livre_auteur
        3 auteurs possible pour un livre
        recuperer les auteurs depuis le livesearch,
        check si plusieurs noms et separation des pk
        suppression des donnees
        """
        fields = self.request.form
        livrePk = fields.get('livrePk', None)
        auteurNom = fields.get('auteurNom', None)

        auteurPk = []
        for nom in auteurNom:
            if len(nom) > 0:
                b = nom.split('- ')
                auteurPk.append(int(b[1]))

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        LinkLivreAuteurTable = wrapper.getMapper('link_livre_auteur')
        query = session.query(LinkLivreAuteurTable)
        query = query.filter(LinkLivreAuteurTable.livre_fk == livrePk)
        allLivres = query.all()
        for livrePk in allLivres:
            session.delete(livrePk)
        session.flush()

    def getAllLivres(self):
        """
        recuperation de tous les livres
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        LivreTable = wrapper.getMapper('livre')
        query = session.query(LivreTable)
        query = query.order_by(LivreTable.liv_pk)
        allLivres = query.all()
        return allLivres

    def getLivreByPk(self, LivrePk):
        """
        recuperation d'un Livre selon sa pk
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        LivreTable = wrapper.getMapper('livre')
        query = session.query(LivreTable)
        query = query.filter(LivreTable.per_pk == LivrePk)
        livre = query.one()
        return livre

    def getAllLivresByLettre(self, lettre):
        """
        recuperation de tous les périodiques commencant par la lettre
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        LivreTable = wrapper.getMapper('livre')
        query = session.query(LivreTable)
        query = query.filter(LivreTable.liv_titre.like("%s" % lettre))
        query = query.order_by(LivreTable.liv_titre)
        allLivres = query.all()
        return allLivres

    def getLivresByAuteur(self):
        """
        recuperation de tous les livres d'un auteur
        """
        fields = self.request.form
        auteurNom = fields.get('auteurNom', None)
        auteurPk = []
        if len(auteurNom) > 0:
            b = auteurNom.split('- ')
            auteurPk.append(int(b[1]))

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        LinkLivreAuteurTable = wrapper.getMapper('link_livre_auteur')
        query = session.query(LinkLivreAuteurTable)

        for pk in auteurPk:
            query = query.filter(LinkLivreAuteurTable.auteur_fk == pk)

        allLivresPk = query.all()
        return allLivresPk

    def getLivreByLeffeSearch(self, searchString):
        """
        table pg Livre
        recuperation d'un Livre via le livesearch
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        LivreTable = wrapper.getMapper('livre')
        query = session.query(LivreTable)
        query = query.filter(LivreTable.liv_titre.ilike("%%%s%%" % searchString))
        livre = ["%s" % (elem.liv_titre) for elem in query.all()]
        return livre

    def getSearchingLivre(self, livrePk=None):
        """
        table pg Livre
        recuperation du Livre selon la pk
        la pk peut arriver via le form en hidden ou via un lien construit,
         (cas du listing de resultat de moteur de recherche)
        je teste si la pk arrive par param, si pas je prends celle du form
        """
        fields = self.request.form
        livreTitre = fields.get('livreTitre')
        if not livrePk:
            livrePk = fields.get('livre_pk')

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        LivreTable = wrapper.getMapper('livre')
        query = session.query(LivreTable)
        if livreTitre:
            query = query.filter(LivreTable.liv_titre == livreTitre)
        if livrePk:
            query = query.filter(LivreTable.liv_pk == livrePk)
        allLivres = query.all()
        return allLivres

    def insertLivre(self):
        """
        ajout d'un item Livre
        """
        fields = self.context.REQUEST
        LivreTitre = getattr(fields, 'LivreTitre')
        livreInventaire = getattr(fields, 'livreInventaire', None)

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        insertLivre = wrapper.getMapper('livre')
        newEntry = insertLivre(liv_titre=LivreTitre, \
                               liv_inventaire=livreInventaire)
        session.save(newEntry)
        session.flush()
        #cible = "%s/ajouter-un-Livre" % (self.context.portal_url(), )
        #self.context.REQUEST.RESPONSE.redirect(cible)

    def updateLivre(self):
        """
        mise a jour d'un item Livre
        """
        fields = self.request.form

        livrePk = fields.get('livrePk', None)
        livreTitre = fields.get('livreTitre', None)
        livreInventaire = fields.get('livreInventaire', None)
        livreCoteRang = fields.get('livreCoteRang', None)
        livreEdition = fields.get('livreEdition', None)
        livreEditeur = fields.get('livreEditeur', None)
        livreLieuEdition = fields.get('livreLieuEdition', None)
        livreDateEdition = fields.get('livreDateEdition', None)
        livreNbrePages = fields.get('livreNbrePages', None)
        livreCollection = fields.get('livreCollection', None)
        livreNotes = fields.get('livreNotes', None)
        livreIsbn = fields.get('livreIsbn', None)
        livreMotsCles = fields.get('livreMotsCles', None)
        livrePret = fields.get('livrePret', None)

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        updateLivreTable = wrapper.getMapper('livre')
        query = session.query(updateLivreTable)
        query = query.filter(updateLivreTable.liv_pk == livrePk)
        livre = query.one()
        livre.liv_titre = unicode(livreTitre, 'utf-8')
        livre.liv_inventaire = unicode(livreInventaire, 'utf-8')
        livre.liv_cote_rang = unicode(livreCoteRang, 'utf-8')
        livre.liv_edition = unicode(livreEdition, 'utf-8')
        livre.liv_lieu = unicode(livreLieuEdition, 'utf-8')
        livre.liv_editeur = unicode(livreEditeur, 'utf-8')
        livre.liv_date = unicode(livreDateEdition, 'utf-8')
        livre.liv_pages = unicode(livreNbrePages, 'utf-8')
        livre.liv_collection = unicode(livreCollection, 'utf-8')
        livre.liv_notes = unicode(livreNotes, 'utf-8')
        livre.liv_isbn = unicode(livreIsbn, 'utf-8')
        livre.liv_mots_cles = unicode(livreMotsCles, 'utf-8')
        livre.liv_pret = unicode(livrePret, 'utf-8')

        session.flush()

        self.deleteAuteurLivre()
        self.insertAuteurLivre()

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Les données du livre '%s' ont bien été modifiées !" % (unicode(livreTitre, 'utf-8'), )
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/documentation/bibliotheque/decrire-le-livre?livrePk=%s" % (portalUrl, livrePk)
        self.request.response.redirect(url)
        return ''

    def deleteLivre(self):
        """
        table pg Livre
        suppression des Livres
        """
        fields = self.context.REQUEST
        LivrePk = getattr(fields, 'LivrePk')

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        deleteLivreTable = wrapper.getMapper('livre')
        query = session.query(deleteLivreTable)
        query = query.filter(deleteLivreTable.per_pk == LivrePk)
        allLivres = query.all()
        for LivrePk in allLivres:
            session.delete(LivrePk)
        session.flush()

    def gestionLivre(self):
        """
        insertion ou update d'un Livre
        """
        fields = self.context.REQUEST
        operation = getattr(fields, 'operation')

        if operation == "insert":
            self.insertLivre()
            self.insertAuteurLivre()

        if operation == "update":
            self.updateLivre()

        if operation == "delete":
            self.deleteLivre()
