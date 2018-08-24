import pygame as pg
import math
import figure as fig_char
import draw
import random

def check_collision(list,col,row):
    for fg in list:
        if fg.col == col and fg.row == row:
            return True
    return False

def show_step(screen,col, row, color = (0, 255, 0)  ):
    if col < 1 or col > 8 or row > 8 or row < 1:
        return
    rect_1_rect = pg.Rect((200 + (col - 1) * 30, 110 + (row - 1) * 30), (30, 30))
    rect_1_color = color
    rect_1_width = 3
    pg.draw.rect(screen, rect_1_color, rect_1_rect, rect_1_width)

class figure(object):
    def __init__(self, color, role, screen):
        self.color = color
        self.role = role
        self.screen = screen
        fig_img = pg.image.load("images/game/" + self.role + "_" + self.color + ".png")
        fig_img = pg.transform.scale(fig_img, (30, 30))
        self.image = fig_img
        fig_img = pg.image.load("images/game/" + self.role + "_" + self.color + ".png")
        fig_img = pg.transform.scale(fig_img, (60, 60))
        self.image_2 = fig_img

    def draw(self, col, row ):
        x = 200 + (col-1)*30
        y = 110 + (row-1)*30
        self.screen.blit(self.image, (x,y))

class unit(object):
    def __init__(self, figure, col, row):
        self.figure = figure
        self.col = col
        self.row = row
        self.enable = True

    def draw(self):
        self.figure.draw(self.col, self.row)

    def move(self,col,row,game):
        self.col = col
        self.row = row
        game.change_side()

    def highlight(self,x,y):
        if x > 200 + (self.col-1)*30 and x < 200 + self.col*30 and y > 110 + (self.row-1)*30 and y < 110 + self.row*30:
            return True
        return False

    def light(self):
        rect_1_rect = pg.Rect((200 + (self.col-1)*30, 110 + (self.row-1)*30), (30, 30))
        rect_1_color = (255, 255, 0)
        rect_1_width = 3
        pg.draw.rect(self.figure.screen, rect_1_color, rect_1_rect, rect_1_width)

    def red_light(self):
        rect_1_rect = pg.Rect((200 + (self.col - 1) * 30, 110 + (self.row - 1) * 30), (30, 30))
        rect_1_color = (255, 0, 0)
        rect_1_width = 4
        pg.draw.rect(self.figure.screen, rect_1_color, rect_1_rect, rect_1_width)

    def die(self):
        self.col = -200
        self.row = -200
        self.enable = False

    def make_step(self,x ,y, list, game, color = "black"):
        row = math.floor((y - 110)/30 + 1)
        col = math.floor((x - 200)/30 + 1)

        if (col < 9 and col >= 1 and row < 9 and row >=1 ):
            if self.figure.role == "pawn":
                if ((self.row - row == 1 and color == "black") or (self.row - row == -1 and color == "white")) and self.col - col == 0:

                    empty_col = False
                    for fg in list:
                        if fg.col == col and fg.row == row:
                            empty_col = True
                    if empty_col == False:
                        self.move(col,row,game)
                if ((self.row - row == 2 and color == "black") or (self.row - row == -2 and color == "white")) and self.col - col == 0:
                    empty_col = False
                    if self.row > 6:
                        for fg in list:
                            if fg.col == col and fg.row == row:
                                empty_col = True
                        if empty_col == False:
                            self.move(col,row, game)
                if (self.row - row == 1 and color == "black") or (self.row - row == -1 and color == "white"):
                    if self.col - col == 1:
                        for fg in list[16:]:
                            if fg.col == col and fg.row == row:
                                if fg.figure.role == "king":
                                    return
                                fg.die()
                                self.move(col,row,game)
                    if self.col - col == -1:
                        for fg in list[16:]:
                            if fg.col == col and fg.row == row:
                                if fg.figure.role == "king":
                                    return
                                fg.die()
                                self.move(col,row,game)
            if self.figure.role == "knight":
                for i in range(-1, 2, 2):
                    for j in range(-2, 3, 4):
                        if col == self.col + i and row == self.row + j:
                            if check_collision(list[:16], self.col + i, self.row + j) == False:
                                for fg in list[16:]:
                                    if fg.col == col and fg.row == row:
                                        if fg.figure.role != "king":
                                            fg.die()
                                        else:
                                            return
                                self.move(col,row,game)
                        elif col == self.col + j and row == self.row + i:
                            if check_collision(list[:16], self.col + j, self.row + i) == False:
                                for fg in list[16:]:
                                    if fg.col == col and fg.row == row:
                                        if fg.figure.role != "king":
                                            fg.die()
                                        else:
                                            return
                                self.move(col,row,game)
            if self.figure.role == "bishop" or self.figure.role == "queen":
                block_up_left = False
                block_up_right = False
                block_down_left = False
                block_down_right = False
                for i in range(1, 9):
                    if check_collision(list[:16], self.col + i, self.row + i) == False:
                        if block_down_right == False:
                            if check_collision(list[16:], self.col + i, self.row + i) == False:
                                if self.col + i == col and self.row + i == row:
                                    self.move(col,row,game)
                            else:
                                if self.col + i == col and self.row + i == row:
                                    for fg in list[16:]:
                                        if fg.col == col and fg.row == row:
                                            if fg.figure.role != "king":
                                                fg.die()
                                                self.move(col, row,game)
                                block_down_right = True
                    else:
                        block_down_right = True

                    if check_collision(list[:16], self.col + i, self.row - i) == False:
                        if block_up_right == False:
                            if check_collision(list[16:], self.col + i, self.row - i) == False:
                                if self.col + i == col and self.row - i == row:
                                    self.move(col,row,game)
                            else:
                                if self.col + i == col and self.row - i == row:
                                    for fg in list[16:]:
                                        if fg.col == col and fg.row == row:
                                            if fg.figure.role != "king":
                                                fg.die()
                                                self.move(col, row,game)
                                block_up_right = True
                    else:
                        block_up_right = True

                    if check_collision(list[:16], self.col - i, self.row + i) == False:
                        if block_down_left == False:
                            if check_collision(list[16:], self.col - i, self.row + i) == False:
                                if self.col - i == col and self.row + i == row:
                                    self.move(col,row,game)
                            else:
                                if self.col - i == col and self.row + i == row:
                                    for fg in list[16:]:
                                        if fg.col == col and fg.row == row:
                                            if fg.figure.role != "king":
                                                fg.die()
                                                self.move(col, row,game)
                                block_down_left = True
                    else:
                        block_down_left = True

                    if check_collision(list[:16], self.col - i, self.row - i) == False:
                        if block_up_left == False:
                            if check_collision(list[16:], self.col - i, self.row - i) == False:
                                if self.col - i == col and self.row - i == row:
                                    self.move(col,row,game)
                            else:
                                if self.col - i == col and self.row - i == row:
                                    for fg in list[16:]:
                                        if fg.col == col and fg.row == row:
                                            if fg.figure.role != "king":
                                                fg.die()
                                                self.move(col, row,game )
                                block_up_left = True
                    else:
                        block_up_left = True
            if self.figure.role == "rook" or self.figure.role == "queen":
                block_up = False
                block_right = False
                block_left = False
                block_down = False
                for i in range(1, 9):
                    if check_collision(list[:16], self.col + i, self.row ) == False:
                        if block_right == False:
                            if check_collision(list[16:], self.col + i, self.row) == False:
                                if self.col + i == col and self.row == row:
                                    self.move(col,row,game)
                            else:
                                if self.col + i == col and self.row == row:
                                    for fg in list[16:]:
                                        if fg.col == col and fg.row == row:
                                            if fg.figure.role != "king":
                                                fg.die()
                                                self.move(col, row,game)
                                block_right = True
                    else:
                        block_right = True
                    if check_collision(list[:16], self.col - i, self.row ) == False:
                        if block_left == False:
                            if check_collision(list[16:], self.col - i, self.row) == False:
                                if self.col - i == col and self.row == row:
                                    self.move(col,row,game)
                            else:
                                if self.col - i == col and self.row == row:
                                    for fg in list[16:]:
                                        if fg.col == col and fg.row == row:
                                            if fg.figure.role != "king":
                                                fg.die()
                                                self.move(col, row,game)
                                block_left = True
                    else:
                        block_left = True
                    if check_collision(list[:16], self.col, self.row + i ) == False:
                        if block_down == False:
                            if check_collision(list[16:], self.col, self.row + i) == False:
                                if self.col == col and self.row + i == row:
                                    self.move(col,row,game)
                            else:
                                if self.col == col and self.row + i == row:
                                    for fg in list[16:]:
                                        if fg.col == col and fg.row == row:
                                            if fg.figure.role != "king":
                                                fg.die()
                                                self.move(col, row,game)
                                block_down = True
                    else:
                        block_down = True
                    if check_collision(list[:16], self.col, self.row - i ) == False:
                        if block_up == False:
                            if check_collision(list[16:], self.col, self.row - i) == False:
                                if self.col == col and self.row - i == row:
                                    self.move(col,row,game)
                            else:
                                if self.col == col and self.row - i == row:
                                    for fg in list[16:]:
                                        if fg.col == col and fg.row == row:
                                            if fg.figure.role != "king":
                                                fg.die()
                                                self.move(col, row,game)
                                block_up = True
                    else:
                        block_up = True
            if self.figure.role == "king":
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if col == self.col + i and row == self.row + j:
                            if (i != 0 or j != 0) and check_collision(list[:16], self.col + i, self.row + j) == False:
                                if check_collision(list[16:], self.col + i, self.row + j) == False:
                                    self.move(col,row, game)
                                else:
                                    for fg in list[16:]:
                                        if fg.col == self.col + i and fg.row == self.row + j:
                                            if fg.figure.role != "king":
                                                fg.die()
                                                self.move(col,row, game)


    def show_steps(self,list):
        if self.figure.role == "pawn":
            if self.row > 6:
                empty_col = False
                for fg in list:
                    if fg.col == self.col and fg.row == self.row - 2:
                        empty_col = True
                if empty_col == False:
                    show_step(self.figure.screen, self.col, self.row - 2)
            empty_col = False
            for fg in list:
                if fg.col == self.col and fg.row == self.row -1:
                    empty_col = True
            if empty_col == False:
                show_step(self.figure.screen, self.col, self.row - 1)
            new_row = self.row - 1
            new_col1 = self.col - 1
            new_col2 = self.col + 1
            for fg in list[16:]:
                if fg.row == new_row:
                    if fg.col == new_col1:
                        if fg.figure.role != "king":
                            show_step(self.figure.screen,new_col1, new_row, (150, 255, 150))
                    if fg.col == new_col2:
                        if fg.figure.role != "king":
                            show_step(self.figure.screen, new_col2, new_row, (150, 255, 150))
        if self.figure.role == "knight":
           for i in range(-1,2,2):
               for j in range(-2,3,4):
                   if check_collision( list[:16], self.col + i, self.row + j) == False:
                       if check_collision( list[16:], self.col + i, self.row + j) == False:
                           show_step(self.figure.screen, self.col + i, self.row + j)
                       else:
                           king = True
                           for fg in list[16:]:
                               if fg.col == self.col + i and fg.row == self.row + j:
                                   if fg.figure.role == "king":
                                       king = False
                           if king == True:
                               show_step(self.figure.screen, self.col + i, self.row + j, (150, 255, 150))
                   if check_collision( list[:16], self.col + j, self.row + i) == False:
                       if check_collision( list[16:], self.col + j, self.row + i) == False:
                            show_step(self.figure.screen, self.col + j, self.row + i)
                       else:
                           king = True
                           for fg in list[16:]:
                               if fg.col == self.col + j and fg.row == self.row + i:
                                   if fg.figure.role == "king":
                                       king = False
                           if king == True:
                               show_step(self.figure.screen, self.col + j, self.row + i, (150, 255, 150))

        if self.figure.role == "bishop" or self.figure.role == "queen":
            block_up_left = False
            block_up_right = False
            block_down_left = False
            block_down_right = False
            for i in range(1,9):
                if check_collision(list[:16], self.col + i, self.row + i) == False:
                    if block_down_right == False:
                        if check_collision(list[16:], self.col + i, self.row + i) == False:
                            show_step(self.figure.screen, self.col + i, self.row + i)
                        else:
                            for fg in list[16:]:
                                if fg.col == self.col + i and fg.row == self.row + i:
                                    if fg.figure.role != "king":
                                        show_step(self.figure.screen, self.col + i, self.row + i, (150,255,150))
                            block_down_right = True
                else:
                    block_down_right = True
                if check_collision(list[:16], self.col + i, self.row - i) == False:
                    if block_up_right == False:
                        if check_collision(list[16:], self.col + i, self.row - i) == False:
                            show_step(self.figure.screen, self.col + i, self.row - i)
                        else:
                            for fg in list[16:]:
                                if fg.col == self.col + i and fg.row == self.row - i:
                                    if fg.figure.role != "king":
                                        show_step(self.figure.screen, self.col + i, self.row - i, (150,255,150))
                            block_up_right = True
                else:
                    block_up_right = True
                if check_collision(list[:16], self.col - i, self.row + i) == False:
                    if block_down_left == False:
                        if check_collision(list[16:], self.col - i, self.row + i) == False:
                            show_step(self.figure.screen, self.col - i, self.row + i)
                        else:
                            for fg in list[16:]:
                                if fg.col == self.col - i and fg.row == self.row + i:
                                    if fg.figure.role != "king":
                                        show_step(self.figure.screen, self.col - i, self.row + i, (150,255,150))
                            block_down_left = True
                else:
                    block_down_left = True
                if check_collision(list[:16], self.col - i, self.row - i) == False:
                    if block_up_left == False:
                        if check_collision(list[16:], self.col - i, self.row - i) == False:
                            show_step(self.figure.screen, self.col - i, self.row - i)
                        else:
                            for fg in list[16:]:
                                if fg.col == self.col - i and fg.row == self.row - i:
                                    if fg.figure.role != "king":
                                        show_step(self.figure.screen, self.col - i, self.row - i, (150,255,150))
                            block_up_left = True
                else:
                    block_up_left = True
        if self.figure.role == "rook" or self.figure.role == "queen":
            block_up = False
            block_down = False
            block_left = False
            block_right = False
            for i in range(1,9):
                if check_collision(list[:16], self.col + i, self.row) == False:
                    if block_right == False:
                        if check_collision(list[16:], self.col + i, self.row) == False:
                            show_step(self.figure.screen, self.col + i, self.row)
                        else:
                            for fg in list[16:]:
                                if fg.col == self.col + i and fg.row == self.row:
                                    if fg.figure.role != "king":
                                        show_step(self.figure.screen, self.col + i, self.row, (150, 255, 150))
                            block_right = True
                else:
                    block_right = True
                if check_collision(list[:16], self.col - i, self.row) == False:
                    if block_left == False:
                        if check_collision(list[16:], self.col - i, self.row) == False:
                            show_step(self.figure.screen, self.col - i, self.row)
                        else:
                            for fg in list[16:]:
                                if fg.col == self.col - i and fg.row == self.row:
                                    if fg.figure.role != "king":
                                        show_step(self.figure.screen, self.col - i, self.row, (150, 255, 150))
                            block_left = True
                else:
                    block_left = True
                if check_collision(list[:16], self.col, self.row + i) == False:
                    if block_down == False:
                        if check_collision(list[16:], self.col, self.row + i) == False:
                            show_step(self.figure.screen, self.col, self.row + i)
                        else:
                            for fg in list[16:]:
                                if fg.col == self.col and fg.row == self.row + i:
                                    if fg.figure.role != "king":
                                        show_step(self.figure.screen, self.col, self.row + i, (150, 255, 150))
                            block_down = True
                else:
                    block_down = True
                if check_collision(list[:16], self.col, self.row - i) == False:
                    if block_up == False:
                        if check_collision(list[16:], self.col, self.row - i) == False:
                            show_step(self.figure.screen, self.col, self.row - i)
                        else:
                            for fg in list[16:]:
                                if fg.col == self.col and fg.row == self.row - i:
                                    if fg.figure.role != "king":
                                        show_step(self.figure.screen, self.col, self.row - i, (150, 255, 150))
                            block_up = True
                else:
                    block_up = True
        if self.figure.role == "king":
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (i != 0 or j != 0) and check_collision(list[:16], self.col + i, self.row + j) == False:
                        if check_collision(list[16:], self.col + i, self.row + j) == False:
                            show_step(self.figure.screen, self.col + i, self.row + j)
                        else:
                            for fg in list[16:]:
                                if fg.col == self.col + i and fg.row == self.row + j:
                                    if fg.figure.role != "king":
                                        show_step(self.figure.screen, self.col + i, self.row + j, (150, 255, 150))
    def show_steps_list(self,list,color = "black"):
        result_steps = []
        result_atack = []
        if self.figure.role == "pawn":
            if (self.row > 6 and color == "black") or (self.row < 3 and color == "white"):
                empty_col = False
                for fg in list:
                    if fg.col == self.col:
                        if (fg.row == self.row - 2 and color == "black") or (fg.row == self.row + 2 and color == "white"):
                            empty_col = True
                if empty_col == False:
                    if color == "black":
                        result_steps.append( [self.col, self.row - 2])
                    else:
                        result_steps.append( [self.col, self.row + 2])
            empty_col = False
            for fg in list:
                if fg.col == self.col:
                    if (fg.row == self.row - 1 and color == "black") or (fg.row == self.row + 1 and color == "white"):
                        empty_col = True
            if empty_col == False:
                if color == "black":
                    result_steps.append( [self.col, self.row - 1])
                else:
                    result_steps.append( [self.col, self.row + 1])
            if color == "black":
                new_row = self.row - 1
            else:
                new_row = self.row + 1
            new_col1 = self.col - 1
            new_col2 = self.col + 1
            for fg in list[16:]:
                if fg.row == new_row:
                    if fg.col == new_col1:
                            result_atack.append( [new_col1, new_row] )
                    if fg.col == new_col2:
                            result_atack.append( [new_col2, new_row] )
        if self.figure.role == "knight":
           for i in range(-1,2,2):
               for j in range(-2,3,4):
                   if check_collision( list[:16], self.col + i, self.row + j) == False:
                       if check_collision( list[16:], self.col + i, self.row + j) == False:
                           result_steps.append( [self.col + i, self.row + j] )
                       else:
                            result_atack.append([self.col + i, self.row + j])
                   if check_collision( list[:16], self.col + j, self.row + i) == False:
                       if check_collision( list[16:], self.col + j, self.row + i) == False:
                            result_steps.append([self.col + j, self.row + i])
                       else:
                            result_atack.append([self.col + j, self.row + i])

        if self.figure.role == "bishop" or self.figure.role == "queen":
            block_up_left = False
            block_up_right = False
            block_down_left = False
            block_down_right = False
            for i in range(1,9):
                if check_collision(list[:16], self.col + i, self.row + i) == False:
                    if block_down_right == False:
                        if check_collision(list[16:], self.col + i, self.row + i) == False:
                            result_steps.append([self.col + i, self.row + i])
                        else:
                            result_atack.append([self.col + i, self.row + i])
                            block_down_right = True
                else:
                    block_down_right = True
                if check_collision(list[:16], self.col + i, self.row - i) == False:
                    if block_up_right == False:
                        if check_collision(list[16:], self.col + i, self.row - i) == False:
                            result_steps.append([self.col + i, self.row - i])
                        else:
                            result_atack.append([self.col + i, self.row - i])
                            block_up_right = True
                else:
                    block_up_right = True
                if check_collision(list[:16], self.col - i, self.row + i) == False:
                    if block_down_left == False:
                        if check_collision(list[16:], self.col - i, self.row + i) == False:
                            result_steps.append([self.col - i, self.row + i])
                        else:
                            result_atack.append([self.col - i, self.row + i])
                            block_down_left = True
                else:
                    block_down_left = True
                if check_collision(list[:16], self.col - i, self.row - i) == False:
                    if block_up_left == False:
                        if check_collision(list[16:], self.col - i, self.row - i) == False:
                            result_steps.append([ self.col - i, self.row - i])
                        else:
                            result_atack.append([self.col - i, self.row - i])
                            block_up_left = True
                else:
                    block_up_left = True
        if self.figure.role == "rook" or self.figure.role == "queen":
            block_up = False
            block_down = False
            block_left = False
            block_right = False
            for i in range(1,9):
                if check_collision(list[:16], self.col + i, self.row) == False:
                    if block_right == False:
                        if check_collision(list[16:], self.col + i, self.row) == False:
                            result_steps.append([self.col + i, self.row])
                        else:
                            result_atack.append([self.col + i, self.row])
                            block_right = True
                else:
                    block_right = True
                if check_collision(list[:16], self.col - i, self.row) == False:
                    if block_left == False:
                        if check_collision(list[16:], self.col - i, self.row) == False:
                            result_steps.append([self.col - i, self.row])
                        else:
                            result_atack.append([self.col - i, self.row])
                            block_left = True
                else:
                    block_left = True
                if check_collision(list[:16], self.col, self.row + i) == False:
                    if block_down == False:
                        if check_collision(list[16:], self.col, self.row + i) == False:
                            result_steps.append([self.col, self.row + i])
                        else:
                            result_atack.append( [self.col, self.row + i])
                            block_down = True
                else:
                    block_down = True
                if check_collision(list[:16], self.col, self.row - i) == False:
                    if block_up == False:
                        if check_collision(list[16:], self.col, self.row - i) == False:
                            result_steps.append([self.col, self.row - i])
                        else:
                            result_atack.append([self.col, self.row - i])
                            block_up = True
                else:
                    block_up = True
        if self.figure.role == "king":
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (i != 0 or j != 0) and check_collision(list[:16], self.col + i, self.row + j) == False:
                        if check_collision(list[16:], self.col + i, self.row + j) == False:
                            result_steps.append([self.col + i, self.row + j])
                        else:
                            result_atack.append([self.col + i, self.row + j])
        return result_steps,result_atack

    def mat(self, step_list, list):
        if self.figure.role == "king":
            for i in range(-1,2):
                for j in range(-1,2):
                    if self.col + i > 0 and self.col + i < 9 and self.row + j > 0 and self.row + j < 9:
                        if (i != 0 or j != 0) and check_collision(list, self.col + i, self.row + j) == False:
                            attack = False
                            for step in step_list:
                                if self.col + i == step[0] and self.row + j == step[1]:
                                    attack = True
                            if attack == False:
                                return False
            return True



