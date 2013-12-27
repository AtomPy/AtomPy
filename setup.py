,from setuptools import setup

setup(
    name = 'AtomPy',
    version = '0.5.0',
    author = 'Josiah Boswell',
    description='A cloud atomic data service for astrophysical applications.',
    packages=['atompy'],
    install_requires = [
        "xlrd >= 0.9.2",
        "google-api-python-client >= 0.0.0",
	"xlwt >= 0.0.0",
        "gdata >= 0.0.0"
    ],
)
