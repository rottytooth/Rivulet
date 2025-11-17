from rivulet.riv_parser import Parser

comment_thread_program = """
╵╭─ ┌── ────╮
 │  │ ┌─╰─╮ ╰──╮  
 │ ╶╯ │   └─── │
 ╰──╮╶╯ ╭──────╯        
    ╰───╯       ╷
"""

parser = Parser()
tree = parser.parse_program(comment_thread_program)

glyph = tree[0]
print(f"Tokens (filtered): {len(glyph['tokens'])}")
print(f"Raw tokens (with comments): {len(glyph.get('raw_tokens', glyph['tokens']))}")
print()
print("Raw tokens breakdown:")
for i, t in enumerate(glyph.get('raw_tokens', glyph['tokens'])):
    print(f"  {i}: type={t.get('type')}, name={t.get('name')}, x={t.get('x')}, y={t.get('y')}")
