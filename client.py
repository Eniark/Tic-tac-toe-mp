import threading
import pygame
import config
from network import Network

# class for the screen
class GameScreen:
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
    YELLOW =  (255,255, 0)
    LIGHT_YELLOW = (255, 238, 107)
    __line_x_locations = [0,]
    __line_y_locations = [0,]

    def __init__(self, scr_width, scr_height, pl_mark="X", size=config.DEFAULT_SIZE):
        self.size = size
        self.player = pl_mark
        self.is_victorious = False
        self.win = pygame.display.set_mode((scr_width, scr_height))
        self.dimensions = (scr_width - config.SIDEBAR, scr_height)
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
        pygame.draw.line(win, color, (x1,y1), (x2,y2), line_width)
        pygame.draw.line(win, color, (x2, y1), (x1, y2), line_width)

    def draw_O(self, win, color, x, y, radius=50, line_width=5):
        x,y = self.__find_topleft_border(x,y)
        x += GameScreen.__line_x_locations[1]/2
        y += GameScreen.__line_y_locations[1]/2
        pygame.draw.circle(win, color, (x,y), radius, line_width)


    def __draw_sidebar(self):
        pygame.draw.rect(self.win, GameScreen.LIGHT_YELLOW, (self.dimensions[0], 0, self.dimensions[0]+config.SIDEBAR, self.dimensions[1]))

    def draw_screen(self):
        self.win.fill(GameScreen.BLACK)
        self.__draw_sidebar()
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

    def draw_victory_line(self, x_start, y_start, x_end, y_end):
        x_middle = GameScreen.__line_x_locations[1] * 0.5
        y_middle = GameScreen.__line_y_locations[1] * 0.5
        y1 = GameScreen.__line_x_locations[x_start] + y_middle
        x1 = GameScreen.__line_y_locations[y_start] + x_middle

        y2 = GameScreen.__line_x_locations[x_end] + y_middle
        x2 = GameScreen.__line_y_locations[y_end] + x_middle
        self.__draw_line(self.win, GameScreen.RED, x1, y1, x2, y2, 10)



# Helper functions
def unpack(data: str):
    data = data.split(',')
    if data[0]=='|==Victory==|':
            # | status  | player |      x     |     y       | victory_x1  |  victory_y1 | victory_x2  |  victory_y2  |  turn_counter |
        return (data[0],data[1], int(data[2]), int(data[3]), int(data[4]), int(data[5]), int(data[6]), int(data[7]), int(data[8]))
    return (data[0],data[1], int(data[2]), int(data[3]), int(data[8]))

def pack(data):
    return str(data)

def helper_listener(n):
    global callback
    while True:
        callback= unpack(n.receive())
        print(f"Callback: {callback}")

# entry point
def main():
    global callback
    callback = []
    n = Network()
    player = n.getInitialData()
    turn_counter = 0
    threading.Thread(target=helper_listener, args=(n,)).start()
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
                if x<screen.dimensions[0]:
                    idx_x, idx_y = screen.convert_to_indices(x,y)
                    data = (idx_x, idx_y, x, y) # sending idxs and mouse coords
                    if turn_counter%2==0 and player=='X':
                        screen.draw_X(screen.win, screen.WHITE, x, y)
                    elif turn_counter%2==1 and player=='O':
                        screen.draw_O(screen.win, screen.WHITE, x, y)
                    else:
                        print("ERROR!") # ??
                        continue
                    n.send(pack(data))

        if callback:
            turn_counter= callback[-1]
            print(f"turn: {turn_counter}")
            if callback[0]=='|==Data==|':
                if callback[1] == 'O':
                    screen.draw_O(screen.win, screen.WHITE, callback[2], callback[3])
                else:
                    screen.draw_X(screen.win, screen.WHITE, callback[2], callback[3])
            elif callback[0]=='|==Victory==|':
                if callback[1] == 'O':
                    screen.draw_O(screen.win, screen.WHITE, callback[2], callback[3])
                else:
                    screen.draw_X(screen.win, screen.WHITE, callback[2], callback[3])
                screen.draw_victory_line(callback[4],callback[5],callback[6],callback[7])
            # turn receiver?
            elif callback[0]=='|==Error==|':
                pass

            callback=None


        pygame.display.update()


if __name__=='__main__':
    main()
