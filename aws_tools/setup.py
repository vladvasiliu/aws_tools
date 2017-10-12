from distutils.core import setup

setup(
    name='aws_tools',
    version='0.0.1',
    packages=[''],
    package_dir={'': 'aws_tools'},
    url='',
    license='',
    author='Vlad Vasiliu',
    author_email='',
    description='',
    install_requires=[
        'Django',
        'django-choices',
        'celery',
        'django-celery-beat',
        'boto3',
        'django-bootstrap3',
        'django-auth-adfs',
        'django-cors-headers',
        'djangorestframework',
        'coreapi',
        'markdown',
        'django-filter',
        'coreapi',
        'django-cors-headers'
    ],
    tests_require=['moto']
)
