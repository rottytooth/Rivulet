# pylint: skip-file
"""
Test glyph full parsing
"""
import copy
import pytest
from rivulet.riv_parser import Parser

glyph_with_one_list = """
╵╰──╮╰─╮╰─╮╰─╮
    │ ─┘  │ ─┘
        ──┘  ╷
"""

def test_cell_order_one_list():
    parser = Parser()
    block = parser.parse_program(str(glyph_with_one_list))[0]
    assert block["level"] == 1
    for i in range(4):
        assert block["tokens"][i]["list"] == 1
        assert block["tokens"][i]["assign_to_cell"] == i

glyph_with_one_list_ref_strand = """
╵╰──╮╰─╮╰─╮╰─╮
    │ ─┘  │ ─┘
       ╴──┘  ╷
"""

def test_cell_order_one_list_ref():
    parser = Parser()
    block = parser.parse_program(str(glyph_with_one_list_ref_strand))[0]
    assert block["level"] == 1
    for i in range(4):
        assert block["tokens"][i]["list"] == 1
        assert block["tokens"][i]["assign_to_cell"] == i

glyph_with_two_lists = """
╵╰──╮   ╰─╮
    │╰─╮  │╰─╮
      ─┘╶─┘ ─┘╷
"""

def test_cell_order_two_lists():
    parser = Parser()
    block = parser.parse_program(str(glyph_with_two_lists))[0]
    assert block["level"] == 1
    assert len(block["tokens"]) == 4

    assert block["tokens"][0]["list"] == 1
    assert block["tokens"][0]["assign_to_cell"] == 0
    assert block["tokens"][0]["y"] == 0

    assert block["tokens"][1]["list"] == 2
    assert block["tokens"][1]["assign_to_cell"] == 0
    assert block["tokens"][1]["y"] == 1

    assert block["tokens"][2]["list"] == 1
    assert block["tokens"][2]["assign_to_cell"] == 1
    assert block["tokens"][2]["y"] == 0

    assert block["tokens"][3]["list"] == 2
    assert block["tokens"][3]["assign_to_cell"] == 1
    assert block["tokens"][3]["y"] == 1

glyph_with_one_list_question_strand = """
╵╰──╮╰─╮╷╰─╮
 ╭─╮│ ─┘│ ─┘
 │ ╰────┘ ╭─  
 ╷   ╭────┘
 ╰───┘     ╷
"""

def test_cell_order_one_list_question():
    parser = Parser()
    block = parser.parse_program(str(glyph_with_one_list_question_strand))[0]
    assert block["level"] == 1

    # the question marker should appear at the back of the list, not in x,y order
    for i in range(3):
        assert block["tokens"][i]["list"] == 1
        assert block["tokens"][i]["assign_to_cell"] == i
        assert block["tokens"][i]["type"] == "data"

    assert block["tokens"][3]["type"] == "question_marker"
    with pytest.raises(KeyError):
        assert block["tokens"][3]["list"] == None
    with pytest.raises(KeyError):
        assert block["tokens"][3]["assign_to_cell"] == None

    assert block["tokens"][3]["second"]["type"] == "question_marker"
    with pytest.raises(KeyError):
        assert block["tokens"][3]["second"]["list"] == None
    with pytest.raises(KeyError):
        assert block["tokens"][3]["second"]["assign_to_cell"] == None

glyph_with_wide_question = """
╵╰──╮╰─╮╷╰─╮╭─╮                                ╭─╮
 ╭─╮│ ─┘│ ─┘│ │                                │ │
 │ ╰────┘ ╭─┘ │                                │ │
 ╷   ╭────┘   │                                │ │
 ╰───┘        ╰────────────────────────────────┘ │╷
"""

def test_glyph_with_wide_question():
    parser = Parser()
    block = parser.parse_program(str(glyph_with_wide_question))[0]
    assert block["level"] == 1

    # the question marker should appear at the back of the list, not in x,y order
    for i in range(3):
        assert block["tokens"][i]["list"] == 1
        assert block["tokens"][i]["assign_to_cell"] == i
        assert block["tokens"][i]["type"] == "data"

    assert block["tokens"][3]["type"] == "question_marker"
    with pytest.raises(KeyError):
        assert block["tokens"][3]["list"] == None
    with pytest.raises(KeyError):
        assert block["tokens"][3]["assign_to_cell"] == None

    assert block["tokens"][3]["second"]["type"] == "question_marker"
    with pytest.raises(KeyError):
        assert block["tokens"][3]["second"]["list"] == None
    with pytest.raises(KeyError):
        assert block["tokens"][3]["second"]["assign_to_cell"] == None

