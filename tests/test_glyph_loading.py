# pylint: skip-file
"""
Test glyph locating and separation
"""
import copy
import pytest
from rivulet.riv_parser import Parser

def _prepare(glyph):
    glyph = copy.deepcopy(glyph)
    glyph = [list(ln) for ln in glyph.splitlines()]
    lngst = max(len(e) for e in glyph)
    for ln in glyph:
        if len(ln) < lngst:
            ln.extend([' ' for _ in range(lngst - len(ln))])
    return glyph


zeroes_glyph = """
╵  ╰──╮ ╭───╯╭──╯
 ╰─╮ ─┘ │╰─╮ └─ ╭─╮
   │╰──┐└─╴│╰───╯ │
   ╰─╮ ╰─╮ └─┐  ╭─╯
   ╶─┘   │ ╶─┘  ╰─╮  
       ╶─┘        │
                 ─╯╷
"""
def test_shave_zeroes_1st_level():
    intr = Parser()
    gl = _prepare(zeroes_glyph)
    glyph_locs = intr._Parser__locate_glyphs(gl)
    block_tree = intr._Parser__prepare_glyphs_for_lexing(glyph_locs, gl)
    assert(block_tree[0]["glyph"][0][0] == ' ')
    assert(block_tree[0]["glyph"][-1][-1] == ' ')
    assert(block_tree[0]["level"] == 1)

def test__locate_glyphs_zeroes():
    intr = Parser()
    gl = _prepare(zeroes_glyph)
    gl = intr._Parser__remove_blank_lines(gl)
    glyph_locs = intr._Parser__locate_glyphs(gl)
    assert(len(glyph_locs) == 1)
    assert(glyph_locs[0]['start'] == {"y": 0, "x": 0})
    assert(glyph_locs[0]['end'] == {"y": 6, "x": 19})
    
zeroes2_glyph = """
╵╵  ╰──╮ ╭───╯╭──╯
  ╰─╮ ─┘ │╰─╮ └─ ╭─╮
    │╰──┐└─╴│╰───╯ │
    ╰─╮ ╰─╮ └─┐  ╭─╯
    ╶─┘   │ ╶─┘  ╰─╮  
        ╶─┘        │
                  ─╯╷
"""
def test_shave_zeroes_2nd_level():
    intr = Parser()
    gl = _prepare(zeroes2_glyph)
    glyph_locs = intr._Parser__locate_glyphs(gl)
    block_tree = intr._Parser__prepare_glyphs_for_lexing(glyph_locs, gl)
    assert(block_tree[0]["glyph"][0][0] == ' ')
    assert(block_tree[0]["glyph"][-1][-1] == ' ')
    assert(block_tree[0]["level"] == 2)

glyph_with_partial_start = """
╵  ╰──╮ ╷
 ╰─╮ ─┘ │╰─╮
   │╰──┐└─╴│
       │    ╷
"""
def test__locate_glyphs_with_partial_start():
    intr = Parser()
    gl = _prepare(glyph_with_partial_start)
    gl = intr._Parser__remove_blank_lines(gl)
    glyph_locs = intr._Parser__locate_glyphs(gl)
    assert(len(glyph_locs) == 1)
    assert(glyph_locs[0]['start'] == {"y": 0, "x": 0})
    assert(glyph_locs[0]['end'] == {"y": 3, "x": 12})

glyph_with_line_end_just_after_start_marker = """
 1 ╵
 2  ╵╰──╮    
 3  │   ╰────
"""
def test__glyph_with_line_end_just_after_start_marker():
    intr = Parser()
    gl = _prepare(glyph_with_partial_start)
    gl = intr._Parser__remove_blank_lines(gl)
    glyph_locs = intr._Parser__locate_glyphs(gl)
    assert(len(glyph_locs) == 1)
    assert(glyph_locs[0]['start'] == {"y": 0, "x": 0})


glyph_with_partial_start_bottom = """
╵  ╰──╮ ╮
 ╰─╮ ─┘ │╰─╮
   │╰──┐└─╴│
       ╵    ╷
"""
def test__locate_glyphs_with_partial_start_bottom():
    intr = Parser()
    gl = _prepare(glyph_with_partial_start_bottom)
    gl = intr._Parser__remove_blank_lines(gl)
    glyph_locs = intr._Parser__locate_glyphs(gl)
    assert(len(glyph_locs) == 1)
    assert(glyph_locs[0]['start'] == {"y": 0, "x": 0})
    assert(glyph_locs[0]['end'] == {"y": 3, "x": 12})

