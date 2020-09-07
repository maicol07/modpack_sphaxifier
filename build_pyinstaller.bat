rem [WIP] 🚧 Work in progress.
pyinstaller -y ^
--add-data VERSION;VERSION ^
--add-data resources/html;resources/html ^
--add-data resources/KOMIKAX_.ttf;resources/KOMIKAX_.ttf ^
--add-data resources/img;resources/img ^
--add-data resources/views;resources/views ^
--add-data C:\Users\Maicol\.conda\envs\Modpack_Sphaxifier\Lib\site-packages\pyside_material\themes;pyside_material\themes ^
-i resources/img/logo.ico ^
--hidden-import six ^
--hidden-import PySide2.QtXml ^
--upx-exclude=vcruntime140.dll ^
--noupx ^
--windowed ^
main.py