# -*- coding: utf-8 -*-

from plone.theme.interfaces import IDefaultPloneLayer
from zope.interface import Interface


class ICenforsocTheme(IDefaultPloneLayer):
    """
    Theme for cenforsoc
    """


class IManageCenforsoc(Interface):
    """
    """


class IManagePeriodique(Interface):
    """
    gestion de la table des periodiques
    """
    def gestionPeriodique():
        """
        insertion ou update d'un periodique

        """


class IManageLivre(Interface):
    """
    gestion de la table des livres
    """
    def gestionLivre():
        """
        insertion ou update d'un livre
        """


class IManageAffiche(Interface):
    """
    gestion de la table des affiches
    """
    def gestionAffiche():
        """
        insertion ou update d'une affiche
        """
