# pylint: skip-file
"""
Test SVG generator
"""
import os
import tempfile
import pytest
from rivulet.riv_parser import Parser
from rivulet.riv_svg_generator import SvgGenerator
from rivulet.riv_themes import Themes

comment_thread_program = """
╵╭─ ┌── ────╮
 │  │ ┌─╰─╮ ╰──╮  
 │ ╶╯ │   └─── │
 ╰──╮╶╯ ╭──────╯        
    ╰───╯       ╷
"""

def test_comment_thread_in_svg():
    """Test that comment threads are rendered in SVG output"""
    parser = Parser()
    parse_tree = parser.parse_program(comment_thread_program)
    
    # Create SVG generator with default theme
    svg_params = Themes["monokai"]
    generator = SvgGenerator(svg_params)
    
    # Generate SVG to a temporary file
    temp_file = tempfile.mktemp(suffix='.svg')
    
    try:
        generator.generate(parse_tree, outfile=temp_file)
        
        # Read the generated SVG
        with open(temp_file, 'r') as f:
            svg_content = f.read()
        
        # Verify SVG was generated
        assert svg_content is not None
        assert len(svg_content) > 0
        
        # Verify it's valid SVG structure
        assert '<svg' in svg_content
        assert '</svg>' in svg_content
        
        # Verify it contains path elements (the strands)
        assert '<path' in svg_content
        
        # The comment thread should be rendered as paths
        # We expect: 3 data strands + 1 comment thread = 4 strands
        # Plus 2 glyph markers (start and end) = 6 total paths
        path_count = svg_content.count('<path')
        assert path_count == 6, f"Expected 6 paths (4 strands + 2 markers), got {path_count}"
        
    finally:
        # Clean up temp file
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_svg_generator_basic():
    """Test basic SVG generation with a simple program"""
    simple_program = """
╵╰─╮
   │╷
"""
    
    parser = Parser()
    parse_tree = parser.parse_program(simple_program)
    
    svg_params = Themes["monokai"]
    generator = SvgGenerator(svg_params)
    
    temp_file = tempfile.mktemp(suffix='.svg')
    
    try:
        generator.generate(parse_tree, outfile=temp_file)
        
        with open(temp_file, 'r') as f:
            svg_content = f.read()
        
        assert '<svg' in svg_content
        assert '</svg>' in svg_content
        assert svg_content.count('<path') >= 1
        
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_svg_with_multiple_strands():
    """Test SVG generation with multiple strands"""
    multi_strand_program = """
╵╰──╮╰─╮
    │ ─┘
    ──┘ ╷
"""
    
    parser = Parser()
    parse_tree = parser.parse_program(multi_strand_program)
    
    svg_params = Themes["monokai"]
    generator = SvgGenerator(svg_params)
    
    temp_file = tempfile.mktemp(suffix='.svg')
    
    try:
        generator.generate(parse_tree, outfile=temp_file)
        
        with open(temp_file, 'r') as f:
            svg_content = f.read()
        
        # Should have multiple paths for multiple strands
        path_count = svg_content.count('<path')
        assert path_count >= 2, "Should have multiple path elements for multiple strands"
        
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
