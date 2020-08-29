import json
from datetime import datetime

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

    def __init__(self, name, map_dict=None, operations=None):
        if map_dict:
            self.__dict__ = map_dict
        else:
            self.exportFormatVersion = 1
            self.operations = operations if operations else []
        self.name = name
        print(f"New Map: {self.name}")
        self.tokens = self.make_tokens(self.operations)
        print("Tokens Loaded")
        self.edges_l, self.edges_t = self.make_edges(self.operations)
        print("Edges Loaded")
        self.fills = self.make_fills(self.operations)
        print("Fills Loaded")
        self.ops_lists = [self.tokens, self.edges_l, self.edges_t, self.fills]


    def json_format(self):
        return {"exportFormatVersion": self.exportFormatVersion, "operations": self.operations}

    def get_bb_dimensions(self):
        """returns absolute dimensions of bounding box"""
        (ux, uy), (lx, ly) = self.bb
        return lx-ux+1, ly-uy+1

    def set_bounding_box(self):
        """returns bounding box of a map in squares x,y"""
        print(" -------------------------")
        print("   Getting Bounding Box   ")
        print("  Position and Dimensions ")
        print(" -------------------------")
        x_list, y_list = [], []
        cells = []
        cells.extend(self.fills.keys())
        cells.extend(self.edges_l.keys())
        cells.extend(self.edges_t.keys())
        for cell_pos in cells:
            xs, ys = cell_pos
            x_list += [xs]
            y_list += [ys]
        for token in self.tokens.values():
            xs, ys = token.get_xys()
            x_list += xs
            y_list += ys
        ul_corner = min(x_list), min(y_list)
        lr_corner = max(x_list), max(y_list)
        self.bb = ul_corner, lr_corner
        return self.bb

    def as_ops(self):
        """returns tokens, edges, fills as a combined list of operations"""

        ops = []
        # add tokens as separate operations
        for token in self.tokens.values():
            ops.append(token.as_op())

        # add edges as single op
        edges_op = {
            "id": "2",
            "type": "UpdateCellEdges",
            "left": self.dict_to_cells(self.edges_l),
            "top": self.dict_to_cells(self.edges_t)
            }
        ops.append(edges_op)

        # add fills as single op
        fills_op = {
            "id": "1",
            "type": "FillCells",
            "cellFills": self.dict_to_cells(self.fills)
            }
        ops.append(fills_op)

        return ops

    def dict_to_cells(self, dict):
        """converts {position: color} dict to list cells [[x,y], color]"""
        cells = []
        for pos, color in dict.items():
            cell = [list(pos), color]
            cells.append(cell)
        return cells

    def offset_ops(self, offset):
        """offset positions of all operations by offset (x,y)"""
        x, y = offset
        for id, token in self.tokens.items():
            token.update(x=x, y=y)

        new_dict = {}
        for pos in self.edges_l:
            new_pos = pos[0]+x, pos[1]+y
            new_dict.update({new_pos: self.edges_l[pos]})
        self.edges_l = new_dict

        new_dict = {}
        for pos in self.edges_t:
            new_pos = pos[0]+x, pos[1]+y
            new_dict.update({new_pos: self.edges_t[pos]})
        self.edges_t = new_dict

        new_dict = {}
        for pos in self.fills:
            new_pos = pos[0]+x, pos[1]+y
            new_dict.update({new_pos: self.fills[pos]})
        self.fills = new_dict

    def make_tokens(self, op_list, debug=False):
        """returns a dict of {tokenId: token_obj} from op_list

        Uses final position of token, and omits deleted tokens
        """
        token_dict = {}
        for op in op_list:
            if op['type'] == 'CreateToken':
                if debug: print(f"+CREATED TOKEN {op['tokenId']}")
                token_dict.update({op['tokenId']: shmobjs.Token(**op)})
            elif op['type'] == 'DeleteToken':
                token_dict.pop(op['tokenId'])
                if debug: print(f"-DELETED TOKEN {op['tokenId']}")
            elif op['type'] in TOKEN_OPS.keys():
                token_obj = token_dict[op['tokenId']]
                if debug: print(f"=TOKEN OP {op['type']}")
                if debug:
                    print(f'  Token properties before:\n      {token_obj.__dict__}')
                token_obj.update(**op)
        return token_dict

    def make_edges(self, op_list):
        """returns edge dict {posiiton:color} from op_list

        Uses final position of token, and omits deleted tokens
        """
        left_edge_dict = {}
        top_edge_dict = {}
        for op in op_list:
            if op['type'] == 'UpdateCellEdges':
                if op['left'] != []:
                    for position, color in op['left']:
                        left_edge_dict.update({tuple(position): color})
                if op['top'] != []:
                    for position, color in op['top']:
                        top_edge_dict.update({tuple(position): color})
        return left_edge_dict, top_edge_dict

    def make_fills(self, op_list):
        """returns a dict of {position: color} from op_list

        Uses final position of token, and omits deleted tokens
        """
        cells_dict = {}  # {position: color}
        for op in op_list:
            if op['type'] == 'FillCells':
                for position, color in op['cellFills']:
                    cells_dict.update({tuple(position): color})
        return cells_dict

    def export_to(self, outpath, filename=None):
        """exports map to outpath"""
        print(f"\nAttempting Export to:\n  {outpath}\n")

        if not filename:
            ts = str(datetime.now())[:-7]
            ts = ts.replace(':', '').replace('-', '').replace(' ', '_')
            filename = f"{self.name}_{ts}.json"

        outpath = (outpath / filename).resolve()
        print(f"Full Export Path:\n  {outpath}")
        try:
            with outpath.open(mode='w') as j_file:
                json.dump(self.json_format(), j_file, indent=2)
            result = f"SUCCESS, exported {outpath.name} to:\n  {outpath}"
        except FileNotFoundError:
            result = "Export failed, please enter a valid output destination."
        except SyntaxError as e:
            result = f"Export failed, check that you have entered a valid path name.\n {e}"
        except PermissionError as e:
            result = f"Export failed due to {e}. Usually this is because you did not specify a filename."
        return result
