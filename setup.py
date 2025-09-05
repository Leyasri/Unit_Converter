from cx_Freeze import setup, Executable
import os

# Path to PyQt5 plugins (adjust if necessary)
pyqt5_plugin_path = r"C:\Users\Lenovo\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages\PyQt5\Qt5\plugins"

executables = [
    Executable("app.py", base="Win32GUI", icon=None)  # No console, optional icon
]

setup(
    name="UnitConverter",
    version="1.0",
    description="Unit Converter Application",
    executables=executables,
    options={
        "build_exe": {
            "packages": ["PyQt5.QtWidgets", "PyQt5.QtCore", "PyQt5.QtGui", "sys"],
            "excludes": ["PyQt5.QtQml", "PyQt5.QtQuick", "PyQt5.QtQmlModels", "PyQt5.QtWebEngine"],
            "include_files": [(pyqt5_plugin_path, "PyQt5/Qt5/plugins")],  # Include PyQt5 plugins
            "include_msvcr": True,  # Include Microsoft Visual C++ runtime
            "optimize": 2,
        }
    }
)