def draw_square(screen, size, x, y, color):
    rect_1_rect = pg.Rect((x, y), (size, size))
    if color == "black":
        rect_1_color = (50, 50, 50)
    if color == "white":
        rect_1_color = (255,255,255)
    rect_1_width = 0
    pg.draw.rect(screen, rect_1_color, rect_1_rect, rect_1_width)

def draw_square_contur(screen, size, x, y, width):
    rect_1_rect = pg.Rect((x, y), (size, size))
    rect_1_color = (50, 50, 50)
    rect_1_width = width
    pg.draw.rect(screen, rect_1_color, rect_1_rect, rect_1_width)

def main():
    pg.init()
    pg.display.set_caption("chess simulator")
    screen = pg.display.set_mode((640,480))
    running = True
    image = pg.image.load("images/menu/background.jpg")
    image2 = pg.image.load("images/game/background.jpg")
    chose = 0
    ch = 0
    gamestate = 0
    game_start = False
    current_game = draw.game()

    #инициализация фигур
    white_pawn = figure("white", "pawn", screen)
    black_pawn = figure("black", "pawn", screen)

    white_rook = figure("white", "rook", screen)
    black_rook = figure("black", "rook", screen)

    white_bishop = figure("white", "bishop", screen)
    black_bishop = figure("black", "bishop", screen)

    white_knight = figure("white", "knight", screen)
    black_knight = figure("black", "knight", screen)

    white_king = figure("white", "king", screen)
    black_king = figure("black", "king", screen)

    white_queen = figure("white","queen", screen)
    black_queen = figure("black", "queen", screen)

    # инициализация белых фигур
    black_teem = []
    white_teem = []

    # первые 8 фигур в списке пешки
    for i in range(1, 9):
        white_pawn_unit = unit(white_pawn, i, 2)
        white_teem.append(white_pawn_unit)
        black_pawn_unit = unit(black_pawn, i, 7)
        black_teem.append(black_pawn_unit)

    # вторые 2 фигуры ладьи
    white_teem.append(unit(white_rook, 1, 1))
    white_teem.append(unit(white_rook, 8, 1))
    ###
    black_teem.append(unit(black_rook, 1, 8))
    black_teem.append(unit(black_rook, 8, 8))

    # третьи 2 фигуры кони 11 - 12
    white_teem.append(unit(white_knight, 2, 1))
    white_teem.append(unit(white_knight, 7, 1))
    ###
    black_teem.append(unit(black_knight, 2, 8))
    black_teem.append(unit(black_knight, 7, 8))

    # четвертые 2 фигуры слоны 13-14
    white_teem.append(unit(white_bishop, 3, 1))
    white_teem.append(unit(white_bishop, 6, 1))
    ###
    black_teem.append(unit(black_bishop, 3, 8))
    black_teem.append(unit(black_bishop, 6, 8))

    # пятнадцатая фигура - ферзь
    white_teem.append(unit(white_queen, 5, 1))
    black_teem.append(unit(black_queen, 5, 8))

    # шестнадцатая фигура - король
    white_teem.append(unit(white_king, 4, 1))
    black_teem.append(unit(black_king, 4, 8))

    # выбор фигуры
    chose_figure = 0

    while running:
        pg.display.flip()

        # режим меню
        if gamestate == 0:
            # фон рисуется
            screen.blit(image, (0, 0))
            font = pg.font.Font(None, 70)
            game = font.render("Chess Simulator", True, (255, 255, 255))
            screen.blit(game, [130, 100])
            font = pg.font.Font(None, 50)
            play = None
            if chose != 1:
                if game_start == False:
                    play = font.render("PLAY", True, (255, 255, 255))
                    screen.blit(play, [270, 200])
                else:
                    play = font.render("CONTINUE", True, (230, 200, 255))
                    screen.blit(play, [230, 200])
                    if chose != 3:
                        playnew = font.render("NEW GAME", True, (220, 255, 220))
                    else:
                        playnew = font.render("NEW GAME", True, (255, 255, 0))

                    screen.blit(playnew, [230, 268])
            else:
                if game_start == False:
                    play = font.render("PLAY", True, (255, 255, 0))
                    screen.blit(play, [270, 200])
                else:
                    play = font.render("CONTINUE", True, (230, 200, 0))
                    screen.blit(play, [230, 200])
                    if chose != 3:
                        playnew = font.render("NEW GAME", True, (220, 255, 220))
                    else:
                        playnew = font.render("NEW GAME", True, (255, 255, 0))
                    screen.blit(playnew, [230, 268])
            if chose != 2:
                options = font.render("OPTIONS", True, (255, 255, 255))
                screen.blit(options, [240, 235])
            else:
                options = font.render("OPTIONS", True, (255, 255, 0))
                screen.blit(options, [240, 235])
            # все остальное
            pos = pg.mouse.get_pos()
            mouse_x, mouse_y = pos[0], pos[1]
            if mouse_x > 270 and mouse_x < 270 + play.get_width() and mouse_y > 200 and mouse_y < 200 + play.get_height():
                chose = 1
                for ev in pg.event.get():
                    if ev.type == pg.MOUSEBUTTONDOWN:
                        gamestate = 1
                        game_start = True
                        screen.fill((255, 255, 255))

            elif mouse_x > 240 and mouse_x < 240 + options.get_width() and mouse_y > 235 and mouse_y < 235 + options.get_height():
                chose = 2
            elif game_start == True:
                if mouse_x > 230 and mouse_x < 230 + playnew.get_width() and mouse_y > 268 and mouse_y < 268 + playnew.get_height():
                    chose = 3
                    for ev in pg.event.get():
                        if ev.type == pg.MOUSEBUTTONDOWN:
                            game_start = False
                            # инициализация белых фигур
                            black_teem = []
                            white_teem = []

                            # первые 8 фигур в списке пешки
                            for i in range(1, 9):
                                white_pawn_unit = unit(white_pawn, i, 2)
                                white_teem.append(white_pawn_unit)
                                black_pawn_unit = unit(black_pawn, i, 7)
                                black_teem.append(black_pawn_unit)

                            # вторые 2 фигуры ладьи
                            white_teem.append(unit(white_rook, 1, 1))
                            white_teem.append(unit(white_rook, 8, 1))
                            ###
                            black_teem.append(unit(black_rook, 1, 8))
                            black_teem.append(unit(black_rook, 8, 8))

                            # третьи 2 фигуры кони 11 - 12
                            white_teem.append(unit(white_knight, 2, 1))
                            white_teem.append(unit(white_knight, 7, 1))
                            ###
                            black_teem.append(unit(black_knight, 2, 8))
                            black_teem.append(unit(black_knight, 7, 8))

                            # четвертые 2 фигуры слоны 13-14
                            white_teem.append(unit(white_bishop, 3, 1))
                            white_teem.append(unit(white_bishop, 6, 1))
                            ###
                            black_teem.append(unit(black_bishop, 3, 8))
                            black_teem.append(unit(black_bishop, 6, 8))

                            # пятнадцатая фигура - ферзь
                            white_teem.append(unit(white_queen, 5, 1))
                            black_teem.append(unit(black_queen, 5, 8))

                            # шестнадцатая фигура - король
                            white_teem.append(unit(white_king, 4, 1))
                            black_teem.append(unit(black_king, 4, 8))
                            chose_figure = 0
                else:
                    chose = 0
            else:
                chose = 0
        # режим игры
        if gamestate == 1:
            # фон
            screen.blit(image2,(0,0))
            # логка игры
            for i in range(1,9):
                for j in range(1,9):
                    k = (j+1) + i*9
                    if k%2 == 0:
                        draw_square(screen,30,200 + (j-1)*30 ,110 + (i-1)*30,"black")
                    else:
                        draw_square(screen, 30, 200 + (j - 1) * 30, 110 + (i - 1) * 30, "white")
            draw_square_contur(screen,242, 198, 108, 2)



            # инициальзация легенды поля

            legend = pg.font.Font(None, 30)
            for i in range(1,9):
                num = legend.render(str(i), True, (0, 0, 0))
                screen.blit(num, [180, 118 + (i-1)*30])
            for i in range(1,9):
                letter = chr(ord('a') + (i-1))
                let = legend.render(letter, True, (0,0,0))
                screen.blit(let, [208 + (i-1)*30, 355 ])



            pos = pg.mouse.get_pos()
            mouse_x, mouse_y = pos[0], pos[1]

            #  ПРОРИСОВКА ЮНИТОВ
            count = 1
            for un in black_teem:

                if un.enable:
                # проверки на действие
                    if un.highlight(mouse_x,mouse_y) == True:
                        un.light()
                        for ev in pg.event.get():
                            if ev.type == pg.MOUSEBUTTONDOWN:
                                chose_figure = count



                    un.draw()
                count = count + 1
            for un in white_teem:

                # проверки на действие
                if un.enable:
                    if un.highlight(mouse_x, mouse_y) == True:
                        un.light()

                    un.draw()

            y_cnt = 0
            col_cnt = 0
            for zombi in white_teem:
                if zombi.enable == False:
                    x = 30 + col_cnt*28
                    y = 110 + y_cnt*45
                    y_cnt = y_cnt + 1
                    if y_cnt >= 5:
                        col_cnt = col_cnt + 1
                        y_cnt = 0
                    screen.blit(zombi.figure.image_2, (x, y))
            y_cnt = 0
            col_cnt = 0
            for zombi in black_teem:
                if zombi.enable == False:
                    x = 460 + col_cnt * 28
                    y = 110 + y_cnt * 45
                    if y_cnt >= 5:
                        col_cnt = col_cnt + 1
                        y_cnt = 0
                    screen.blit(zombi.figure.image_2, (x, y))

            if current_game.black == True:
                if chose_figure != 0:
                    black_teem[chose_figure-1].red_light()
                    black_teem[chose_figure-1].show_steps( black_teem + white_teem)
                    for ev in pg.event.get():
                        if ev.type == pg.MOUSEBUTTONDOWN:
                            black_teem[chose_figure-1].make_step(mouse_x,mouse_y, black_teem + white_teem, current_game)
            else:
                chose_figure = random.randint(1,16)
                st,at = white_teem[chose_figure - 1].show_steps_list(white_teem + black_teem,"white")
                steps = st + at
                if len(steps) != 0:
                    white_teem[chose_figure - 1].red_light()
                    chosing_step = random.randint(1,len(steps) ) - 1
                    new_x = 200 + (steps[chosing_step][0]-1) * 30 + 15
                    new_y = 110 + (steps[chosing_step][1]-1) * 30 + 15
                    white_teem[chose_figure-1].make_step(new_x, new_y, white_teem + black_teem, current_game, color = "white")
                    chose_figure = 0



            black_future_steps = []
            black_future_attacks = []
            white_future_steps = []
            white_future_attacks = []

            for fg in black_teem:
                st,at = fg.show_steps_list(black_teem + white_teem)
                black_future_steps = black_future_steps + st
                black_future_attacks = black_future_attacks + at

            for cords in black_future_attacks:
                if white_teem[15].col == cords[0] and white_teem[15].row == cords[1]:
                    font = pg.font.Font(None, 30)
                    check = font.render("CHECK", True, (190,0,0))
                    screen.blit(check,[150,70])


            # логика внутриигрового меню
            font = pg.font.Font(None, 50)
            if ch == 0:
                pause = font.render("pause", True, (0, 0, 0))
            else:
                pause = font.render("pause", True, (255, 255, 0))
            screen.blit(pause, [260, 60])

            if mouse_x > 260 and mouse_x < 260 + pause.get_width() and mouse_y > 60 and mouse_y < 60 + pause.get_height():
                ch = 1
                if ev.type == pg.MOUSEBUTTONDOWN:
                    gamestate = 0
            else:
                ch = 0
            if mouse_x < 200 or mouse_y < 110 or mouse_x > 440 or mouse_y > 350:
                for ev in pg.event.get():
                    if ev.type == pg.MOUSEBUTTONDOWN:
                        chose_figure = 0
        # выход
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                running = False
if __name__ == "__main__":
    main()