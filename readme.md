make.vg
=======

**make.vg** is a web space for Andrew G. Crowell, an independent game developer. This repository serves as an open location for the pages that will appear on the site. All documents are HTML fragments, cleverly tagged as Markdown files, so that they can be previewed on Github -- HTML is permissible subset of Markdown.

*Documents are under a [Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License](http://creativecommons.org/licenses/by-nc-sa/3.0/), unless otherwise noted.*

*For scripts, the license is included in the source.*

mdtool.py
---------
This script is useful for taking a bunch of markdown files and dumping the output into a directory of .html files. To use this, make sure that Python-Markdown's **markdown** module (https://github.com/waylan/Python-Markdown/ or in PyPI) is installed, or otherwise on your sys.path.

Run `./mdtool.py` without arguments to see its usage.