# pylint: skip-file
"""
Test strand analysis in lexer
"""
import copy
import pytest
from rivulet.riv_parser import Parser

zeroes_st_glyph = """
  ╰──╮ ╭───╯╭──╯
╰─╮ ─┘ │╰─╮ └─ ╭─╮
  │╰──┐└─╴│╰───╯ │
  ╰─╮ ╰─╮ └─┐  ╭─╯
  ╶─┘   │ ╶─┘  ╰─╮  
      ╶─┘        │
                ─╯
"""
zeroes_st_glyph = [list(ln) for ln in zeroes_st_glyph.splitlines()] # format
zeroes_st_glyph = zeroes_st_glyph[1:] # remove first line

def test_find_starts_data_strands():
    "Find the start of every strand"
    intr = Parser()
    gl = copy.deepcopy(zeroes_st_glyph)
    starts = intr._Parser__find_strand_starts(gl)
    assert len(starts) == 7
    assert all(s["type"] == "data" for s in starts)
    assert starts[0]["x"] == 2
    assert starts[0]["y"] == 0
    assert starts[1]["x"] == 11
    assert starts[1]["y"] == 0
    assert starts[2]["x"] == 15
    assert starts[2]["y"] == 0
    assert starts[3]["x"] == 0
    assert starts[3]["y"] == 1
    assert starts[4]["x"] == 8
    assert starts[4]["y"] == 1
    assert starts[5]["x"] == 3
    assert starts[5]["y"] == 2
    assert starts[6]["x"] == 11
    assert starts[6]["y"] == 2

def test_lex_zeroes():
    "Test each strand is a value strand with value 0"
    lexr = Parser()
    gl = [{"glyph": copy.deepcopy(zeroes_st_glyph)}]
    lexr._Parser__load_primes(gl)
    starts = lexr._Parser__lex_glyph(gl[0]["glyph"])
    for s in starts:
      assert s["type"] == "data"
      assert s["subtype"] == "value"
      assert s["value"] == 0

glyph_with_ref_strand_vert = """
╰──╮
   │
   ╷
"""
glyph_with_ref_strand_vert = [list(ln) for ln in glyph_with_ref_strand_vert.splitlines()] # format
glyph_with_ref_strand_vert = glyph_with_ref_strand_vert[1:] # remove first line

def test_glyph_with_ref_strand_vert():
    "Test a glyph with an action element strand"
    lexr = Parser()
    gl = [{"glyph": copy.deepcopy(glyph_with_ref_strand_vert)}]
    lexr._Parser__load_primes(gl)
    starts = lexr._Parser__lex_glyph(gl[0]["glyph"])
    assert len(starts) == 1
    assert starts[0]["type"] == "data"
    assert starts[0]["subtype"] == "ref"
    assert starts[0]["x"] == 0
    assert starts[0]["y"] == 0
    assert starts[0]["end_x"] == 3
    assert starts[0]["end_y"] == 2


glyph_with_action_strand = """
╰──╮╰─╮╰─╮
   │ ─┘  │
     ────┘
      ╭
      │
      │
"""
glyph_with_action_strand = [list(ln) for ln in glyph_with_action_strand.splitlines()] # format
glyph_with_action_strand = glyph_with_action_strand[1:] # remove first line

def test_identify_action_element_strand():
    "Test a glyph with an action element strand"
    lexr = Parser()
    gl = [{"glyph": copy.deepcopy(glyph_with_action_strand)}]
    lexr._Parser__load_primes(gl)
    starts = lexr._Parser__lex_glyph(gl[0]["glyph"])
    assert len(starts) == 4
    assert starts[3]["type"] == "action"
    assert starts[3]["subtype"] == "element"
    assert starts[3]["command"]["name"] == "multiplication_assignment"

