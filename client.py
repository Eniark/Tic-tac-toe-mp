import threading
import pygame
import config
from network import Network
pygame.init()

# class for the screen
class GameScreen:
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    RED = (255, 60, 56)
    PURPLE = (162, 62, 72)
    BLUE = (0,0,255)
    YELLOWISH =  (255, 242, 117)
    line_x_locations = [0,]
    line_y_locations = [0,]
    line_width = 7
    statusRect_locations = []

    def __init__(self, width, height, pl_mark, size=config.DEFAULT_SIZE):
        self.size = size
        self.player = pl_mark
        self.win = pygame.display.set_mode((width, height))
        self.width = width - config.SIDEBAR
        self.height = height
        pygame.display.set_caption("Client")


    def __draw_line(self, win, color, x1, y1, x2, y2, line_width=line_width):
        pygame.draw.line(win, color, (x1,y1), (x2,y2), line_width)

    def draw_X(self,win, color, x, y, line_width=5):
        x,y = self.__find_topleft_border(x,y)
        self.__x_one_fourths = GameScreen.line_x_locations[1] * 0.25
        self.__x_three_fourths = GameScreen.line_x_locations[1] * 0.75
        self.__y_one_fourths = GameScreen.line_y_locations[1] * 0.25
        self.__y_three_fourths = GameScreen.line_y_locations[1] * 0.75
        x1 = x + self.__x_one_fourths
        y1 = y + self.__y_one_fourths
        x2 = x + self.__x_three_fourths
        y2 = y + self.__y_three_fourths
        pygame.draw.line(win, color, (x1,y1), (x2,y2), line_width)
        pygame.draw.line(win, color, (x2, y1), (x1, y2), line_width)

    def draw_O(self, win, color, x, y, radius=50, line_width=5):
        x,y = self.__find_topleft_border(x,y)
        x += GameScreen.line_x_locations[1]/2
        y += GameScreen.line_y_locations[1]/2
        pygame.draw.circle(win, color, (x,y), radius, line_width)

    def __draw_status(self, player, font_size=32):
        font = pygame.font.Font('freesansbold.ttf', font_size//2)
        playerLabel = font.render(f'You are  player {player}', True, GameScreen.PURPLE)
        playerLabelRect = playerLabel.get_rect()
        playerLabelRect.center = (self.width+config.SIDEBAR*0.65, self.height*0.05)
        self.win.blit(playerLabel, playerLabelRect)

        statusLabel = font.render('Status', True, GameScreen.BLACK)
        statusLabelRect = statusLabel.get_rect()
        statusLabelRect.center = (self.width+config.SIDEBAR//2, self.height//2 - self.height*0.25)
        self.win.blit(statusLabel, statusLabelRect)

    def update_status(self, text, font_size=16):
        font = pygame.font.Font('freesansbold.ttf', font_size)
        pygame.draw.rect(self.win, GameScreen.WHITE, (GameScreen.statusRect_locations[0],GameScreen.statusRect_locations[1],
                                                      GameScreen.statusRect_locations[2],GameScreen.statusRect_locations[3])) # redraw text rectangle
        if text in ('You lost!', 'Not your turn!', 'You won!'):
            text = font.render(text, True, GameScreen.RED)
        else:
            text = font.render(text, True, GameScreen.BLACK)
        self.win.blit(text, self.statusTextRect)

    def __draw_sidebar(self):
        self.sidebar = pygame.draw.rect(self.win, GameScreen.YELLOWISH, (self.width, 0, self.width+config.SIDEBAR, self.height))
        x1, y1, x2, y2 = self.width+config.SIDEBAR*0.15, self.height*0.3, config.SIDEBAR*0.75, self.height*0.4
        self.statusTextRect = pygame.draw.rect(self.win, GameScreen.WHITE, (x1,y1,x2,y2))
        GameScreen.statusRect_locations.append(x1)
        GameScreen.statusRect_locations.append(y1)
        GameScreen.statusRect_locations.append(x2)
        GameScreen.statusRect_locations.append(y2)
        self.statusTextRect.center = (self.statusTextRect.x + config.SIDEBAR//2.5, self.statusTextRect.y*2)

    def draw_screen(self, player):
        """
        :param player: player to pass to __draw_status
        function to draw initial screen
        """
        self.win.fill(GameScreen.BLACK)
        self.__draw_sidebar()
        self.__draw_status(player)
        AMOUNT_OF_LINES = self.size - 1
        line_colour = GameScreen.YELLOWISH
        for i in range(1, AMOUNT_OF_LINES + 1): # draw lines
            y1 = 0
            y2 = self.height
            x1 = x2 = i * self.width/(AMOUNT_OF_LINES+1)
            self.__draw_line(self.win, line_colour, x1,y1,x2,y2)
            GameScreen.line_x_locations.append(int(x1))

        for i in range(1, AMOUNT_OF_LINES + 1): # draw lines
            x1 = 0
            x2 = self.width
            y1 = y2 = i * self.height / (AMOUNT_OF_LINES + 1)
            self.__draw_line(self.win, line_colour, x1,y1,x2,y2)
            GameScreen.line_y_locations.append(int(y1))

        GameScreen.line_x_locations.append(self.width)
        GameScreen.line_y_locations.append(self.height)
        self.update_status('Waiting for other player...',font_size=12)
        pygame.display.update()

    def __find_topleft_border(self, x, y):
        """
        :param x: mouse x location
        :param y: mouse y location
        """
        for idx, el in enumerate(GameScreen.line_x_locations):
            if el>=x:
                x = GameScreen.line_x_locations[idx-1]
                break
        for idx, el in enumerate(GameScreen.line_y_locations):
            if el>=y:
                y = GameScreen.line_y_locations[idx-1]
                break
        return (x, y)
    def convert_to_indices(self, x, y):
        """
        :param x: mouse x
        :param y: mouse y
        convert mouse-x-y to indices
        """
        step_x = GameScreen.line_x_locations[1]
        step_y = GameScreen.line_y_locations[1]
        counter = 0
        x_idx = y_idx = 0
        length = len(GameScreen.line_x_locations)
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

        x_idx, y_idx = y_idx, x_idx
        return (x_idx,y_idx)

    def draw_victory_line(self, x_start, y_start, x_end, y_end):
        """
        :param x_start, y_start, x_end, y_end: indexes
        """
        x_middle = GameScreen.line_x_locations[1] * 0.5
        y_middle = GameScreen.line_y_locations[1] * 0.5
        y1 = GameScreen.line_y_locations[x_start] + y_middle
        x1 = GameScreen.line_x_locations[y_start] + x_middle

        y2 = GameScreen.line_y_locations[x_end] + y_middle
        x2 = GameScreen.line_x_locations[y_end] + x_middle
        self.__draw_line(self.win, GameScreen.RED, x1, y1, x2, y2, 10)



# Helper functions
def unpack(data: str):
    data = data.split(',')
    if data[0] in ('Victory', 'Loss'):
            # | status  | player |      x     |     y       | victory_x1  |  victory_y1 | victory_x2  |  victory_y2  |  turn_counter |
        return (data[0],data[1], int(data[2]), int(data[3]), int(data[4]), int(data[5]), int(data[6]), int(data[7]), int(data[8]))
    return (data[0],data[1], int(data[2]), int(data[3]), int(data[8]))

def pack(data):
    return str(data)

def helper_listener(n): # threaded server listener
    global callback, turn_callback
    while True:
        data = unpack(n.receive())
        if data[0]!='None':
            callback = data
            print(f"Callback: {callback}")
        else:
            turn_callback = data
            print(f"Turn_callback: {turn_callback}")


def main():
    global callback, turn_callback
    callback = None
    turn_callback = None
    connected = False
    threads = []
    turn_counter = 0

    n = Network('192.168.0.113') # ip to get connected to
    player = n.getInitialData()
    screen = GameScreen(config.WIDTH, config.HEIGHT, player)
    screen.draw_screen(player)
    connected = bool(n.receive())
    screen.update_status('<---Player X turn--->')
    t = threading.Thread(target=helper_listener, args=(n,)).start()
    threads.append(t)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP and connected:
                mouse = pygame.mouse.get_pos()
                valid_location = True
                x, y = mouse
                for i in range(len(screen.line_x_locations)):
                    if screen.line_x_locations[i]-screen.line_width < x < screen.line_x_locations[i]+screen.line_width  \
                        or screen.line_y_locations[i]-screen.line_width < y < screen.line_y_locations[i]+screen.line_width \
                        or x>screen.width:
                        valid_location = False
                        break


                if valid_location:
                    idx_x, idx_y = screen.convert_to_indices(x,y)
                    data = (idx_x, idx_y, x, y)
                    if turn_counter%2==0 and player=='X':
                        screen.draw_X(screen.win, screen.WHITE, x, y)
                    elif turn_counter%2==1 and player=='O':
                        screen.draw_O(screen.win, screen.WHITE, x, y)
                    else:
                        screen.update_status('Not your turn!')
                        continue
                    n.send(pack(data))

        if callback:
            if callback[0]=='Data':
                if callback[1] == 'O':
                    screen.draw_O(screen.win, screen.WHITE, callback[2], callback[3])
                else:
                    screen.draw_X(screen.win, screen.WHITE, callback[2], callback[3])

            elif callback[0] in ('Victory', 'Loss'):
                if callback[1] == 'O':
                    screen.draw_O(screen.win, screen.WHITE, callback[2], callback[3])
                else:
                    screen.draw_X(screen.win, screen.WHITE, callback[2], callback[3])
                screen.draw_victory_line(callback[4],callback[5],callback[6],callback[7])
                screen.update_status('You won!')
                if callback[0]=='Loss':
                    screen.update_status('You lost!')
                turn_callback=None
            callback=None

        if turn_callback:
            turn_counter= turn_callback[-1]
            if turn_counter%2==0:
                screen.update_status('<---Player X turn--->')
            else:
                screen.update_status('<---Player O turn--->')
            turn_callback=None

        pygame.display.update()

if __name__=='__main__':
    main()
