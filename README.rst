Products.PluginRegistry
=======================

Products.PluginRegistry offers a simple persistent registry which allows
the site manager to registe components for specific interfaces, and
to order them.

Installation
------------

The normal way it install this package is via ``setuptools``, either
via ``easy_install`` into a virtual environment::

  $ cd /path/to/virtualenv
  $ bin/easy_install Products.PluginRegistry

or by including the package in the configuration for a ``zc.buildout``-based
deployment::

  $ cd /path/to/buildout
  $ grep "eggs =" buildout.cfg
  ...
  eggs = Products.PluginRegistry
  ...

The product can also be installed as a depencency of another distribution.

To install this package manually, without using setuptools,
untar the package file downloaded from the PyPI site and look for
the folder named "PluginRegistry" underneath the "Products" folder
at the root of the extracted tarball. Copy or link this "PluginRegistry"
folder into your Zope "Products" folder and restart Zope.
