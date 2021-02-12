from Entities.board import BoardError
from Service.service import ServiceError


class UI:
    def __init__(self, board, service):
        self._board = board
        self._service = service

    def command_split(self, given_command):
        user_input = given_command.strip().split(' ', 1)
        user_input[0] = user_input[0].strip().lower()
        return user_input[0], '' if len(user_input) == 1 else user_input[1].strip().lower()

    def move_snake(self, steps):
        self._service.move_snake(steps)

    def change_direction(self, direction):
        self._service.change_direction(direction)

    def start(self):
        print("Welcome to a game of  S N E K")
        directions = ['up', 'down', 'left', 'right']
        done = False
        while not done:
            print(self._board)
            command = input("command> ")
            command_word, command_parameter = self.command_split(command)
            if command_word == 'move':
                if command_parameter == '':
                    try:
                        self.move_snake(1)
                    except ServiceError as se:
                        print(se)
                    except BoardError as ee:
                        print(ee)
                        done = True
                else:
                    try:
                        self.move_snake(int(command_parameter))
                    except ServiceError as error:
                        print(error)
                    except ValueError as ve:
                        print(ve)
                    except BoardError as be:
                        print(be)
                        done = True
            elif command_word in directions:
                try:
                    self.change_direction(command_word)
                except ServiceError as se:
                    print(se)
                except BoardError as be:
                    print(be)
                    done = True
            elif command_word == 'exit':
                done = True
            else:
                print("bad command")