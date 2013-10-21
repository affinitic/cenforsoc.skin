# -*- coding: utf-8 -*-

import datetime
#import time
#import random
#from sqlalchemy import select, func
from mailer import Mailer
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

    def sendMail(self, sujet, message):
        """
        envoi de mail à cenforsoc-admin, Thierry Vanloo
        "cenforsoc@brutele.be"
        """
        mailer = Mailer("localhost", "alain.meurant@affinitic.be")
        mailer.setSubject(sujet)
        mailer.setRecipients("alain.meurant@affinitic.be")
        mail = message
        mailer.sendAllMail(mail)

    def sendMailToCenforsoc(self, sujet, message):
        """
        envoi de mail à l'operateur dont les donnees change d'état
        """
        mailer = Mailer("localhost", 'cenforsoc@brutele.be')
        #mailer = Mailer("relay.skynet.be", 'alain.meurant@affinitic.be')
        mailer.setSubject(sujet)
        #recipients = "%s" % ('alain.meurant@skynet.be')
        recipients = "%s, %s" % ('alain.meurant@affinitic.be', 'cenforsoc@brutele.be')
        mailer.setRecipients(recipients)
        mail = message
        mailer.sendAllMail(mail)

    def sendMailForInscription(self, sujetInscrit, messageInscrit, emailInscrit):
        """
        envoi de mail à la personne qui a fait une demande d'inscription
        """
        mailer = Mailer("localhost", emailInscrit)
        mailer = Mailer("relay.skynet.be", 'alain.meurant@skynet.be')
        mailer.setSubject(sujetInscrit)
        #recipients = "%s" % ('alain.meurant@affinitic.be')
        recipients = "%s, %s, %s" % ('alain.meurant@affinitic.be', 'cenforsoc@brutele.be', emailInscrit)
        mailer.setRecipients(recipients)
        mail = messageInscrit
        mailer.sendAllMail(mail)

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
