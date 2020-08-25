
class Token:
    """represents a single shmeppy token"""
    def __init__(self, id, type, tokenId, position=(0, 0), color="#FFF", width=1, height=1):
        self.id = tokenId
        self.tokenid = tokenId
        self.type = 'CreateToken'
        self.position = position
        self.color = color
        self.label = ""
        self.width = width
        self.height = height

    def update(self, id=None, type=None, position=None, color=None, label="", tokenId=None, width=None, height=None):
        """updates token properties with any value present"""
        print(f' UPDATE INFO = P:{position}, C:{color}, L:{label}, W:{width}, H:{height}')
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

    def as_op(self):
        """exports the token as a shmeppy compatible operation"""
        out_dict = self.__dict__
        out_dict['position'] = list(out_dict['position'])
        return out_dict
