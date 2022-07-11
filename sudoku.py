import pygame
import random
pygame.font.init()

NODE_SIZE = 100
BORDER_SIZE = 98

WIDTH = 908
HEIGHT = 908
pygame.display.set_caption("sudoku")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 60
NUMBER_FONT = pygame.font.SysFont('comicsans', 70)

WHITE = (255, 255, 255)
BLACK = (0, 0 , 0)
GREEN = (0, 255, 0)
RED = (255, 0 , 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
GREY = (169, 169, 169)

VALID_SUDOKU = [
    [
        [5,3,0,0,7,0,0,0,0],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9]
    ],
    [
        [3,0,6,5,0,8,4,0,0],
        [5,2,0,0,0,0,0,0,0],
        [0,8,7,0,0,0,0,3,1],
        [0,0,3,0,1,0,0,8,0],
        [9,0,0,8,6,3,0,0,5],
        [0,5,0,0,9,0,6,0,0],
        [1,3,0,0,0,0,2,5,0],
        [0,0,0,0,0,0,0,7,4],
        [0,0,5,2,0,6,3,0,0]
    ]
]

class Node():

    def __init__(self, x, y, value, given, pos):
        self.rect = pygame.Rect(x, y, NODE_SIZE, NODE_SIZE)
        self.border = pygame.Rect(x+1, y+1, BORDER_SIZE, BORDER_SIZE)
        self.value = value
        self.given = given
        self.pos = pos
        self.selected = False
        self.clicked = False
        self.invalid = False

    def reset(self):
        if not self.given:
            self.change_value(0)
            self.set_valid()
            self.unselect()

    def set_valid(self):
        self.invalid = False

    def set_invalid(self):
        self.invalid = True

    def change_value(self, value):
        self.value = value

    def unselect(self):
        self.selected = False

    def select(self):
        self.selected = True

    def draw(self):
        action = False

        mouse_pos = pygame.mouse.get_pos()

        pygame.draw.rect(screen, WHITE, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 1)

        if self.selected:
            pygame.draw.rect(screen, GREEN, self.border, 4)

        if self.invalid:
            pygame.draw.rect(screen, RED, self.border, 4)

        if self.rect.collidepoint(mouse_pos) and not self.given:

            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
                self.selected = not self.selected

            elif pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        if self.value:
            if self.given:
                number_text = NUMBER_FONT.render(str(self.value), 1, BLACK)
            else:
                number_text = NUMBER_FONT.render(str(self.value), 1, GREY)
            screen.blit(number_text, (self.rect.x + number_text.get_width()//2, self.rect.y))

        return action


class Board():

    def __init__(self):
        self.board = None
        self.selected_node = None
        self.make_board()

    def make_board(self):
        valid_start = random.choice(VALID_SUDOKU)
        self.board = []
        y_offset = 0
        for y in range(9):
            row = []
            x_offset = 0
            if y%3 == 0 and y != 0:
                y_offset += 4
            for x in range(9):
                if x%3 == 0 and x != 0:
                    x_offset += 4
                node = Node(x*NODE_SIZE+x_offset,y*NODE_SIZE+y_offset,valid_start[y][x],True if valid_start[y][x] != 0 else False, (x,y))
                row.append(node)
            self.board.append(row)

    def new(self):
        self.selected_node = None
        self.reset()
        self.make_board()

    def reset(self):
        for y in self.board:
            for x in y:
                x.reset()

    def change_node_value(self, value):
        if self.selected_node:
            if self.check_node_value(value):
                self.selected_node.change_value(value)
                self.selected_node.set_valid()
                return True
            else:
                self.selected_node.change_value(value)
                self.selected_node.set_invalid()
                return False

    def check_node_value(self, value):
        if value == 0:
            return True
        col, row = self.selected_node.pos
        for x in range(9):
            # horizontal search
            if self.board[row][x].value == value:
                return False
            # vertical search
            if self.board[x][col].value == value:
                return False
        # cube search
        for y in range(row//3 * 3, row//3 * 3 + 3):
            for x in range (col//3 * 3, col//3 * 3 + 3):
                if self.board[y][x].value == value:
                    return False
        return True

    def unselect_other_nodes(self, node):
        for y in self.board:
            for x in y:
                if x != node:
                    x.unselect()

    def draw(self):
        screen.fill(BLACK)
        for y in self.board:
            for x in y:
                if x.draw():
                    if x.selected:
                        self.selected_node = x
                        self.unselect_other_nodes(x)
                    else:
                        self.selected_node = None

    def Backtrack(self, x, y):

        previous_node = None

        while self.board[y][x].value:
            if x < 8:
                x += 1
            elif y < 8:
                x = 0
                y += 1
            elif x == 8 and y == 8:
                return True

        self.selected_node = self.board[y][x]
        self.unselect_other_nodes(x)
        self.selected_node.select()
        previous_node = self.selected_node

        for value in range(1,10):
            if self.check_node_value(value):
                self.change_node_value(value)
                screen.fill(WHITE)
                self.draw()
                pygame.display.update()
                pygame.time.delay(50)
                if self.Backtrack(x, y):
                    return True
                else:
                    self.selected_node = previous_node
                    self.change_node_value(0)
        return False

def main():

    board = Board()
    clock = pygame.time.Clock()
    running = True
    solved = False
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board.reset()
                    solved = False
                if event.key == pygame.K_n:
                    board.new()
                    solved = False
                if event.key == pygame.K_s:
                    board.reset()
                    if board.Backtrack(0, 0):
                        solved = True
                if event.key == pygame.K_0 or event.key == pygame.K_KP0:
                    board.change_node_value(0)
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    board.change_node_value(1)
                if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    board.change_node_value(2)
                if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    board.change_node_value(3)
                if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    board.change_node_value(4)
                if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    board.change_node_value(5)
                if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    board.change_node_value(6)
                if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    board.change_node_value(7)
                if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    board.change_node_value(8)
                if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    board.change_node_value(9)

        screen.fill(WHITE)
        board.draw()

        pygame.display.update()

if __name__ == '__main__':
    main()