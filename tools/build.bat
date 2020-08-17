pyinstaller ^
--console ^
--noconfirm ^
--add-data "help.txt;." ^
--add-data "readme.md;." ^
--add-data "config.json;." ^
--add-data "./input_files/dragonsmaw.png;./input_files" ^
--add-data "./output_files/example_map_for_import.json;./output_files" ^
--name Image_to_Shmeppy_JSON ^
./shmeppify.py
