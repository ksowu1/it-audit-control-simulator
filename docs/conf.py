
import os
import sys
sys.path.insert(0, os.path.abspath('..'))


extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "autodoc2",
]

autodoc2_packages = [
    {
        "path": os.path.abspath("../controls"),
        "root_name": "controls",
        "auto_mode": "all",
    }
]

