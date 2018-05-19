from distutils.core import setup

setup(
    name = 'djangohushrest',
    packages = ['djangohushrest'],
    version = '1.0.0',  # Ideally should be same as your GitHub release tag varsion
    description = 'djangohushrest provides a base for simple restful Django resources.',
    author = 'Lawrence Wakefield',
    author_email = 'lawrence@iamlawrence.me',
    url = 'https://github.com/lwakefield/django-hush-rest',
    download_url = 'https://github.com/lwakefield/django-hush-rest/archive/v1.0.0.tar.gz',
    keywords = ['rest', 'crud', 'django'],
    install_requires=['django'],
    classifiers = [],
)
