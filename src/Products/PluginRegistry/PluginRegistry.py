##############################################################################
#
# Copyright (c) 2001 Zope Foundation and Contributors
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this
# distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################
""" Classes: PluginRegistry
"""
import logging
import os

import six

from AccessControl import ClassSecurityInfo
from AccessControl.class_init import default__class_init__ as InitializeClass
from AccessControl.Permissions import manage_users as ManageUsers
from Acquisition import aq_inner
from Acquisition import aq_parent
from App.Common import package_home
from App.ImageFile import ImageFile
from OFS.interfaces import IWriteLock
from OFS.SimpleItem import SimpleItem
from Persistence import PersistentMapping
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from zope.interface import implementer

from Products.PluginRegistry.interfaces import IPluginRegistry


try:
    from Products.PluginRegistry.exportimport import PluginRegistryExporter
    from Products.PluginRegistry.exportimport import _updatePluginRegistry
except ImportError:
    _HAS_GENERIC_SETUP = False
else:
    _HAS_GENERIC_SETUP = True

product_dir = package_home(globals())
product_prefix = os.path.split(product_dir)[0]

_wwwdir = os.path.join(product_dir, 'www')

logger = logging.getLogger('PluginRegistry')


@implementer(IPluginRegistry, IWriteLock)
class PluginRegistry(SimpleItem):

    """ Implement IPluginRegistry as an independent, ZMI-manageable object.

    o Each plugin type holds an ordered list of (id, wrapper) tuples.
    """

    security = ClassSecurityInfo()
    meta_type = 'Plugin Registry'
    zmi_icon = 'fas fa-plug'
    _plugins = None

    def __init__(self, plugin_type_info=()):

        if isinstance(plugin_type_info, six.string_types):
            # some tool is passing us our ID.
            raise ValueError('Must pass a sequence of plugin info dicts!')

        self._plugin_types = [x[0] for x in plugin_type_info]
        self._plugin_type_info = PersistentMapping()
        for interface in plugin_type_info:
            self._plugin_type_info[interface[0]] = {
                  'id': interface[1],
                  'title': interface[2],
                  'description': interface[3]}

    #
    #   IPluginRegistry implementation
    #
    @security.protected(ManageUsers)
    def listPluginTypeInfo(self):

        """ See IPluginRegistry.
        """
        result = []

        for ptype in self._plugin_types:

            info = self._plugin_type_info[ptype].copy()
            info['interface'] = ptype
            info['methods'] = list(ptype.names())

            result.append(info)

        return result

    @security.protected(ManageUsers)
    def listPlugins(self, plugin_type):

        """ See IPluginRegistry.
        """
        result = []

        parent = aq_parent(aq_inner(self))

        for plugin_id in self._getPlugins(plugin_type):

            plugin = parent._getOb(plugin_id)
            if not _satisfies(plugin, plugin_type):
                logger.debug('Active plugin %s no longer implements %s' %
                             (plugin_id, plugin_type))
            else:
                result.append((plugin_id, plugin))

        return result

    @security.protected(ManageUsers)
    def getPluginInfo(self, plugin_type):

        """ See IPluginRegistry.
        """
        plugin_type = self._getInterfaceFromName(plugin_type)
        return self._plugin_type_info[plugin_type]

    @security.protected(ManageUsers)
    def listPluginIds(self, plugin_type):

        """ See IPluginRegistry.
        """

        return self._getPlugins(plugin_type)

    @security.protected(ManageUsers)
    def activatePlugin(self, plugin_type, plugin_id):

        """ See IPluginRegistry.
        """
        plugins = list(self._getPlugins(plugin_type))

        if plugin_id in plugins:
            raise KeyError('Duplicate plugin id: {0}'.format(plugin_id))

        parent = aq_parent(aq_inner(self))
        plugin = parent._getOb(plugin_id)

        if not _satisfies(plugin, plugin_type):
            raise ValueError(
                'Plugin does not implement {0}'.format(plugin_type))

        plugins.append(plugin_id)
        self._plugins[plugin_type] = tuple(plugins)

    @security.protected(ManageUsers)
    def deactivatePlugin(self, plugin_type, plugin_id):

        """ See IPluginRegistry.
        """
        plugins = list(self._getPlugins(plugin_type))

        if plugin_id not in plugins:
            raise KeyError('Invalid plugin id: {0}'.format(plugin_id))

        plugins = [x for x in plugins if x != plugin_id]
        self._plugins[plugin_type] = tuple(plugins)

    @security.protected(ManageUsers)
    def movePluginsTop(self, plugin_type, ids_to_move):

        """ See IPluginRegistry.
        """
        ids = list(self._getPlugins(plugin_type))
        indexes = list(map(ids.index, ids_to_move))
        indexes.sort()
        for i1 in indexes:
            ids.insert(0, ids.pop(i1))
        self._plugins[plugin_type] = tuple(ids)

    @security.protected(ManageUsers)
    def movePluginsUp(self, plugin_type, ids_to_move):

        """ See IPluginRegistry.
        """
        ids = list(self._getPlugins(plugin_type))
        count = len(ids)

        indexes = list(map(ids.index, ids_to_move))
        indexes.sort()

        for i1 in indexes:

            if i1 < 0 or i1 >= count:
                raise IndexError(i1)

            i2 = i1 - 1
            if i2 < 0:
                # i1 is already on top
                continue

            ids[i2], ids[i1] = ids[i1], ids[i2]

        self._plugins[plugin_type] = tuple(ids)

    @security.protected(ManageUsers)
    def movePluginsDown(self, plugin_type, ids_to_move):

        """ See IPluginRegistry.
        """
        ids = list(self._getPlugins(plugin_type))
        count = len(ids)

        indexes = list(map(ids.index, ids_to_move))
        indexes.sort()
        indexes.reverse()

        for i1 in indexes:

            if i1 < 0 or i1 >= count:
                raise IndexError(i1)

            i2 = i1 + 1
            if i2 == len(ids):
                # i1 is already on the bottom
                continue

            ids[i2], ids[i1] = ids[i1], ids[i2]

        self._plugins[plugin_type] = tuple(ids)

    #
    #   ZMI
    #
    arrow_right_gif = ImageFile('www/arrow-right.gif', globals())
    arrow_left_gif = ImageFile('www/arrow-left.gif', globals())
    arrow_up_gif = ImageFile('www/arrow-up.gif', globals())
    arrow_down_gif = ImageFile('www/arrow-down.gif', globals())

    @security.protected(ManageUsers)
    def manage_activatePlugins(self, plugin_type, plugin_ids, RESPONSE):
        """ Shim into ZMI.
        """
        interface = self._getInterfaceFromName(plugin_type)
        for id in plugin_ids:
            self.activatePlugin(interface, id)
        RESPONSE.redirect('%s/manage_plugins?plugin_type=%s' %
                          (self.absolute_url(), plugin_type))

    @security.protected(ManageUsers)
    def manage_deactivatePlugins(self, plugin_type, plugin_ids, RESPONSE):
        """ Shim into ZMI.
        """
        interface = self._getInterfaceFromName(plugin_type)
        for id in plugin_ids:
            self.deactivatePlugin(interface, id)

        RESPONSE.redirect('%s/manage_plugins?plugin_type=%s' %
                          (self.absolute_url(), plugin_type))

    @security.protected(ManageUsers)
    def manage_movePluginsUp(self, plugin_type, plugin_ids, RESPONSE):
        """ Shim into ZMI.
        """
        interface = self._getInterfaceFromName(plugin_type)
        self.movePluginsUp(interface, plugin_ids)

        RESPONSE.redirect('%s/manage_plugins?plugin_type=%s' %
                          (self.absolute_url(), plugin_type))

    @security.protected(ManageUsers)
    def manage_movePluginsDown(self, plugin_type, plugin_ids, RESPONSE):
        """ Shim into ZMI.
        """
        interface = self._getInterfaceFromName(plugin_type)
        self.movePluginsDown(interface, plugin_ids)

        RESPONSE.redirect('%s/manage_plugins?plugin_type=%s' %
                          (self.absolute_url(), plugin_type))

    @security.protected(ManageUsers)
    def getAllPlugins(self, plugin_type):

        """ Return a mapping segregating active / available plugins.

        'plugin_type' is the __name__ of the interface.
        """
        interface = self._getInterfaceFromName(plugin_type)

        active = self._getPlugins(interface)
        available = []

        for id, value in aq_parent(aq_inner(self)).objectItems():
            if _satisfies(value, interface):
                if id not in active:
                    available.append(id)

        return {'active': active, 'available': available}

    @security.protected(ManageUsers)
    def removePluginById(self, plugin_id):

        """ Remove a plugin from any plugin types which have it configured.
        """
        for plugin_type in self._plugin_types:

            if plugin_id in self._getPlugins(plugin_type):
                self.deactivatePlugin(plugin_type, plugin_id)

    security.declareProtected(ManageUsers,  # noqa: D001
                              'manage_plugins')
    manage_plugins = PageTemplateFile('plugins', _wwwdir)
    security.declareProtected(ManageUsers,  # noqa: D001
                              'manage_active')
    manage_active = PageTemplateFile('active_plugins', _wwwdir)
    manage_twoLists = PageTemplateFile('two_lists', _wwwdir)

    manage_options = (({'label': 'Plugins', 'action': 'manage_plugins'},
                       {'label': 'Active', 'action': 'manage_active'})
                      + SimpleItem.manage_options)

    if _HAS_GENERIC_SETUP:
        security.declareProtected(ManageUsers,  # noqa: D001
                                  'manage_exportImportForm')
        manage_exportImportForm = PageTemplateFile('export_import', _wwwdir)

        @security.protected(ManageUsers)
        def getConfigAsXML(self):
            """ Return XML representing the registry's configuration.
            """
            pre = PluginRegistryExporter(self).__of__(self)
            return pre.generateXML()

        @security.protected(ManageUsers)
        def manage_exportImport(self, updated_xml, should_purge, RESPONSE):
            """ Parse XML and update the registry.
            """
            # encoding?
            _updatePluginRegistry(self, updated_xml, should_purge)
            RESPONSE.redirect('%s/manage_exportImportForm'
                              '?manage_tabs_message=Registry+updated.' %
                              self.absolute_url())

        @security.protected(ManageUsers)
        def manage_FTPget(self, REQUEST, RESPONSE):
            """
            """
            return self.getConfigAsXML()

        @security.protected(ManageUsers)
        def PUT(self, REQUEST, RESPONSE):
            """
            """
            xml = REQUEST['BODYFILE'].read()
            _updatePluginRegistry(self, xml, True)

        manage_options = (manage_options[:2]
                          + ({'label': 'Export / Import',
                              'action': 'manage_exportImportForm'},)
                          + manage_options[2:])

    #
    #   Helper methods
    #
    @security.private
    def _getPlugins(self, plugin_type):

        if plugin_type not in self._plugin_types:
            raise KeyError(plugin_type)

        if self._plugins is None:
            self._plugins = PersistentMapping()

        return self._plugins.setdefault(plugin_type, ())

    @security.private
    def _getInterfaceFromName(self, plugin_type_name):

        """ Convert the string name to an interface.

        o Raise KeyError if no such interface is known.
        """
        found = [x[0] for x in self._plugin_type_info.items()
                 if x[1]['id'] == plugin_type_name]
        if not found:
            raise KeyError(plugin_type_name)

        if len(found) > 1:
            raise KeyError('Waaa!:  {0}'.format(plugin_type_name))

        return found[0]


InitializeClass(PluginRegistry)


def _satisfies(plugin, iface):
    checker = getattr(iface, 'providedBy', None)
    if checker is None:  # BBB for Zope 2.7?
        checker = iface.isImplementedBy

    return checker(plugin)


def emptyPluginRegistry(ignored):
    """ Return empty registry, for filling from setup profile.
    """
    return PluginRegistry(())
