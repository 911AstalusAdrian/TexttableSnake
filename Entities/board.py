import random

from texttable import Texttable


class BoardError(Exception):
    class ServiceError(Exception):
        def __init__(self, message=''):
            self._message = message

        def __str__(self):
            return self._message



class Board:
    def __init__(self, dimension, apples):
        self._rows = dimension
        self._columns = dimension
        self._apples = apples
        self._direction = [-1, 0]
        self._board = [[0 for col in range(self._columns)] for row in range(self._rows)]
        self.set_snake()
        self.set_initial_apples()

    def get_direction(self):
        return self._direction

    def set_direction(self, new_direction):
        self._direction = new_direction

    def get_snake_head(self):
        """
        Function to determine the coodinates of the snake's head on the board
        :return: tuple of the coordinates
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
