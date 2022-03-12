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
        return str((self.x_idx, self.y_idx))

# class for the game
class Game:
    def __init__(self, size=config.DEFAULT_SIZE):
        self.size = size
        self.board = [["" for i in range(self.size)] for j in range(self.size)]


    def check_victory(self, player):
        h_counter = 0
        v_counter = 0
        d_counter = 0
        self.victory_line_points = []
        # horizontal victory
        for i in range(len(self.board)):
            for j in range(1, len(self.board)):
                self.victory_line_points.append(self.board[i][j-1])
                if isinstance(self.board[i][j-1], Point) and isinstance(self.board[i][j], Point) \
                    and self.board[i][j-1].mark==self.board[i][j].mark==player: # horizontal victory
                    h_counter+=1
                    if h_counter==self.size-1:
                        self.victory_line_points.append(self.board[i][j])

                        return True
            self.victory_line_points = []
            h_counter = 0
        # vertical victory
        for i in range(len(self.board)):
            for j in range(1, len(self.board)):
                self.victory_line_points.append(self.board[j-1][i])
                if isinstance(self.board[j-1][i], Point) and isinstance(self.board[j][i], Point) \
                    and self.board[j-1][i].mark==self.board[j][i].mark==player: # vertical victory
                    v_counter+=1
                    if v_counter==self.size-1:
                        self.victory_line_points.append(self.board[j][i])
                        return True
            self.victory_line_points = []
            v_counter = 0

        # diagonals
        for j in range(1, len(self.board)):
            self.victory_line_points.append(self.board[j-1][j-1])
            if isinstance(self.board[j-1][j-1], Point) and isinstance(self.board[j][j], Point) \
                and self.board[j-1][j-1].mark==self.board[j][j].mark==player:
                d_counter+=1
                if d_counter==self.size-1:
                    self.victory_line_points.append(self.board[j][j])
                    return True
        self.victory_line_points = []

        d_counter = 0
        for j in range(1, len(self.board)):
            self.victory_line_points.append(self.board[j-1][len(self.board) - j])
            if isinstance(self.board[j-1][len(self.board) - j], Point) and isinstance(self.board[j][len(self.board) - j - 1], Point):
                d_counter+=1
                if d_counter==self.size-1:
                    self.victory_line_points.append(self.board[j][len(self.board) - j - 1])
                    return True
        return False

    def __handle_logic(self, x, y, player):
        if not self.board[x][y]:
            self.board[x][y] = Point((x,y), player)
            return True
        return False
    def make_move(self, x, y, player): # merge with __handle_logic?
        return self.__handle_logic(x, y, player)



server = "192.168.0.113" # hosts ip
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

turn_counter=0
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


def threaded_client(conn, player:int):
    """
    :param conn: Socket object connection
    :param player: player number
    Threaded connection to socket objects
    """
    global turn_counter, player_mouse_moves, currentPlayer
    player=players[player]
    conn.send(str.encode(player))
    if currentPlayer%2==0:
        connections['X'].send(str.encode(pack(True)))
        connections['O'].send(str.encode(pack(True)))
    parameters = 9
    reply_template = [None for _ in range(parameters)]
    turn_updater_reply = None
    while True:
        try:
            data = conn.recv(2048).decode()
            x, y, mouse_x, mouse_y = unpack(data)
            if not data:
                print("Disconected")
                break
            else:
                res = game.make_move(x,y, player)
                if res:
                    player_mouse_moves[player] = [mouse_x, mouse_y]
                    if player=='X':
                        x,y = player_mouse_moves['X']
                        reply_template[1]="X"
                        reply_template[2] = x
                        reply_template[3] = y
                    else:
                        x,y = player_mouse_moves['O']
                        reply_template[1]="O"
                        reply_template[2] = x
                        reply_template[3] = y

                    victory= game.check_victory(player)
                    if victory:
                        victory_x_start, victory_y_start = game.victory_line_points[0].x_idx, game.victory_line_points[0].y_idx
                        victory_x_end, victory_y_end = game.victory_line_points[-1].x_idx, game.victory_line_points[-1].y_idx
                        print(game.victory_line_points)
                        reply_template[0] = "Victory"
                        reply_template[4]= victory_x_start
                        reply_template[5]= victory_y_start
                        reply_template[6]= victory_x_end
                        reply_template[7]= victory_y_end
                    else:
                        reply_template[0] = "Data"

                    turn_counter+=1
                    reply_template[8] = turn_counter
                    reply_template = list(map(str, reply_template))
                    reply = ','.join(reply_template)
                    try:
                        if reply_template[0]=="Data":
                            if player=='X': # forwarding messages to clients
                                connections['O'].send(str.encode(pack(reply)))
                            elif player=='O':
                                connections['X'].send(str.encode(pack(reply)))

                        elif reply_template[0]=="Victory":
                            # sending to all clients the victory coords
                            if player=='X':
                                connections['X'].send(str.encode(pack(reply)))
                                # modifying reply
                                reply = reply.split(',')
                                reply[0] = 'Loss'
                                reply = ','.join(reply)
                                connections['O'].send(str.encode(pack(reply)))

                            elif player=='O':
                                connections['O'].send(str.encode(pack(reply)))
                                # modifying reply
                                reply = reply.split(',')
                                reply[0] = 'Loss'
                                reply = ','.join(reply)
                                connections['X'].send(str.encode(pack(reply)))
                        # creating reply for turn updater
                        turn_updater_reply = [None for _ in range(parameters)] # turn updater for each client
                        turn_updater_reply[-1] = turn_counter
                        turn_updater_reply[2], turn_updater_reply[3] = 0, 0
                        turn_updater_reply = list(map(str, turn_updater_reply))
                        turn_updater_reply = ','.join(turn_updater_reply)

                        connections['X'].send(str.encode(pack(turn_updater_reply)))
                        connections['O'].send(str.encode(pack(turn_updater_reply)))

                    except KeyError:
                            print("|==ERROR==|: Not enough players!")
                    reply_template = [None for _ in range(parameters)]
        except socket.error as e:
            print(f"ERROR::{e}")
            break


    print('Lost connection')
    currentPlayer-=1
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

