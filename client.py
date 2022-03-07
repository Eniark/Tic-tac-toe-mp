import pygame
from pprint import pprint
import config
from network import Network

# class for the game
class GameScreen:
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
    YELLOW =  (255,255, 0)
    __line_x_locations = [0,]
    __line_y_locations = [0,]

    def __init__(self, scr_width, scr_height, pl_mark="X", size=3):
        self.size = size
        self.player = pl_mark
        self.is_victorious = False
        self.win = pygame.display.set_mode((scr_width, scr_height))
        self.dimensions = (scr_width, scr_height)
        pygame.display.set_caption("Client")


    def __draw_line(self, win, color, x1, y1, x2, y2, line_width=7):
        pygame.draw.line(win, color, (x1,y1), (x2,y2), line_width)

    def draw_X(self,win, color, x, y, line_width=5):
        x,y = self.__find_topleft_border(x,y)
        self.__x_one_fourths = GameScreen.__line_x_locations[1] * 0.25
        self.__x_three_fourths = GameScreen.__line_x_locations[1] * 0.75
        self.__y_one_fourths = GameScreen.__line_y_locations[1] * 0.25
        self.__y_three_fourths = GameScreen.__line_y_locations[1] * 0.75
        x1 = x + self.__x_one_fourths
        y1 = y + self.__y_one_fourths
        x2 = x + self.__x_three_fourths
        y2 = y + self.__y_three_fourths
        print(x1, y1)
        print(x2, y2)
        pygame.draw.line(win, color, (x1,y1), (x2,y2), line_width)
        pygame.draw.line(win, color, (x2, y1), (x1, y2), line_width)

    def draw_O(self, win, color, x, y, radius=50, line_width=5):
        x,y = self.__find_topleft_border(x,y)
        x += GameScreen.__line_x_locations[1]/2
        y += GameScreen.__line_y_locations[1]/2
        pygame.draw.circle(win, color, (x,y), radius, line_width)

    def draw_screen(self):
        self.win.fill(GameScreen.BLACK)
        amount_of_lines = self.size - 1
        line_colour = GameScreen.YELLOW
        for i in range(1, amount_of_lines + 1): # draw lines
            y1 = 0
            y2 = self.dimensions[1]
            x1 = x2 = i * self.dimensions[0]/(amount_of_lines+1)
            self.__draw_line(self.win, line_colour, x1,y1,x2,y2)
            GameScreen.__line_x_locations.append(int(x1))


        for i in range(1, amount_of_lines + 1): # draw lines
            x1 = 0
            x2 = self.dimensions[0]
            y1 = y2 = i * self.dimensions[1]/ (amount_of_lines + 1)
            self.__draw_line(self.win, line_colour, x1,y1,x2,y2)
            GameScreen.__line_y_locations.append(int(y1))


        GameScreen.__line_x_locations.append(self.dimensions[0])
        GameScreen.__line_y_locations.append(self.dimensions[1])


    # def check_victory(self):
    #     h_counter = 0
    #     v_counter = 0
    #     d_counter = 0
    #     self.__victory_line_points = []
    #     for i in range(len(self.board)):
    #         for j in range(1, len(self.board)):
    #             self.__victory_line_points.append(self.board[i][j-1])
    #             if isinstance(self.board[i][j-1], Point) and isinstance(self.board[i][j], Point): # horizontal victory
    #                 h_counter+=1
    #                 if h_counter==self.size-1:
    #                     self.__victory_line_points.append(self.board[i][j])
    #                     return True
    #         self.__victory_line_points = []
    #         h_counter = 0
    #
    #
    #     for i in range(len(self.board)):
    #         for j in range(1, len(self.board)):
    #             self.__victory_line_points.append(self.board[j-1][i])
    #             if isinstance(self.board[j-1][i], Point) and isinstance(self.board[j][i], Point): # vertical victory
    #                 v_counter+=1
    #                 if v_counter==self.size-1:
    #                     self.__victory_line_points.append(self.board[j][i])
    #                     return True
    #         self.__victory_line_points = []
    #         v_counter = 0
    #
    #
    #     # diagonals
    #     for j in range(1, len(self.board)):
    #         self.__victory_line_points.append(self.board[j-1][j-1])
    #         if isinstance(self.board[j-1][j-1], Point) and isinstance(self.board[j][j], Point):
    #             d_counter+=1
    #             if d_counter==self.size-1:
    #                 self.__victory_line_points.append(self.board[j][j])
    #                 return True
    #     self.__victory_line_points = []
    #
    #     d_counter = 0
    #     for j in range(1, len(self.board)):
    #         self.__victory_line_points.append(self.board[j-1][len(self.board) - j])
    #         if isinstance(self.board[j-1][len(self.board) - j], Point) and isinstance(self.board[j][len(self.board) - j - 1], Point):
    #             d_counter+=1
    #             if d_counter==self.size-1:
    #                 self.__victory_line_points.append(self.board[j][len(self.board) - j - 1])
    #                 return True
    #     return False


    def __find_topleft_border(self, x, y):
        for idx, el in enumerate(GameScreen.__line_x_locations):
            if el>=x:
                x = GameScreen.__line_x_locations[idx-1]
                break
        for idx, el in enumerate(GameScreen.__line_y_locations):
            if el>=y:
                y = GameScreen.__line_x_locations[idx-1]
                break
        return (x, y)
    def convert_to_indices(self, x, y):
        step_x = GameScreen.__line_x_locations[1]
        step_y = GameScreen.__line_y_locations[1]
        counter = 0
        x_idx = y_idx = 0
        length = len(GameScreen.__line_x_locations)
        for i in range(length):

            counter+=step_x
            if counter>x:
                x_idx = i
                break

        counter = 0
        for i in range(length):
            counter+=step_y
            if counter>y:
                y_idx = i
                break

        x_idx, y_idx = y_idx, x_idx # had to swap them for correct logic
        return (x_idx,y_idx)
    # def __handle_logic(self, idxs):
    #     x, y = idxs
    #     self.board[x][y] = Point((x,y), self.player)
    #     print(self.board)
    #     return self.check_victory()
    def __draw_victory_line(self):
        x_middle = GameScreen.__line_x_locations[1] * 0.5
        y_middle = GameScreen.__line_y_locations[1] * 0.5
        y1 = GameScreen.__line_x_locations[self.__victory_line_points[0].x_idx] + y_middle
        x1 = GameScreen.__line_y_locations[self.__victory_line_points[0].y_idx] + x_middle

        y2 = GameScreen.__line_x_locations[self.__victory_line_points[-1].x_idx] + y_middle
        x2 = GameScreen.__line_y_locations[self.__victory_line_points[-1].y_idx] + x_middle
        self.__draw_line(self.win, GameScreen.RED, x1, y1, x2, y2, 10)
    # def make_move(self, x, y):
    #     for idx, el in enumerate(GameScreen.__line_x_locations):
    #         if el>=x:
    #             x = GameScreen.__line_x_locations[idx-1]
    #             break
    #     for idx, el in enumerate(GameScreen.__line_y_locations):
    #         if el>=y:
    #             y = GameScreen.__line_x_locations[idx-1]
    #             break
    #     idxs = self.__convert_to_indices(x,y)
    #     victory = self.__handle_logic(idxs)
    #     if victory:
    #         print("Victory")
    #         self.__draw_victory_line()
    #     if self.player=='X':
    #         self.__draw_X(self.win, GameScreen.WHITE, x, y)
    #     elif self.player=='O':
    #         self.__draw_O(self.win, GameScreen.WHITE, x, y)



# Helper functions
def unpack(coords: tuple):
    return str(coords[0]) + ',' + str(coords[1])

def pack(data):
    return str(data)

# entry point
def main():
    n = Network()
    player = n.getInitialData()
    print(f'I am player: {player}')
    screen = GameScreen(config.WIDTH, config.HEIGHT, player)
    screen.draw_screen()
    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse = pygame.mouse.get_pos()
                x, y = mouse
                data = screen.convert_to_indices(x,y)
                print(f"Sending.. {data}")
                callback = n.send(pack(data))
                if callback:
                    print(f"Player: {player}")
                    if player=='X':
                        screen.draw_X(screen.win, screen.WHITE, x, y)
                    else:
                        screen.draw_O(screen.win, screen.WHITE, x, y)

                print(callback)

        pygame.display.update()


if __name__=='__main__':
    main()
