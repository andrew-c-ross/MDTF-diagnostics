# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import re
import abc
import inspect
import unittest.mock as mock
import traceback
stdlib_path = os.path.dirname(traceback.__file__)
cwd = os.path.dirname(os.path.realpath(__file__))
code_root = os.path.abspath(os.path.join(cwd, '..'))
sys.path.insert(0, os.path.abspath(cwd))
sys.path.insert(0, code_root)
sys.path.insert(0, os.path.join(code_root, 'src'))

# AutoStructify needed for getting full Sphinx features from markdown (.md) files
# https://recommonmark.readthedocs.io/en/latest/auto_structify.html
import recommonmark
from recommonmark.transform import AutoStructify

# mock out imports of non-standard library modules -- not installed when
# we build docs on readthedocs
autodoc_mock_imports = [
    'numpy', 'xarray', 'cftime', 'cfunits', 'cf_xarray',
    'pandas', 'intake', 'intake_esm', "yaml"
]
# need to manually mock out explicit patching of cf_xarray.accessor done
# on import in xr_parser; may be possible to do this with mock.patch() but the
# following works
mock_accessor = mock.MagicMock(**({
    '__name__': 'accessor', '__doc__': '', # for functools.wraps
    'CFDatasetAccessor': object, 'CFDataArrayAccessor': object
}))
sys.modules['cf_xarray'] = mock.Mock()
setattr(sys.modules['cf_xarray'], 'accessor', mock_accessor)

# Also necessary to manually mock out cfunits.Units since src.units.Units
# inherits from it.


class Units:

    def __init__(self, units=None, calendar=None, formatted=False, names=False,
                 definition=False, _ut_unit=None):

        """Initialization is as in `cfunits.Units
        <https://ncas-cms.github.io/cfunits/cfunits.Units.html>`__."""
        pass


sys.modules['cfunits'] = mock.Mock(name='cfunits')
setattr(sys.modules['cfunits'], 'Units', Units)

# -- Project information -----------------------------------------------------

project = u'MDTF Diagnostics'
copyright = u'2022, Model Diagnostics Task Force'
author = u'Model Diagnostics Task Force'

# The short X.Y version
version = u''
# The full version, including alpha/beta/rc tags
release = u'3.0'

# only used for resolving relative links in markdown docs
# use develop branch because that's what readthedocs is configured to use
_project_github_url = 'https://github.com/NOAA-GFDL/MDTF-diagnostics/tree/main/'

# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '5.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'copy_external_docs',
    'sphinx.ext.autosummary',
    'sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'recommonmark'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown'
}

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
# NB: this is *only* applied to built .rst files, not to the imports done
# by sphinx-apidoc.
exclude_patterns = [u'_build', 'Thumbs.db', '**/test*']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'default'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'alabaster'

# Theme options are theme-specific.
# See https://alabaster.readthedocs.io/en/latest/customization.html
html_theme_options = {
    'page_width': '1152px',
    'sidebar_width': '280px',
    'sidebar_collapse': False,
    'fixed_sidebar': False,
    'extra_nav_links': {
        "Full documentation [PDF]": "https://mdtf-diagnostics.readthedocs.io/_/downloads/en/latest/pdf/"
    }
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# Sphinx automatically copies referenced image files.
html_static_path = ['_static']

# # Paths (filenames) here must be relative to (under) html_static_path as above:
html_css_files = [
    '_static/custom.css',
]

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
html_sidebars = {
    '**': ['about.html', 'navigation.html', 'relations.html', 'searchbox.html']
}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'MDTF-diagnosticsdoc'


# -- Options for LaTeX output ------------------------------------------------

# pdflatex is default, xelatex recommended for better unicode support
latex_engine = 'xelatex'

# A dictionary that contains LaTeX snippets that override those Sphinx
# usually puts into the generated .tex files.
latex_elements = {
    'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    'pointsize': '11pt',
    'geometry': r"\usepackage[xetex,letterpaper]{geometry}",
    # Latex figure (float) alignment
    'figure_align': 'H',
    # Additional stuff for the LaTeX preamble.
    'preamble': r"""
        \RequirePackage{unicode-math}
        \makeatletter
        \fancypagestyle{normal}{
            \fancyhf{}
            \fancyfoot[LE,RO]{{\py@HeaderFamily\thepage}}
            % \fancyfoot[LO]{{\py@HeaderFamily\nouppercase{\rightmark}}}
            % \fancyfoot[RE]{{\py@HeaderFamily\nouppercase{\leftmark}}}
            \fancyhead[LE,RO]{{\py@HeaderFamily \@title, \py@release}}
            \renewcommand{\headrulewidth}{0.4pt}
            \renewcommand{\footrulewidth}{0pt}
        }
        \fancypagestyle{plain}{
            % used for first page of a chapter only
            \fancyhf{}
            \fancyfoot[LE,RO]{{\py@HeaderFamily\thepage}}
            \renewcommand{\footrulewidth}{0pt}
        }
        \setlength{\headheight}{13.61pt} % otherwise get errors from fancyhdr
        \makeatother
    """,
    'extraclassoptions': 'openany'
}
# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        # "Main" PDF containing all source files. This is built automatically by
        # ReadTheDocs (filename is fixed by the RTD account name).
        'tex_all', 'mdtf-diagnostics.tex',
        u'MDTF Diagnostics Documentation', author, 'manual'
    )
]

