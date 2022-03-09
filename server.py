import socket
from _thread import start_new_thread
import os
import config

# class Point
class Point:
    def __init__(self, indices: tuple[int, int], mark: str):
        self.x_idx, self.y_idx = indices
        self.mark = mark

    def __repr__(self):
        return self.mark

# class for the game
class Game:
    def __init__(self, pl_mark="X", size=config.DEFAULT_SIZE):
        self.size = size
        self.board = [["" for i in range(self.size)] for j in range(self.size)]
        self.player = pl_mark
        self.is_victorious = False


    def check_victory(self, player):
        h_counter = 0
        v_counter = 0
        d_counter = 0
        self.__victory_line_points = []
        for i in range(len(self.board)):
            for j in range(1, len(self.board)):
                self.__victory_line_points.append(self.board[i][j-1])
                if isinstance(self.board[i][j-1], Point) and isinstance(self.board[i][j], Point) \
                    and self.board[i][j-1].mark==self.board[i][j].mark==player: # horizontal victory
                    h_counter+=1
                    if h_counter==self.size-1:
                        self.__victory_line_points.append(self.board[i][j])
                        return True
            self.__victory_line_points = []
            h_counter = 0


        for i in range(len(self.board)):
            for j in range(1, len(self.board)):
                self.__victory_line_points.append(self.board[j-1][i])
                if isinstance(self.board[j-1][i], Point) and isinstance(self.board[j][i], Point) \
                    and self.board[j-1][i].mark==self.board[j][i].mark==player: # vertical victory
                    v_counter+=1
                    if v_counter==self.size-1:
                        self.__victory_line_points.append(self.board[j][i])
                        return True
            self.__victory_line_points = []
            v_counter = 0


        # diagonals
        for j in range(1, len(self.board)):
            self.__victory_line_points.append(self.board[j-1][j-1])
            if isinstance(self.board[j-1][j-1], Point) and isinstance(self.board[j][j], Point) \
                and self.board[j-1][j-1].mark==self.board[j][j].mark==player:
                d_counter+=1
                if d_counter==self.size-1:
                    self.__victory_line_points.append(self.board[j][j])
                    return True
        self.__victory_line_points = []

        d_counter = 0
        for j in range(1, len(self.board)):
            self.__victory_line_points.append(self.board[j-1][len(self.board) - j])
            if isinstance(self.board[j-1][len(self.board) - j], Point) and isinstance(self.board[j][len(self.board) - j - 1], Point):
                d_counter+=1
                if d_counter==self.size-1:
                    self.__victory_line_points.append(self.board[j][len(self.board) - j - 1])
                    return True
        return False

    def __handle_logic(self, x, y, player):
        if not self.board[x][y]:
            self.board[x][y] = Point((x,y), player)
            print(self.board)
            return True
        print(self.board)
        return False
    def make_move(self, x, y, player):

        # idxs = self.__convert_to_indices(x,y)

        return self.__handle_logic(x, y, player)
        #     self.__draw_victory_line()
        # if self.player=='X':
        #     self.__draw_X(self.win, Game.WHITE, x, y)
        # elif self.player=='O':
        #     self.__draw_O(self.win, Game.WHITE, x, y)



server = "192.168.0.113"
port = 5555 # open port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)


AMOUNT_OF_PLAYERS = 2
s.listen(AMOUNT_OF_PLAYERS)
print('Waiting for connection. Server Started')

players=['X','O']
player_mouse_moves = { players[0]:[0,0],
                       players[1]:[0,0]}

# Helper functions
def unpack(data):
    data = data[1:-1].split(', ')
    return (int(data[0]), int(data[1]), int(data[2]), int(data[3]))

def pack(data):
    return str(data)

player_turn_counter=0 # for future

def threaded_client(conn, player):
    global player_turn_counter, player_mouse_moves
    player=players[player]
    conn.send(str.encode(player))

    reply = ''
    while True:
        try:
            data = conn.recv(2048).decode()
            print(f'Received.. {data}')
            x, y, mouse_x, mouse_y = unpack(data)

            if not data:
                print("Disconected")
                break
            else:
                res = game.make_move(x,y, player)
                player_mouse_moves[player] = [mouse_x, mouse_y]
                print(player_mouse_moves)
                if res:
                    if player=='X':
                        reply = "X,"+str(player_mouse_moves['X'])[1:-1]+','
                    else:
                        reply="O,"+str(player_mouse_moves['O'])[1:-1]+','

                    reply += str(game.check_victory(player))

                    if player=='X': ## hardcoded
                        connections['O'].send(str.encode(pack(reply)))
                    elif player=='O':
                        connections['X'].send(str.encode(pack(reply)))
                    else:
                        print('Not your turn!')

                    player_turn_counter+=1 # fix in future, plz!!!
                    print('Reply:', reply)
                    if player_turn_counter>=AMOUNT_OF_PLAYERS:
                        player_turn_counter=0
        except socket.error as e:
            print(f"ERROR::{e}")
            break


    print('Lost connection')
    conn.close()

currentPlayer = 0
game = Game()
connections = {}
while True:
    conn, addr = s.accept()
    connections[players[currentPlayer]]=conn
    print(f'Connected to: {addr}')

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer+=1
