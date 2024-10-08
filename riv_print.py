"Summarize strands or translate to pseudo-code"

class Printer:
    "Summarize strands or translate to pseudo-code"

    def print_glyph_summary(self, glyph):
        "Summarize the glyph with descriptions of each strand"

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
                a(f"end_x: {token['end_x']}", True)
                a(f"end_x: {token['end_y']}", True)
                a(f"second.start_x: {token['second']['x']}", True)
                a(f"second.start_y: {token['second']['y']}", True)
                a(f"second.end_x: {token['second']['end_x']}", True)
                a(f"second.end_y: {token['second']['end_y']}", True)
            if token["action"]:
                a(f"action: {token['action']['command']}", True)
        return retstr


    def print_glyph_pseudo(self, glyph):
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
                a("question_marker:",True)
                a(f"end_x: [{token['end_x']},{token['end_y']}]",True)
                a(f"second.start: [{token['second']['x']},{token['second']['y']}]",True)
                a(f"second.end: [{token['second']['end_x']},{token['second']['end_y']}]",True)
            elif token["action"] and "command" in token["action"]:
                if token["action"]["command"] == "subtraction_assignment":
                    a(f"list{token['list']}[{token['assign_to_cell']}] -= ")
                elif token["action"]["command"] == "overwrite":
                    a(f"list{token['list']}[{token['assign_to_cell']}] = ")
                elif token["action"]["command"] == "append":
                    a(f"list{token['list']} append ")
                elif token["action"]["command"] == "insert":
                    a(f"list{token['list']} after cell {token['assign_to_cell']} insert ")
                else:
                    a(f"list{token['list']}[{token['assign_to_cell']}] += ")
            elif token["subtype"] in ("list2list","list"):
                a(f"for each cell in list{token['list']} += ")
            else:
                a(f"list{token['list']}[{token['assign_to_cell']}] += ")

            if token["subtype"] == "value":
                a(str(token['value']))
            if token["subtype"] == "ref":
                a(f"list{token['ref_cell'][0]}[{token['ref_cell'][1]}]")
            a('',True)

            # if token["subtype"] == "value":
            #     a(f"{token['value']}")
        return retstr

    def print_program(self, parse_tree, pseudo=False):
        "Summarize the program"
        retstr = ""
        for idx, glyph in enumerate(parse_tree):
            retstr += f"\nglyph {idx}\n"

            if pseudo:
                retstr += self.print_glyph_pseudo(glyph)
            else:
                retstr += self.print_glyph_summary(glyph)
        print(retstr)
