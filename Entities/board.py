import random
from texttable import Texttable


# Basic error class for the Board entity
class BoardError(Exception):
    class ServiceError(Exception):
        def __init__(self, message=''):
            self._message = message

        def __str__(self):
            return self._message


'''
The 'Board' class is a DIM x DIM matrix initialised with 0
On this matrix, the apples are represented by values of -1, and the snake is represented by natural numbers.
To be more precise, the snake's head has the value 1, and the rest of the body has the values 2, 3, and so on.

Example:
    
    This is our initial state of the game:
    +---+---+---+---+---+---+---+
    | . |   |   |   |   |   | . |
    +---+---+---+---+---+---+---+
    |   | . |   |   |   | . |   |
    +---+---+---+---+---+---+---+
    | . |   | . | + |   |   |   |
    +---+---+---+---+---+---+---+
    |   | . |   | * |   |   |   |
    +---+---+---+---+---+---+---+
    |   |   |   | * | . |   | . |
    +---+---+---+---+---+---+---+
    |   | . |   |   |   |   |   |
    +---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+
    
    But, actually this is what the actual values of our matrix are:
    +---+---+---+---+---+---+---+
    |-1 | 0 | 0 | 0 | 0 | 0 |-1 |
    +---+---+---+---+---+---+---+
    | 0 |-1 | 0 | 0 | 0 |-1 | 0 |
    +---+---+---+---+---+---+---+
    |-1 | 0 |-1 | 1 | 0 | 0 | 0 |
    +---+---+---+---+---+---+---+
    | 0 |-1 | 0 | 2 | 0 | 0 | 0 |
    +---+---+---+---+---+---+---+
    | 0 | 0 | 0 | 3 |-1 | 0 |-1 |
    +---+---+---+---+---+---+---+
    | 0 |-1 | 0 | 0 | 0 | 0 | 0 |
    +---+---+---+---+---+---+---+
    | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
    +---+---+---+---+---+---+---+
    
    
The action of moving the snake is quite simple:
    - we change the coordinate of the snake's head based on the direction it's heading
    - we 'drag' the rest of the body after the head, taking into consideration whether the head 'ate' an apple or not
        - if it didn't eat an apple, the 'tail' of the snake is removed (because the snake doesn't grow)
        - if it actually ate an apple, the 'tail' is kept
        
Example - the snake from above moving one cell up:

    +---+---+---+---+---+---+---+   - initial state of the snake
    |-1 | 0 | 0 | 0 | 0 | 0 |-1 |
    +---+---+---+---+---+---+---+
    | 0 |-1 | 0 | 0 | 0 |-1 | 0 |
    +---+---+---+---+---+---+---+
    |-1 | 0 |-1 | 1 | 0 | 0 | 0 |
    +---+---+---+---+---+---+---+
    | 0 |-1 | 0 | 2 | 0 | 0 | 0 |
    +---+---+---+---+---+---+---+
    | 0 | 0 | 0 | 3 |-1 | 0 |-1 |
    +---+---+---+---+---+---+---+
    | 0 |-1 | 0 | 0 | 0 | 0 | 0 |
    +---+---+---+---+---+---+---+
    | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
    +---+---+---+---+---+---+---+
    
    +---+---+---+---+---+---+---+   - the head is moved one cell 'up', hence the '1' value from the second row
    |-1 | 0 | 0 | 0 | 0 | 0 |-1 |  
    +---+---+---+---+---+---+---+ 
    | 0 |-1 | 0 | 1 | 0 |-1 | 0 |
    +---+---+---+---+---+---+---+
    |-1 | 0 |-1 | 1 | 0 | 0 | 0 |
    +---+---+---+---+---+---+---+
    | 0 |-1 | 0 | 2 | 0 | 0 | 0 |
    +---+---+---+---+---+---+---+
    | 0 | 0 | 0 | 3 |-1 | 0 |-1 |
    +---+---+---+---+---+---+---+
    | 0 |-1 | 0 | 0 | 0 | 0 | 0 |
    +---+---+---+---+---+---+---+
    | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
    +---+---+---+---+---+---+---+
    
    +---+---+---+---+---+---+---+   - after the new head is placed correctly, the rest of the body is 'dragged' by 
    |-1 | 0 | 0 | 0 | 0 | 0 |-1 |     increasing the values bigger than 0 by 1 (because the board is 0, the apples are -1,
    +---+---+---+---+---+---+---+     the only values bigger than 0 are the snake's body
    | 0 |-1 | 0 | 1 | 0 |-1 | 0 |
    +---+---+---+---+---+---+---+
    |-1 | 0 |-1 | 2 | 0 | 0 | 0 |
    +---+---+---+---+---+---+---+
    | 0 |-1 | 0 | 3 | 0 | 0 | 0 |
    +---+---+---+---+---+---+---+
    | 0 | 0 | 0 | 4 |-1 | 0 |-1 |
    +---+---+---+---+---+---+---+
    | 0 |-1 | 0 | 0 | 0 | 0 | 0 |
    +---+---+---+---+---+---+---+
    | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
    +---+---+---+---+---+---+---+
    
    +---+---+---+---+---+---+---+   - knowing that the snake's length doesn't change, because it didn't eat an apple,
    |-1 | 0 | 0 | 0 | 0 | 0 |-1 |     the values from the board bigger than the snake's length (in this case, the 4 from
    +---+---+---+---+---+---+---+     the 5th row) are reset to 0, meaning that cell is now empty.
    | 0 |-1 | 0 | 1 | 0 |-1 | 0 |
    +---+---+---+---+---+---+---+   - in the case when the snake's head went on an apple, the length of the snake is increased
    |-1 | 0 |-1 | 2 | 0 | 0 | 0 |     by one, therefore no cell resetting is happening. Moreover, a new random apple is placed
    +---+---+---+---+---+---+---+     on the board.
    | 0 |-1 | 0 | 3 | 0 | 0 | 0 |
    +---+---+---+---+---+---+---+
    | 0 | 0 | 0 | 0 |-1 | 0 |-1 |
    +---+---+---+---+---+---+---+
    | 0 |-1 | 0 | 0 | 0 | 0 | 0 |
    +---+---+---+---+---+---+---+
    | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
    +---+---+---+---+---+---+---+

        
Furthermore, the snake's initial direction of movement is recorded in the 'self._direction' variable
These directions lists of the coordinates X and Y depending on which the snake moves
    - up: [-1, 0] meaning that the snake moves one row 'up' on the same column (the head's X coordinate is decreased by 1)
    - down: [1, 0] meaning that the snake moves one row 'down' on the same column (the head's X coordinate is increased by 1)
    - left: [0, -1] meaning that the snake moves on the same row, but one column to the left (the head's Y coordinate is decreased by 1)
    - right: [0, 1] meaning that the snake moves on the same row, but one column to the right (the head's Y coordinate is increased by 1)
'''
class Board:
    def __init__(self, dimension, apples):
        self._rows = dimension
        self._columns = dimension
        self._apples = apples
        self._direction = [-1, 0]   # the initial direction of the snake, 'up'
        self._board = [[0 for col in range(self._columns)] for row in range(self._rows)] #initializing the matrix with 0 values
        self.set_snake()    # calling the function which places our snake on the board
        self.set_initial_apples()   # calling the function that initialises our apples at the start of the game

    def get_direction(self):
        return self._direction

    # This function is used when the snake's direction changes, setting the new direction
    def set_direction(self, new_direction):
        self._direction = new_direction

    def get_snake_head(self):
        """
        Function to determine the coordinates of the snake's head on the board
        :return: tuple of the coordinates
        The snake's head is represented by the value '1' from the board
        """
        for row in range(self._rows):
            for column in range(self._columns):
                if self._board[row][column] == 1:
                    return row, column

    def long_snake(self):
        """
        Function to determine the length of the snake
        :return: Snake's length
        """
        # The snake-s length is equal to the biggest value present on the board
        # Example: 4 | 3 | 2 | 1 | 0 snake has length 4
        snake_length = 0
        for row in range(self._rows):
            for column in range(self._columns):
                if self._board[row][column] > snake_length:
                    snake_length = self._board[row][column]
        return snake_length

    def check_bounds(self, head_x, head_y):
        """
        Function to check if the snake's head is within the bounds of the board
        :param head_x: x-coordinate of the head
        :param head_y: y-coordinate of the head
        :return: True if it is okay, False otherwise
        """
        if head_x < 0 or head_x > self._rows - 1:
            return False
        elif head_y < 0 or head_y > self._columns - 1:
            return False
        elif self._board[head_x][head_y] > 1:
            return False
        else:
            return True

    def move(self, initial_x, initial_y, direction):
        """
        Function used to set the way in which the snake moves
        :param initial_x: initial x-coordinate of the snake's head
        :param initial_y: initial y-coordinate of the snake's head
        :param direction: a list with the coordinates which signal the direction in which the snake moves
        :return: -
        """
        # direction list is of type [x-direction, y-direction]
        x_axis = direction[0]
        y_axis = direction[1]
        # We 'calculate' the position of the snake's 'new' head
        new_head_x = initial_x + x_axis
        new_head_y = initial_y + y_axis
        # Error handling when the snake's 'new' head hits the edge
        if self.check_bounds(new_head_x, new_head_y) is False:
            raise BoardError("Snake game ended! It hit an edge or itself")
        if self._board[new_head_x][new_head_y] == -1:
            self.move_snake_apple(new_head_x, new_head_y)
            self.place_new_apple()
        else:
            length_of_snake = self.long_snake()
            self.move_snake_simple(new_head_x, new_head_y, length_of_snake)

    def move_snake_apple(self, head_x, head_y):
        """
        Function used to move the snake in the case it has met an apple
        :param head_x: x-coordinate of the head
        :param head_y: y-coordinate of the head
        :return: -
        """
        # In this case, the length of the snake increases, so we don't need to remove the 'extra' body part
        self._board[head_x][head_y] = 1
        for row in range(self._rows):
            for column in range(self._columns):
                if self._board[row][column] >= 1 and (row != head_x or column != head_y):
                    self._board[row][column] += 1

    def move_snake_simple(self, head_x, head_y, snake_length):
        """
        Function to move the snake in the case it hasn't met an apple an apple
        :param head_x: x-coordinate of the head
        :param head_y: y-coordinate of the head
        :param snake_length: the length of the snake
        :return: -
        """
        # We firstly place the snake's head
        self._board[head_x][head_y] = 1
        """
        # We 'update' the body of the snake
        Example: 3 | 2 | 1 | 0  --> 0 | 3 | 2 | 1
        """
        for row in range(self._rows):
            for column in range(self._columns):
                if self._board[row][column] >= 1 and (row != head_x or column != head_y):
                    self._board[row][column] += 1

        # After updating, we'll have an extra part of the snake (of value len+1), which needs to be removed
        for row in range(self._rows):
            for column in range(self._columns):
                if self._board[row][column] == snake_length + 1:
                    self._board[row][column] = 0

    def place_new_apple(self):
        """
        Function used to set a new apple on the board after one's been eaten by the snake
        Works the same way as the initial setting, but placing only one apple
        :return:
        """
        # We get all the possible coordinates on which an apple can be placed on the board
        field = []
        for row in range(self._rows):
            for column in range(self._columns):
                if self._board[row][column] == 0: # if a cell is 0, it means it's empty (this way we can avoid overlapping the snake)
                    field.append((row, column))
        apples = 1
        while apples > 0:
            # We get a random location, check if it has adjacent apples and place an apple if we can
            location = random.choice(field)
            row = location[0]
            column = location[1]
            field.remove(location)
            if self.adjacent_apples(row, column) is False:
                self._board[row][column] = -1  # -1 on the board means it's an apple
                apples -= 1

    def set_snake(self):
        """
        Putting the snake in the middle of the board
        1 - represents the head of the snake
        2, 3, ... - represent the body parts of the snake and implicitly its length
        :return:
        """
        middle_row = self._rows // 2
        middle_col = self._columns // 2
        self._board[middle_row][middle_col] = 2  # 2, 3, .. means the body of the snake
        self._board[middle_row + 1][middle_col] = 3
        self._board[middle_row - 1][middle_col] = 1  # 1 means the head of the snake

    def set_initial_apples(self):
        """
        Function used to set the initial apples
        :return:
        """
        # We get all the possible coordinates on which an apple can be placed on the board
        field = []
        for row in range(self._rows):
            for column in range(self._columns):
                if self._board[row][column] == 0:  # if a cell is 0, it means it's empty (this way we can avoid overlapping the snake)
                    field.append((row, column))

        apples = self._apples
        while apples > 0:
            # We get a random location, check if it has adjacent apples and place an apple if we can
            location = random.choice(field)
            row = location[0]
            column = location[1]
            field.remove(location)
            if self.adjacent_apples(row, column) is False:
                self._board[row][column] = -1  # -1 on the board means it's an apple
                apples -= 1

    def adjacent_apples(self, row, column):
        """
        Function to check if there are adjacent apples to the current place on the board
        :param row: the row of the place we check
        :param column: the column of the respective place
        :return: True if there exist adjacent apples, False otherwise
        """
        if 0 <= column - 1 <= self._columns - 1:
            if self._board[row][column - 1] == -1:
                return True
        if 0 <= column + 1 <= self._columns - 1:
            if self._board[row][column + 1] == -1:
                return True
        if 0 <= row - 1 <= self._rows - 1:
            if self._board[row - 1][column] == -1:
                return True
        if 0 <= row + 1 <= self._rows - 1:
            if self._board[row + 1][column] == -1:
                return True
        return False

    def __str__(self):
        t = Texttable()
        # Add each table row
        for row in range(0, self._rows):
            data = []
            for val in self._board[row][:]:
                if val == 0:
                    data.append(' ')
                elif val == -1:
                    data.append('.')
                elif val == 1:
                    data.append('+')
                elif val > 1:
                    data.append("*")
            t.add_row(data)
        return t.draw()
