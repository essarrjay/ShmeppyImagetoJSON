pyinstaller ^
--onefile ^
--console ^
--noconfirm ^
--name map_combiner_v0.2.1 ^
--distpath ../build ^
--workpath ../pyinstaller_workfiles ^
--specpath ../pyinstaller_workfiles ^
../src/combine_maps.py
