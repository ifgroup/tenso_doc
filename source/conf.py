import os
import sys

# Point to the 'src' folder
sys.path.insert(0, os.path.abspath('/home/juan/tenso-dev-main_2/tenso-dev-main/src'))

project = 'TENSO'
copyright = '2026, Xinxian Chen'
author = 'Xinxian Chen'
release = '1.0'

extensions = [
    'myst_nb',             
    'sphinx.ext.autodoc',  
    'sphinx.ext.napoleon', 
    'autoapi.extension',   
    'sphinx_math_dollar',  
]

# AutoAPI setup
autoapi_type = 'python'
autoapi_dirs = ['/home/juan/tenso-dev-main_2/tenso-dev-main/src/tenso']
autoapi_root = 'autoapi'
autoapi_python_use_implicit_namespaces = True

# MyST-NB setup for notebooks and markdown
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'myst-nb',
    '.ipynb': 'myst-nb',
}
nb_execution_mode = "off" 

html_theme = 'sphinx_rtd_theme'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '**.ipynb_checkpoints']
