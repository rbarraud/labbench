# This software was developed by employees of the National Institute of
# Standards and Technology (NIST), an agency of the Federal Government.
# Pursuant to title 17 United States Code Section 105, works of NIST employees
# are not subject to copyright protection in the United States and are
# considered to be in the public domain. Permission to freely use, copy,
# modify, and distribute this software and its documentation without fee is
# hereby granted, provided that this notice and disclaimer of warranty appears
# in all copies.
#
# THE SOFTWARE IS PROVIDED 'AS IS' WITHOUT ANY WARRANTY OF ANY KIND, EITHER
# EXPRESSED, IMPLIED, OR STATUTORY, INCLUDING, BUT NOT LIMITED TO, ANY WARRANTY
# THAT THE SOFTWARE WILL CONFORM TO SPECIFICATIONS, ANY IMPLIED WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND FREEDOM FROM
# INFRINGEMENT, AND ANY WARRANTY THAT THE DOCUMENTATION WILL CONFORM TO THE
# SOFTWARE, OR ANY WARRANTY THAT THE SOFTWARE WILL BE ERROR FREE. IN NO EVENT
# SHALL NIST BE LIABLE FOR ANY DAMAGES, INCLUDING, BUT NOT LIMITED TO, DIRECT,
# INDIRECT, SPECIAL OR CONSEQUENTIAL DAMAGES, ARISING OUT OF, RESULTING FROM,
# OR IN ANY WAY CONNECTED WITH THIS SOFTWARE, WHETHER OR NOT BASED UPON
# WARRANTY, CONTRACT, TORT, OR OTHERWISE, WHETHER OR NOT INJURY WAS SUSTAINED
# BY PERSONS OR PROPERTY OR OTHERWISE, AND WHETHER OR NOT LOSS WAS SUSTAINED
# FROM, OR AROSE OUT OF THE RESULTS OF, OR USE OF, THE SOFTWARE OR SERVICES
# PROVIDED HEREUNDER. Distributions of NIST software should also include
# copyright and licensing statements of any third-party software that are
# legally bundled with the code in compliance with the conditions of those
# licenses.

# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import traitlets as tl
import sys
import os
import shutil

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
if '..' not in sys.path:
	sys.path.insert(0, '..')

from labbench import __version__ as version

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    #    'sphinxcontrib.restbuilder',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.graphviz',
    # 'nbsphinx',
    # 'sphinx.ext.mathjax',  
    'recommonmark'  
    #    'sphinx_pyreverse'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
# source_suffix = ['.rst', '.md']
source_suffix = ['.rst', '.md']

# The encoding of source files.
#source_encoding = 'utf-8-sig'

autodoc_mock_imports = ["traitlets", 'sortedcontainers']

# The master toctree document.
master_doc = 'labbench'

# General information about the project.
project = u'labbench'
copyright = 'United States government work, not subject to copyright in the United States'

author = 'Dan Kuester, Shane Allman, Paul Blanchard, Yao Ma (NIST)'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
#version = '0.0.1'

# The full version, including alpha/beta/rc tags.
release = version

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', '**.ipynb_checkpoints']

# The reST default role (used for this markup: `text`) to use for all
# documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

autodoc_default_flags = ['inherited-members']


def maybe_skip_member(app, what, name, obj, skip, options):
    """ Skip extra cruft from Device.state objects
    """
    if skip:
        return True
    from traitlets import TraitType
    import labbench as lb
    TraitMixIn = lb.Bool.__mro__[1]
    whitelist = []

    if name not in whitelist and hasattr(tl.HasTraits, name):
        tlobj = getattr(tl.HasTraits, name)
        
        if (tlobj is obj or (hasattr(tlobj, 'im_func')
                             and tlobj.__func__ is obj.__func__))\
            or (name.startswith('class') or name == 'trait_events'):
            with open('test.txt', 'a') as f:
                f.write('skip: ' + repr(what) + ' with name ' +
                        name + ' in ' + repr(obj) + '\r\n')
            return True
        else:
            with open('test.txt', 'a') as f:
                f.write('nearly skip: ' + repr(what) + ' with name ' +
                        name + ' in ' + repr(obj) + '\r\n')

    # Skip any type definition attribute that's already in TraitType
    # or TraitMixIn
    for cls in (TraitType, TraitMixIn):
        if name not in whitelist and hasattr(cls, name):
            if getattr(cls, name) is obj:
                with open('test.txt', 'a') as f:
                    f.write('skip: ' + repr(what) + ' with name ' +
                            name + ' in ' + repr(obj) + '\r\n')
                return True
            else:
                with open('test.txt', 'a') as f:
                    f.write('nearly skip: ' + repr(what) + ' with name ' +
                            name + ' in ' + repr(obj) + '\r\n')

    return False

