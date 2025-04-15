# Tutorial

Let's write a Fibonacci program in Rivulet.

A glyph is an organizational unit of a Rivulet program. In the first glyph, we will introduce the starting state of the program. 

All data in Rivulet is organized in lists. List 1 is used to output our results, so we will skip list 1 and populate lists 2 and 3.

List 2 will hold two values to be added for the next Fibonacci number. These are zero and one.

Writing zero is done often in Rivulet. There are many different ways to write zero. Each of these strands writes zero to the second list:

1 ╵ ──╮  ╭─╮ ╭─╮  
2   ╰─╯╰─╯ │╶╯ │  
3         ─╯   ╰─╮
5             ╭──╯
7             ╰─ ╷

All three of these apply to the second list, as their hooks are on that line.


List 3 will hold 21, the max value, which will trigger an end of the program.



The lists are numbered starting with 1 and then by each successive prime. 
