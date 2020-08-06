from datetime import datetime
import json
from pathlib import Path

export_obj = {"exportFormatVersion":1,"operations":[]}

class Fill_Operation:
    def __init__(self, id='', type='FillCells'):
        self.id = id
        self.type = type
        self.cellFills = []

    def add_fill(self,x_coord,y_coord,color):
        coordinates = [x_coord,y_coord]
        fill_data = [coordinates,color]
        self.cellFills.append(fill_data)

    def export_json(self, data_dir=r'./'):
        #exports table_data as JSON
        if data_dir[-1] != '/': data_dir += '/'

        #generate export path
        timestamp_str = str(datetime.now())[:-7]
        timestamp_str = timestamp_str.replace(':','').replace(' ','_')
        filename = f'game_map_{timestamp_str}.json'
        export_path = Path(data_dir + filename)
        export_obj["operations"].append(self.__dict__)

        try:
            result = f"Exporting mapfile to {str(export_path)}"
            with export_path.open(mode='w') as json_file:
                json.dump(export_obj,json_file)
        except:
            result = "Error, unable to export."

        return result