latex_additional_files = [
    'latex/latexmkrc'
]

latex_logo = 'img/CPO_MAPP_MDTF_Logo.jpg'

# # For "manual" documents, if this is true, then top-level headings are
# # parts, not chapters.
# latex_toplevel_sectioning = 'chapter'

# If true, show page references after internal links.
latex_show_pagerefs = True

# If true, show URL addresses after external links.
latex_show_urls = 'footnote'

# If false, no module index is generated.
latex_domain_indices = True

# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'mdtf-diagnostics', u'MDTF-diagnostics Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'MDTF-diagnostics', u'MDTF-diagnostics Documentation',
     author, 'MDTF-diagnostics', 'One line description of project.',
     'Miscellaneous'),
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']


# == Extension configuration ==================================================

# -- Autodoc configuration

# set options, see http://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
autodoc_member_order = 'bysource'
autoclass_content = 'class'
autodoc_default_options = {
    'special-members': '__init__',# __post_init__',
    'inherited-members': True
}


def no_namedtuple_attrib_docstring(app, what, name, obj, options, lines):
    """Remove duplicated doc info in namedtuples.
    https://chrisdown.name/2015/09/20/removing-namedtuple-docstrings-from-sphinx.html
    """
    is_namedtuple_docstring = (
        len(lines) == 1 and
        lines[0].startswith('Alias for field number')
    )
    if is_namedtuple_docstring:
        # We don't return, so we need to purge in-place
        del lines[:]


def abbreviate_logger_in_signature(app, what, name, obj, options, signature, return_annotation):
    """Abbreviate logger arguments in function/method signatures.
    """
    if isinstance(signature, str):
        signature = re.sub(r'log=<Logger[^>]+>', r'log=<Logger>', signature)
    return (signature, return_annotation)


def skip_members_handler(app, what, name, obj, skip, options):
    """1) Skip unit test related classes and methods;
    2) Skip all inherited methods from python builtins,
    3) Skip __init__ on abstract base classes, or if it doesn't have its own
        docstring.
    """
    def _get_class_that_defined_method(meth):
        # https://stackoverflow.com/a/25959545
        if inspect.ismethod(meth) or (
            inspect.isbuiltin(meth) and getattr(meth, '__self__', None) is not None \
                and getattr(meth.__self__, '__class__', None)
        ):
            for cls in inspect.getmro(meth.__self__.__class__):
                if meth.__name__ in cls.__dict__:
                    return cls
            meth = getattr(meth, '__func__', meth)  # fallback to __qualname__ parsing
        if inspect.isfunction(meth):
            cls = getattr(inspect.getmodule(meth),
                        meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0],
                        None)
            if isinstance(cls, type):
                return cls
        return getattr(meth, '__objclass__', None)  # handle special descriptor objects

    try:
        # other methods of excluding unit tests aren't working?
        if what in ('module', 'class') and name.startswith('test_'):
            return True

        cls_ = None
        if what in ('class', 'exception', "method", "attribute"):
            cls_ = _get_class_that_defined_method(obj)
        if cls_ is None:
            cls_ = obj

        # Suppress init on abstract classes, or without custom docstrings
        if name == '__init__':
            if inspect.isabstract(cls_) or issubclass(cls_, abc.ABC):
                return True
            docstring = getattr(obj, '__doc__', '')
            if not docstring or docstring == object.__init__.__doc__:
                return True
            docstring = getattr(cls_.__init__, '__doc__', '')
            if not docstring or docstring == object.__init__.__doc__:
                return True
            return False

        # Resort to manually excluding methods on some builtins
        if issubclass(cls_, tuple) and name in ('count', 'index'):
            return True
        if issubclass(cls_, dict) and name in ('copy', 'clear', 'fromkeys', 'get',
            'items', 'keys', 'pop', 'popitem', 'setdefault', 'update', 'values'):
            return True

        # # We set 'inherited-members': True to include inherited methods, but this
        # # brings in methods inherited from python builtins etc. To exclude these,
        # # skip any item that wasn't defined by code in the repo.
        if inspect.isbuiltin(obj) or inspect.isbuiltin(cls_):
            return True
        try:
            if inspect.getfile(cls_).startswith(stdlib_path):
                return True
        except TypeError:
            return None

        return None # value for default behavior
    except Exception:
        return None

