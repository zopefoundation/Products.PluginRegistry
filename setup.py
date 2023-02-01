from setuptools import find_packages
from setuptools import setup


NAME = 'PluginRegistry'

with open('README.rst') as f:
    README = f.read()

with open('CHANGES.rst') as f:
    CHANGES = f.read()

setup(
    name='Products.PluginRegistry',
    version='2.0',
    description='Configure application plugins based on interfaces',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Plone',
        'Framework :: Plone :: 5.2',
        'Framework :: Plone :: Core',
        'Framework :: Zope',
        'Framework :: Zope :: 5',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development',
        'Topic :: System :: Archiving :: Packaging',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    keywords='web application server zope zope2',
    author='Zope Foundation and Contributors',
    author_email='zope-dev@zope.dev',
    url='https://github.com/zopefoundation/Products.PluginRegistry',
    project_urls={
        'Issue Tracker': ('https://github.com/zopefoundation/Products.'
                          'PluginRegistry/issues'),
        'Sources': 'https://github.com/zopefoundation/Products.PluginRegistry',
    },
    license='ZPL 2.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    namespace_packages=['Products'],
    zip_safe=False,
    python_requires='>=3.7',
    install_requires=[
        'setuptools',
        'Zope >= 4.0b4',
        'Products.GenericSetup >= 2.0b1',
    ],
    entry_points="""
    [zope2.initialize]
    Products.PluginRegistry = Products.PluginRegistry:initialize
    """,
)
