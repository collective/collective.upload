# -*- coding: utf-8 -*-

from collective.upload import _
from collective.upload import config
from zope import schema
from zope.interface import Interface


class IUploadBrowserLayer(Interface):
    """A marker interface for the theme layer.
    """


class IUploadSettings(Interface):

    """Global upload settings. This describes records stored in the
    configuration registry and obtainable via plone.registry.
    """

    show_widget = schema.Bool(
        title=_(u'Show upload widget in folder contents view?'),
        description=_(
            u'If selected, the upload widget will be shown in the context of '
            u'the folder contents view also. The widget will be always '
            u'accessible via the "Add new…" menu regardless this value.'
        ),
        default=True,
    )

    upload_extensions = schema.TextLine(
        title=_(u'Allowed Extensions'),
        description=_(
            u'allowed_extensions_key',
            default=u'List the file extensions allowed for upload, without dots and separated by "|"'),
        required=False,
        default=config.UPLOAD_EXTENSIONS,
    )

    max_file_size = schema.Int(
        title=_(u'Max file size'),
        description=_(
            u'max_file_size_key',
            default=u'The maximum allowed file size in bytes. Please note that '
                    u'intermediate web servers may put limits on this value; '
                    u'ask your Systems Administrator in case of doubt.'),
        required=False,
        default=config.MAX_FILE_SIZE,
    )

    resize_max_width = schema.Int(
        title=_(u'maximum width'),
        description=_(
            u'resize_max_width_key',
            default=u'The maximum width for uploaded images.'),
        required=False,
        default=config.RESIZE_MAX_WIDTH,
    )

    resize_max_height = schema.Int(
        title=_(u'maximum height'),
        description=_(
            u'resize_max_height_key',
            default=u'The maximum height for uploaded images.'),
        required=False,
        default=config.RESIZE_MAX_HEIGHT,
    )
