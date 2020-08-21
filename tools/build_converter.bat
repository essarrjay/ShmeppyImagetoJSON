pyinstaller ^
--console ^
--noconfirm ^
--add-data "../src/help.txt;." ^
--add-data "../src/config.json;." ^
--add-data "../README.md;." ^
--add-data "../examples/images/dragonsmaw.png;./Maps" ^
--name Image_to_Shmeppy_JSON_v2.2.1 ^
--distpath ../build ^
--workpath ../pyinstaller_workfiles ^
--specpath ../pyinstaller_workfiles ^
../src/shmeppify.py
