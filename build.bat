rem Remove all files
@RD /S /Q "build";

rem Compile
python setup.py build

rem Inno Setup installer