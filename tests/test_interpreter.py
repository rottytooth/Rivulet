# pylint: skip-file
"""
Test glyph full parsing
"""
import copy
import pytest
from rivulet.riv_interpreter import Interpreter

def test_treeify_1_3_3():
    set_one = [
        {'level': 1},
        {'level': 3},
        {'level': 3},
    ]

    int = Interpreter()
    tree = int.treeify_glyphs(set_one, 1, [])
    assert len(tree) == 2
    assert isinstance(tree[1], list)
    assert len(tree[1]) == 1
    assert isinstance(tree[1][0], list)
    assert len(tree[1][0]) == 2

def test_treeify_1_3_2_2_3_3_1():
    set_one = [
        {'level': 1},
        {'level': 3},
        {'level': 2},
        {'level': 2},
        {'level': 3},
        {'level': 3},
        {'level': 1},
    ]

    int = Interpreter()
    tree = int.treeify_glyphs(set_one, 1, [])
    assert len(tree) == 3
    assert not isinstance(tree[0], list)
    assert isinstance(tree[1], list)
    assert not isinstance(tree[2], list)

    assert isinstance(tree[1][0], list)
    assert not isinstance(tree[1][1], list)
    assert not isinstance(tree[1][2], list)
    assert isinstance(tree[1][3], list)

    assert len(tree[1][0]) == 1
    assert len(tree[1][3]) == 2


two_strand_with_ref_left = """
1 ╵╰──╮
2   ╴─╯╶╮
3       ╰─ ╷
"""

def test_correct_ref_cells_second_strand_left():
    "Glyph with single val and single ref with ref left of val"
    int = Interpreter()
    st = None

    def callback(state):
        nonlocal st
        st = state

    int.interpret_program(str(two_strand_with_ref_left), False, callback)

    # val cell is not yet populated when copied to ref cell
    assert len(st) > 1
    assert st['1'] == [0]
    assert st['2'] == [3]

two_strand_with_ref_right = """
1 ╵   ╭──╯ 
2   ╴─╯╶╮
3       ╰─ ╷
"""

def test_correct_ref_cells_second_strand_right():
    "Glyph with single val and single ref with ref right of val"
    int = Interpreter()
    st = None

    def callback(state):
        nonlocal st
        st = state

    int.interpret_program(str(two_strand_with_ref_right), False, callback)

    # val cell is already populated when copied to ref cell
    assert len(st) > 1
    assert st['1'] == [3]
    assert st['2'] == [3]


one_ref_strand_alone = """
1 ╵ ╶╮ 
2  ╴─╯╷
"""

def test_single_ref_strand_no_vals():
    "Glyph with single val and single ref with ref right of val"
    int = Interpreter()
    st = None

    def callback(state):
        nonlocal st
        st = state

    int.interpret_program(str(one_ref_strand_alone), False, callback)

    # val cell is never populated
    assert len(st) > 0
    assert st['1'] == [0]

mult_copies = """
 1 ╵    ╰─────╮╮╮╮╮
 2  ╵╵╵╵╵╰──╮ │││││
 3  │││││   ╰─│││││
 5  ││││╰─────╯││││
 7  │││╰───────╯│││
11  ││╰─────────╯││
13  │╰───────────╯│
17  ╰─────────────╯ ╷
"""

def test_copy_before_and_after():
    "Glyph that copies previous and post values"
    int = Interpreter()
    st = None

    def callback(state):
        nonlocal st
        st = state

    int.interpret_program(str(mult_copies), False, callback)

    # first cell should be zero, the others 7
    assert len(st) > 1
    assert st['1'] == [0, 7, 7, 7, 7]

pop_append_basic = """
 1 ╵╰── ╰─╮╰──╮
 2   ─────╯   ╰────── ╷

 1 ╵ ╴──╮
 2     ╶╯
 3      ╭╴
 5      │
 7      │ 
11      │ ╷
"""

def test_pop_append_basic():
    "Basic pop/append action"
    int = Interpreter()
    st = []
    iteration = 0

    def callback(state):
        nonlocal st
        nonlocal iteration
        iteration += 1
        st.append(state)

    int.interpret_program(str(pop_append_basic), False, callback)

    # assert len(st) > 1
    # assert len(st[1]) > 1

    # first iteration, data is loaded
    assert st[0]['1'] == [2, -9, 14]

    # second time, the 2 should be moved from list1 to list2
    assert st[1]['1'] == [-9, 14]
    assert st[1]['2'] == [2]
