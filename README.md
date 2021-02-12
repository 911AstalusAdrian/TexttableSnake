This is a console-based version of the beloved [game of Snake](https://www.google.com/search?q=play+snake) using Python 3 
and object-driven layered architecture. The program works in the following way:
1. At program start, the game area is displayed.
   - The game area is a `DIM x DIM` matrix of squares that contains the snake, and a number of `apple_count` apples. 
     The snake always starts with a head segment (`*`) and two body segments (`+`) and is placed in the middle of the board. 
     Each apple is represented using a dot (`.`). 
     Apples are placed randomly, so that two apples cannot be adjacent on the row or column, and cannot overlap the snake's starting position.
   - The values of `DIM` (odd natural number) and `apple_count` (natural number) are read from a settings file and are presumed correct.
```
+---+---+---+---+---+---+---+
|   | . |   |   |   | . |   |
+---+---+---+---+---+---+---+
|   |   |   | . |   |   |   |
+---+---+---+---+---+---+---+
| . |   | . | * |   |   |   |
+---+---+---+---+---+---+---+
|   |   |   | + |   |   |   |
+---+---+---+---+---+---+---+
|   |   |   | + |   |   | . |
+---+---+---+---+---+---+---+
| . |   |   | . |   | . |   |
+---+---+---+---+---+---+---+
|   | . |   |   |   |   |   |
+---+---+---+---+---+---+---+
Example starting position, DIM=7, apple_count=10. The snake is pointing up
```

2. The user can move the snake using the following commands:
    - `move [n]`. This moves the snake `n` squares, in the direction it is currently facing.
      `move` with no parameters moves the snake by `1` square.
    - `up | right | down | left` changes the snake's direction accordingly. 
      Trying to change the snake's direction by 180 degrees will result in an error message (a snake going up cannot immediately go down). 
      Entering the direction the snake is currently heading for does nothing.
    - When the snake eats an apple, its tail grows by `1 square`. 
      A new apple is immediately added to the game area, following the rules at `Point 1`.

3. The game ends when the snake hits the edge of the game area, or one of its own segments.
