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


class IManagePeriodiques(Interface):
    """
    gestion de la table es periodiques
    """
    def gestionPeriodique():
        """
        insertion ou update d'un periodique
        """
    def getPeriodiqueByPk():
        """
        recuperation d'un periodique selon sa pk
        """
