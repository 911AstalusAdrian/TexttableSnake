from Entities.board import BoardError
from Service.service import ServiceError

# UI class used to deal with all the user inputs and prints
class UI:
    def __init__(self, board, service):
        self._board = board
        self._service = service

    # Function used to separate the string given by the user into (at most) two keywords
    # Example: 'move 4' returns a tuple consisting of the strings 'move' and '4'
    def command_split(self, given_command):
        user_input = given_command.strip().split(' ', 1)
        user_input[0] = user_input[0].strip().lower()
        return user_input[0], '' if len(user_input) == 1 else user_input[1].strip().lower()

    # Calling the Service function for moving the snake, passing the number of steps the snake moves
    def move_snake(self, steps):
        self._service.move_snake(steps)

    # Calling the Service function for changing the snake's direction, passing the new direction given by the user
    def change_direction(self, direction):
        self._service.change_direction(direction)


    # The main function of the program, the loop that displays our Board in the console
    def start(self):
        print("Welcome to a game of  S N E K")
        directions = ['up', 'down', 'left', 'right'] # a list of the valid directions a user can give
        done = False
        # The game goes on as long as the snake doesn't hit itself or an edge, or it ends when the user enters the keyword 'exit'
        while not done:
            # Firstly, we print the current state of the board
            print(self._board)
            # Then, we get the user's input, and separate the keywords
            command = input("command> ")
            command_word, command_parameter = self.command_split(command)
            # Depending on the user's input, we go on a specific branch:

            # Snake move branch
            # If the user didn't specify how many moves the snake does, then it will make only one move
            # The callings of the move function are put in a 'try... except...' block in order to catch any errors that can occur
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

            # Snake change direction branch
            # We check if the keyword is valid, and call the change_direction function in a 'try... except...' block
            # so we can catch any possible errors
            elif command_word in directions:
                try:
                    self.change_direction(command_word)
                except ServiceError as se:
                    print(se)
                # A special case is the BoardError, which is raised when the snake hit itself or a border of the board,
                # therefore signaling the end of the game (hence the 'done=True' in this except block)
                except BoardError as be:
                    print(be)
                    done = True
            # Special keyword used when the user ends the game 
            elif command_word == 'exit':
                done = True
            else:
                print("bad command")