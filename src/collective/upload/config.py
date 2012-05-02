# -*- coding: utf-8 -*-

PROJECTNAME = 'collective.upload'

# XXX: we don't want to put limits here; that should be user configurable
UPLOAD_EXTENSIONS = u'gif, jpeg, jpg, png'

# XXX: that should be big enough
MAX_FILE_SIZE = 10 * 1024  # 10MB

# XXX: the following values are for images of aprox 10 MP
RESIZE_MAX_WIDTH = 3872
RESIZE_MAX_HEIGHT = 3872
