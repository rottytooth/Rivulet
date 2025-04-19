# Tutorial: A Fibonacci program

## Value Strands

To get started, we'll need to look at how to write values in Rivulet. Here's an example:
```
1 ╵ ──╮  ╭─╮ ╰──╮ 
2   ╰─╯╰─╯ │╶╮ ─╯  
3         ─╯ ╰─╮
5           ╭──╯
7           ╰─ ╷
```

This excerpt is a single *glyph*, meaning a block of code that executes together. It is marked with ╵ in the upper left corner and ╷ in the bottom right. It has four *strands*, continuous lines made up of psudographic characters. We determine their reading by checking the *hooks* they begin with (the short curve that begins the strand). 

Here are just the hooks, with dashed lines showing the direction the strand flows away from each:
```
1 ╵          ╰┈
2   ╰┈ ╰┈   ╶╮
3            ┊
```
Three have hooks pointing up, one has a hook pointing to the left. According to the [synax reference](syntax.md#value-strands), this marks all three as value strands.

Value strands begin (their hooks sit on) the line corresponding to the list they write to. In this case, three begin on line 2, and so write to `list 2`. The other begins on line 1.

## Using the Print argument to Debug

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
At the top is the glyph number followed by a picture of how the glyph is read by the interpreter. This can be useful if we aren't sure our start and end markers are in the right place. Then the glyph's *level*, which we'll look at later. This is followed by pseudo-code for the entire glyph. 

First thing to note is that the strands are read left-to-right and only secondarily top-to-bottom. The strand beginning on line 1 (corresponding to `list1`), is read third, not first. It is read just before the assingment to `list2[2]`, which begins in the same column.

Second, all four strands are *zero-strands*, essentially no-ops. 

Each takes a very different path to writing zero. Value is written with the ─ character. When read right-to-left, it subtracts the value of its line number. When flowing to the right, it adds that number. 
```
1  ──╮
2  ╰─╯
```  
Movement of the strand always begins at the hook. The first strand moves to the right one cell on line 2, then loops around and moves two cells to the left, subtracting one twice.
```
1  
2 ╶╮
3  ╰─╮
5 ╭──╯
7 ╰─
```
The last strand begins with a downward movement (no effect). It turns to the right on line 3, adding the value 3 once. It then subtracts 5 twice, for -7, and completes by adding 7.

## Starting State

The data needs of our Fibonacci program are:
* a list to hold the output of the program
* two variables to hold the values to be added for the next Fibonacci number
* a way to trigger the end of the program

`list1` is always used for output. An option for the interpreter will print list1 at program completion.

We'll store the next values (for the succeeding Fibonacci number) in `list2`, along with other variables we might need in our main loop. These will begin with `[0, 1]`.

`list3` will be devoted to testing for program completion. We'll do this by writing the max Fibonacci number; when the program produces this value or higher, we'll want to stop. For this example, we'll set `21` as the max.

Here is the pseudo-code we want:
```
list3[0] += 21
list2[0] += 0
list2[1] += 1
```

Here are two examples of how to write these as value strands:

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

| :note: NOTE |
|:---------------------------|
| Each of the fibonacci programs in the `programs` folder gives an alternate version of the complete tutorial. |   

## Moving Data Across Lists

## Actions Other Than Add/Assignment

## List and List2List Actions

## Conditional Rollbacks

## A While Loop
