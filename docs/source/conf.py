# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information


# Standard libs
import os
import sys

# DALEC imports
import sphinx_rtd_theme

sys.path.insert(0, os.path.abspath("../.."))

project = "Dalec - Gitlab"
copyright = "2023, Webu"
author = "Webu"
release = "0.1.4"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    # "sphinx.ext.intersphinx",
    # "sphinx.ext.viewcode",
    # "sphinx.ext.napoleon",
    "myst_parser",
    "sphinx_rtd_theme",
]

templates_path = ["_templates"]
exclude_patterns = []
autodoc_mock_imports = ["django", "dalec", "gitlab"]

autodoc_default_options = {
    "member-order": "bysource",
    "undoc-members": True,
    "private-members": True,
}

source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
