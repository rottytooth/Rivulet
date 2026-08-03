from rivulet.riv_svg_generator import SvgGenerator


Themes = {
    "default": SvgGenerator.Parameters({
        "bg_pattern": SvgGenerator.BgPattern['lines'],
        "bg_color": "#002b36",
        "color_set": ["#93a1a1", "#b58900", "#cb4b16", "#6c71c4", "#268bd2", "#859900"],
        "line_color": "#e1e1e1",
        "line_opacity": 0.05,
        "line_width": 5,
        "stroke_linecap": "round",

        "curve_size": 0.8,
        "cell_width": 70,
        "cell_height": 100,
    }),
    "synth": SvgGenerator.Parameters({
        "bg_pattern": SvgGenerator.BgPattern['blank'], 
        "bg_color": "#2d2725", 
        "color_set": ["#f22c40","#c38418","#df5320","#00ad9c","#7b9726","#407ee7","#6666ea","#c33ff3"],
        "stroke_linecap": "round",
        "glyph_marker": "#407ee7",
    }),
    "frost": SvgGenerator.Parameters({
        "bg_pattern": SvgGenerator.BgPattern['blank'],
        "bg_color": "#eceff4",
        "color_set": ["#8fbcbb","#7abece","#81a1c1","#5e81ac"],
        "stroke_linecap": "butt",
        "glyph_marker": "#5e81ac",
        "stroke_width": 15,

        "curve_size": 0.2,
        "cell_width": 50,
        "cell_height": 100,
    }),
    "solar": SvgGenerator.Parameters({
        "bg_pattern": SvgGenerator.BgPattern['blank'],
        "bg_color": "#FDF6E3",
        "color_set": ["#586E75","#2AA198","#CB4B16","#859900","#268BD2","#6C71C4","#B58900","#93A1A1"],
        "glyph_marker": "#616f77",
        "line_color": "#3e3e3e",
        "stroke_linecap": "square",
        "stroke_width": "23",
        
        "cell_width": 80,
        "cell_height": 100,
    }),
    "monokai": SvgGenerator.Parameters({
        "bg_pattern": SvgGenerator.BgPattern['blank'],
        "bg_color": "#272822",
        "color_set": ["#f92672","#546190","#819aff","#e2e22e","#8c6bc8"],
        "stroke_linecap": "square",
        "glyph_marker": "#75715e",

        "cell_width": 70,
        "cell_height": 100,
    }),
    "pacman": SvgGenerator.Parameters({
        "bg_pattern": SvgGenerator.BgPattern['dots'],
        "bg_color": "#241f32",
        "color_set": ["#45d074","#9cd0da","#a97427","#d045a1","#37507C","#f3e894"],
        "dot_color": "#eee8d5",
        "dot_opacity": .05,
        "glyph_marker": "#d045a1",
        "stroke_linecap": "round",
        "curve_size": 0.5,
        "stroke_width": 25
    }),


    # "test": SvgGenerator.Parameters({
    #     "bg_pattern": SvgGenerator.BgPattern['blank'],
    #     "bg_color": "#86BBD8",
    #     "color_set": ["#33658A","#F6AE2D","#2F4858","#F26419"],
    #     "stroke_linecap": "square",
    #     "stroke_width": 30
    # }),

}
