# -*- coding: utf-8 -*-

#import datetime
#import time
#import random
#from sqlalchemy import and_
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

    def getAllLivres(self):
        """
        recuperation de tous les livres
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        LivreTable = wrapper.getMapper('livre')
        query = session.query(LivreTable)
        query = query.order_by(LivreTable.liv_titre)
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

    def getAllLivresByMotCle(self, motCle):
        """
        recuperation de tous les périodiques selon un motcle
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        LivreTable = wrapper.getMapper('livre')
        query = session.query(LivreTable)
        query = query.filter(LivreTable.liv_mots_cles.like("%s" % motCle))
        query = query.order_by(LivreTable.liv_titre)
        allLivres = query.all()
        return allLivres

    def getLivresByAuteurPk(self, auteurPk):
        """
        recuperation de tous les livres d'un auteur via sa  pk
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        LinkLivreAuteurTable = wrapper.getMapper('link_livre_auteur')
        query = session.query(LinkLivreAuteurTable)
        query = query.filter(LinkLivreAuteurTable.auteur_fk == auteurPk)
        allLivresPk = query.all()
        allLivres = []
        for livre in allLivresPk:
            livrePk = livre.livres.liv_pk
            livreTitre = livre.livres.liv_titre
            allLivres.append((livrePk, livreTitre))
        return allLivres

    def getLivresByAuteurNom(self, auteurNom=None):
        """
        recuperation de tous les livres d'un auteur via son Nom
        """
        auteurPk = []
        if not auteurNom:
            fields = self.request.form
            auteurNom = fields.get('auteurNom', None)
        else:
            b = auteurNom.split('- ')
            auteurPk.append(int(b[1]))

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        LinkLivreAuteurTable = wrapper.getMapper('link_livre_auteur')
        query = session.query(LinkLivreAuteurTable)

        for pk in auteurPk:
            query = query.filter(LinkLivreAuteurTable.auteur_fk == pk)

        allLivresPk = query.all()

        allLivres = []
        for livre in allLivresPk:
            livrePk = livre.livres.liv_pk
            livreTitre = livre.livres.liv_titre
            allLivres.append((livrePk, livreTitre))

        return allLivres

    def getLivreTitreByLeffeSearch(self, searchString):
        """
        table pg Livre
        recuperation d'un Livre via son titre par le livesearch
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        LivreTable = wrapper.getMapper('livre')
        query = session.query(LivreTable)
        query = query.filter(LivreTable.liv_titre.ilike("%%%s%%" % searchString))
        query = query.order_by(LivreTable.liv_titre )
        livre = ["%s" % (elem.liv_titre) for elem in query.all()]
        return livre

    def getLivreMotCleByLeffeSearch(self, searchString):
        """
        table pg Livre
        recuperation d'un Livre via ses motclé par le livesearch
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        LivreTable = wrapper.getMapper('livre')
        query = session.query(LivreTable)
        query = query.filter(LivreTable.liv_mots_cles.ilike("%%%s%%" % searchString))
        livre = ["%s" % (elem.liv_mots_cles) for elem in query.all()]
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
        auteurPk = fields.get('auteurNom', None)

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        insertLivre = wrapper.getMapper('livre')
        newEntry = insertLivre(liv_titre=livreTitre, \
                               liv_inventaire=livreInventaire, \
                               liv_cote_rang=livreCoteRang, \
                               liv_edition=livreEdition, \
                               liv_lieu=livreLieuEdition, \
                               liv_editeur=livreEditeur, \
                               liv_date=livreDateEdition, \
                               liv_pages=livreNbrePages, \
                               liv_collection=livreCollection, \
                               liv_notes=livreNotes, \
                               liv_isbn=livreIsbn, \
                               liv_mots_cles=livreMotsCles, \
                               liv_pret=livrePret)
        session.add(newEntry)
        session.flush()
        session.refresh(newEntry)
        livrePk = newEntry.liv_pk
        self.insertAuteurLivre(livrePk, auteurPk)

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Le nouveau livre '%s' a bien été ajouté !" % (unicode(livreTitre, 'utf-8'), )
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/gestion-de-la-base/les-livres/admin-decrire-le-livre?livrePk=%s" % (portalUrl, livrePk)
        self.request.response.redirect(url)

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

        auteurPk = fields.get('auteurPk', None)

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

        self.deleteAuteurLivre(livrePk)
        self.insertAuteurLivre(livrePk, auteurPk)

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"L'ouvrage  '%s' est ajouté !" % (unicode(livreTitre, 'utf-8'), )
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/gestion-de-la-base/les-livres/admin-decrire-le-livre?livrePk=%s" % (portalUrl, livrePk)
        self.request.response.redirect(url)
        return ''

    def deleteLivre(self, livrePk):
        """
        table pg Livre
        suppression des Livres
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        deleteLivreTable = wrapper.getMapper('livre')
        query = session.query(deleteLivreTable)
        query = query.filter(deleteLivreTable.per_pk == LivrePk)
        allLivres = query.all()
        for LivrePk in allLivres:
            session.delete(LivrePk)
        session.flush()

    def insertAuteurLivre(self, livrePk, auteurPk):
        """
        table pg link_livre_auteur
        plusieurs auteurs possible pour un livre
        """
        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        LinkLivreAuteurTable = wrapper.getMapper('link_livre_auteur')
        for pk in auteurPk:
            newEntry = LinkLivreAuteurTable(livre_fk=livrePk,
                                            auteur_fk=pk)
            session.add(newEntry)
        session.flush()

    def deleteAuteurLivre(self, livrePk):
        """
        table pg link_livre_auteur
        3 auteurs possible pour un livre
        recuperer les auteurs depuis le livesearch,
        check si plusieurs noms et separation des pk
        suppression des donnees
        """
        #auteurPk = []
        #for nom in auteurNom:
        #    if len(nom) > 0:
        #        b = nom.split('- ')
        #        auteurPk.append(int(b[1]))

        wrapper = getSAWrapper('cenforsoc')
        session = wrapper.session
        LinkLivreAuteurTable = wrapper.getMapper('link_livre_auteur')
        query = session.query(LinkLivreAuteurTable)
        query = query.filter(LinkLivreAuteurTable.livre_fk == livrePk)
        allLivres = query.all()
        for livrePk in allLivres:
            session.delete(livrePk)
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
