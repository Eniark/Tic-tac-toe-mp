import pygame
from pprint import pprint
import config


# class Point for keeping coordinates? To draw winning line
class Point:
    def __init__(self, coords: tuple[int, int], indices: tuple[int, int], mark: str):
        self.x, self.y = coords
        self.x_idx, self.y_idx = indices
        self.mark = mark

    def __repr__(self):
        return self.mark

# class for the game
class Game:
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
        self.board = [["" for i in range(self.size)] for j in range(self.size)]
        self.player = pl_mark
        self.is_victorious = False
        self.win = pygame.display.set_mode((scr_width, scr_height))
        self.dimensions = (scr_width, scr_height)
        pygame.display.set_caption("Client")


    def __draw_line(self, win, color, x1, y1, x2, y2, line_width=7):
        pygame.draw.line(win, color, (x1,y1), (x2,y2), line_width)

    def __draw_X(self,win, color, x, y, line_width=5):
        self.__x_one_fourths = Game.__line_x_locations[1] * 0.25
        self.__x_three_fourths = Game.__line_x_locations[1] * 0.75
        self.__y_one_fourths = Game.__line_y_locations[1] * 0.25
        self.__y_three_fourths = Game.__line_y_locations[1] * 0.75
        x1 = x + self.__x_one_fourths
        y1 = y + self.__y_one_fourths
        x2 = x + self.__x_three_fourths
        y2 = y + self.__y_three_fourths

        pygame.draw.line(win, color, (x1,y1), (x2,y2), line_width)
        pygame.draw.line(win, color, (x2, y1), (x1, y2), line_width)

    def __draw_O(self, win, color, x, y, radius=50, line_width=5):
        x += Game.__line_x_locations[1]/2
        y += Game.__line_y_locations[1]/2
        pygame.draw.circle(win, color, (x,y), radius, line_width)

    def draw_screen(self):
        self.win.fill(Game.BLACK)
        amount_of_lines = self.size - 1
        line_colour = Game.YELLOW
        for i in range(1, amount_of_lines + 1): # draw lines
            y1 = 0
            y2 = self.dimensions[1]
            x1 = x2 = i * self.dimensions[0]/(amount_of_lines+1)
            self.__draw_line(self.win, line_colour, x1,y1,x2,y2)
            Game.__line_x_locations.append(int(x1))


        for i in range(1, amount_of_lines + 1): # draw lines
            x1 = 0
            x2 = self.dimensions[0]
            y1 = y2 = i * self.dimensions[1]/ (amount_of_lines + 1)
            self.__draw_line(self.win, line_colour, x1,y1,x2,y2)
            Game.__line_y_locations.append(int(y1))


        Game.__line_x_locations.append(self.dimensions[0])
        Game.__line_y_locations.append(self.dimensions[1])


    def check_victory(self):
        h_counter = 0
        v_counter = 0
        d_counter = 0

        for i in range(len(self.board)):
            for j in range(1, len(self.board)):
                if self.board[i][j-1]==self.board[i][j]==self.player: # horizontal victory
                    h_counter+=1
                if self.board[j-1][i]==self.board[j][i]==self.player: # vertical victory

                    v_counter+=1
            if h_counter==self.size-1 or v_counter==self.size-1:
                return True
            h_counter = 0
            v_counter = 0

        # diagonals
        for j in range(1, len(self.board)):
            if self.board[j-1][j-1]==self.board[j][j]==self.player:
                d_counter+=1
        if d_counter==self.size-1:
            return True

        d_counter = 0
        for j in range(1, len(self.board)):
            if self.board[j-1][len(self.board) - j]==self.board[j][len(self.board) -j-1]==self.player:
                d_counter+=1
        if d_counter==self.size-1:
            return True

        return False

    def __convert_to_indices(self, x, y):
        step_x = Game.__line_x_locations[1]
        step_y = Game.__line_y_locations[1]
        counter = 0
        x_idx = y_idx = 0
        length = len(Game.__line_x_locations)
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
        return (x_idx, y_idx)
    def __handle_logic(self, idxs):
        x, y = idxs
        self.board[x][y] = self.player
        print(self.board)
        return self.check_victory()
    def __draw_victory_line(self, x, y):
        x_middle = Game.__line_x_locations[1] * 0.5
        y_middle = Game.__line_y_locations[1] * 0.5
        x1 = x + x_middle
        y1 = y + y_middle
        x2 = self.dimensions[0] - x_middle
        y2 = self.dimensions[1] - y_middle
        self.__draw_line(self.win, Game.RED, x1, y1, x2, y2)
    def make_move(self, x, y):
        for idx, el in enumerate(Game.__line_x_locations):
            if el>=x:
                x = Game.__line_x_locations[idx-1]
                break
        for idx, el in enumerate(Game.__line_y_locations):
            if el>=y:
                y = Game.__line_x_locations[idx-1]
                break
        idxs = self.__convert_to_indices(x,y)
        victory = self.__handle_logic(idxs)
        if victory:
            print("Victory")
            self.__draw_victory_line(x, y)
        self.__draw_X(self.win, Game.WHITE, x, y)
        # self.__draw_O(self.win, Game.WHITE, x, y)


# entry point
def main():
    game = Game(config.WIDTH, config.HEIGHT)
    game.draw_screen()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse = pygame.mouse.get_pos()
                x, y = mouse
                game.make_move(x,y)

        pygame.display.update()


if __name__=='__main__':
    main()
