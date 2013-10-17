from setuptools import setup

setup(
    name = 'AtomPy',
    version = '0.5.0',
    author = 'Josiah Boswell',
    license='LICENSE.txt',
    description='A cloud atomic data service for astrophysical applications.',
    long_description = open('atompy/README.txt').read(),
    packages=['atompy'],
    install_requires = [
        "xlrd >= 0.9.2",
        "google-api-python-client >= 0.0.0",
        "pandas >= 0.11.0",
	"xlwt >= 0.0.0"
    ],
)