glyph_with_action_list_strand = """
╰──╮╰─╮╰─╮
   │ ─┘  │
     ────┘
      ╭
      │
      │
      ╰─
"""
glyph_with_action_list_strand = [list(ln) for ln in glyph_with_action_list_strand.splitlines()] # format
glyph_with_action_list_strand = glyph_with_action_list_strand[1:] # remove first line

def test_identify_action_list_strand():
    "Test a glyph with an action list strand"
    lexr = Parser()
    gl = [{"glyph": copy.deepcopy(glyph_with_action_list_strand)}]
    lexr._Parser__load_primes(gl)
    starts = lexr._Parser__lex_glyph(gl[0]["glyph"])
    assert len(starts) == 4
    assert starts[3]["type"] == "action"
    assert starts[3]["subtype"] == "list"
    assert starts[3]["command"]["name"] == "multiplication_assignment"

glyph_with_action_horz_l2l_strand = """
╰──╮╰─╮╰─╮
   │ ─┘  │
     ────┘
      ╭
      │
      │
      ╰─╶
"""
glyph_with_action_horz_l2l_strand = [list(ln) for ln in glyph_with_action_horz_l2l_strand.splitlines()] # format
glyph_with_action_horz_l2l_strand = glyph_with_action_horz_l2l_strand[1:] # remove first line

def test_identify_action_horz_l2l_strand():
    "Test a glyph with an action list strand"
    lexr = Parser()
    gl = [{"glyph": copy.deepcopy(glyph_with_action_horz_l2l_strand)}]
    lexr._Parser__load_primes(gl)
    starts = lexr._Parser__lex_glyph(gl[0]["glyph"])
    assert len(starts) == 4
    assert starts[3]["type"] == "action"
    assert starts[3]["subtype"] == "list2list"
    assert starts[3]["command"]["name"] == "multiplication_assignment"

# question strand set
glyph_with_question_strands = """
╰──╮╰─╮╰─╮╷
   │ ─┘  ││
╭───╮╶───┘│
╰─╮ │ ╭───┘
╭─╯ │ │╭──╮
╰─╮ │ ╷│╭─╯
╭─┘ ╰─┘│╰─╮
╰──────╯ ─╯
"""
glyph_with_question_strands = [list(ln) for ln in glyph_with_question_strands.splitlines()] # format
glyph_with_question_strands = glyph_with_question_strands[1:] # remove first line

def test_correct_count_ends_with_left_facing():
    "Find the correct starts for a glyph with a question strand set where a questions strand ends facing left"
    lexr = Parser()
    gl = [{"glyph": copy.deepcopy(glyph_with_question_strands)}]
    lexr._Parser__load_primes(gl)
    starts = lexr._Parser__find_strand_starts(gl[0]["glyph"])
    assert len(starts) == 5

def test_identify_question_strands():
    "Test a glyph with a question strand set"
    lexr = Parser()
    gl = [{"glyph": copy.deepcopy(glyph_with_question_strands)}]
    lexr._Parser__load_primes(gl)
    starts = lexr._Parser__lex_glyph(gl[0]["glyph"])
    assert starts[3]["type"] == "question_marker"
    assert starts[3]['x'] == 10
    assert starts[3]['y'] == 0
    assert starts[3]['end_x'] == 6
    assert starts[3]['end_y'] == 5
    assert starts[4]["type"] == "question_marker"
    assert starts[4]['x'] == 6
    assert starts[4]['y'] == 5
    assert starts[4]['end_x'] == 9
    assert starts[4]['end_y'] == 7

glyph_with_uneven_lines = """
╰──╮    ╰─╮
   │╰─╮   │╰─╮
     ─┘ ──┘ ─┘
"""
glyph_with_uneven_lines = [list(ln) for ln in glyph_with_uneven_lines.splitlines()] # format
glyph_with_uneven_lines = glyph_with_uneven_lines[1:] # remove first line

def test__lex_glyph_with_uneven_lines():
    "Test a glyph with an action list strand"
    lexr = Parser()
    gl = [{"glyph": copy.deepcopy(glyph_with_uneven_lines)}]
    lexr._Parser__load_primes(gl)
    starts = lexr._Parser__lex_glyph(gl[0]["glyph"])
    assert len(starts) == 4