# From https://groups.google.com/forum/#!msg/sphinx-users/NYUYffRrE78/MPMa57KN1sEJ
# to make output paths compatible with github
def change_pathto(app, pagename, templatename, context, doctree):
    """
    Replace pathto helper to change paths to folders with a leading
underscore.
    """
    pathto = context.get('pathto')
    def gh_pathto(otheruri, *args, **kw):
        if otheruri.startswith('_'):
            otheruri = otheruri[1:]
        return pathto(otheruri, *args, **kw)
    context['pathto'] = gh_pathto

# From https://groups.google.com/forum/#!msg/sphinx-users/NYUYffRrE78/MPMa57KN1sEJ
# to make output paths compatible with github
def move_private_folders(app, e):
    """
    remove leading underscore from folders in in the output folder
    """
    def join(dir):
        return os.path.join(app.builder.outdir, dir)

    for item in os.listdir(app.builder.outdir):
        if item.startswith('_') and os.path.isdir(join(item)):
            shutil.move(join(item), join(item[1:]))

def setup(app):
    app.connect('autodoc-skip-member', maybe_skip_member)
    app.connect('html-page-context', change_pathto)
    app.connect('build-finished', move_private_folders)
    # app.connect('autodoc-process-signature', resignature)


# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
#keep_warnings = False

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'nature'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
# html_theme_path = ['_templates']

# The name for this set of Sphinx documents.
# "<project> v<release> documentation" by default.
html_title = f'labbench v{version}'

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#html_logo = None

# The name of an image file (relative to this directory) to use as a favicon of
# the docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
#html_extra_path = []

# If not None, a 'Last updated on:' timestamp is inserted at every page
# bottom, using the given strftime format.
# The empty string is equivalent to '%b %d, %Y'.
#html_last_updated_fmt = None

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx = False

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Language to be used for generating the HTML full-text search index.
# Sphinx supports the following languages:
#   'da', 'de', 'en', 'es', 'fi', 'fr', 'hu', 'it', 'ja'
#   'nl', 'no', 'pt', 'ro', 'ru', 'sv', 'tr', 'zh'
#html_search_language = 'en'

# A dictionary with options for the search language support, empty by default.
# 'ja' uses this config value.
# 'zh' user can custom change `jieba` dictionary path.
#html_search_options = {'type': 'default'}

# The name of a javascript file (relative to the configuration directory) that
# implements a search results scorer. If empty, the default will be used.
#html_search_scorer = 'scorer.js'

# Output file base name for HTML help builder.
htmlhelp_basename = project + 'doc'

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    'preamble': r'\setcounter{tocdepth}{5}',

    # Latex figure (float) alignment
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, '{}-api.tex'.format(project),
     r'API reference for {}'.format(project),
     author, 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, '{}-api'.format(project), u'API reference for {}'.format(project),
     [author], 1)
]

# If true, show URL addresses after external links.
#man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, '{}-api'.format(project), u'API reference for {}'.format(project),
     author, '{}-api'.format(
         project), 'instrument automation drivers for shared-spectrum metrology',
     'Miscellaneous'),
]

# Documents to append as an appendix to all manuals.
#texinfo_appendices = []

# If false, no module index is generated.
#texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
#texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
#texinfo_no_detailmenu = False


# -- Options for Epub output ----------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright

# The basename for the epub file. It defaults to the project name.
#epub_basename = project