glyph_with_ref_strand = """
╵╰──╮   ╰─╮
    │╰─╮╴─┘╰─╮
      ─┘     │
           ──┘╷
"""

def test_ref_of_ref_strand():
    parser = Parser()
    block = parser.parse_program(str(glyph_with_ref_strand))[0]

    assert block["tokens"][2]["list"] == 1
    assert block["tokens"][2]["assign_to_cell"] == 1
    assert block["tokens"][2]["ref_cell"] == [2, 1]

ref_of_ref_upward_facing = """
╵╰──╮   ╵
    │╰─╮│ ╰─╮
      ─┘╰───┘╷
"""

def test_ref_of_ref_upward_facing():
    parser = Parser()
    block = parser.parse_program(str(ref_of_ref_upward_facing))[0]

    assert block["tokens"][2]["list"] == 2
    assert block["tokens"][2]["assign_to_cell"] == 1
    assert block["tokens"][2]["ref_cell"] == [1, 1]

ref_from_high_row = """
╵╰──╮   ╵
    │╰─╮│╰─╮
      ─┘│ ─┘
        │
        │
        └─╯╷
"""

def test_ref_from_high_row():
    parser = Parser()
    block = parser.parse_program(str(ref_from_high_row))[0]

    assert block["tokens"][3]["list"] == 11
    assert block["tokens"][3]["assign_to_cell"] == 0
    assert block["tokens"][3]["ref_cell"] == [1, 1]

ref_value_assignment = """
 1 ╵╰──╮╰─╴╰──╮╶╮
 2    ─┘     ─┘ ╰─╮
 3              ╭─┘
 5              │        
 7              │           
11              ╰─ ╷
"""
def test_ref_value_assignment():
    parser = Parser()
    block = parser.parse_program(str(ref_value_assignment))[0]

    for i in range(4):
        assert block["tokens"][i]["list"] == 1
        assert block["tokens"][i]["type"] == "data"
        assert block["tokens"][i]["subtype"] == "value"

    assert block["tokens"][0]["value"] == 0
    assert block["tokens"][1]["value"] == 1
    assert block["tokens"][2]["value"] == 0
    assert block["tokens"][3]["value"] == 10

ref_value_assignment_2 = """
 1 ╵╰──╮╰─ ╭──╯ ╶╮
 2    ─┘   └─    │
 3    ╭──────────┘
 5    └────────  ╷
"""
def test_ref_value_assignment_2():
    parser = Parser()
    block = parser.parse_program(str(ref_value_assignment_2))[0]

    for i in range(4):
        assert block["tokens"][i]["list"] == 1
        assert block["tokens"][i]["type"] == "data"
        assert block["tokens"][i]["subtype"] == "value"

    assert block["tokens"][0]["value"] == 0
    assert block["tokens"][1]["value"] == 1
    assert block["tokens"][2]["value"] == 0
    assert block["tokens"][3]["value"] == 10

multiple_ref_assignments = """
 1 ╵╵     ╭───╮ ╭─ 
 2    ╴─╮╶╯╶╮ ╷╶╯  
 3  ╵╰──┘   │      
 5  ╰───────╯      
 7   ╭╴     ╭╴     
11   │      │     ╷
"""
def test_correct_ref_cells():
    parser = Parser()
    block = parser.parse_program(str(multiple_ref_assignments))[0]

    assert len(block["tokens"]) == 4
    assert block["tokens"][0]["ref_cell"] == [2, 0]
    assert block["tokens"][1]["ref_cell"] == [2, 2]
    assert block["tokens"][2]["ref_cell"] == [3, 0]

