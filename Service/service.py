
# Basic error class for the service-related errors
class ServiceError(Exception):
    def __init__(self, message=''):
        self._message = message

    def __str__(self):
        return self._message


'''
    In our service, we only have 3 simple functions, which in turn call functions from the Board
    The snake can only move, or turn, therefore here we get the correct parameters for each function, 
        then we call the corresponding functions from the Board, which is initialised in __init__
'''
class Service:
    def __init__(self, board):
        self._board = board

    # Getting the current direction in which the snake is heading
    def get_direction(self):
        return self._board.get_direction()

    def move_snake(self, steps):
        '''
        Function used to set the movement of the snake on the board
        The snake can move more than one cell, hence the 'steps' variable
        :param steps: The number of cells the snake moves over
        :return: -
        In case there are more steps, the snake repeatedly moves over one cell (we use a loop here)
        '''
        direction = self.get_direction() # We get the direction it's moving
        # Perform the move action a 'steps' number of times
        for each_step in range(steps):
            snake_x, snake_y = self._board.get_snake_head() # Because we actually only move the head, we need its coordinates first
            self._board.move(snake_x, snake_y, direction)

    def change_direction(self, direction_name):
        """
        Function called when the snake changes its movement direction
        :param direction_name: a string containing the keyword for each direction
        :return: -
        """
        # Based on the keyword 'direction_name' we get the new_direction of the snake's movement, while also raising an error
        # in the case the keyword is invalid
        if direction_name == 'up':
            new_direction = [-1, 0]
        elif direction_name == 'down':
            new_direction = [1, 0]
        elif direction_name == 'left':
            new_direction = [0, -1]
        elif direction_name == 'right':
            new_direction = [0, 1]
        else:
            raise ServiceError("Direction non existent!")

        # As the snake can't change its direction by 180 degrees (i.e. up->down or vice versa, left->right or vice versa),
        # we check if the direction change is a valid change, raising an error in the case it is not.
        current_direction = self.get_direction()
        if current_direction != new_direction:
            if current_direction[0] == new_direction[0] or current_direction[1] == new_direction[1]:
                raise ServiceError("You can't change the direction by 180!")
            else:
                self._board.set_direction(new_direction)
