# pylint: skip-file
"""
Test appropriate responses for Syntax Errors
"""
import copy
import pytest
from rivulet.riv_parser import Parser
from rivulet.riv_exceptions import InternalError, RivuletSyntaxError

no_glyph = """
╰─╮
  │
  ╰─╮
   ─┘
"""

def test_missing_glyph_markers():
    lexr = Parser()
    gl = copy.deepcopy(no_glyph)
    with pytest.raises(RivuletSyntaxError) as err:
        lexr.parse_program(gl)       

    assert "No glyph" in str(err.value)

hooks_both_ends_glyph = """
╵╰─╮
   │
   ╰─╮
   ╰─┘╷
"""

def test_hooks_both_ends():
    lexr = Parser()
    gl = copy.deepcopy(hooks_both_ends_glyph)
    with pytest.raises(RivuletSyntaxError) as err:
        lexr.parse_program(gl)

    assert "char 3, 2" in str(err.value)

bad_start = """
╵
╰─╮
  │
  ╰─╮
   ─┘╷
"""

def test_bad_start():
    "where a Glyph Start looks ambiguously like a ref marker"
    lexr = Parser()
    gl = copy.deepcopy(bad_start)
    with pytest.raises(RivuletSyntaxError) as err:
        lexr.parse_program(gl)

    assert "corresponding Start" in str(err.value)
    assert "5, 4" in str(err.value)

orphan_question_strand = """
╵╶╮ ╷ 
  ╰─╯╷
"""

def test_orphan_question_strand():
    "where a Glyph Start looks ambiguously like a ref marker"
    lexr = Parser()
    gl = copy.deepcopy(orphan_question_strand)
    with pytest.raises(RivuletSyntaxError) as err:
        lexr.parse_program(gl)

    assert "without a second" in str(err.value)
    assert "glyph 0" in str(err.value)
    assert "4, 0" in str(err.value)

double_hooked = """
 1  ╶╮
 2   │
 3 ╭─╯╷
"""
def test_error_for_double_hooked():
    "starts and ends with a hook"
    lexr = Parser()
    gl = copy.deepcopy(orphan_question_strand)
    with pytest.raises(RivuletSyntaxError) as err:
        lexr.parse_program(gl)