# generate autodocs by running sphinx-apidoc when evaluated on readthedocs.org.
# source: https://github.com/readthedocs/readthedocs.org/issues/1139#issuecomment-398083449
def run_apidoc(_):
    ignore_paths = ["**/test*"]
    argv = ["--force", "--no-toc", "--separate", "-o", "./sphinx", "../src"
        ] + ignore_paths

    try:
        # Sphinx 1.7+
        from sphinx.ext import apidoc
        apidoc.main(argv)
    except ImportError:
        # Sphinx 1.6 (and earlier)
        from sphinx import apidoc
        argv.insert(0, apidoc.__file__)
        apidoc.main(argv)

# -- Extensions to the Napoleon GoogleDocstring class ---------------------
# copied from: https://michaelgoerz.net/notes/extending-sphinx-napoleon-docstring-sections.html
# purpose: provide correct formatting of class attributes when documented
# with Google-style docstrings.

from sphinx.ext.napoleon.docstring import GoogleDocstring

# first, we define new methods for any new sections and add them to the class
def parse_keys_section(self, section):
    return self._format_fields('Keys', self._consume_fields())


GoogleDocstring._parse_keys_section = parse_keys_section


def parse_attributes_section(self, section):
    return self._format_fields('Attributes', self._consume_fields())


GoogleDocstring._parse_attributes_section = parse_attributes_section


def parse_class_attributes_section(self, section):
    return self._format_fields('Class Attributes', self._consume_fields())


GoogleDocstring._parse_class_attributes_section = parse_class_attributes_section

# we now patch the parse method to guarantee that the above methods are
# assigned to the _section dict


def patched_parse(self):
    self._sections['keys'] = self._parse_keys_section
    self._sections['class attributes'] = self._parse_class_attributes_section
    self._unpatched_parse()


GoogleDocstring._unpatched_parse = GoogleDocstring._parse
GoogleDocstring._parse = patched_parse

napoleon_include_private_with_doc = False

# -- Options for intersphinx extension -----------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html

intersphinx_mapping = {
    'python': ('https://docs.python.org/3.10', None),
    'pandas': ('https://pandas.pydata.org/pandas-docs/stable/', None),
    'numpy': ('https://docs.scipy.org/doc/numpy/', None),
    'xarray': ('https://xarray.pydata.org/en/stable/', None)
}

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# == Overall Sphinx app setup hook =============================================


def setup(app):
    # register autodoc events
    app.connect('builder-inited', run_apidoc)
    app.connect('autodoc-process-docstring', no_namedtuple_attrib_docstring)
    app.connect('autodoc-process-signature', abbreviate_logger_in_signature)
    app.connect('autodoc-skip-member', skip_members_handler)

    # AutoStructify for recommonmark
    # see e.g., https://stackoverflow.com/a/52430829
    app.add_config_value('recommonmark_config', {
        'url_resolver': lambda url: _project_github_url + url,
        'enable_auto_toc_tree': False,
        'enable_math': True,
        'enable_inline_math': True,
        'enable_eval_rst': True
        # 'enable_auto_doc_ref': True, # deprecated, now default behavior
    }, True)
    app.add_transform(AutoStructify)
