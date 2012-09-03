# -*- coding: utf-8 -*-

import datetime
#import time
#import random
#from sqlalchemy import select, func
#from mailer import Mailer
#from LocalFS import LocalFS
from Products.Five import BrowserView
from zope.interface import implements
#from z3c.sqlalchemy import getSAWrapper
#from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
#from Products.CMFPlone.utils import normalizeString
from Products.CMFCore.utils import getToolByName
#from Products.CMFPlone import PloneMessageFactory as _
#from Products.AddRemoveWidget.AddRemoveWidget import AddRemoveWidget
#from Products.Archetypes.atapi import LinesField
#from Products.Archetypes.Renderer import renderer
#from Products.Archetypes.atapi import BaseContent
from interfaces import IManageCenforsoc
#from collective.captcha.browser.captcha import Captcha


class ManageCenforsoc(BrowserView):
    implements(IManageCenforsoc)

    def getTimeStamp(self):
        timeStamp = datetime.datetime.now()
        return timeStamp

    def getUserAuthenticated(self):
        """
        retourne le nom du user loggué
        """
        pm = getToolByName(self, 'portal_membership')
        user = pm.getAuthenticatedMember()
        user = user.getUserName()
        return user

    def getRoleUserAuthenticated(self):
        """
        retourne le nom du user loggué
        """
        pm = getToolByName(self.context, 'portal_membership')
        user = pm.getAuthenticatedMember()
        userRole = user.getRoles()
        return userRole
