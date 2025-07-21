# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'TENSO'
copyright = '2025, Franco Group'
author = 'Xinxian Chen'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
              "sphinx_math_dollar",
              "nbsphinx",
              "pygments",
              "myst_nb",
              "autoapi.extension",]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

#html_theme = 'sphinx_book_theme'
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_logo = '_static/logo.jpg'

nb_execution_mode = "off"
myst_enable_extensions = ["dollarmath", "amsmath"]
autoapi_dirs = ["/home/juan/tenso2/src"]