left_facing_ref_strand = """
╰─╮
╴─┘
"""
left_facing_ref_strand = [list(ln) for ln in left_facing_ref_strand.splitlines()] # format
left_facing_ref_strand = left_facing_ref_strand[1:] # remove first line

def test_left_facing_ref_strand():
    lexr = Parser()
    gl = [{"glyph": copy.deepcopy(left_facing_ref_strand)}]
    lexr._Parser__load_primes(gl)
    starts = lexr._Parser__lex_glyph(gl[0]["glyph"])
    assert starts[0]["type"] == "data"
    assert starts[0]["subtype"] == "ref"

right_facing_ref_strand = """
╭─╯
└─╶
"""
right_facing_ref_strand = [list(ln) for ln in right_facing_ref_strand.splitlines()] # format
right_facing_ref_strand = right_facing_ref_strand[1:] # remove first line

def test_right_facing_ref_strand():
    lexr = Parser()
    gl = [{"glyph": copy.deepcopy(right_facing_ref_strand)}]
    lexr._Parser__load_primes(gl)
    starts = lexr._Parser__lex_glyph(gl[0]["glyph"])
    assert starts[0]["type"] == "data"
    assert starts[0]["subtype"] == "ref"

third_left_facing_ref_strand = """
 ╰──╮    ╰─╮
    │╰─╮ ╴─┘╰─╮
      ─┘     ─┘
"""
third_left_facing_ref_strand = [list(ln) for ln in third_left_facing_ref_strand.splitlines()][1:] # format and remove first line

def test_third_left_facing_ref_strand():
    lexr = Parser()
    gl = [{"glyph": copy.deepcopy(third_left_facing_ref_strand)}]
    lexr._Parser__load_primes(gl)
    starts = lexr._Parser__lex_glyph(gl[0]["glyph"])
    assert starts[1]["type"] == "data"
    assert starts[1]["subtype"] == "ref"

ref_from_low_road = """
╰──╮   ╵
   │╰─╮│╰─╮
     ─┘│ ─┘
       │
       │
       └─╯
"""
ref_from_low_road = [list(ln) for ln in ref_from_low_road.splitlines()] # format
ref_from_low_road = ref_from_low_road[1:] # remove first line

def test_ref_from_low_road():
    lexr = Parser()
    gl = [{"glyph": copy.deepcopy(ref_from_low_road)}]
    lexr._Parser__load_primes(gl)
    starts = lexr._Parser__lex_glyph(gl[0]["glyph"])
    assert starts[3]["type"] == "data"
    assert starts[3]["subtype"] == "ref"

lex_left_prestart ="""
╶╮
 ╰─╮
 ╭─┘
 │        
 │           
 ╰─
"""
lex_left_prestart = [list(ln) for ln in lex_left_prestart.splitlines()][1:] # format

def test_lex_left_prestart():
    lexr = Parser()
    gl = [{"glyph": copy.deepcopy(lex_left_prestart)}]
    lexr._Parser__load_primes(gl)
    starts = lexr._Parser__lex_glyph(gl[0]["glyph"])
    assert len(starts) == 1
    assert starts[0]["type"] == "data"
    assert starts[0]["subtype"] == "value"

lex_right_prestart ="""
╭╴
╰─╮
╭─┘
│        
│           
╰─
"""
lex_right_prestart = [list(ln) for ln in lex_right_prestart.splitlines()][1:] # format

def test_lex_right_prestart():
    lexr = Parser()
    gl = [{"glyph": copy.deepcopy(lex_right_prestart)}]
    lexr._Parser__load_primes(gl)
    starts = lexr._Parser__lex_glyph(gl[0]["glyph"])
    assert len(starts) == 1
    assert starts[0]["type"] == "action"
    assert starts[0]["subtype"] == "list"
