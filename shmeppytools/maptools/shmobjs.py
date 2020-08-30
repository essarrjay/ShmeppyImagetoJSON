"""shmobjs.py

Objects representing various features of a Shmeppy map
"""


class Shm_Op:
    """A single Shmeppy Operation"""
    def __init__(self, id='', type=''):
        self.id = id
        self.type = type


class Token:
    """represents a single shmeppy token"""
    def __init__(
            self, id=3, type='CreateToken', tokenId="", position=(0, 0), color="#FFF",
            label="", width=1, height=1):
        self.id = tokenId
        self.tokenId = tokenId
        self.type = type
        self.position = position
        self.color = color
        self.label = label
        self.width = width
        self.height = height

    def update(
            self, id=None, type=None, tokenId=None, position=None,
            color=None, label="", width=None, height=None,
            x=None, y=None, debug=False):
        """updates token properties with any value present"""
        if debug:
            print(f'  UPDATE INFO = P:{position}, C:{color}, L:{label}, W:{width}, H:{height}, X:{x}, Y:{y}')
        if position:
            self.position = position
        if color:
            self.color = color
        if label:
            self.label = label
        if width:
            self.width = width
        if height:
            self.height = height
        if x:
            self.position[0] += x
        if y:
            self.position[1] += y

    def get_xys(self):
        x, y = self.position
        w, h = self.width, self.height
        return [x, x+w], [y, y+h]

    def as_op(self):
        """exports the token as a shmeppy compatible operation"""
        out_dict = self.__dict__
        out_dict['position'] = list(out_dict['position'])
        return out_dict


class FillCells(Shm_Op):
    """A shmeppy .json FillCells operation"""
    def __init__(self, cellFills, id=1, type='FillCells'):
        super().__init__(id, type)
        self.cellFills = cellFills if cellFills else []

    def get_xys(self):
        """returns lists of x,y coords"""

        x_list = []
        y_list = []
        for cell in self.cellFills:
            x, y = cell[0]
            x_list.append(x)
            y_list.append(y)
        return x_list, y_list


class Cell():
    def __init__(self, position, color):
        self.position = position  # [x, y]
        self.color = color  # hex value


class Edge(Shm_Op):
    """A shmeppy .json UpdateCellEdges operation"""
    def __init__(left, top, self, id=2, type='UpdateCellEdges'):
        super().__init__(id, type)
        self.left = left  # dict of cells {position: color}
        self.top = top  # dict of cells {position: color}

    def get_xys(self):
        """returns lists of x,y coords"""

        x_list = []
        y_list = []
        for cell in self.top:
            x, y = cell[0]
            x_list.append(x)
            y_list.append(y)
        for cell in self.left:
            x, y = cell[0]
            x_list.append(x)
            y_list.append(y)
        return x_list, y_list
