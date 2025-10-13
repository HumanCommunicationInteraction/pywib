import os
import sys
sys.path.insert(0, os.path.abspath('../../src'))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'pywib'
copyright = '2025, Guillermo Dylan Carvajal Aza, Alejandro Álvarez Varela'
author = 'Guillermo Dylan Carvajal Aza, Alejandro Álvarez Varela'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.mathjax",
    "sphinx_autodoc_typehints",
    "sphinxcontrib.bibtex",
    "myst_parser",
]

# When True (default) Sphinx prefixes documented object names with the
# full module path. Set to False to show just the object name in
# autodoc/autosummary signatures 
add_module_names = False

# Bibliography for sphinxcontrib-bibtex
bibtex_bibfiles = ['references.bib']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_favicon = 'favicon.ico'
html_static_path = ['_static']

def setup(app):
    app.add_css_file("custom.css")