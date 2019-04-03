import os

from setuptools import find_packages
from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))
package = os.path.join(here, 'Products', 'PluginRegistry')


def _package_doc(name):
    f = open(os.path.join(package, name))
    return f.read()


NAME = 'PluginRegistry'

VERSION = _package_doc('version.txt').strip()

with open('README.rst') as f:
    README = f.read()

with open('CHANGES.rst') as f:
    CHANGES = f.read()

setup(
    name='Products.PluginRegistry',
    version=VERSION,
    description='Configure application plugins based on interfaces',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Plone',
        'Framework :: Plone :: 5.2',
        'Framework :: Zope',
        'Framework :: Zope :: 4',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development',
        'Topic :: System :: Archiving :: Packaging',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    keywords='web application server zope zope2',
    author='Zope Foundation and Contributors',
    author_email='zope-cmf@lists.zope.org',
    url='https://github.com/zopefoundation/Products.PluginRegistry',
    project_urls={
        'Issue Tracker': ('https://github.com/zopefoundation/Products.'
                          'PluginRegistry/issues'),
        'Sources': 'https://github.com/zopefoundation/Products.PluginRegistry',
    },
    license='ZPL 2.1',
    packages=find_packages(),
    include_package_data=True,
    namespace_packages=['Products'],
    zip_safe=False,
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',
    install_requires=[
        'setuptools',
        'six',
        'Zope >= 4.0b4',
        'Products.GenericSetup >= 2.0b1',
    ],
    entry_points="""
    [zope2.initialize]
    Products.PluginRegistry = Products.PluginRegistry:initialize
    """,
)
