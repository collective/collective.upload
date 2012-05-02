# -*- coding: utf-8 -*-

PROJECTNAME = 'collective.upload'

# XXX: we don't want to put limits here; that should be user configurable
UPLOAD_EXTENSIONS = u'gif, jpeg, jpg, png'
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB; that should be big enough
RESIZE_MAX_WIDTH = 3872  # 10 MP landscape
RESIZE_MAX_HEIGHT = 3872  # 10 MP portrait
