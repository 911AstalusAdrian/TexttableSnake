from Entities.board import Board
from Service.service import Service
from UI.ui import UI

settings_file = open("settings.txt", 'r+')
values = settings_file.read().split()
DIM = int(values[0])
apple_count = int(values[1])


board = Board(DIM, apple_count)
service = Service(board)
ui = UI(board, service)
ui.start()