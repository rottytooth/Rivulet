"Summarize strands or translate to pseudo-code"

class PythonTranspiler:
    "Summarize strands or translate to pseudo-code"
    #FIXME: This should have a base class for Printer/Transpiler to handle pseudo-code and desciption

    def print_glyph_debug(self, glyph):
        "Prints meaning of each strand for debugging"

        retstr = ""
        def a(txt, endline=False):
            nonlocal retstr

            retstr += txt
            if endline:
                retstr += "\n"

        a(f"level: {glyph["level"]}")
        for token in glyph["tokens"]:
            a('', True)
            a(f"type = {token["type"]}", True)
            a(f"subtype = {token["subtype"]}", True)
            if token["type"] != "question_marker":
                a(f"list = {token["list"]}", True)
                a(f"cell = {token["assign_to_cell"]}", True)
            if token["subtype"] == "value":
                a(f"value: {token['value']}", True)
            if token["subtype"] == "ref":
                a(f"ref_cell: {token['ref_cell']}", True)
            if token["type"] == "question_marker":
                a(f"test: {token['test']}", True)
                
                # if "end_position" in token:
                #     a(f"end_position: {token['end_position']}", True)
                # a(f"applies_to: {token['applies_to']}", True)

                if token["applies_to"] == "list":
                    a(f"ref_list: {token['ref_list']}")
                else:
                    a(f"ref_cell: {token['ref_cell']}")
            if token["action"]:
                a(f"action: {token['action']['command']}", True)
        return retstr


    def glyph_pseudo(self, glyph):
        "Return pseudo-code for the glyph"

        retstr = ""
        def a(txt, endline=False):
            nonlocal retstr

            retstr += txt
            if endline:
                retstr += "\n"

        a(f"level: {glyph["level"]}",True)
        for token in glyph["tokens"]:
            if token["type"] == "question_marker":
                a(f"block_type = {token["block_type"]}")
                test = "<= 0"
                if token["applies_to"] == "list":
                    a(f"if (list{token['ref_list']}) has x: x {test}: roll back")
                else:
                    a(f"if {token['ref_cell']} {test}: roll back")
            elif token["action"] and "command" in token["action"]:
                if token["action"]["command"] == "subtraction_assignment":
                    a(f"list{token['list']}[{token['assign_to_cell']}] -= ")
                elif token["action"]["command"] == "multiplication_assignment":
                    a(f"list{token['list']}[{token['assign_to_cell']}] *= ")
                elif token["action"]["command"] == "division_assignment":
                    a(f"list{token['list']}[{token['assign_to_cell']}] /= ")
                elif token["action"]["command"] == "mod_assignment":
                    a(f"list{token['list']}[{token['assign_to_cell']}] %= ")
                elif token["action"]["command"] == "reverse_mod_assignment":
                    a(f"list{token['list']}[{token['assign_to_cell']}] rev %= ")
                elif token["action"]["command"] == "exponent_assignment":
                    a(f"list{token['list']}[{token['assign_to_cell']}] ^= ")
                elif token["action"]["command"] == "overwrite":
                    a(f"list{token['list']}[{token['assign_to_cell']}] = ")
                elif token["action"]["command"] == "append":
                    a(f"list{token['list']} append ")
                elif token["action"]["command"] == "insert":
                    a(f"list{token['list']} after cell {token['assign_to_cell']} insert ")
                elif token["action"]["command"] == "pop":
                    a(f"list{token["list"]}[{token['assign_to_cell']}] (pops) += ")
                elif token["action"]["command"] == "pop_and_append":
                    a(f"list{token["list"]} pop/appends ")
                else:
                    a(f"list{token['list']}[{token['assign_to_cell']}] += ")
            elif token["subtype"] in ("list2list","list"):
                a(f"for each cell in list{token['list']} += ")
            else:
                a(f"list{token['list']}[{token['assign_to_cell']}] += ")

            if token["subtype"] == "value":
                a(str(token['value']))
            if token["subtype"] == "ref":
                if token["action"] and token["action"]["command"] == "pop_and_append" and (token["action"]["subtype"] == "list" or token["action"]["subtype"] == "list2list"):
                    # in this case, we refer to the whole list
                    # FIXME: there ought to be a flag for this in the command token
                    a(f"list{token['ref_cell'][0]}")
                else:
                    a(f"list{token['ref_cell'][0]}[{token['ref_cell'][1]}]")
            a('',True)

            # if token["subtype"] == "value":
            #     a(f"{token['value']}")
        return retstr
    
    def glyph_drawn(self, glyph):
        "Print the literal glyph"
        retstr = ""
        for y in glyph:
            for x in y:
                retstr += x
            retstr += "\n"
        return retstr

    def print_program(self, parse_tree, pseudo=False):
        "Summarize the program"
        #FIXME: Move pseudo to another method in base class (to be created)
        retstr = ""
        for idx, glyph in enumerate(parse_tree):
            retstr += f"\nglyph {idx}\n"

            retstr += self.glyph_drawn(glyph["glyph"])
            retstr += "GLYPH_SUMMARY\n"
            retstr += self.glyph_pseudo(glyph)
            if pseudo:
                retstr += "\nSTRAND SUMMARY\n"
                retstr += self.print_glyph_debug(glyph)

        print(retstr)
