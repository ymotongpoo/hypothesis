# This file is part of Hypothesis, which may be found at
# https://github.com/HypothesisWorks/hypothesis/
#
# Copyright the Hypothesis Authors.
# Individual contributors are listed in AUTHORS.rst and the git log.
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at https://mozilla.org/MPL/2.0/.

import datetime
import os
import sys
import types

import sphinx_rtd_theme

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))


autodoc_member_order = "bysource"
autodoc_typehints = "none"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "hoverxref.extension",
    "sphinx_codeautolink",
    "sphinx_selective_exclude.eager_only",
]

templates_path = ["_templates"]

source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "Hypothesis"
author = "David R. MacIver"
copyright = f"2013-{datetime.datetime.utcnow().year}, {author}"

_d = {}
with open(
    os.path.join(os.path.dirname(__file__), "..", "src", "hypothesis", "version.py")
) as f:
    exec(f.read(), _d)
    version = _d["__version__"]
    release = _d["__version__"]


def setup(app):
    if os.path.isfile(os.path.join(os.path.dirname(__file__), "..", "RELEASE.rst")):
        app.tags.add("has_release_file")

    # patch in mock array_api namespace so we can autodoc it
    from hypothesis.extra.array_api import make_strategies_namespace, mock_xp

    mod = types.ModuleType("xps")
    mod.__dict__.update(make_strategies_namespace(mock_xp).__dict__)
    assert "xps" not in sys.modules
    sys.modules["xps"] = mod


language = "ja"

exclude_patterns = ["_build"]

pygments_style = "sphinx"

todo_include_todos = False

# See https://sphinx-hoverxref.readthedocs.io/en/latest/configuration.html
hoverxref_auto_ref = True
hoverxref_domains = ["py"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "pytest": ("https://docs.pytest.org/en/stable/", None),
    "django": ("https://django.readthedocs.io/en/stable/", None),
    "dateutil": ("https://dateutil.readthedocs.io/en/stable/", None),
    "redis": ("https://redis-py.readthedocs.io/en/stable/", None),
    "attrs": ("https://www.attrs.org/en/stable/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}

autodoc_mock_imports = ["numpy", "pandas", "redis"]

codeautolink_autodoc_inject = False
codeautolink_global_preface = """
from hypothesis import *
import hypothesis.strategies as st
from hypothesis.strategies import *
"""

# This config value must be a dictionary of external sites, mapping unique
# short alias names to a base URL and a prefix.
# See http://sphinx-doc.org/ext/extlinks.html
_repo = "https://github.com/HypothesisWorks/hypothesis/"
extlinks = {
    "commit": (_repo + "commit/%s", "commit "),
    "gh-file": (_repo + "blob/master/%s", ""),
    "gh-link": (_repo + "%s", ""),
    "issue": (_repo + "issues/%s", "issue #"),
    "pull": (_repo + "pull/%s", "pull request #"),
    "pypi": ("https://pypi.org/project/%s/", ""),
    "bpo": ("https://bugs.python.org/issue%s", "bpo-"),
    "xp-ref": ("https://data-apis.org/array-api/latest/API_specification/%s", ""),
    "wikipedia": ("https://en.wikipedia.org/wiki/%s", ""),
}

# -- Options for HTML output ----------------------------------------------

html_theme = "sphinx_rtd_theme"

html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

html_static_path = ["_static"]

htmlhelp_basename = "Hypothesisdoc"

html_favicon = "../../brand/favicon.ico"

html_logo = "../../brand/dragonfly-rainbow-150w.svg"

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {}

latex_documents = [
    (master_doc, "Hypothesis.tex", "Hypothesis Documentation", author, "manual")
]

man_pages = [(master_doc, "hypothesis", "Hypothesis Documentation", [author], 1)]

texinfo_documents = [
    (
        master_doc,
        "Hypothesis",
        "Hypothesis Documentation",
        author,
        "Hypothesis",
        "Advanced property-based testing for Python.",
        "Miscellaneous",
    )
]
