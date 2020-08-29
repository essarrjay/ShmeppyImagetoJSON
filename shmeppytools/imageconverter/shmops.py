class Shm_Op:
    """A single Shmeppy Operation"""
    def __init__(self, id='', type=''):
        self.id = id
        self.type = type


class Fill_Operation(Shm_Op):
    """Represents a single FillCells operation for Shmeppy imports."""
    def __init__(self, id='', type='FillCells'):
        Shm_Op.__init__(self, id, type)
        self.cellFills = []

    def add_fill(self, x_coord, y_coord, color):
        """Appends single-color fill action to Fill_Operation"""
        coordinates = [x_coord, y_coord]
        fill_data = [coordinates, color]
        self.cellFills.append(fill_data)


class UpdateCellEdges(Shm_Op):
    """Represents a single UpdateCellEdges operation"""
    def __init__(self, id='', type='UpdateCellEdges'):
        Shm_Op.__init__(self, id, type)
        self.left = []
        self.top = []