zeroes_prog_cmt = """
A COMMENT            
                     
 1 ╵  ╰──╮ ╭───╯╭──╯
 2  ╰─╮ ─┘ │╰─╮ └─ ╭─╮
 3    │╰──┐└─╴│╰───╯ │
 5    ╰─╮ ╰─╮ └─┐  ╭─╯
 7    ╶─┘   │ ╶─┘  ╰─╮  
11        ╶─┘        │
13                  ─╯╷
                      
ANOTHER COMMENT"""
def test__locate_glyphs_zeroes_comments():
    intr = Parser()
    pr = _prepare(zeroes_prog_cmt)
    pr = intr._Parser__remove_blank_lines(pr)
    glyph_locs = intr._Parser__locate_glyphs(pr)
    assert(len(glyph_locs) == 1)
    assert(glyph_locs[0]['start'] == {"y": 2, "x": 3})
    assert(glyph_locs[0]['end'] == {"y": 8, "x": 22})

two_glyphs_prog = """
 1 ╵  ╰──╮ ╭───╯╭──╯     ╵╰──╮╶─╮ ╰╴╰─╮╭─┘
 2  ╰─╮ ─┘ │╰─╮ └─ ╭─╮      ─┘  ╰─╮╭──┘│
 3    │╰──┐└─╴│╰───╯ │          ╰─┘╰─╴ │   
 5    ╰─╮ ╰─╮ └─┐  ╭─╯              ───┘ ╷
 7    ╶─┘   │ ╶─┘  ╰─╮                    
11        ╶─┘        │
13                  ─╯╷
                      
"""
def test_locate_two_glyphs():
    intr = Parser()
    pr = _prepare(two_glyphs_prog)
    pr = intr._Parser__remove_blank_lines(pr)
    glyph_locs = intr._Parser__locate_glyphs(pr)
    assert(len(glyph_locs) == 2)
    assert(glyph_locs[0]['start'] == {'y': 0, 'x': 3})
    assert(glyph_locs[0]['end'] == {'y': 6, 'x': 22})
    assert(glyph_locs[1]['start'] == {'y': 0, 'x': 25})
    assert(glyph_locs[1]['end'] == {'y': 3, 'x': 41})

def test_prepare_two_glyphs():
    intr = Parser()
    pr = _prepare(two_glyphs_prog)
    pr = intr._Parser__remove_blank_lines(pr)
    glyph_locs = intr._Parser__locate_glyphs(pr)
    assert(len(glyph_locs) == 2)
    block_tree = intr._Parser__prepare_glyphs_for_lexing(glyph_locs, pr)
    assert(len(block_tree) == 2)

def test_level_for_2_glyphs():
    intr = Parser()
    pr = _prepare(two_glyphs_prog)
    pr = intr._Parser__remove_blank_lines(pr)
    glyph_locs = intr._Parser__locate_glyphs(pr)
    assert len(glyph_locs) == 2 
    assert glyph_locs[0]['level'] == 1
    assert glyph_locs[1]['level'] == 1 

three_glyphs_prog = """
 1 ╵  ╰──╮ ╭───╯╭──╯     ╵╰──╮╶─╮ ╰╴╰─╮╭─┘
 2  ╰─╮ ─┘ │╰─╮ └─ ╭─╮      ─┘  ╰─╮╭──┘│
 3    │╰──┐└─╴│╰───╯ │          ╰─┘╰─╴ │   
 5    ╰─╮ ╰─╮ └─┐  ╭─╯              ───┘ ╷
 7    ╶─┘   │ ╶─┘  ╰─╮  
11        ╶─┘        │
13                  ─╯╷
                                           
╵╵╰──╮╰─╮╰─
    ─┘  │
    ────┘
      ╭
      │   ╷    
"""
def test_locate_three_glyphs():
    intr = Parser()
    pr = _prepare(three_glyphs_prog)
    pr = intr._Parser__remove_blank_lines(pr)
    glyph_locs = intr._Parser__locate_glyphs(pr)
    assert(len(glyph_locs) == 3)
    assert(glyph_locs[0]['start'] == {'y': 0, 'x': 3})
    assert(glyph_locs[0]['end'] == {'y': 6, 'x': 22})
    assert(glyph_locs[1]['start'] == {'y': 0, 'x': 25})
    assert(glyph_locs[1]['end'] == {'y': 3, 'x': 41})
    assert(glyph_locs[2]['start'] == {'y': 8, 'x': 1})
    assert(glyph_locs[2]['end'] == {'y': 12, 'x': 10})

has_ref_at_end = """
╵╭─╶ ╮  ╭─┘╭─╶         
 │   │╭─┘╭─╯           
 │╶╮ │╰─ │             
 ╰─┘ ╰───┘
     ╮                 
   │ │         
   ╰─┘       ╷

"""
def test_scan_glyph_with_ref_at_end():
    intr = Parser()
    pr = _prepare(has_ref_at_end)
    pr = intr._Parser__remove_blank_lines(pr)
    glyph_locs = intr._Parser__locate_glyphs(pr)
    assert(len(glyph_locs) == 1)