def test_action_strands_connect_to_correct_data_strands():
    parser = Parser()
    block = parser.parse_program(str(multiple_ref_assignments))[0]

    assert len(block["tokens"]) == 4
    assert block["tokens"][1]["action"] == None
    assert block["tokens"][3]["action"] == None

    assert block["tokens"][0]["action"]['x'] == 2
    assert block["tokens"][0]["action"]['y'] == 4

    assert block["tokens"][2]["action"]['x'] == 9
    assert block["tokens"][2]["action"]['y'] == 4

action_strand_add_replace = """
 1 ╵╵     ╭───╮ ╭─
 2    ╴─╮╶╯╶╮ │╶╯
 3  ╵╰──┘   │ ╷
 5  ╰───────╯
 7   ╭╴     ╭╴
11   │      │
13 │ │    │ │
17 ╰─╯    ╰─╯    ╷
"""
def test_action_strand_overwrite():
    parser = Parser()
    block = parser.parse_program(str(action_strand_add_replace))[0]

    assert block["tokens"][0]["action"]["command"] == "overwrite"
    assert block["tokens"][2]["action"]["command"] == "overwrite"

def test_correct_lists_for_cells():
    parser = Parser()
    block = parser.parse_program(str(multiple_ref_assignments))[0]

    assert len(block["tokens"]) == 4
    assert block["tokens"][0]["list"] == 3
    assert block["tokens"][1]["list"] == 2
    assert block["tokens"][2]["list"] == 2
    assert block["tokens"][3]["list"] == 2

# Action Strands

action_strand_with_list_interpretation = """
 1 ╵╵     ╭───╮
 2    ╴─╮╶╯╶╮ ╷
 3  ╵╰──┘   │
 5  ╰───────╯
 7   ╭╴     ╭╴
11   │      │ 
13    ──────╯ ╷
"""
def test_action_strand_with_list_interpretation():
    parser = Parser()
    block = parser.parse_program(str(action_strand_with_list_interpretation))[0]

    assert block["tokens"][0]["action"]["command"] == "insert"
    assert block["tokens"][2]["action"]["command"] == "append"
    assert block["tokens"][2]["action"]["subtype"] == "list"
    assert block["tokens"][2]["subtype"] == "ref"


action_strand_with_list2list_interpretation = """
 1 ╵╵     ╭───╮
 2    ╴─╮╶╯╶╮ ╷
 3  ╵╰──┘   │
 5  ╰───────╯
 7   ╭╴     ╭╴
11   │      │
13        ╴─╯ ╷
"""
def test_action_strand_with_list2list_interpretation():
    parser = Parser()
    block = parser.parse_program(str(action_strand_with_list2list_interpretation))[0]

    assert block["tokens"][0]["action"]["command"] == "insert"
    assert block["tokens"][2]["action"]["command"] == "append"
    assert block["tokens"][2]["action"]["subtype"] == "list2list"
    assert block["tokens"][2]["action"]["applies_to"] == "list"

action_strand_with_list2list_interpretation_nonlist = """
 1 ╵╵     ╭───╮
 2    ╴─╮╶╯╶╮ ╷
 3  │╰──┘   │
 5  ╰───────╯
 7   ╭╴     ╭╴
11   │      │
13    ──────╯ ╷
"""
def test_action_strand_with_list_val_interpretation():
    parser = Parser()
    block = parser.parse_program(str(action_strand_with_list2list_interpretation_nonlist))[0]

    assert block["tokens"][0]["action"]["command"] == "insert"
    assert block["tokens"][2]["action"]["command"] == "append"
    assert block["tokens"][2]["action"]["subtype"] == "list"
    assert block["tokens"][2]["subtype"] == "value"

action_strand_with_negative_action = """
 1 ╵╵     ╭───╮
 2    ╴─╮╶╯╶╮ ╷
 3  ╵╰──┘   │
 5  ╰───────╯ │
 7   ╭╴     ╭╴│
11   │ │    ╰─╯
13   │ │    
17   ╰─╯        ╷
"""
def test_action_strand_with_negative_action():
    parser = Parser()
    block = parser.parse_program(str(action_strand_with_negative_action))[0]

    assert block["tokens"][0]["action"]["command"] == "division_assignment"
    assert block["tokens"][2]["action"]["command"] == "root_assignment"

