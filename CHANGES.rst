Change Log
==========

1.4.1 (2019-06-18)
------------------

- Add ``movePluginsTop`` method to registry.


1.4 (2016-03-01)
----------------

- Fix usage of ``os.path.split()``. Could result in Errors during import
  on Windows.


1.3 (2012-02-27)
----------------

- Change default encoding for ``importexport`` from None to utf-8.


1.3b1 (2010-07-01)
------------------

- Improved test coverage.

- Removed dependency on ``zope.app.testing``.

- Dropped support for use with  Zope < 2.12.

- Added a buildout for running tests.


1.2 (2009-11-15)
----------------

- Moved documentation out of the product directory.

- Fixed plugin management links on the Active screen.

- Fixed deprecation warnings for use of Globals.

- Purged old Zope2 interfaces for Zope 2.12 compatibility.

- Updated GenericSetup import to initialize plugin registry's ``_plugins``
  attribute if necessary.


1.1.3 (2007-11-28)
------------------

- Fixed bad behaviour when moving the top plugin up.
  https://bugs.launchpad.net/bugs/164717


1.1.2 (2007-04-24)
------------------

- Updated ``PluginRegistry.listPlugins`` to drop previously-activated
  plugins when they no longer implement the plugin interface.
  https://bugs.launchpad.net/zope-pas/+bug/161281

- Updated ``exportimport`` to skip adding duplicate interfaces during
  non-purge imports.
  https://bugs.launchpad.net/zope-pas/+bug/161280

- Fixed test breakage on Zope 2.10.


1.1.1 (2006-07-25)
------------------

- Added workaround for autogen factories which assume they can
  pass an ID to the registry's ``__init__``.  In particular, this
  allows the registry to be created and popluated as a "normal"
  content object using GenericSetup.

- Improved BBB for testing under Zope 2.8.


1.1 (2006-02-25)
----------------

- Moved interfaces into a top-level module (no need for a package),
  and made them forward-compatible with Z3 interfaces.

- Wired in DAV / FTP / ExternalEditor support for the registry,
  along with a ZMI form for updating it as XML.

- Added support for exporting / importing the registry via GenericSetup.

- Moved from CVS to subversion (2005-10-14).

- Removed deprecation warings under Zope 2.8.x.

- Repaired warings appearing in Zope 2.8.5 due to a couple typos
  in security declarations.


1.0.2 (2005-01-31)
------------------

- Simplified package directory computation using ``package_home``.

- Added ``test_suite`` to registry tests to improve testability under
  ``zopectl test``.


1.0.1 (2004-04-28)
------------------

- Initial public release.


1.0 (2004-04-28)
----------------

- Vendor import from ZC repository.
