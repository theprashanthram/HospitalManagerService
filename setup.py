from setuptools import find_packages, setup, Command
import subprocess
import os
import sys

class GenerateAPISchemaCommand(Command):
    description = "Generate OpenAPI schema file"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.makedirs('build', exist_ok=True)
        subprocess.run(f"{sys.executable} manage.py spectacular --file build/schema.yml".split(' '))

setup(
    name='hospitalmanagerservice',
    version='0.1',
    packages=find_packages(),
    cmdclass={
        'generate_api_schema': GenerateAPISchemaCommand,
    },
    install_requires=[
        'Django==4.2.21',
        'djangorestframework==3.16.0',
        'djangorestframework-simplejwt==5.5.0',
        'asgiref==3.8.1',
        'sqlparse==0.5.3',
        'typing_extensions==4.13.2',
        'drf-spectacular',
        'psycopg2-binary',
        'pytest',
        'pytest-cov',
        'pytest-django',
        'pytest-html',
    ]
)
