from distutils.core import setup

setup(
    name="aws_tools",
    version="0.0.1",
    packages=[""],
    package_dir={"": "aws_tools"},
    url="",
    license="",
    author="Vlad Vasiliu",
    author_email="",
    description="",
    install_requires=[
        "Django",
        "django-choices",
        "celery",
        "django-celery-beat",
        "boto3",
        "botocore",
        "djangorestframework",
        "django-filter",
        "django-netfields",
    ],
    tests_require=["moto"],
)
