# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import Interface

from plone.theme.interfaces import IDefaultPloneLayer

from collective.upload import _
from collective.upload import config


class IUploadBrowserLayer(IDefaultPloneLayer):
    """A marker interface for the theme layer.
    """


class IUploadSettings(Interface):
    """Global upload settings. This describes records stored in the
    configuration registry and obtainable via plone.registry.
    """

    upload_extensions = schema.TextLine(
        title=_(u"Allowed Extensions"),
        description=_(u"allowed_extensions_key",
        default=u"List the file extensions allowed for upload, "
                u"without dot, comma separated"),
        required=False,
        default=config.UPLOAD_EXTENSIONS,
        )

    max_file_size = schema.Int(
        title=_(u"Max file size"),
        description=_(u"max_file_size_key",
                      default=u"The maximum allowed file size in bytes. "
                              u"Please note that intermediate web servers "
                              u"may put limits on this value; ask your "
                              u"Systems Administrator in case of doubt."),
        required=False,
        default=config.MAX_FILE_SIZE,)

    resize_max_width = schema.Int(
        title=_(u"maximum width"),
        description=_(u"resize_max_width_key",
                      default=u"The maximum width for uploaded images."),
        required=False,
        default=config.RESIZE_MAX_WIDTH,
        )

    resize_max_height = schema.Int(
        title=_(u"maximum height"),
        description=_(u"resize_max_height_key",
                      default=u"The maximum height for uploaded images."),
        required=False,
        default=config.RESIZE_MAX_HEIGHT,
        )
