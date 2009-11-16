import os
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))
package = os.path.join(here, 'Products', 'PluginRegistry')

def _package_doc(name):
    f = open(os.path.join(package, name))
    return f.read()

NAME = 'PluginRegistry'

VERSION = _package_doc('version.txt').strip()

_boundary = '\n\n'
README = ( open('README.txt').read()
         + _boundary
         + open('CHANGES.txt').read()
         )

setup(name='Products.PluginRegistry',
      version=VERSION,
      description='Configure application plugins based on interfaces',
      long_description=README,
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Plone",
        "Framework :: Zope2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Zope Public License",
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: System :: Archiving :: Packaging",
        "Topic :: Software Development :: Libraries :: "
                "Application Frameworks",
        ],
      keywords='web application server zope zope2',
      author="Zope Corporation and contributors",
      author_email="zope-cmf@lists.zope.org",
      url="http://pypi.python.org/pypi/Products.PluginRegistry",
      license="ZPL 2.1 (http://www.zope.org/Resources/License/ZPL-2.1)",
      packages=find_packages(),
      include_package_data=True,
      namespace_packages=['Products'],
      zip_safe=False,
      install_requires=[
          'setuptools',
#          'Zope >= 2.10'
          ],
      entry_points="""
      [zope2.initialize]
      Products.PluginRegistry = Products.PluginRegistry:initialize
      """,
      )
