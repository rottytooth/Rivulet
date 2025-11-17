"Tool to create svg files from Rivulet source code"
from enum import Enum
import os
from pathlib import Path
import svg

class SvgGenerator:
    "Tool to create svg files from Rivulet source code"

    BgPattern = Enum('BackPattern', [('blank', 1), ('lines', 2), ('dots', 3)])
    Linecap = Enum('Linecap', [('square', 0), ('butt', 1), ('round', 2)])
    Direction = Enum('Direction', [('up', 1), ('down', 2), ('left', 3), ('right', 4)])

    dir = Direction

    class Parameters:
        "Parameter Set for SvgGenerator"
        cell_width = 80
        cell_height = 100
        bg_pattern = None
        bg_color = "#ffffff"
        # self.bg_color = "#e0d0f4"
        color_set = ["#000000"]
        stroke_width = 20

        curve_size = 1.0

        glyph_marker = "#999999"

        line_color = "#000000"
        line_opacity = 0.35
        line_width = 1

        dot_color = "#000000"
        dot_opacity = 0.1

        stroke_linecap = None


        def __init__(self, dictionary):
            for k, v in dictionary.items():
                setattr(self, k, v)

            if self.stroke_linecap is None:
                self.stroke_linecap = SvgGenerator.Linecap('square')


    def __init__(self, parameters):
        self.p = parameters
        self.initial_x_off = 3 # currently assumes vertical layout
        self.initial_y_off = 1 #self.p.cell_height

    def generate(self, parse_tree, outfile=False):
        "Generate an SVG file from the parse tree"
        if not outfile:
            outfile = "out/output.svg" # this should increment probly

        glyph_widths = []

        elements = []

        lines_skipped = [] # used for drawing lines

        elements.append(svg.Rect(x=0, y=0, width="100%", height="100%", fill=self.p.bg_color))

        widest_glyph = len(max(parse_tree, key = lambda x: len(x["glyph"][0]))["glyph"][0])

        y_off = self.initial_y_off
        for g, glyph in enumerate(parse_tree):
            prev_dir = None
            widths = []
            x_off = self.initial_x_off

            if x_off + widest_glyph > 30:
                x_off = self.initial_x_off
                y_off += 1

            # opening glyph marker
            for i in range(0, glyph["level"]):
                d = []
                d.append(svg.M(x_off * self.p.cell_width, y_off * self.p.cell_height))
                self._add_start_spacing(d, .5, 0)
                d.append(svg.v(self.p.cell_height/2))
                elements.append(
                    svg.Path(
                        d=d,
                        fill="none",
                        stroke=self.p.glyph_marker,
                        stroke_width=self.p.stroke_width,
                        stroke_linecap=self.p.stroke_linecap
                    )
                )
                x_off += 1
            
            # Use raw_tokens to include comments for visualization
            tokens_to_render = glyph.get("raw_tokens", glyph["tokens"])
            for idx, token in enumerate(tokens_to_render):
                d = []
                # move to upper left of starting cell
                d.append(svg.M((token["x"] + x_off) * self.p.cell_width, (token["y"] + y_off) * self.p.cell_height))
                widths.append(token["x"] + x_off)

                prev_dir = self._process_cell(token, d, prev_dir, True, widths)
                for c in token["cells"]:
                    prev_dir = self._process_cell(c, d, prev_dir, False, widths)
                if token["action"] is not None:
                    d.append(svg.M((token["action"]["x"] + x_off) * self.p.cell_width, (token["action"]["y"] + y_off) * self.p.cell_height))

                    prev_dir = self._process_cell(token["action"], d, prev_dir, True, widths)
                    for c in token["action"]["cells"]:
                        prev_dir = self._process_cell(c, d, prev_dir, False, widths)
                if "second" in token and token["second"] is not None:
                    d.append(svg.M((token["second"]["x"] + x_off) * self.p.cell_width, (token["second"]["y"] + y_off) * self.p.cell_height))

                    prev_dir = self._process_cell(token["second"], d, prev_dir, True, widths)
                    for c in token["second"]["cells"]:
                        prev_dir = self._process_cell(c, d, prev_dir, False, widths)
                glyph_widths.append(max(widths))

                elements.append(
                    svg.Path(
                        d=d,
                        fill="none",
                        stroke=self.p.color_set[idx % len(self.p.color_set)],
                        stroke_width=self.p.stroke_width,
                        stroke_linecap=self.p.stroke_linecap
                    )
                )

            # closing glyph marker
            d = []
            closing_marker_x = glyph["end_loc"][1] + 1.0 + self.initial_x_off
            d.append(svg.M(closing_marker_x * self.p.cell_width, (y_off + len(glyph["glyph"]) - 1) * self.p.cell_height))
            self._add_start_spacing(d, .5, .5)
            d.append(svg.v(self.p.cell_height/2))
            elements.append(
                svg.Path(
                    d=d,
                    fill="none",
                    stroke=self.p.glyph_marker,
                    stroke_width=self.p.stroke_width,
                    stroke_linecap=self.p.stroke_linecap
                )
            )
            # Track the closing marker position for width calculation
            glyph_widths.append(int(closing_marker_x) + 1)

            y_off += (len(glyph["glyph"]) + 2)
            lines_skipped.append(y_off - 1)

        if self.p.bg_pattern == SvgGenerator.BgPattern['dots']:
            for y in range(1, y_off):
                for x in range(0, max(glyph_widths) + 4):
                    elements.append(svg.Circle(r=self.p.stroke_width/2, cx=(x + 0.5) * self.p.cell_width, cy=y * self.p.cell_height, fill=self.p.dot_color, fill_opacity=self.p.dot_opacity))

        elif self.p.bg_pattern == SvgGenerator.BgPattern['lines']:
            for y in range(0, y_off):
                if y not in lines_skipped:
                    elements.append(svg.Line(x1=0, y1=self.p.cell_height * y, x2=(max(glyph_widths) + 4.0) * self.p.cell_width, y2=self.p.cell_height * y, stroke=self.p.line_color, stroke_opacity=self.p.line_opacity, stroke_width=self.p.line_width))

        canvas = svg.SVG(
            width=(max(glyph_widths) + 4) * self.p.cell_width,
            height=y_off * self.p.cell_height,
            elements=elements,
            style="background-color:" + self.p.bg_color,
        )

        os.makedirs(os.path.dirname(outfile), exist_ok=True)

        if Path(outfile).is_file():
            outcount = 0
            while Path(outfile).is_file():
                outcount += 1
                outfile = f"out/output{outcount}.svg"

        with open(outfile, "w", encoding="utf-8") as file:
            file.write(str(canvas))

    def _add_start_spacing(self, d, x, y):
        d.append(svg.m(self.p.cell_width * x, self.p.cell_height * y))

    def _add_curve(self, d, x1, y1, x, y, dir1:Direction, dir2:Direction):
        # Draws a quadratic Bézier curve from the current point to (x,y)
        # with control point (x1,y1), each multiplied by half base cell size

        if (self.p.curve_size == 1.0):
            d.append(svg.q(self.p.cell_width * x1 / 2, self.p.cell_height * y1 / 2, self.p.cell_width * x / 2, self.p.cell_height * y / 2))
        else:
            d.append(self._get_short_straight_line(dir1, (1.0 - self.p.curve_size)))

            d.append(svg.q(self.p.cell_width * self.p.curve_size * x1 / 2, self.p.cell_height * self.p.curve_size * y1 / 2, self.p.cell_width * self.p.curve_size * x / 2, self.p.cell_height * self.p.curve_size * y / 2))

            d.append(self._get_short_straight_line(dir2, (1.0 - self.p.curve_size)))

    def _get_short_straight_line(self, d:Direction, size):
        if d == SvgGenerator.dir['up']:
            return svg.v(0-size * self.p.cell_height / 2)
        elif d == SvgGenerator.dir['down']:
            return svg.v(size * self.p.cell_height / 2)
        elif d == SvgGenerator.dir['left']:
            return svg.h(0-size * self.p.cell_width / 2)
        elif d == SvgGenerator.dir['right']:
            return svg.h(size * self.p.cell_width / 2)

    def _process_cell(self, cell, d, prev_dir, start, widths):
        if "dir" in cell:
            dir = cell["dir"]
        else:
            dir = prev_dir

        # Each begins in the upper left of the box. We need to move it to the appropriate entry point

        # rounded corners
        if cell["symbol"] == '╰' or cell["symbol"] == ['╰', '└']:
            if dir == "right":
                if start:
                    self._add_start_spacing(d, .5, 0)
                self._add_curve(d, 0, 1, 1, 1, SvgGenerator.dir['down'], SvgGenerator.dir['right'])
                widths.append(widths[-1] + 1)
            elif dir == "up":
                if start:
                    self._add_start_spacing(d, 1, .5)
                self._add_curve(d, -1, 0, -1, -1, SvgGenerator.dir['left'], SvgGenerator.dir['up'])
        elif cell["symbol"] == '╮' or cell["symbol"] == ['╮', '┐']:
            if dir == "down":
                if start:
                    self._add_start_spacing(d, 0, .5)
                self._add_curve(d, 1, 0, 1, 1, SvgGenerator.dir['right'], SvgGenerator.dir['down'])
            elif dir == "left":
                if start:
                    self._add_start_spacing(d, .5 ,1)
                self._add_curve(d, 0, -1, -1, -1, SvgGenerator.dir['up'], SvgGenerator.dir['left'])
                widths.append(widths[-1] - 1)
        elif cell["symbol"] == '╭' or cell["symbol"] == ['╭','┌']:
            if dir == "down":
                if start:
                    self._add_start_spacing(d, 1, .5)
                self._add_curve(d, -1, 0, -1, 1, SvgGenerator.dir['left'], SvgGenerator.dir['down'])
            elif dir == "right":
                if start:
                    self._add_start_spacing(d, .5, 1)
                self._add_curve(d, 0, -1, 1, -1, SvgGenerator.dir['up'], SvgGenerator.dir['right'])
                widths.append(widths[-1] + 1)
        elif cell["symbol"] == '╯' or cell["symbol"] == ['╯','┘']:
            if dir == "left":
                if start:
                    self._add_start_spacing(d, .5, 0)
                self._add_curve(d, 0, 1, -1, 1, SvgGenerator.dir['down'], SvgGenerator.dir['left'])
                widths.append(widths[-1] - 1)
            elif dir == "up":
                if start:
                    self._add_start_spacing(d, 0, .5)
                self._add_curve(d, 1, 0, 1, -1, SvgGenerator.dir['right'], SvgGenerator.dir['up'])

        # square corners
        elif cell["symbol"] == '┐':
            if dir == "down":
                if start:
                    self._add_start_spacing(d, 0, .5)
                d.append(svg.h(self.p.cell_width / 2))
                d.append(svg.v(self.p.cell_height / 2))
            elif dir == "left":
                if start:
                    self._add_start_spacing(d, .5, 1)
                d.append(svg.v(0-self.p.cell_height / 2))
                d.append(svg.h(0-self.p.cell_width / 2))
                widths.append(widths[-1] - 1)
        elif cell["symbol"] == '└':
            if dir == "right":
                if start:
                    self._add_start_spacing(d, .5, 0)
                d.append(svg.v(self.p.cell_height / 2))
                d.append(svg.h(self.p.cell_width / 2))
                widths.append(widths[-1] + 1)
            elif dir == "up":
                if start:
                    self._add_start_spacing(d, 1, .5)
                d.append(svg.h(0-self.p.cell_width / 2))
                d.append(svg.v(0-self.p.cell_height / 2))
        elif cell["symbol"] == '┌':
            if dir == "down":
                if start:
                    self._add_start_spacing(d, 1, .5)
                d.append(svg.h(0-self.p.cell_width / 2))
                d.append(svg.v(self.p.cell_height / 2))
            elif dir == "right":
                if start:
                    self._add_start_spacing(d, .5, 1)
                d.append(svg.v(0-self.p.cell_height / 2))
                d.append(svg.h(self.p.cell_width / 2))
                widths.append(widths[-1] + 1)
        elif cell["symbol"] == '┘':
            if dir == "left":
                if start:
                    self._add_start_spacing(d, .5, 0)
                d.append(svg.v(self.p.cell_height / 2))
                d.append(svg.h(0-self.p.cell_width / 2))
                widths.append(widths[-1] - 1)
            elif dir == "up":
                if start:
                    self._add_start_spacing(d, 0, .5)
                d.append(svg.h(self.p.cell_width / 2))
                d.append(svg.v(0-self.p.cell_height / 2))


        # straight lines
        elif cell["symbol"] == '─' or cell["symbol"] == ['─']:
            if dir == "right":
                d.append(svg.h(self.p.cell_width))
                widths.append(widths[-1] + 1)
            elif dir == "left":
                d.append(svg.h(0-self.p.cell_width))
                widths.append(widths[-1] - 1)
        elif cell["symbol"] == '│' or cell["symbol"] == ['│']:
            if dir == "down":
                if start:
                    self._add_start_spacing(d, .5, 0)
                d.append(svg.v(self.p.cell_height))
            elif dir == "up":
                if start:
                    self._add_start_spacing(d, .5, 1)
                d.append(svg.v(0-self.p.cell_height))
        elif cell["symbol"] == '╷' or cell["symbol"] == ['╷']:
            if dir == "down":
                self._add_start_spacing(d, 0, .5)
                d.append(svg.v(self.p.cell_height/2))
            elif dir == "up":
                if start:
                    self._add_start_spacing(d, .5, 1)
                d.append(svg.v(0-self.p.cell_height/2))
        elif cell["symbol"] == '╵' or cell["symbol"] == ['╵']:
            if dir == "up":
                self._add_start_spacing(d, 0, -.5)
                d.append(svg.v(0-self.p.cell_height/2))
            elif dir == "down":
                if start:
                    self._add_start_spacing(d, .5, 0)
                d.append(svg.v(self.p.cell_height/2))
        elif cell["symbol"] == '╴' or cell["symbol"] == ['╴']:
            if dir == "left":
                self._add_start_spacing(d, -0.4, 0)
                d.append(svg.h(0-self.p.cell_width * 0.6))
                widths.append(widths[-1] - 1)
            elif dir == "right":
                self._add_start_spacing(d, .5, .5)
                d.append(svg.v(self.p.cell_height/2))
                widths.append(widths[-1] + 1)
        elif cell["symbol"] == '╶' or cell["symbol"] == ['╶']:
            if dir == "right":
                self._add_start_spacing(d, 0.4, 0)
                d.append(svg.h(self.p.cell_width * 0.6))
                widths.append(widths[-1] + 1)
            elif dir == "left":
                self._add_start_spacing(d, .5, .5)
                d.append(svg.v(0-self.p.cell_height/2))
                widths.append(widths[-1] - 1)

        return dir
