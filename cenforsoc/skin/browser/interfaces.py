# -*- coding: utf-8 -*-

from plone.theme.interfaces import IDefaultPloneLayer
from zope.interface import Interface


class ICenforsocTheme(IDefaultPloneLayer):
    """
    Theme for cenforsoc
    """


class IManageCenforsoc(Interface):
    """
    outils communs
    """
    def getWysiwygField(name, value):
        """
        generates a WYSIWYG field containing value
        """

    def getAddRemoveField(name, title, values, nameKey='name', pkKey='pk', selectedPks=[]):
        """
        generates an Add / Remove from list field with already selected pks
        nameKey and pkKey are used for the display value and the record pk to
        save
        """


class IManagePeriodique(Interface):
    """
    gestion de la table des periodiques
    """
    def gestionPeriodique():
        """
        insertion ou update d'un periodique

        """
    def getPeriodiqueByLeffeSearch(self, searchString):
        """
        table pg periodique
        recuperation d'un periodique via le livesearch
        """


class IManageLivre(Interface):
    """
    gestion de la table des livres
    """
    def gestionLivre():
        """
        insertion ou update d'un livre
        """
    def getLivreByLeffeSearch(self, searchString):
        """
        table pg livre
        recuperation d'un livre via le livesearch
        """
    def getSearchingLivre(self, livrePk=None):
        """
        table pg livre
        recuperation des infos d'un livre selon son titre ou sa pk
        """
    def insertLivre():
        """
        insert a new item in livre
        """
    def updateLivre():
        """
        update items in livre
        """


class IManageAffiche(Interface):
    """
    gestion de la table des affiches
    """
    def gestionAffiche():
        """
        insertion ou update d'une affiche
        """

    def getAfficheByLeffeSearch(self, searchString):
        """
        table pg affiche
        recuperation d'une affiche via le livesearch
        """


class IManageAuteur(Interface):
    """
    gestion de la table des auteurs
    """
    def gestionAuteur():
        """
        insertion ou update d'un auteur
        """

    def getAuteurByLeffeSearch(self, searchString):
        """
        table pg auteur
        recuperation d'une auteur via le livesearch
        """
    def insertAuteur():
        """
        insert a new item in auteur
        """
    def updateAuteur():
        """
        update items in auteur
        """


class IManageFormation(Interface):
    """
    gestion des demandes de formations
    """
    def gestionFormation():
        """
        insertion ou update d'un auteur
        """

    def getFormationByLeffeSearch(self, searchString):
        """
        table pg auteur
        recuperation d'une auteur via le livesearch
        """
    def insertFormation():
        """
        insert a new item in formation
        """
    def updateFormation():
        """
        update items in formation
        """
