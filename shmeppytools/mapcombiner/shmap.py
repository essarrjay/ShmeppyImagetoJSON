import shmobjs

TOKEN_OPS = {
    'CreateToken': ['color', 'position', 'tokenId'],
    'MoveToken': ['position', 'tokenId'],
    'UpdateTokenLabel': ['label', 'tokenId'],
    'DeleteToken': ['tokenId'],
    'ResizeToken': ['width', 'height', 'tokenId']
    }


class Shmap:
    """represents a shmeppy map

    does not include fog of war
    """

    def __init__(self, map_dict=None):
        if map_dict:
            self.__dict__
        else:
            self.exportFormatVersion = 1
            self.operations = []

        self.tokens = self.make_tokens(self.operations)
        self.edges_l, self.edges_t = self.make_edges(self.operations)
        self.fills = self.make_fills(self.operations)

        self.bb = self.get_map_bounding_box()

    def get_map_bounding_box(self):
        # deprecated, as requires edge, fill objs (which are excessive)
        x_list, y_list = [], []

        for op in self.operations:
            print(f"op_type is {op['type']}")
            if op.type in ["CreateToken", "FillCells", "UpdateCellEdges"]:
                xs, ys = op.get_xys
                x_list += xs
                y_list += ys
            else:
                print(f"{op['type']} is NOT drawing or CreateToken op")
        ul_corner = min(x_list), min(y_list)
        lr_corner = max(x_list), max(y_list)
        return ul_corner, lr_corner

    def get_bb(self):
        """returns bounding box of a map in squares x,y"""
        print(" --------------------")
        print(" Getting Bounding Box")
        print(" --------------------")
        x_list, y_list = [], []
        cells = self.fills.values() + self.edges_l.values() + self.edges_t.values()
        for cell_pos in cells:
            xs, ys = cell_pos
            x_list += xs
            y_list += ys
        for token in self.tokens:
            xs, ys = token.get_xys()
            x_list += xs
            y_list += ys
        ul_corner = min(x_list), min(y_list)
        lr_corner = max(x_list), max(y_list)
        return ul_corner, lr_corner

    def make_tokens(op_list, debug=False):
        """returns a dict of {tokenId: token_obj} from op_list

        Uses final position of token, and omits deleted tokens
        """
        token_dict = {}
        for op in op_list:
            if op['type'] == 'CreateToken':
                print(f"+CREATED TOKEN {op['tokenId']}")
                token_dict.update({op['tokenId']: shmobjs.Token(**op)})
            elif op['type'] == 'DeleteToken':
                token_dict.pop(op['tokenId'])
                print(f"-DELETED TOKEN {op['tokenId']}")
            elif op['type'] in TOKEN_OPS.keys():
                token_obj = token_dict[op['tokenId']]
                print(f"=TOKEN OP {op['type']}")
                if debug:
                    print(f'  Token properties before:\n      {token_obj.__dict__}')
                print(f'  OP: {op}')
                token_obj.update(**op)
        return token_dict

    def make_edges(op_list):
        """returns an Edge obj from op_list

        Uses final position of token, and omits deleted tokens
        """
        left_edge_dict = {}
        top_edge_dict = {}
        for op in op_list:
            if op['type'] == 'UpdateCellEdges':
                for position, color in op['left']:
                    left_edge_dict.update({position: color})
                for position, color in op['top']:
                    top_edge_dict.update({position: color})
        return left_edge_dict, top_edge_dict

    def make_fills(op_list):
        """returns a dict of {position: color} from op_list

        Uses final position of token, and omits deleted tokens
        """
        cells_dict = {}  # {position: color}
        for op in op_list:
            if op['type'] == 'FillCells':
                for position, color in op['cellFills']:
                    cells_dict.update({position: color})
        return cells_dict
