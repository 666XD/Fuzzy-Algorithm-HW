import os.path
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

import cx_Freeze
executables = [cx_Freeze.Executable("autoCar.py")]

cx_Freeze.setup(
    name = 'tutorial',
    options = {'build_exe': {'packages':['pygame', 'numpy'], 'include_files':[]}},
    executables = executables,
    version="1.0.0"
)

# python game2exe.py build
