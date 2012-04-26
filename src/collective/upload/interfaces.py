# -*- coding: utf-8 -*-
from zope import schema
from zope.interface import Interface

from zope.i18nmessageid import MessageFactory
from plone.theme.interfaces import IDefaultPloneLayer

_ = MessageFactory('collective.upload')


class IUploadBrowserLayer(IDefaultPloneLayer):
    """A marker interface for the theme layer.
    """


class IUploadSettings(Interface):
    """Global upload settings. This describes records stored in the
    configuration registry and obtainable via plone.registry.
    """

    upload_extensions = schema.TextLine(title=_(u"Allowed Extensions"),
                                         description=_(u"allowed_extensions_key",
                                         default=u"List the file extensions allowed for upload, "
                                                  "without dot, comma separated"),
                                         required=False,
                                         default=u'gif, jpg, jpeg, png',)

    max_file_size = schema.Int(title=_(u"Max file size"),
                                         description=_(u"max_file_size_key",
                                         default=u"The maximum allowed file size in bytes "
                                                  "ej: 10000000 ~ 10mb"),
                                         required=False,
                                         default=10000000,)

    resize_max_width = schema.Int(title=_(u"maximum width"),
                                         description=_(u"resize_max_width_key",
                                                       default=u"The maximum width for uploaded images."),
                                         required=False,
                                         default=1000,
                                         )
    resize_max_height = schema.Int(title=_(u"maximum height"),
                                         description=_(u"resize_max_height_key",
                                                       default=u"The maximum height for uploaded images."),
                                         required=False,
                                         default=1000,
                                         )
