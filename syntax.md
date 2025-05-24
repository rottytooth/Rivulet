# Syntax Reference

## Table of Contents

- [Lexemes](#lexemes)
- [Glyphs](#glyphs)
- [Lines of code](#lines-of-code)
- [Data Strands](#data-strands)
    - [Value Strands](#value-strands)
    - [Reference Strands](#reference-strands)
- [Action Strands](#action-strands)
    - [List Indicator](#list-indicator)
    - [List 2 List](#list-2-list)
- [Question Strand Sets](#question-strand-sets)

Rivulet's nuanced grammar may seem overwhelming at first but becomes easy to read and write with practice.

## Lexemes

Rivulet commands are written with these signs. Some re-use characters in a way that only context can disambiguate:

| Name      | Signs | Context | Interpretation
| --- | --- | --- | --- |
| Glyph Start and End | ╵ ╷ | Not be adjacent another sign with a vertical reading | Marks the glyph, the smallest block of code in Rivulet 
| Location | ╵ ╷ ╴╶ | Leaves a gap, to punctuate the end of a strand e.g. from left: ──╶ | A reference pointer to a cell
| Continue | ─ │ | Continues the flows in the same direction e.g.  ──── | Depending on the strand type, it can add or subtract the line number of its horizontal or vertical line number, or simply continue the strand
| Corner |╯┘╰└ ╮┐╭┌ | Sharp or curved corners have the same meaning and can be used interchangeably | Turns direction of flow
| Hook | ╯┘╰╴└╴ ╮┐╭╴┌╴| It's a character or characters that turn ninety degrees at the beginning of some strands. If it turns to the right or left, it is extended with a half-length line, the same character used to indicate Location, but flipped to extend the hook and not leave a gap.
| Non-hook Begin Strand | ╷ above a │| Strands with no hook begin with the half-length character to extend it | Marks the beginning of a Question Strand

## Glyphs

Glyphs begin with markers: ╵ in the upper left and end with ╷ at the bottom right. They must not have a vertically-oriented character directly above or below them, or they'll be confused for strands. Any text outside of glyph markers is ignored.

The level of the glyph is marked by how many ╵s appear at the beginning of the glyph. Levels tell where glyphs fall within larger blocks of code.

Glyphs can be arranged vertically or side-by-side. They are read in the order of their starting marker location: top-to-bottom, left-to-right.

In other words, this program:

    1 ╵╰──╮╰─ ╭──╯ ╶╮
    2    ─┘   └─    │
    3    ╭──────────┘
    5    └────────  ╷

    1 ╵╵     ╭───╮ ╭─
    2    ╴─╮╶╯╶╮ ╷╶╯
    3  ╵╰──┘   │
    5  ╰───────╯

is identical to this one:

    1 ╵╰──╮╰─ ╭──╯ ╶╮ ╵╵     ╭───╮ ╭─
    2    ─┘   └─    │    ╴─╮╶╯╶╮ ╷╶╯
    3    ╭──────────┘  ╵╰──┘   │
    5    └────────  ╷  ╰───────╯


## Lines of code

The interpreter refers to code locations in terms of glyph numbers and then line numbers. Line numbers reset to 1 in each glyph. After line 1, they are numbered for each successive prime. These numbers are semantically meaningful for some strands.

Other strand types use horizontal line numbers, counting in primes away from their starting hook. They always begin on line 1 and their neighbors are 2 on each side. They progress through primes, but always in distance from their starting point. Line numbers are every-other-line vertically: this is so vertical lines are not packed too tightly.

Here are examples of such strands:

      ╭─╮ ╭╴  ╭╴ 
      │ │ │   │ │
    │ │ ╰─╯   │ │
    ╰─╯       ╰─╯
	5 3 2 1   1 2


## Data Strands

### Value Strands

A value strand indicates a command that takes a constant value. Value strands (and other data strands), begin with a hook that points up (as in the first two strands below) or to the left (as in the third). All three of the strands below are value strands:

    1 ╵╰──╮╭──╯╶╮
    2    ─┘└─   └─╮
    3               
    5              ╷

Each of these value strands writes to list 1, as their hooks sit on line 1. The first strand writes to the first cell (cell 0), as it appears first on that line, the second writes to the second cell (cell 1), etc.

The first strand moves two spaces (two ── characters) to the right on line 1, adding 1 twice. It then moves one ── to the left on line 2, subtracting two. This leaves zero. This makes the first strand a *zero strand*. The default command applied to a strand is addition assignement, and so zero strands usually invoke no operation.

The second strand is also a zero strand: it makes the same motions in reverse of the first strand, subtracting two and then adding two strand back.

The third strand adds the value two to the third cell or list 1. The importance of the two zero strands is in marking the third strand to write to cell 2 of list 1, rather than cell 0.

### Reference Strands

Reference strands look identical to value strands, only they end with a Location Marker, a small gap that punctuates the end of the strand. It appears in the two top strands here:

    1 ╵╰──╮  ╭──╯
    2   ╴─┘╶╮└─╶ 
    3       └─╮        
    5            ╷

The movement of Reference Strands back and forth through the glyph has no effect on what they reference; only where they end.

The first strand above is no longer a Zero Strand, but a reference to the first cell (cell 0) of List 2. The second strand beginning on line 1 refers to the second cell (cell 1) of List 2. This is because between those two strands is a strand writing to cell 0 of List 2. If we wanted both of the top strands to read from cell 0 of List 2, we would move its end to before that assignment (here using the vertical version of the Location Marker):

    1 ╵╰──╮╭────╯
    2   ╴─┘╷╶╮ 
    3        └─╮        
    5            ╷

## Action Strands

The default command is addition assignment ( += ). To choose another commands, we create an Action Strand to apply to an existing data strand.

| :note: Contibutors: |
|:---------------------------|
| The list of actions is still very sparse. This is intentional, to see how people use the language. If you find commands are missing that you need, please create issues for them. |

Action Strands have hooks that point down or to the right. They sit directly below the data strand they apply to. If two data strands' hooks are aligned vertically, the top action strand applies to the top data strand, the second to the second, etc.

Where a data strand's value is determined by movements to the left and right, action strands determine value through vertical movement. Their line numbers are independent of the other strands in the glyph, each beginning with line 1 as the column where they begin. Their neighbors to the left and right are line 2, followed by 3 and 5. 

EXAMPLE: This command that raises the values of list 1, cells 0 and 1, each to their fourth power:

     1 ╵╰─╮ ╰─╮
     2    │   │ 
     3  ╭╴└─╭╴└─
     5  │   │ 
	 7  │   │
    11  ╰─╮ ╰─╮
    13    │   │ ╷
        1 2 1 2

The action strands each have a value of 4, which corresponds to exponentiation_assignment, under data strands of value 4. Here is the (INCOMPLETE) command list, showing which values assign to what command:

| Value  | Command | Interpretation |
| --- | --- | --- |
| default | addition_assignment | add to location, set to zero by default |
| 0 | overwrite | assignment, overwriting existing value |
| 1 | insert | inserts value after indicated cell |
| -1 | subtraction assignment | |
| 2 | multiplication assignment | |
| -2 | division assignment | |
| 3 | pop / pop_and_append | Removes from source list. With a list indicator, it pops from the assignee  |
| -3 | mod assignment | modulus of cell value against supplied argument |
| 4 | exponentiation assignment | raise to power of supplied argument" |
| -4 | root assignment | take root at power of supplied argument |


:WARNING: It is every-other-line that increments between the primes, as the vertical length for a block-drawing char is longer than their horizontal length. This sounds confusing but is usually clear visually.

Here is an example of two action strands and their numbering:

      ╭─╮ ╭╴  ╭╴ 
      │ │ │   │ │
    │ │ ╰─╯   │ │
    ╰─╯       ╰─╯
    5 3 2 1   1 2

The first strand has a value of: `(1 * 1) + (-1 * 2) + (2 * 3) + (-1 * 5) == 0`, overwrite. The second strand has a value of `(2 * 1) + (-2 * 2) == -2`, division assignment.

### List indicator

Action strands can also mark that a command applies not to a single cell (as is the default) but to an entire list. It is marked by the last character of an action strand. Ending on a horizontal movement `─` in either direction. 

*Example:*

```
 1 ╵  ╶╮  ╶╮  ╶╮  ╶╮  ╶╮       
 2     ╰── ╰── ╰── ╰── │
 3  ╭── ╭──────────────╯
 5  │ ╭─╯              ╭╴
 7  │ ╷    ╶╮       ─╮ │
11  │   ╭───╯        │ │
13  │   ╷ ╶╮         ╰─╯
17  ╰──────╯            ╷
```
The first value assigned is a 4 to `list1`. This will then be assigned to the next three:
```
 1    ╶╮  ╶╮  ╶╮  ╶╮         
 2     ╰── ╰── ╰── ╰──
```
Just after the first 4 is assigned, `list3` is assigned the value -96 ((-6 * 17) + (2 * 3)) to `list13`. That value is soon after copied to `list7`:

```
 1       
 2    
 3  ╭──  
 5  │ 
 7  │      ╶╮
11  │   ╭───╯
13  │   ╷ ╶╮
17  ╰──────╯
```
The two remaining strands are a ref and action strand combination:
```
 1                    ╶╮       
 2                     │
 3      ╭──────────────╯
 5    ╭─╯              ╭╴
 7    ╷             ─╮ │
11                   │ │
13                   ╰─╯
17                      
```
The horizontal line at the end of the action strand (on line 7) indicates that it applies to the entire list (`list1`). This includes every cell of `list1` that already has a value. In this case, it is currently `[4, 4, 4, 4]`, so all of those will be affected by this action. Had the list contained zeros, those would be manipulated as well.

However, since there is no `list2list` indicator, it's only a single value that's the source (input) of this action. And since it's a ref strand, not a val strand, on top, it refers to a single value: in this case, the -96 from the first cell of `list7`.

This action is an overwrite, so the resulting values in `list` are `[-96, -96, -96, -96]`.

Most actions are similar to the example in that it's the same action as a cell-to-cell action, only applied to every cell of a list, like a map() lambda. Some actions, however, have alternate readings if applied to a list. The number 1 for instance:

```
Cell reading:
    "name": "insert",
    "note": "inserts value after indicated cell (applied immediately)"

List reading:
    "name": "append",
    "note": "appends value to list"
```
The List indicator, in this case, turns an action that requires an individual cell as referrent (showing where a new value should be inserted), into one that considers the list as a whole (append).

The list indicator does not change the strand's precedence. So it is read in the same order, from left-to-right, alongside ordinary ref and val strands. Which cell in the list it points to does not affect its reading. This sometimes gives flexibility in where it is drawn, but in many cases, including the example above, it is constrained both by the cell it refers to and when in the glyph it needs to be executed.

### List 2 List

This variation of the List Action Strand applies each cell of one list to each of the other. A simple assignment would look like this:
```
listX[0] = listY[0]
listX[1] = listY[1]
listX[2] = listY[2]
...
listX.append(listY[36])
(for however many elements listY is longer than listX)
```
This can apply to any type of Action Strand, not just simple assignments. These take the list version of the action.

*Example:*
```
 1 ╵                    ╶╮
 2  ╵╰──╮                │
 3  │   ╰────            │
 5  │  ╭────╮╭────╮╭───╮ │
 7  │  ╷╶╮╵╶╯╷╶╮╵╶╯╷╶╮╶╯ ╷
11  │╭───╯╰────╯╰────╯   ╭╴
13  │╷ ╶╮              ╵ │
17  ╰───╯              │ │ 
19                     ╰─╯ ╷
```

The ref strand to the far right and its list2list action sitting below copy the entire contents of `list7` to `list1`.

## Question Strand Sets

Question Strands appear in pairs, one above the other.

Together, they pose a question about the state of the data. Should it be found wanting, the glyph and its siblings (those at the same level) are rolled back. If in a loop, only the most recent iteration is undone. This is the only way to exit a loop.

The top question strand begins with a vertical line. It ends either to the left or right of where it began (above or below has no semantic meaning).

The bottom question strand begins directly above its partner. It too ends either to the left or right of where it began, and it ends with a vertical piece (indicating the question applies only to a single cell) or a horizontal piece (indicating the entire list is to be questioned, the answer an accumulation of its answer).

Question strands, read only by their beginning vs end, can move back and forth through the glyph, filling in blank spaces. They are often decorative, gap-filling lines.

Question lines always fail if an item is less than or equal to zero.

| Top Line | Bottom Line | Use | Checks
| --- | --- | --- | --- |
| Left | Horizontal | If | List (all items)
| Left | Vertical | If | Cell
| Right | Horizontal | While | List
| Right | Vertical | While | Cell

(any) vs (all) are equivalent if testing only a single cell
