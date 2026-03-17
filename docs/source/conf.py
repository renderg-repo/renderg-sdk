# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
from recommonmark.parser import CommonMarkParser

project = 'RenderGSDK'
copyright = '2025, RenderG'
author = 'RenderG'
release = '0.1.29'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

import os
import sys
sys.path.insert(0, os.path.abspath('../../'))

source_parsers = {
    '.md': CommonMarkParser,
}

source_suffix = ['.rst', '.md']

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
]

templates_path = ['_templates']
exclude_patterns = []

language = 'zh_cn'

# -- autodoc / typehints configuration --------------------------------------
# 使用 description 模式：类型信息来自 Napoleon 解析的 Google-style 文档，
# 而非函数签名，避免 sphinx_autodoc_typehints 生成无法解析的交叉引用。
autodoc_typehints = 'none'
autoclass_content = 'both'

# 抑制 nitpick 模式下的交叉引用未找到警告（optional、callable 等非 Python 标准类型）
nitpick_ignore = [
    ('py:class', 'optional'),
    ('py:class', 'callable'),
    ('py:class', 'iterable'),
    ('py:class', 'str/int'),
    ('py:class', 'enum.Enum'),
    ('py:class', 'logging.Logger'),
    ('py:attr',  'download_path'),
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# 配置sphinx_rtd_theme主题选项
def setup(app):
    app.add_css_file('custom.css')
    app.add_js_file('custom.js')

# 主题配置选项
html_theme_options = {
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'style_nav_header_background': '#2980B9',
}
