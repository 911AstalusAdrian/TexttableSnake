class ServiceError(Exception):
    def __init__(self, message=''):
        self._message = message

    def __str__(self):
        return self._message


class Service:
    def __init__(self, board):
        self._board = board

    def get_direction(self):
        return self._board.get_direction()

    def move_snake(self, steps):
        direction = self.get_direction()
        for each_step in range(steps):
            snake_x, snake_y = self._board.get_snake_head()
            self._board.move(snake_x, snake_y, direction)

    def change_direction(self, direction_name):
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

        current_direction = self.get_direction()
        if current_direction != new_direction:
            if current_direction[0] == new_direction[0] or current_direction[1] == new_direction[1]:
                raise ServiceError("You can't change the direction by 180!")
            else:
                self._board.set_direction(new_direction)
