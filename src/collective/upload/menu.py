# -*- coding:utf-8 -*-
from collective.upload import _
from collective.upload.config import ICON
from plone.app.contentmenu.menu import FactoriesMenu as BaseMenu
from plone.app.contentmenu.menu import FactoriesSubMenuItem as BaseMenuItem
from plone.app.contentmenu.interfaces import IFactoriesSubMenuItem
from zope.interface import implements


class FactoriesSubMenuItem(BaseMenuItem):
    implements(IFactoriesSubMenuItem)

    submenuId = 'upload_contentmenu_factory'


class FactoriesMenu(BaseMenu):
    """ Customized version of FactoriesMenu
    """

    def getMenuItems(self, context, request):
        # menuitems is a list of tal-friendly dictionaries
        menuitems = super(FactoriesMenu, self).getMenuItems(context, request)

        url = context.absolute_url()
        new_menu = {'extra': {'separator': None,
                              'id': 'multiple-files',
                              'class': 'contenttype-multiple-files'},
                    'submenu': None,
                    'description': _(u'A form to upload multiple files.'),
                    'title': _(u'Multiple Files'),
                    'action': '%s/@@media_uploader' % url,
                    'selected': False,
                    'id': 'Multiple Files',
                    'icon': ICON}
        menuitems.insert(-1, new_menu)

        return menuitems
