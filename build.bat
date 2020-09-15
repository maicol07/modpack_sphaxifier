rem Pyinstaller
pyinstaller -y ^
--add-data VERSION;. ^
--add-data resources/html;resources/html ^
--add-data resources/KOMIKAX_.ttf;resources/KOMIKAX_.ttf ^
--add-data resources/img;resources/img ^
--add-data resources/views;resources/views ^
--add-data C:\Users\Maicol\AppData\Local\Programs\Python\Python38\Lib\site-packages\pyside_material\themes;pyside_material\themes ^
-i resources/img/logo.ico ^
--hidden-import six ^
--hidden-import PySide2.QtXml ^
--upx-exclude=vcruntime140.dll ^
--noupx ^
--windowed ^
main.py

rem Create setup with Inno Setup (Add install path to the system PATH)
iscc build_exe.iss