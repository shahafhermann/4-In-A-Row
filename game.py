#############################################################
# FILE : game.py
# WRITER : Shahaf Hermann , shahaf.hermann , 308156983
# EXERCISE : intro2cs ex12 2017-2018s
# DESCRIPTION: The Game class - The main engine of the game, runs the
# algorithm and keeps track of game status.
#############################################################


class Game:

    PLAYER_ONE = 0
    PLAYER_TWO = 1
    DRAW = 2
    HEIGHT = 6
    WIDTH = 7
    WIN = 4
    EMPTY_SPOT = "_"
    ILLEGAL_MOVE = "Illegal move"


    def __init__(self):
        """
        Initialize the Game object.
        """
        self.__board = [["_" for _ in range(self.WIDTH)] for __ in range(
            self.HEIGHT)]
        self.__dict_col = {k: 0 for k in range(1,self.WIDTH + 1)}
        self.__cur_player = self.PLAYER_ONE

    def make_move(self, column):
        """
        The function checks whether the column that the player wants to
        place a disk is valid (ie the column not full, whether it is in
        the board and whether the game is not finished).
        :param column: A number representing the column in which you want
                        to place a disk.
        :return: If the column is valid, the function updates and returns
        the updated board. If the column is invalid the function returns false.
        """
        if self.in_borders(column):
            if self.is_empty(column) and not self.game_over():
                row = self.HEIGHT - self.__dict_col[column] #The lowest
                                            # available line in this column
                self.__dict_col[column] += 1
                cur_player = self.get_current_player()
                self.set_board(row, column, cur_player)
                self.set_current_player(cur_player)
                return self.__board
        return False

    def set_board(self, row, col, player):
        """
        The function get 3 numbers representing a row, column and value
        respectively. The function changes the value of the board in
        (row, column) to 'num' val.
        :param row: A number representing the row on board
        :param col: A number representing the column on board
        :param num: A number representing the player number
        :return:
        """
        self.__board[row - 1][col - 1] = player
        return self.__board

    def is_empty(self, col):
        """
        The function checks whether the column in which the player has chosen
        to put a disk is legal, ie is not full.
        :param col: A number representing a column
        :return: True if is a valid column
        """
        try:
            if self.__dict_col[col] < self.HEIGHT:
                return True
        except Exception:
            print(self.ILLEGAL_MOVE)

    def in_borders(self, col):
        """
        The function checks whether the column the player has selected is
        within the borders of the board.
        :param col: A number representing a column
        :return: True if in borders
        """
        try:
            if col >= 1 and col <= self.WIDTH:
                return True
        except Exception:
            print(self.ILLEGAL_MOVE)

    def game_over(self):
        """
        The function checks if the game is over. That is, if one of the
        players won or there is a draw.
        :return: True if game over
        """
        try:
            winning_seq, winner = self.get_winner()
            if winner != None:
                return True
        except Exception:
            print(self.ILLEGAL_MOVE)

    def get_winner(self):
        """
        The function checks whether one of the players has won or there is a
        draw.
        :return: returns PLAYER ONE the
        list of winning coordinates if player one won, or PLAYER TWO the
        list of winning coordinates if player two won , or DRAW if there is
        a draw. else return None if the game is not over yet.
        """
        b = self.__board
        for row in range(len(b)):
            for col in range(len(b[row])):
                if b[row][col] == self.PLAYER_ONE:
                    lst_idx = self.check_all_directions(row,col)
                    if lst_idx != []:
                        return lst_idx, self.PLAYER_ONE
                if b[row][col] == self.PLAYER_TWO:
                    lst_idx = self.check_all_directions(row,col)
                    if lst_idx != []:
                        return lst_idx, self.PLAYER_TWO
        if not self.filled_board():
            return None, None
        return None, self.DRAW

    def check_all_directions(self, row, col):
        """
        This function receives a coordinate and checks if therews any
        winning sequence around it (and including it). if exists, return the
        list of winning coordinates.
        """
        lst_idx = []
        if self.check_row(row, col) != lst_idx:
            lst_idx = self.check_row(row, col)
        elif self.check_col(row, col) != []:
            lst_idx = self.check_col(row, col)
        elif self.check_diag1(row, col) != []:
            lst_idx = self.check_diag1(row, col)
        elif self.check_diag2(row, col) != []:
            lst_idx = self.check_diag2(row, col)
        return lst_idx

    def check_row(self,pos_x,pos_y):
        """
        The function receives a coordinates that representing a row and a
        column on board and checks if there's a sequence of 4 of the same
        color in  a row. If yes, return a list of  the winning coordinates (
        as tuples).otherwise return an empty list.
        """
        idx = 1
        lst_idx = [(pos_x, pos_y)]
        while idx != self.WIN and pos_y + idx < self.WIDTH:
            if self.__board[pos_x][pos_y] == self.__board[pos_x][pos_y + idx]:
                lst_idx.append((pos_x, pos_y + idx))
                idx += 1
            else:
                break
        if len(lst_idx) == self.WIN:
            return lst_idx
        else:
            return []

    def check_col(self, pos_x, pos_y):
        """
        The function receives a coordinates that representing a row and a
        column on board and checks if there's a sequence of 4 of the same
        color in  a column. If yes, return a list of  the winning coordinates (
        as tuples).otherwise return an empty list.
        """
        idx = 1
        lst_idx = [(pos_x, pos_y)]
        while idx != self.WIN and pos_x - idx < self.HEIGHT and pos_x - idx \
                >= 0:
            if self.__board[pos_x][pos_y] == self.__board[pos_x - idx][pos_y]:
                lst_idx.append((pos_x - idx, pos_y))
                idx += 1
            else:
                break
        if len(lst_idx) == self.WIN:
            return lst_idx
        else:
            return []

    def check_diag1(self, pos_x, pos_y):
        """
        The function receives a coordinates that representing a row and a
        column on board and checks if there's a sequence of 4 of the same
        color in  a diagonal. If yes, return a list of  the winning
        coordinates (as tuples).otherwise return an empty list.
        """
        idx = 1
        lst_idx = [(pos_x, pos_y)]
        while idx != self.WIN and pos_x - idx < self.HEIGHT and pos_y + idx <\
                self.WIDTH and pos_x - idx >= 0:
            if self.__board[pos_x][pos_y] == self.__board[pos_x - idx][pos_y
                    + idx]:
                lst_idx.append((pos_x - idx,pos_y + idx))
                idx += 1
            else:
                break
        if len(lst_idx) == self.WIN:
            return lst_idx
        else:
            return []

    def check_diag2(self, pos_x, pos_y):
        """
        The function receives a coordinates that representing a row and a
        column on board and checks if there's a sequence of 4 of the same
        color in  a diagonal. If yes, return a list of  the winning
        coordinates (as tuples).otherwise return an empty list.
       """
        idx = 1
        lst_idx = [(pos_x, pos_y)]
        while idx != self.WIN and pos_x - idx < self.HEIGHT and pos_y - idx >= 0 \
                and pos_x - idx >= 0:
            if self.__board[pos_x][pos_y] == self.__board[pos_x - idx][pos_y
                    - idx]:
                lst_idx.append((pos_x - idx,pos_y - idx))
                idx += 1
            else:
                break
        if len(lst_idx) == self.WIN:
            return lst_idx
        else:
            return []

    def filled_board(self):
        """
        The function checks whether the game board is full.
        :return: True if its full. else return False.
        """
        for val in self.__dict_col.values():
            if val != self.HEIGHT:
                return False
        return True

    def get_player_at(self, row, col):
        """
        :param row: A number representing the row on board
        :param col: A number representing the column on board
        :return: The function returns which disk is in (row,col) in board.
        """
        if self.__board[row][col] == self.EMPTY_SPOT:
            return None
        return self.__board[row][col]

    def get_current_player(self):
        """
        :return:The function returns the current player.
        """
        return self.__cur_player

    def set_current_player(self, player):
        """
        :param player: The function change the current player to the next
        player.
        """
        if player == self.PLAYER_ONE:
            self.__cur_player = self.PLAYER_TWO
        else:
            self.__cur_player = self.PLAYER_ONE

    def get_board(self):
        """
        :return: The function returns the game board.
        """
        return self.__board
