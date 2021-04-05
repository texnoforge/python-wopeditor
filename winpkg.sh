# script to build windows installer using PyInstaller and NSIS
rm -rf dist
python -m PyInstaller wopeditor.spec
makensis wopeditor.nsi
