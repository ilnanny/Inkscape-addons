.. |TexText| replace:: **TexText**

.. role:: bash(code)
   :language: bash
   :class: highlight

.. role:: latex(code)
   :language: latex
   :class: highlight

.. _macos-install:

================
TexText on MacOS
================

.. caution::

    These installation instrcuctions are not fully tested. Please report any
    issues, comments or hints to https://github.com/textext/textext/issues/new

To install |TexText| on MacOS do the following steps:

#. `Install dependencies <macos-install-dependencies_>`_ of |TexText|

    - `Install inkscape <macos-install-inkscape_>`_
    - `Install python2.7 <macos-install-python27_>`_
    - `Install GUI library PyGTK2 <macos-install-pygtk2_>`_
    - `Install pdflatex/lualatex/xelatex <macos-install-latex_>`_
    - `Install pdf->svg converter (pdf2svg or pstoedit) <macos-install-pdf-to-svg-converter_>`_

#. `Install TexText <macos-install-textext_>`_

.. _macos-install-dependencies:

Install dependencies
====================

.. _macos-install-inkscape:

Install inkscape
~~~~~~~~~~~~~~~~

To install using homebrew:

.. code-block:: bash

    brew cask install inkscape

.. (Two labels to catch links from failed requirement check!)
.. _macos-install-python27:
.. _macos-install-tkinter:

Install python2.7
~~~~~~~~~~~~~~~~~

Make sure that a Python 2.7 distribution is installed and found by
your system. Make sure it contains the Tkinter package so |TexText| will run
at least with a basic interface.

To install using homebrew and forcing the Tkinter package to be installed:

.. code-block:: bash

    brew cask install python@2 --with-tcl-tk

.. (Two labels to catch links from failed requirement check!)
.. _macos-install-gui-library:
.. _macos-install-pygtk2:

Install PyGTK2 (recommended)
----------------------------

Compared to the Tkinter interface the PyGTK interface will offer a lot more
functionality. Hence, install the following packages.

-  ``python-gtk2``
-  ``python-gtksourceview2`` (enables syntax highlighting)

To install using homebrew:

.. code-block:: bash

    brew install pygtk gtksourceview

.. _macos-install-pdf-to-svg-converter:

Install a pdf->svg converter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You have two options: ``pdf2svg`` (recommended) or ``pstoedit + ghostscript``:

.. _macos-install-pdf2svg:

Install pdf2svg (recommended)
----------------------------------
Install the ``pdf2svg`` package

To install using homebrew:

.. code-block:: bash

    brew install pdf2svg

.. _macos-install-pstoedit:

Install pstoedit (not recommended)
----------------------------------

Some versions ``pstoedit`` fails to produce `svg` so it's preferable to use ``pdf2svg``.

To use ``pstoedit`` converter install the ``pstoedit`` package and check versions of
installed versions of ``pstoedit`` and ``ghostscript``

To install using homebrew:

.. code-block:: bash

    brew install ghostscript pstoedit

To check versions run:

.. code-block:: bash

    pstoedit --version
    ghostscript --version

.. warning::
    Those combinations of ``pstoedit`` and ``ghostscript`` versions fails to produce `svg` on
    most distributions (see  `bb issue 48 <https://bitbucket.org/pitgarbe/textext/issues/48/ghostscript-still-bug-under-linux>`_):

    +--------------+-----------------+
    | ``pstoedit`` | ``ghostscript`` |
    +--------------+-----------------+
    |     3.70     |      9.22       |
    +--------------+-----------------+

    Please report any observations or problems in :issue:`30`.

.. _macos-install-latex:

Install pdflatex/lualatex/xelatex
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``pdflatex``, ``lualatex`` and ``xelatex`` are part of ``mactex`` package.

To install using homebrew:

.. code-block:: bash

    brew install mactex


.. _macos-install-textext:

Install TexText
===============

Install TexText
===============

1.  Download the most recent package from :textext_current_release_page:`GitHub release page <release>` (direct links: :textext_download_zip:`.zip <MacOS>`, :textext_download_tgz:`.tar.gz <MacOS>`)
2.  Extract the package and change to created directory.
3.  Run :bash:`setup.py` from your terminal:

    .. code-block:: bash

        python setup.py --inkscape-executable=/usr/local/bin/inkscape

    The script will check if all requirements described in :ref:`macos-install-dependencies`
    are met. If so, it will install the extension files into the user's Inkscape configuration
    directory (usually this is ``~/.config/inkscape/extensions``). If not, instructions are given
    helping to fix the problem.

    .. note::

        If you would like to skip the requirement checks during installation call the script
        from the command line as follows:

        .. code-block:: bash

            python setup.py --inkscape-executable=/usr/local/bin/inkscape --skip-requirements-check
