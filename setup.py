from setuptools import setup, find_packages
from io import open

setup(
    name='django-angularmagic',
    version='1.0.0',
    description='(description)',
    long_description=open('README.md', encoding='utf-8').read(),
    author='Dmitriy Ferens',
    author_email='ferensdima@gmail.com',
    url='https://github.com/dferens/django-angularmagic',
    download_url='https://pypi.python.org/pypi/django-angularmagic',
    license='MIT',
    packages=find_packages(exclude=('tests',)),
    package_data={'': ['LICENSE', 'README.md']},
    install_requires=['Django>=1.4,<1.7'],
    include_package_data=True,
    zip_safe=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
