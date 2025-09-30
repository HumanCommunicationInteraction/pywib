from setuptools import find_packages, setup

def read(file_path):
	with open(file_path, "r") as in_stream:
		return in_stream.read()


setup(
    name='',
    packages=find_packages(),
    version='0.1.0',
    description='',
    author='Guillermo Dylan Carvajal Aza',
    author_email='carvajalguillermo@uniovi.es',
    keywords=['HCI', 'Web Interaction', 'Analyzer'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',],
	long_description=read("README.md"),
    long_description_content_type="text/markdown",
)