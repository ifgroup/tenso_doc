import os
import sys

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
# Resolve the path to the tenso source relative to this conf.py so the
# documentation can be built from any machine without editing this file.
_docs_dir = os.path.dirname(os.path.abspath(__file__))
_src_dir   = os.path.join(_docs_dir, '..', 'src', 'tenso')
sys.path.insert(0, os.path.abspath(_src_dir))

# ---------------------------------------------------------------------------
# Project information
# ---------------------------------------------------------------------------
project   = 'TENSO'
copyright = '2026, Xinxian Chen and Ignacio Franco'
author    = 'Xinxian Chen and Ignacio Franco'
release   = '1.0'

# ---------------------------------------------------------------------------
# Extensions
# ---------------------------------------------------------------------------
extensions = [
    'myst_nb',                  # Jupyter notebooks + MyST markdown
    'sphinx.ext.autodoc',       # Docstring extraction
    'sphinx.ext.napoleon',      # NumPy / Google docstring styles
    'sphinx.ext.mathjax',       # Math rendering
    'sphinx.ext.viewcode',      # [source] links in API docs
    'autoapi.extension',        # Automatic API docs from source
    'sphinx_math_dollar',       # $...$ and $$...$$ math in .md files
    'sphinx_design',            # Grid cards on the landing page
]

# ---------------------------------------------------------------------------
# AutoAPI
# ---------------------------------------------------------------------------
autoapi_type                          = 'python'
autoapi_dirs                          = [os.path.abspath(_src_dir)]
autoapi_root                          = 'autoapi'
autoapi_keep_files = True       # skip regeneration if source unchanged

# ---------------------------------------------------------------------------
# MyST-NB (notebooks and Markdown)
# ---------------------------------------------------------------------------
source_suffix = {
    '.rst': 'restructuredtext',
    '.md':  'myst-nb',
    '.ipynb': 'myst-nb',
}
nb_execution_mode = 'off'   # do not re-execute notebooks at build time

myst_enable_extensions = [
    'colon_fence',   # :::  directive syntax in .md
    'dollarmath',    # $...$ math in .md
    'tasklist',
]

# ---------------------------------------------------------------------------
# HTML output
# ---------------------------------------------------------------------------
html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
    'sticky_navigation': True,
    'includehidden': True,
}

html_static_path = ['_static']

# ---------------------------------------------------------------------------
# General
# ---------------------------------------------------------------------------
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    '**.ipynb_checkpoints',
]

# Show the full module path in API docs (e.g. tenso.heom.eom.Hierarchy)
add_module_names = True