# The HTML theme for the epub output. Since the default themes are not
# optimized for small screen space, using the same theme for HTML and epub
# output is usually not wise. This defaults to 'epub', a theme designed to save
# visual space.
#epub_theme = 'epub'

# The language of the text. It defaults to the language option
# or 'en' if the language is not set.
#epub_language = ''

# The scheme of the identifier. Typical schemes are ISBN or URL.
#epub_scheme = ''

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#epub_identifier = ''

# A unique identification for the text.
#epub_uid = ''

# A tuple containing the cover image and cover page html template filenames.
#epub_cover = ()

# A sequence of (type, uri, title) tuples for the guide element of content.opf.
#epub_guide = ()

# HTML files that should be inserted before the pages created by sphinx.
# The format is a list of tuples containing the path and title.
#epub_pre_files = []

# HTML files that should be inserted after the pages created by sphinx.
# The format is a list of tuples containing the path and title.
#epub_post_files = []

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']

# The depth of the table of contents in toc.ncx.
#epub_tocdepth = 3

# Allow duplicate toc entries.
#epub_tocdup = True

# Choose between 'default' and 'includehidden'.
#epub_tocscope = 'default'

# Fix unsupported image types using the Pillow.
#epub_fix_images = False

# Scale large images.
#epub_max_image_width = 0

# How to display URL addresses: 'footnote', 'no', or 'inline'.
#epub_show_urls = 'inline'

# If false, no index is generated.
#epub_use_index = True

nbsphinx_execute = 'never'

# List of arguments to be passed to the kernel that executes the notebooks:
nbsphinx_execute_arguments = [
    "--InlineBackend.figure_formats={'svg', 'pdf'}",
    "--InlineBackend.rc={'figure.dpi': 96}",
]

# If True, the build process is continued even if an exception occurs:
#nbsphinx_allow_errors = True

# Controls when a cell will time out (defaults to 30; use -1 for no timeout):
#nbsphinx_timeout = 60

# Default Pygments lexer for syntax highlighting in code cells:
#nbsphinx_codecell_lexer = 'ipython3'

# Width of input/output prompts used in CSS:
#nbsphinx_prompt_width = '8ex'

# If window is narrower than this, input/output prompts are on separate lines:
#nbsphinx_responsive_width = '700px'

# This is processed by Jinja2 and inserted before each notebook
nbsphinx_prolog = r"""
{% set docname = env.doc2path(env.docname, base='doc') %}
.. only:: html
    .. role:: raw-html(raw)
        :format: html
    .. nbinfo::
        This page was generated from `{{ docname }}`__.
        Interactive online version:
        :raw-html:`<a href="https://mybinder.org/v2/gh/spatialaudio/nbsphinx/{{ env.config.release }}?filepath={{ docname }}"><img alt="Binder badge" src="https://mybinder.org/badge_logo.svg" style="vertical-align:text-bottom"></a>`
    __ https://github.com/spatialaudio/nbsphinx/blob/
        {{ env.config.release }}/{{ docname }}
.. raw:: latex
    \nbsphinxstartnotebook{\scriptsize\noindent\strut
    \textcolor{gray}{The following section was generated from
    \sphinxcode{\sphinxupquote{\strut {{ docname | escape_latex }}}} \dotfill}}
"""

# This is processed by Jinja2 and inserted after each notebook
nbsphinx_epilog = r"""
.. raw:: latex
    \nbsphinxstopnotebook{\scriptsize\noindent\strut
    \textcolor{gray}{\dotfill\ \sphinxcode{\sphinxupquote{\strut
    {{ env.doc2path(env.docname, base='doc') | escape_latex }}}} ends here.}}
"""

# Input prompt for code cells. "%s" is replaced by the execution count.
#nbsphinx_input_prompt = 'In [%s]:'

# Output prompt for code cells. "%s" is replaced by the execution count.
#nbsphinx_output_prompt = 'Out[%s]:'

# Specify conversion functions for custom notebook formats:
#import jupytext
#nbsphinx_custom_formats = {
#    '.Rmd': lambda s: jupytext.reads(s, '.Rmd'),
#}

mathjax_config = {
    'TeX': {'equationNumbers': {'autoNumber': 'AMS', 'useLabelIds': True}},
}