action_strand_to_higher_number_ref_cell = """
 1 ╵╵         ╭───╮ ╭─ ╶╮ ╭─╮  
 2 ╴─╮    ╴─╮╶╯╶╮ ╷╶╯╭──╯╶╯ ╰─╮ ╴─╮
 3   │ ╵ ╰──┘   │ ╭──┘  ╭╴   ─╯  ╶╯
 5   │ ╰────────╯ │     │         ╭╴
 7   ╰────────────╯  ───╯         │
11       ╭╴     ╭╴                │
13       │      │               │ │
17       │ │    ╰─╮             ╰─╯
19       ╰─╯│     │
23          ╰─────╯                ╷
"""
def test_action_strand_to_higher_number_ref_cell():
    parser = Parser()
    block = parser.parse_program(str(action_strand_to_higher_number_ref_cell))[0]

    assert block["tokens"][6]["ref_cell"] == [2, 4]

action_strand_to_middle_number_ref_cell = """
 1 ╵╵         ╭───╮ ╭─ ╶╮ ╭─╮       ╭───
 2 ╴─╮    ╴─╮╶╯╶╮ ╷╶╯╭──╯╶╯ ╰─╮ ╴─╮╶╯
 3   │ ╵ ╰──┘   │ ╭──┘  ╭╴   ─╯  ╶╯
 5   │ ╰────────╯ │     │         ╭╴
 7   ╰────────────╯  ───╯         │
11       ╭╴     ╭╴                │
13       │      │               │ │
17       │ │    ╰─╮             ╰─╯
19       ╰─╯│     │
23          ╰─────╯                     ╷
"""
def test_action_strand_to_middle_number_ref_cell():
    parser = Parser()
    block = parser.parse_program(str(action_strand_to_middle_number_ref_cell))[0]

    assert block["tokens"][6]["ref_cell"] == [2, 4]

def test_action_strand_second_ref_cell():
    parser = Parser()
    block = parser.parse_program(str(action_strand_to_middle_number_ref_cell))[0]

    assert block["tokens"][1]["ref_cell"] == [2, 2]

# Question Strands

question_strand_glyph = '''╵╵ ──╮  ╭─╮╭───╮
   ╰─╯╰─╯ │╰──╮╷
   ╰─╮   ─╯ ╷╶╯
  ╭──╯  ╭─╮ │
  ╰─╭─╮ ╷ │ │
    │ │ │ │ │ 
  ──╯ ╰─╯ ╰─╯  ╷
'''
def test_question_strand_apply_to_list():
    parser = Parser()
    block = parser.parse_program(str(question_strand_glyph))[0]
    print(block)
    assert block["tokens"][4]["end_pos"] == "horizontal"
    assert block["tokens"][4]["applies_to"] == "list"

question_strand_glyph2 = '''╵╵ ──╮  ╭─╮╭───╮
   ╰─╯╰─╯ │╰──╮╷
   ╰─╮   ─╯ ╷╶╯
  ╭──╯  ╭─╮ │
  ╰─╭─╮ ╷ │ │
    │ │ │ │ │ 
    │ ╰─╯ ╰─╯  ╷
'''
def test_question_strand_apply_to_list():
    parser = Parser()
    block = parser.parse_program(str(question_strand_glyph2))[0]
    print(block)
    assert block["tokens"][4]["end_pos"] == "vertical"
    assert block["tokens"][4]["applies_to"] == "cell"


question_strand_vert1 = '''╵        ╷
     ╭─╮ │   
 ╭─╮ │ │ │
 │ │ ╷ │ │ 
 │ ╰─╯ ╰─╯  ╷
'''
def test_question_strand_if_1():
    parser = Parser()
    block = parser.parse_program(str(question_strand_vert1))[0]
    print(block)
    assert block["tokens"][0]["applies_to"] == "cell"
    assert block["tokens"][0]["block_type"] == "if"
    assert block["tokens"][0]["ref_cell"] == [1, 0]

question_strand_while_vert = '''╵  ╷
   │ ╭─╮     
   │ │ ╷  
   ╰─╯ │
    ───╯ ╷
'''
def test_question_strand_while_1():
    parser = Parser()
    block = parser.parse_program(str(question_strand_while_vert))[0]
    print(block)
    assert block["tokens"][0]["applies_to"] == "list"
    assert block["tokens"][0]["block_type"] == "while"
    assert block["tokens"][0]["ref_list"] == 1
