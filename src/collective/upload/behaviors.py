# -*- coding: utf-8 -*-
from zope.interface import Interface

import warnings


class IMultipleUpload(Interface):
    """ just the behavior interface """

    warnings.warn(
        'Use of the IMultipleUpload behavior is no longer needed to have '
        'access to the multiple file upload widget and will be removed in '
        'collective.upload v1.0.', DeprecationWarning, stacklevel=2)