# Second level glyph
fib_2_glyph = """
╵╵╭─╶ ╶╮  ╭─┘╭─╶ 
  │  ╶╮│╭─┘╭─╯  
  │╶╮ ││╰─ │ 
  ╰─┘ │╰───┘
   ╶╮ │
    │         ╷
"""
def test_determine_level_2():
    intr = Parser()
    gl = _prepare(fib_2_glyph)
    gl = intr._Parser__remove_blank_lines(gl)
    glyph_locs = intr._Parser__locate_glyphs(gl)    
    assert(len(glyph_locs) == 1)
    assert(glyph_locs[0]['level'] == 2)

def test_determine_level_1():
    intr = Parser()
    gl = _prepare(has_ref_at_end)
    gl = intr._Parser__remove_blank_lines(gl)
    glyph_locs = intr._Parser__locate_glyphs(gl)    
    assert(len(glyph_locs) == 1)
    assert(glyph_locs[0]['level'] == 1)

# White space on top
whitespace_top_glyph = """



╵╵╭─╶ ╶╮  ╭─┘╭─╶ 
  │  ╶╮│╭─┘╭─╯  
  │╶╮ ││╰─ │ 
  ╰─┘ │╰───┘
   ╶╮ │
    │         ╷
"""
def test_clear_whitespace_top():
    intr = Parser()
    gl = _prepare(whitespace_top_glyph)
    gl = intr._Parser__remove_blank_lines(gl)
    glyph_locs = intr._Parser__locate_glyphs(gl)    
    assert(len(glyph_locs) == 1)

wide_with_uneven_lines = """
╵╰──╮╰─╮╷╰─╮╭─╮
 ╭─╮│ ─┘│ ─┘│ │
 │ ╰────┘ ╭─┘ │
 ╷   ╭────┘   │
 ╰───┘        ╰────────────────────────────────────────────╷
"""

def test_locate_glyph_with_uneven_lines():
    intr = Parser()
    gl = _prepare(wide_with_uneven_lines)
    gl = intr._Parser__remove_blank_lines(gl)
    glyph_locs = intr._Parser__locate_glyphs(gl)    
    assert(len(glyph_locs) == 1)

glyph_load_five_glyphs_vert = """
 1 ╵╰──╮╰─ ╭──╯ ╶╮
 2    ─┘   └─    │
 3    ╭──────────┘
 5    └────────  ╷

 1 ╵╵     ╭───╮ ╭─
 2    ╴─╮╶╯╶╮ ╷╶╯
 3  ╵╰──┘   │
 5  ╰───────╯
 7   ╭╴     ╭╴
11   │      │
13 │ │    │ │
17 ╰─╯    ╰─╯    ╷

 1 ╵╵╶╮ │ │ │
 2  ╵ │ │╶╯╶╯╭─╶
 3  ╰─╯╶╯    └╴╷

 1 ╵╵ ╭──╮╶──╮╶──╮
 2   ╶╯ ─╯ ╭─╯╶╮ │ ╭─╶ ╭─╶
 3        ╶╯   └─╯╶╯   │
 5                 ╭╴ ╶╯
 7               │ │
11               └─╯     ╷

 1 ╵╵╭─  ╭─╮
 2   │   │ │ 
 3   │ ╷ │ ╷
 5  ╶╯ │ │ │
 7  ╭──╯ │ │
11  └────╯ │╷
"""
def test_level_five_glyphs_vert():
    "To address error that level was passed from previous glyph"
    intr = Parser()
    pr = _prepare(glyph_load_five_glyphs_vert)
    pr = intr._Parser__remove_blank_lines(pr)
    glyph_locs = intr._Parser__locate_glyphs(pr)
    assert len(glyph_locs) == 5
    assert glyph_locs[0]['level'] == 1
    assert glyph_locs[1]['level'] == 2 
    assert glyph_locs[2]['level'] == 2 
    assert glyph_locs[3]['level'] == 2 
    assert glyph_locs[4]['level'] == 2 

