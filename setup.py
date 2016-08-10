from setuptools import find_packages, setup


with open('README.rst', 'r') as fh:
    description = '\n'.join(fh.readlines())

tests_require = [
    'pytest>=2.6.0',
    'pytest-cov>=1.7.0',
]

setup(
    name='wsgi-basic-auth',
    version='0.1.0',
    description=description,
    url='https://github.com/mvantellingen/wsgi-basic-auth',
    author="Michael van Tellingen",
    author_email="michaelvantellingen@gmail.com",
    install_requires=[
        'webob>=1.0.0',
    ],
    tests_require=tests_require,
    extras_require={'test': tests_require},
    package_dir={'': 'src'},
    py_modules=['wsgi_basic_auth'],
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
    ],
    zip_safe=False,
)
