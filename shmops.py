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