glyph_load_five_glyphs_horiz = """
 1 ╵╰──╮╰─ ╭──╯ ╶╮ ╵╵     ╭───╮ ╭─ ╵╵╶╮ │ │ │    ╵╵ ╭──╮╶──╮╶──╮          ╵╵╭─  ╭─╮
 2    ─┘   └─    │    ╴─╮╶╯╶╮ ╷╶╯   ╵ │ │╶╯╶╯╭─╶   ╶╯ ─╯ ╭─╯╶╮ │ ╭─╶ ╭─╶    │   │ │ 
 3    ╭──────────┘  ╵╰──┘   │       ╰─╯╶╯    └╴╷        ╶╯   └─╯╶╯   │      │ ╷ │ ╷
 5    └────────  ╷  ╰───────╯                                    ╭╴ ╶╯     ╶╯ │ │ │
 7                   ╭╴     ╭╴                                 │ │         ╭──╯ │ │
11                   │      │                                  └─╯     ╷   └────╯ │╷
13                 │ │    │ │           
17                 ╰─╯    ╰─╯    ╷
"""
def test_level_five_glyphs_horiz():
    "To address error that level was passed from previous glyph"
    intr = Parser()
    pr = _prepare(glyph_load_five_glyphs_horiz)
    pr = intr._Parser__remove_blank_lines(pr)
    glyph_locs = intr._Parser__locate_glyphs(pr)
    assert len(glyph_locs) == 5
    assert glyph_locs[0]['level'] == 1
    assert glyph_locs[1]['level'] == 2 
    assert glyph_locs[2]['level'] == 2 
    assert glyph_locs[3]['level'] == 2 
    assert glyph_locs[4]['level'] == 2 

empty_col_mid_glyph = """
 1 ╵╵ ╭──╮ ───╮ ───╮
 2   ╶╯ ─╯  ╭─╯ ╶╮ │ ╭─╶ ╭─╶
 3         ╶╯    └─╯╶╯   │
 5                   ╭╴ ╶╯
 7                 │ │
11                 └─╯     ╷
"""
def test_empty_col_mid_glyph():
    "glyph with blank col in middle at bottom of program is rejected"
    lexr = Parser()
    gl = _prepare(empty_col_mid_glyph)
    glyph_locs = lexr._Parser__locate_glyphs(gl)
    assert len(glyph_locs) == 1


empty_col_mid_glyph_bottom = """
 1 ╵╵ ╭──╮ ───╮ ───╮
 2   ╶╯ ─╯  ╭─╯ ╶╮ │ ╭─╶ ╭─╶
 3         ╶╯    └─╯╶╯   │
 5                   ╭╴ ╶╯
 7                 │ │
11                 └─╯     ╷



"""
def test_empty_col_mid_glyph_bottom():
    "glyph with blank col in middle and blank below loads correctly"
    lexr = Parser()
    gl = _prepare(empty_col_mid_glyph_bottom)
    glyph_locs = lexr._Parser__locate_glyphs(gl)
    assert len(glyph_locs) == 1


whitespace_in_middle = """
 ╵╭─╶ ╮  ╭─┘╭─╶ 
  │   │╭─┘╭─╯  
  │╶╮ │╰─ │ 
  ╰─┘ ╰───┘   ╷
  """
def test_another_whitespace():
    "a smaller whitespace in middle"
    lexr = Parser()
    gl = _prepare(whitespace_in_middle)
    glyph_locs = lexr._Parser__locate_glyphs(gl)
    assert len(glyph_locs) == 1

really_big_whitespace = """

╵                    ╵
     ╵                                    ╷




              ╷
    ╷
"""
def test_loading_really_big_whitespace():
    "a smaller whitespace in middle"
    lexr = Parser()
    gl = _prepare(really_big_whitespace)
    glyph_locs = lexr._Parser__locate_glyphs(gl)
    assert len(glyph_locs) == 3
    assert glyph_locs[0]['start'] == {"y": 2, "x": 0}
    assert glyph_locs[0]['end'] == {"y": 9, "x": 4}
    assert glyph_locs[1]['start'] == {"y": 2, "x": 21}
    assert glyph_locs[1]['end'] == {"y": 3, "x": 42}
    assert glyph_locs[2]['start'] == {"y": 3, "x": 5}
    assert glyph_locs[2]['end'] == {"y": 8, "x": 14}

really_big_whitespace_levels = """

╵                  ╵╵╵
    ╵╵                                    ╷




              ╷
    ╷
"""
def test_levels_really_big_whitespace():
    "a smaller whitespace in middle"
    lexr = Parser()
    gl = _prepare(really_big_whitespace_levels)
    glyph_locs = lexr._Parser__locate_glyphs(gl)
    assert len(glyph_locs) == 3
    assert glyph_locs[0]['start'] == {"y": 2, "x": 0}
    assert glyph_locs[0]['end'] == {"y": 9, "x": 4}
    assert glyph_locs[0]['level'] == 1
    assert glyph_locs[1]['start'] == {"y": 2, "x": 21}
    assert glyph_locs[1]['end'] == {"y": 3, "x": 42}
    assert glyph_locs[1]['level'] == 3
    assert glyph_locs[2]['start'] == {"y": 3, "x": 5}
    assert glyph_locs[2]['end'] == {"y": 8, "x": 14}
    assert glyph_locs[2]['level'] == 2
