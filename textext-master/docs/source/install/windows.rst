.. |TexText| replace:: **TexText**

.. role:: bash(code)
   :language: bash
   :class: highlight

.. role:: latex(code)
   :language: latex
   :class: highlight

.. _windows-install:

==================
TexText on Windows
==================

To install |TexText| on Windows do the following steps:

#. `Install dependencies <windows-install-dependencies_>`_ of |TexText|

    - `Install inkscape <windows-install-inkscape_>`_
    - `Install GUI library (PyGTK2 or TkInter) <windows-install-gui-library_>`_
    - `Install pdflatex/lualatex/xelatex <windows-install-latex_>`_
    - `Install pdf->svg converter (pdf2svg or pstoedit) <windows-install-pdf-to-svg-converter_>`_

#. `Install TexText <windows-install-textext_>`_

.. _windows-install-dependencies:

Install dependencies
====================

.. _windows-install-inkscape:

Install inkscape
~~~~~~~~~~~~~~~~

Download and install Inkscape 0.92.x from https://inkscape.org/release/

.. warning::

    Please ensure that the Python 2.7 interpreter has been selected during the installation of Inkscape (by default this is the case).


.. _windows-install-gui-library:

Install GUI library
~~~~~~~~~~~~~~~~~~~

Install the Python bindings for the graphical user interface of
|TexText|. You have two options: ``PyGTK2`` (recommended) or ``Tkinter``:

.. _windows-install-pygtk2:

Install PyGTK2 (recommended)
----------------------------

.. _inkscape-0.92.3-64-bit: https://github.com/textext/pygtk-for-inkscape-windows/releases/download/0.92.3/Install-PyGTK-2.24-Inkscape-0.92.3-64bit.exe
.. _inkscape-0.92.3-32-bit: https://github.com/textext/pygtk-for-inkscape-windows/releases/download/0.92.3/Install-PyGTK-2.24-Inkscape-0.92.3-32bit.exe
.. _inkscape-0.92.2-64-bit: https://github.com/textext/pygtk-for-inkscape-windows/releases/download/0.92.2/Install-PyGTK-2.24-Inkscape-0.92.2-64bit.exe
.. _inkscape-0.92.2-32-bit: https://github.com/textext/pygtk-for-inkscape-windows/releases/download/0.92.2/Install-PyGTK-2.24-Inkscape-0.92.2-32bit.exe
.. _inkscape-0.92.0-0.92.1-multi: https://github.com/textext/pygtk-for-inkscape-windows/releases/download/0.92.0%2B0.92.1/Install-PyGTK-2.24-Inkscape-0.92.exe

Install the package that matches your Inkscape version:

 - Inkscape 0.92.2 (`32-bit <inkscape-0.92.2-32-bit_>`_ , `64-bit <inkscape-0.92.2-64-bit_>`_)
 - Inkscape 0.92.3 (`32-bit <inkscape-0.92.3-32-bit_>`_ , `64-bit <inkscape-0.92.3-64-bit_>`_)
 - Inkscape 0.92.0 - 0.92.1 (`32-bit and 64-bit <inkscape-0.92.0-0.92.1-multi_>`_)

.. _windows-install-tkinter:

Install Tkinter (not recommended)
---------------------------------

Tkinter is already included in the Python installation shipped with Inkscape.

.. warning::

    Tk support is broken in Inkscape 0.92.2, fixed in 0.92.3

.. _windows-install-pdf-to-svg-converter:

Install a pdf->svg converter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Again you have two options: ``pdf2svg`` or ``pstoedit + ghostscript`` (recommended):

Install pstoedit (recommended)
------------------------------


.. _pstoedit-installer-64bit: https://sourceforge.net/projects/pstoedit/files/pstoedit/3.73/pstoeditsetup_x64.exe
.. _pstoedit-installer-32bit: https://sourceforge.net/projects/pstoedit/files/pstoedit/3.73/pstoeditsetup_win32.exe

.. _gs-installer-32bit: https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs926/gs926w32.exe
.. _gs-installer-64bit: https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs926/gs926w64.exe

1. Download and install ``pstoedit-3.73`` (`32-bit <pstoedit-installer-32bit_>`_, `64-bit <pstoedit-installer-64bit_>`_)
2. Download and install ``ghostcript-9.26``  (`32-bit <gs-installer-32bit_>`_, `64-bit <gs-installer-64bit_>`_)

.. _windows-install-latex:

.. _windows-install-pdf2svg:

Install pdf2svg
---------------

Install the ``pdf2svg`` package from https://github.com/textext/pdf2svg/releases

.. _windows-install-pstoedit:

Install pdflatex/lualatex/xelatex
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Download and install MiKTeX distribution https://miktex.org/download


.. _windows-install-textext:

Install TexText
===============

You have two options: A setup script or a GUI based installer.

Setup script (recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Download the most recent package from :textext_current_release_page:`GitHub release page <release>` (direct links: :textext_download_zip:`.zip <Windows>`)
2. Extract the package and change into the created directory.
3. Double click on the file :bash:`setup_win.bat`. The script will check if all requirements
   described in :ref:`windows-install-dependencies` are met. If so, it will install the extension
   files into the user's Inkscape configuration directory (usually this is
   ``%USERPROFILE%\AppData\Roaming\Inkscape``). If not, instructions are given helping to
   fix the problem. Unfortunately, the output of the script will not be colored on
   Windows versions < 10 18.03.

.. note::

    If you would like to skip the requirement checks during installation call the script
    from the command line as follows:

    .. code-block:: bash

        setup_win.bat /p:"--skip-requirements-check"

Installer
~~~~~~~~~

If you have trouble with the setup script you can use a GUI based installer:

1. Download the most recent installer from :textext_current_release_page:`GitHub release page <release>` (direct links: :textext_download_exe:`.exe <Windows>`)
2. Use the installer and follow the instructions. It will copy the required files into the user's Inkscape
   configuration directory (usually this is ``%USERPROFILE%\AppData\Roaming\Inkscape``).

.. note::

    The installer does not perform any requirement checks. This means that the extension might
    fail to run if you did not install the programs mentioned in
    :ref:`windows-install-dependencies` correctly.


