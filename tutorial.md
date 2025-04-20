# Tutorial: A Fibonacci program

## Table of Contents
- [Value Strands](#value-strands)
- [Using the Print argument to debug](#using-the-print-argument-to-debug)
- [Starting state](#starting-state)
- [Begin a block of code](#begin-a-block-of-code)
- [Splitting code into glyphs](#splitting-code-into-glyphs)
- [Moving data from other cells](#moving-data-from-other-cells) 
- [Actions other than Add/Assignment](#actions-other-than-add-assignment)
- [List Actions](#list-actions)
- [A While loop](#a-while-loop)
- [Final steps and testing](#final-steps-and-testing)

## Value Strands

To get started, we'll need to look at how to write values in Rivulet.
```
1 ╵ ──╮  ╭─╮ ╰──╮ 
2   ╰─╯╰─╯ │╶╮ ─╯  
3         ─╯ ╰─╮
5           ╭──╯
7           ╰─ ╷
```

This excerpt above is a single *glyph*, meaning a block of code that executes together. It is marked with ╵ in the upper left corner and ╷ in the bottom right. It has four *strands*, continuous lines made up of psudographic characters. We determine their reading by checking the *hooks* they begin with (the short curve that begins the strand). 

Here are just the hooks, with dashed lines showing the direction the strand flows away from each:
```
1 ╵          ╰┈
2   ╰┈ ╰┈   ╶╮
3            ┊
```
Three have hooks pointing up, one has a hook pointing to the left. According to the [syntax reference](syntax.md#value-strands), this marks all three as value strands.

Value strands begin on -- their hooks sit on -- the line corresponding to the list they write to. In this case, three begin on line 2, and so write to `list2`. The other begins on line 1 and writes to `list1`.

## Using the Print argument to debug

The value represented by a value strand is written in its movement back and forth in the space of the glyph. To read this glyph, we can save it as a .riv file and run the interpreter with the `-p` (for "print") argument to generate pseudo-code:
```
glyph 0
  ──╮  ╭─╮ ╰──╮
  ╰─╯╰─╯ │╶╮ ─╯
        ─╯ ╰─╮
          ╭──╯
          ╰─   
GLYPH_SUMMARY
level: 1
list2[0] += 0
list2[1] += 0
list1[0] += 0
list2[2] += 0
```
At the top is the glyph number followed by a picture of how the glyph is read by the interpreter. This can be useful if we aren't sure our start and end markers are in the right place (and so the glyph we'd intended is truncated). Then the glyph's *level*, which we'll look at later. This is followed by pseudo-code for the entire glyph. 

First thing to note is that the strands are read left-to-right and only secondarily top-to-bottom. The topmost strand, beginning on line 1, is read third, not first. We can identify it as the only line of code that writes to `list1[0]`. It is read just before the assignment to `list2[2]`, whose strand begins in the same column, but directly below.

Second, all four strands are *zero-strands*, essentially no-ops. 

Each takes a very different path to writing zero. Value in data strands is written with the `─` character. When read right-to-left, it subtracts the value of its line number. When flowing to the right, it adds that number. 
```
1  ──╮
2  ╰─╯
```  
Movement of the strand always begins at the hook. The first strand from our glyph, exerpted above, moves to the right one cell on line 2 `(1 * 2)`, then loops around and moves two cells to the left, subtracting one twice `(-2 * 1)`:
```
(1 * 2) + (-2 * 1) == 0
```

The last strand (excerpted below) moves lower in the glyph, incorporating higher constants:
```
1  
2 ╶╮
3  ╰─╮
5 ╭──╯
7 ╰─

(1 * 3) + (-2 * 5) + (1 * 7)
```

## Starting state

We will assign a different role for each list used by our Fibonacci program:
* `list1`: holds the output of the program
* `list2`: calculates the next Fibonacci number
* `list 3`: tests for and triggers the end of the program

When output is needed in a Rivulet program, it is always accessed through `list1`. An interpreter option prints its contents at program completion.

`list2` will hold the next two values to be added for the succeeding Fibonacci number. These will begin with the first two Fibonacci numbers: `[0, 1]`.

`list3` will be used to test for program completion. We'll store the max Fibonacci number, and subtract the current Fib number from it; when it crosses zero, we'll exit the loop. For this example, we'll set `21` as the max.

Here is the pseudo-code we want for our starting state:
```
list3[0] += 21 // end of program
list2[0] += 0 // first Fib #
list2[1] += 1 // second Fib #
```

Here are two different examples of how to write these as value strands:

```
 1 ╵──╮───╮╭─
 2  ╰─╯╰──╯│ 
 3 ╰─────╮ │ 
 5       ╰─╯ ╷ 
```

```
 1 ╵  ╭─╮  ╭──╮
 2  ╰─╯ │╰─╯  │
 3 ╰─╮ ─╯╭─  ─╯
 5   ╰───╯    ╷
```

In both these examples, we write to `list3` before `list2`. Here is another example that reverses that order:

```
 1 ╵    ─╮     ╭─╮
 2  ╰─╮╰─╯ ╭─╮ │ │
 3    ╰─╮╰─╯ │ │ │
 5     ─╯    ╰─╯ ╰──╷
 ```

> [!NOTE]
Each of the fibonacci programs in the `programs` folder gives an alternate version of the complete tutorial.

## Begin a block of code

The next part of the program is the main loop.

In Rivulet, blocks of code are indicated by levels, marked by the Start Glyph Markers `╵` that begin a glyph in its upper-left corner. Level is analogous to the indentation of a line of code. A single `╵`, the default, means level 1, `╵╵` is 2, etc. 

Level 1 is the starting level of a program. To indicate a glyph is part of the main loop, we'll mark it as level 2.

If there were any adjacent level 3 glyphs, they would be part of their own block but also part of the level 2 activity. Only a move back to level one or end of program marks the block's completion.

This glyph order: `2 2 3 2 3 1` is equivalent to this:
```
{ // start level 2
      // level 2 activity
      { 
            // level 3
      }
      // more level 2 activity
      { 
            // level 3
      }
} // level 2 block ends when we go back to 1
```

## Splitting code into glyphs

It is usually more elegant to split a program into as few glyphs as possible. A level change will force the start of a new glyph, but other factors may do so as well.

In the main loop of our Fibonacci program, we'll use `list2` to store the next two numbers to add to get the next value. It was initialized to the first two Fib numbers `[0, 1]`. Here is the basic flow of how these three cells  interact:

```
list2[2] += list2[0]
list2[2] += list2[1]
list1 pop/appends list2[0]
```
The values of `list2[0]` and `list2[1]` are added to `list2[2]`. Then cell 0 is popped from `list2` and appended to `list1` (the output). What was `list2[1]` is now `list2[0]`, etc. This is the basic loop of the program.

The first two commands write to the same cell: `list2[2]`. The same cell can't be assigned twice in the same glyph, meaning those two lines of code must be divided into successive glyphs.

However, we don't want to do too little in a single glyph, so we look at what else needs to happen in the main loop and how code can be rearranged. 

We'll need `list3` to test whether to exit the main loop, so we'll write the next Fibonacci value to it: `list3[1] = list2[1]`. The first few assignments are to `list2[2]` and don't draw from `list3`, meaning they could fit into more than one glyph. Here is one way to do it:
```
// glyph one
list2[2] += list2[0]
list3[1] = list2[1]

// glyph two
list2[2] += list2[1]
list1 pop/appends list2[0]

// other work in list3 can be part of either glyph one, two, or more, wherever they fit

// test for end of loop can also appear anywhere in the loop

// possibly a level 1 glyph for any final clean-up
```

## Moving data from other cells

Our next few lines of psuedo-code involve moving data across cells or lists. Value Strands do not allow for this, so we will use Reference Strands.
```
list2[2] += list2[0]
```
Reference strands begin with the same hook as value strands (pointing up or left), but end with a ref marker, a small gap followed by a half-size line. The cell they end on is what they reference.

We can represent `list2[0] = list2[0]` with a line like this:

```
1 ╵
2  ╴──╯╷  
```

Each side of the reference strand references a cell. Which cell is determined by how many cells have been written to the left of its marker. The example above is `list2[0] = list2[0]` and not `list2[1] = list2[0]` because cell 0 is first assigned to -- by this strand itself.

It should be noted that, unlike value strands, the path a reference strand takes has no effect. This gives more freedom in how we draw it through the glyph.

To write to `list2[2]`, we need to introduce two zero-strands assigning to cells 0 and 1 that will sit between the beginning and end of our ref strand. Here are two ways of doing this: 

```
1 ╵╵  ──╮──╮
2  ╴─╮╰─╯╰─╯╭─╯
3    ╰──────╯ ╷
```

```
 1 ╵╵ ╭────────────╮
 2  ╵ │ ╰───╮╰───╮╶╯
 3  ╰─╯   ──╯  ──╯ ╷
```

In the first example, the ref strand begins with an upward hook and ends with a horizontal ref marker, while in the second, it begins with a hook facing left and ends with a vertical ref marker.

The first computes zero with `(1 * 2) + (-2 * 1)`, the second with `(3 * 2) + (-2 * 3)`. 

This glyph takes a more circuitous route for the same result:

```
 1 ╵╵  ╭────╮  ╭──────╮
 2   ╴─╯╰──╮│  │╭──╯╰─╯
 3         ││  ││
 5         │╰──╯│
 7         ╰─╮╭─╯
11          ─╯╰─      ╷

Zero-strands:
(2 * 2) + (1 * 7) + (-1 * 11)
(-2 * 2) + (-1 * 7) + (1 * 11)
```

## Actions other than Add-Assignment

The next line of code is not an add-assign but a replace / overwrite:
```
list3[1] = list2[1]
```

If this were an add-assignment, we would simply write this with a ref strand:
```
 1 ╵╵─╮  ╭─╮   
 2    ╰─╮│ ╰─╯ ╵
 3    ╰─╯╰─ ╰──╯╷ 
```
We have a zero-strand for `list3` followed by a zero-strand for `list2` so the last strand will point to element 1 of each list.

To get this to perform `overwrite`, we add an action strand directly below. We can check what value we need to indicate `overwrite` in the [syntax reference](syntax.md#action-strands). That tells us we need a value of zero. 

Action strands are sort of like value strands turned ninety-degrees. They write value in the vertical space rather than horizontal. Here is one way of adding `overwrite`:
```
 1 ╵╵─╮  ╭─╮   
 2    ╰─╮│ ╰─╯ ╵
 3    ╰─╯╰─ ╰──╯
 5          ╭╴
 7          │
11        │ │  
13        ╰─╯  ╷ 
          2 1
```

Since we need zero for `overwrite`, we can use the same `(2 * 1) + (-1 * 2)` pattern from the data zero-strands, but turned ninety degrees. In action strands, the `│` sign adds the value of its column when it flows downward, and subtracts when it moves up.

The value of columns works differently from rows. The values are relative to the place the action strand starts, not from a fixed point and they go up in value up in both directions away from where our action strand begins, to either left or right.

This is equivalent to the action strand above:
```
╭╴
│
│ │  
╰─╯
1 2 
```
This is a syntax error because it uses a single column (a half value):
```
╭╴
│
││  
╰╯
1
```

| :warning: WARNING          |
|:---------------------------|
| The vertical flow of action strands can interfere with data strands. They can also appear as strange appendages to the glyph if they are thoughtlessly added as a final step. Action strands should be considered early in the glyph design process. Only a holistic approach to the glyph, considering all its strands collectively, leads to a visually-balanced result. |

To work the action strand into the glyph visually, we might rework data strands to flow more to the lower half of the glyph, begin the action strand higher, or, in this case, simply extend the action strand further horizontally to complement the flow of the strands sitting above it:
```
 1 ╵╵─╮  ╭─╮   
 2    ╰─╮│ ╰─╯ ╵
 3    ╰─╯╰─ ╰──╯
 5      ╭─╮ ╭╴
 7      │ │ │
11    │ │ ╰─╯
13    ╰─╯      ╷ 
      5 3 2 1

(1 * 1) + (-1 * 2) + (2 * 3) + (-1 * 5) = 0
```
## List Actions

Our "print" step requires actions that apply to lists:
```
list1 pop/appends list2[0]
```
Popping `list2[0]` is considered a cell-based action since it can't be completed without the cell number as a parameter. But appending to a list is list-based since it always refers to the end, not a particular cell. 

We are writing to a list, so this is a list action. However, the parameter is a single cell `list2[0]`, so it is not a list2list action. This is marked by an action strand that ends with a horizontal movement.

To find the correct value of the action strand we need, we check the [syntax reference](syntax.md#action-strands). `pop_and_append` has a value of 3, which we write vertically:
```
 1 ╵╵╰─╮
 2   ╴─╯
 3   ╭─╮
 5     │
 7   ╭─╯
11   │
13   ╰─╷
```

Had we marked this as list2list (ending the action strand with a ref indicator), it would append the entirety of `list2` to `list1`, leaving `list2` empty.

## A While Loop

There is only one type of branching in Rivulet: a conditional rollback. This rollback applies to an entire block (the current level and deeper). 

To write an `if` statement in Rivulet, one must test the outcome of a scenario and then rewind it, rather than the usual model of test-before-branching. Should a test fail, the entire block unwinds, returning the program to its previous state.

A `while` block is a variation of an `if` block that runs repeatedly. A `while` repeats so long as the test succeeds; when it fails, only the last iteration is reverted.

In our Fibonacci program, we're using `list3` for the loop comparison: 
```
list3[1] = list2[1] // get current Fib #
list3[2] = list3[0] // copy our test value
list3[2] -= list3[1] // subtract current Fib # from our test
block_type = whileif [3, 2] <= 0: roll back
```
The second and third lines both write to `list3[2]`, so we need to begin a new glyph there. Here is a basic glyph and its pseudo-code for line 3:

```
 1 ╵╵╭──  ──╮  ╭─╮     
 2   ╰─╮  ╭─╯╭─╯ │     
 3    ╶╯╵╶╯  │  ╶╯     
 5      ╰────╯   ╭╴ 
 7             │ │  
11             ╰─╯ ╷

list3[2] -= list3[1] // subtract current Fib # from our test       
```

The Conditional Rollback is written in two strands called *question strands*. Each begins vertically, with a half-vertical line `╷` followed by a `│`, flowing down. The first line always ends vertically. The second line begins directly below the first's end, beginning with its own half-vert `╷`.

The first line begins in the cell or list to be tested. In our case, we want to test `list3[2]`.
Whether cell or list is determined by how the second line ends: vertical for cell, horizontal for list (the same pattern as the list indicator for action strands).

The test we want to construct is on `list3[2]`. This is the cell where we have subtracted the current Fib number from our target (21). A test is always whether a cell (or cells) is zero or less.

To mark this as a loop (a test for `while`), we need the first question marker to end further to the right than it started. We can move the action marker line down one cell to make space for it to pass through:

```
 1 ╵╵ ╭──  ──╮  ╭─╮
 2    ╰─╮  ╭─╯╭─╯ │
 3     ╶╯╵╶╯  │ ╷╶╯
 5       ╰────╯ │   ╭─╮
 7            ╭─╯ ╭╴│ │
11            │ │ │ │ │
13            │ ╰─╯ │  
17            ╰─────╯ ╷
```
Note that we could not shape it like this because it would then begin with a curve and could be mistaken for a data strand (hooks are often extended with a half-line):
```
 1 ╵╵ ╭──  ──╮  ╭─╮
 2    ╰─╮  ╭─╯╭─╯ │
 3     ╶╯╵╶╯  │ ╷╶╯
 5       ╰────╯ ╰───╮
 7                ╭╴│
11              │ │  
13              ╰─╯ ╷
```
The second question marker need only end vertically, to mark the test as the test of a cell rathern than a list. It can zig and zag through the remaining space, filling out the glyph:

```
 1 ╵╵ ╭──  ──╮  ╭─╮     
 2    ╰─╮  ╭─╯╭─╯ │     
 3     ╶╯╵╶╯  │ ╷╶╯     
 5   ╭─╮ ╰────╯ │   ╭─╮ 
 7   │ ╰────╮ ╭─╯ ╭╴│ │ 
11   ╰────╮ │ │ │ │ │ │ 
13   ╭────╯ │ │ ╰─╯ │ ╷ 
17   ╰────╮ │ ╰─────╯ │ 
19        │ ╰─────────╯
```

## Final Steps and Testing

We still have one more result to print, waiting in list2. We push this to list 1 in the last glyph. This is due to the rolling back of our last iteration.

Once all the glyphs are written, we can re-assess them and move strands around between glyphs to simplify or combine them. The objective is to find harmony in the program: to edit glyphs that don't complement the stylistic consensus emerging in the edit. Through this process, we can continually re-evaluate with `-p`, ensuring each glyph is still set to perform the correct tasks.

Final debugging can be done with the `-v` indicator (for verbose). In this debug mode, the interpreter reports back the state of the stacks after each glyph runs.
