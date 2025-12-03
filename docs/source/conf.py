# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
from datetime import datetime
sys.path.insert(0, os.path.abspath('../..'))  # ← ВАЖНО!
project = 'password-generator'
copyright = '2025, Варламов Богдан'
author = 'Варламов Богдан'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',          # Поддержка Google/Numpy стилей
    'sphinx.ext.viewcode',          # Ссылки на исходный код
    'sphinx_autodoc_typehints',     # Красивые типы
]

# Napoleon: используем Google стиль (у тебя в коде — Google)
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True

# --- Темы ---
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': 4,
}

# --- Автодокументация ---
autoclass_content = 'both'
autodoc_member_order = 'bysource'
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'private-members': False,
    'special-members': '__init__',
    'inherited-members': False,
    'show-inheritance': True,
}

# --- Путь к статике (если нужно) ---
html_static_path = ['_static']