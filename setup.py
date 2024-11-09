from setuptools import setup, find_packages

setup(
    name='todo-api',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'flask-jwt-extended',
        'flask-bcrypt',
        'flask-cors',
        'python-dotenv',
        'marshmallow'
    ],
)
