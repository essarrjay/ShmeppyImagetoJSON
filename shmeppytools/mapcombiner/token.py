
class Token:
    """represents a single shmeppy token"""
    def __init__(
            self, id, type, tokenId, position=(0, 0), color="#FFF",
            label="", width=1, height=1):
        self.id = tokenId
        self.tokenId = tokenId
        self.type = 'CreateToken'
        self.position = position
        self.color = color
        self.label = label
        self.width = width
        self.height = height

    def update(
            self, id=None, type=None, tokenId=None, position=None,
            color=None, label="", width=None, height=None,
            x=None, y=None):
        """updates token properties with any value present"""
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

    def as_op(self):
        """exports the token as a shmeppy compatible operation"""
        out_dict = self.__dict__
        out_dict['position'] = list(out_dict['position'])
        return out_dict
