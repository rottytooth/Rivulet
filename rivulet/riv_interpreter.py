"Interpreter for the Rivulet programming language"
from argparse import ArgumentParser
from enum import Enum
import json
import math
from rivulet.riv_exceptions import RivuletSyntaxError
from rivulet.riv_parser import Parser
from rivulet.riv_python_transpiler import PythonTranspiler
from rivulet.riv_svg_generator import SvgGenerator
from rivulet.riv_themes import Themes
from rivulet import __version__

VERSION = __version__

class Interpreter:
    "Interpreter for the Rivulet programming language, main entry point"

    class OutputOption(Enum):
        none = 'none'
        unicode = 'unicode'
        numeric = 'numeric'

    Action = Enum('Action', [
        ('rollback', 1),    # undo all changes to state and exit block
        ('cont', 2),        # continue to next glyph
        ('repeat', 3)       # repeat the block
    ])


    def __init__(self):
        self.outfile = None
        self.verbose = False
        self.debug = None
        self.output = Interpreter.OutputOption.none


    def interpret_file(self, progfile, verbose, output):
        "Interpret a Rivulet program file"
        self.verbose = verbose
        self.output = output

        with open(progfile, "r", encoding="utf-8") as file:
            program = file.read()

        return self.interpret_program(program, verbose)
    

    def interpret_program(self, program:str, verbose:bool, debug = None):
        """Interpret a Rivulet program passed by text
        
        program: program text as string
        verbose: flag
        debug: callback function called in the processing of each glyph
        """
        self.verbose = verbose

        parser = Parser()

        glyphs = parser.parse_program(program)

        self.__interpret(glyphs, debug)


    def __interpret(self, glyphs, debug = None):
        state = dict([(1,[])])

        prime_size = max(glyphs, key=lambda x: x["list_size"])["list_size"]

        # initialize state with lists required
        for num in range(2, prime_size ** 2):
            if all(num % i != 0 for i in range(2, int(math.sqrt(num)) + 1)):
                state[num] = []
                if len(state) >= prime_size:
                    break
        if self.verbose:
            self.debug = PythonTranspiler()

        for idx, g in enumerate(glyphs):
            g["id"] = idx

        parse_tree = self.treeify_glyphs(json.loads(json.dumps(glyphs)), 1, [])

        self.__decorate_blocks(parse_tree, 0, None)

        self.__interpret_block(parse_tree, state)

        if 1 in state:
            if self.output == Interpreter.OutputOption.unicode:
                print("".join(chr(num) for num in state[1] if isinstance(num, int) and 0 <= num <= 0x10FFFF))
            elif self.output == Interpreter.OutputOption.numeric:
                print(" ".join(str(num) for num in state[1] if isinstance(num, int) and 0 <= num <= 0x10FFFF))

        if debug:
            debug(parse_tree, state)

    def treeify_glyphs(self, glyphs, curr_level, tree):
        "Reorganize a flat list of glyphs into a tree by level"
        if glyphs[0]["level"] == curr_level:
            tree.append(glyphs.pop(0))
        elif glyphs[0]["level"] > curr_level:
            level = []
            tree.append(level)
            self.treeify_glyphs(glyphs, curr_level + 1, level)
        else:
            # go back up one level
            return tree

        if len(glyphs) > 0:
            self.treeify_glyphs(glyphs, curr_level, tree)

        return tree


    def __decorate_blocks(self, block, level, following = None):
        "for each glyph in a block, link to glyphs that start the block or first fall after it"
        first = None
        for idx, g in enumerate(block):

            # find first glyph for block, even if it is in a sub-block
            if idx == 0:
                first = g
                while isinstance(first, list):
                    first = first[0]

            if not isinstance(g, list):
                g["first"] = first["id"]
                g["level"] = level
                if following:
                    g["following"] = following["id"]
                else:
                    g["following"] = None
            else:
                # set following to the next glyph in the block or its first descendent
                # if there are no more, allow it to remain the existing following
                if idx < len(block) - 1:
                    f = block[idx + 1]
                    while isinstance(f, list):
                        f = f[0]
                    if not isinstance(f, list):
                        following = f
                self.__decorate_blocks(g, level + 1, following)


    def __interpret_block(self, parse_tree, state):

        rollback_state = json.loads(json.dumps(state))

        for g in parse_tree:
            if isinstance(g, list):
                self.__interpret_block(g, state)
            else:
                action = self.__interpret_glyph(g, state)
                if action == self.Action.rollback:
                    state = json.loads(json.dumps(rollback_state))
                    return # a rollback also exits the block
                if action == self.Action.cont:
                    continue
                if action == self.Action.repeat:
                    self.__interpret_block(parse_tree, state)


    def __interpret_glyph(self, glyph, state) -> Action:

        retval = self.Action.cont

        for token in glyph["tokens"]:
            if token["type"] == "question_marker":
                retval = self.__resolve_question(token, state)
            else: # is a value or a ref marker

                # if the cell is not in the list, initialize it to zero
                if 'assign_to_cell' in token and len(state[token['list']]) == token['assign_to_cell'] and \
                    (not token["action"] or not "command" in token["action"] or not token["action"]["command"] in ["pop_and_append","append"]):
                    state[token['list']].append(0)
                # elif 'assign_to_cell' in token and len(state[token['list']]) < token['assign_to_cell']:
                #     # shouldn't be possible
                #     pass

                source = None

                list2list = not token["action"] is None and "subtype" in token["action"] and token["action"]["subtype"] == "list2list"

                # find source item
                if list2list:
                    source = state[token["ref_list"]]
                if token["subtype"] == "value":
                    source = token["value"]
                elif token["subtype"] == "ref":
                    if token["ref_cell"][0] >= len(token):
                        raise RivuletSyntaxError("List reference out of bounds")

                    if token["ref_cell"][1] >= len(state[token["ref_cell"][0]]):
                        # this cell has not yet been populated
                        source = 0
                    else:
                        source = state[token["ref_cell"][0]][token["ref_cell"][1]]

                # find item to apply to
                if list2list:
                    for i in range(len(state[token["list"]])):
                        state[token["list"]][i] = self.__resolve_cmd(token, state[token["list"]][i], source[i])
                elif token["action"] is None or "command" not in token["action"]:
                    # defaults to add_assign
                    state[token["list"]][token["assign_to_cell"]] += source
                elif token["action"]["command"] == "insert":
                    state[token["list"]].insert(token["assign_to_cell"], source)
                elif token["action"]["command"] == "append":
                    state[token["list"]].append(source)
                elif token["action"]["command"] == "pop":
                    state[token["list"]][token["assign_to_cell"]] += source
                    if token["subtype"] == "ref":
                        state[token["ref_cell"][0]].pop(token["ref_cell"][1])
                elif token["action"]["command"] == "pop_and_append":
                    state[token["list"]].append(state[token["ref_cell"][0]].pop(token["ref_cell"][1]))
                elif token["action"]["subtype"] == "list":
                    for i in range(len(state[token["list"]])):
                        state[token["list"]][i] = self.__resolve_cmd(token, state[token["list"]][i], source)
                else:
                    state[token["list"]][token["assign_to_cell"]] = self.__resolve_cmd(token, state[token["list"]][token["assign_to_cell"]], source)

        if self.verbose:
            print(self.debug.glyph_drawn(glyph["glyph"]))
            print(self.debug.glyph_pseudo(glyph))
            print(state)
            print("\n")
        elif self.output == Interpreter.OutputOption.none:
            print(" ")
            print(f"glyph: {glyph['id']}")
            print("\n".join([f"{k}: {v}" for k, v in state.items() if v]))

        return retval
    

    def print_and_exit(self, progfile):
        "Print source and pseudo-code for complete program"
        with open(progfile, "r", encoding="utf-8") as file:
            program = file.read()
        parser = Parser()
        glyphs = parser.parse_program(program)

        self.debug = PythonTranspiler()        
        print(self.debug.print_program(glyphs, False))


    def draw_svg(self, progfile, theme):
        "Generate an SVG of the program source code"
        with open(progfile, "r", encoding="utf-8") as file:
            program = file.read()
        parser = Parser()
        glyphs = parser.parse_program(program)
        svg = SvgGenerator(Themes[theme])
        svg.generate(glyphs)


    def __resolve_cmd(self, token, initial_value, assign_value):
        if not token["action"] or not "command" in token["action"]:
            raise RivuletSyntaxError("No command found in token")

        match token["action"]["command"]:
            case "addition_assignment":
                return initial_value + assign_value
            case "subtraction_assignment":
                return initial_value - assign_value
            case "overwrite":
                return assign_value
            case "multiplication_assignment":
                return initial_value * assign_value
            case "division_assignment":
                return initial_value / assign_value
            case "mod_assignment":
                return initial_value % assign_value
            case "exponent_assignment":
                return initial_value ** assign_value
            case "root_assignment":
                return initial_value ** (1 / assign_value)


    def __resolve_question(self, token, state) -> Action:
        retval = self.Action.cont

        succeeds = False

        if token["applies_to"] == "cell":
            succeeds = state[token["ref_cell"][0]][token["ref_cell"][1]] > 0
        elif token["applies_to"] == "list":
            succeeds = all(i > 0 for i in state[token["ref_list"]])
        else:
            raise RivuletSyntaxError("Could not determine what question marker applies to")

        if succeeds:
            if token["block_type"] == "while":
                retval = self.Action.repeat
        else:
            retval = self.Action.rollback

        return retval


def main():

    arg_parser = ArgumentParser(description=f'Rivulet Interpreter {VERSION}',
                            epilog='More at https://danieltemkin.com/Esolangs/Rivulet')

    arg_parser.add_argument('progfile', metavar='progfile', type=str,
                        help='Rivulet program file')
    arg_parser.add_argument('-p', dest='print', action="store_true", default=False,
                        help='parse and print interpretation of each glyph, then exit')
    arg_parser.add_argument('-v', dest='verbose', action='store_true',
                        default=False, help='verbose logging')
    arg_parser.add_argument('--svg', dest='svg', action='store_true', default=False,
                        help='generate svg of program, then exit')
    arg_parser.add_argument('-o', dest='output', type=Interpreter.OutputOption, default=Interpreter.OutputOption.none, choices=list(Interpreter.OutputOption))
    arg_parser.add_argument('--theme', dest='color_set', default="default", help="color scheme for svg")
    args = arg_parser.parse_args()

    intr = Interpreter()

    if (args.print):
        intr.print_and_exit(args.progfile)
        exit(0)
    if (args.svg):
        intr.draw_svg(args.progfile, args.color_set)
        exit(0)

    intr.interpret_file(args.progfile, args.verbose, args.output)

if __name__ == "__main__":
    main()
