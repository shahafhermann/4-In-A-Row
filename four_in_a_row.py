#############################################################
# FILE : four_in_a_row.py
# WRITER : Shahaf Hermann , shahaf.hermann , 308156983
# EXERCISE : intro2cs ex12 2017-2018s
# DESCRIPTION: The main script that runs the game and creates the GUI.
#############################################################

############################################################
# Imports
############################################################

from tkinter import *
from tkinter import messagebox
from game import Game
from communicator import Communicator
from ai import AI
import sys

############################################################
# Constants
############################################################

ERR_NUM_ARGS = "ERROR: Wrong number of arguments."
ILLEGAL_ARGS = "Illegal program arguments."
SERVER = True
HUMAN = True
HEIGHT = 6
WIDTH = 7
PORT_MIN = 1000
PORT_MAX = 65535
HUMAN_ARG = "human"
AI_ARG = "ai"
WIN_NAME_SRVR_HUMAN = "Server - Player"
WIN_NAME_SRVR_AI = "Server - Computer"
WIN_NAME_CLNT_HUMAN = "Client - Player"
WIN_NAME_CLNT_AI = "Client - Computer"

############################################################
# Main
############################################################


class GUI:

    # Class constants
    # # Messages
    FULL_BOARD_TITLE = "Board is full!"
    FULL_BOARD_MSG = "There are no more available moves.\nIt's a tie!"
    FULL_COL_TITLE = "Invalid Move!"
    FULL_COL_MSG = "This column is full."
    END_GAME_MSG = "Congratulations!"
    RED_WINNER_MSG = "RED Player is the winner!"
    YELLOW_WINNER_MSG = "YELLOW Player is the winner!"
    # # Graphics - The folder "graphics" must be at the same directory as
    # the game files!
    RED_IMG_PATH = "graphics\Red.png"
    YELLOW_IMG_PATH = "graphics\yellow.png"
    RED_SML_IMG_PATH = "graphics\Red_small.png"
    YELLOW_SML_IMG_PATH = "graphics\yellow_small.png"
    BOARD_IMG_PATH = "graphics\Board.png"
    BG_IMG_PATH = "graphics\BG.png"
    STATUS_BG_IMG_PATH = "graphics\Status_BG.png"
    STATUS_TXT_RED_PATH = "graphics\Status_txt_red.png"
    STATUS_TXT_YELLOW_PATH = "graphics\Status_txt_yellow.png"
    TITLE_IMG_PATH = "graphics\Title.png"
    WIN_IMG_PATH = "graphics\White.png"
    TOKEN_BG_COLOR = "#002ae0"
    INS_FRM_BGC = "#c29f7b"
    CANVAS_W = 525  # width
    CANVAS_H = 455  # height
    INS_W = 525  # width
    INS_H = 80  # height
    HLTN = 0  # highlightthickness option - set to 0 for all frames and labels
    BW = 0  # borderwidth option - set to 0 for all frames and labels
    TOKEN_PXL_SIZE = 70
    PXL_POS_Y = 21
    PXL_POS_X = 23
    # # Game Logics
    POP_RESPONSE = "ok"
    # Class variables
    board_dict = {}
    col_limit = [0 for _ in range(WIDTH)]
    insertion_col = 0
    winning_dict = {}
    update_lst = []

    def __init__(self, root, game, board, comm, ai):
        """
        Initialize the GUI. If an AI is playing, make an AI move.
        :param root: The main TKinter window.
        :param game: Object of type Game, representing the current game.
        :param board: The starting board state.
        :param comm: A Communicator object for establishing server/client
        connection.
        :param ai: An AI object that plays the game when it is chosen to.
        """
        self.__game = game
        self.__board = board
        self.__root = root
        self.__ai = ai
        self.__set_background(root)
        self.__set_title(root)
        self.__set_insertion_frame(root)
        self.__set_main_canvas(root)
        self.__set_status_frame(root)
        for row in range(HEIGHT):
            for col in range(WIDTH):
                self.board_dict[(row, col)] = (self.PXL_POS_Y + (
                    row*self.TOKEN_PXL_SIZE), self.PXL_POS_X + (
                                                   col*self.TOKEN_PXL_SIZE))
        self.__comm = comm
        self.__comm.connect()
        self.__comm.bind_action_to_message(self.__decode_msg)
        if not HUMAN and SERVER:
            self.move_ai_turn()

    def __decode_msg(self, msg):
        """
        Upon receiving a message from the Server/Client, update the
        relevant parameters and the board state.
        :param msg: a string of a number representing the column that was
        played and should be updated.
        :return: None.
        """
        for i in range(WIDTH):
            self.__optionsLST[i].grid()
        self.insertion_col = int(msg)
        self.move_turn(self.insertion_col)
        if self.col_limit[int(msg)] == HEIGHT:
            self.col_limit[int(msg)] += 1
        if self.__ai:
            self.move_ai_turn()

    def __set_title(self, root):
        """
        Set the GUI title.
        :param root: The parent window.
        :return: None.
        """
        title_img = PhotoImage(file=self.TITLE_IMG_PATH)
        self.__title = Label(root, image=title_img, borderwidth=self.BW,
                             highlightthickness=self.HLTN)
        self.__title.image = title_img
        self.__title.pack(side=TOP, pady=30)

    def __set_background(self, root):
        """
        Set the game's background image.
        :param root: The parent window.
        :return: None.
        """
        self.__bg_img = PhotoImage(file=self.BG_IMG_PATH)
        self.__bg_label = Label(root, image=self.__bg_img)
        self.__bg_label.image = self.__bg_img
        self.__bg_label.place(x=0, y=0, anchor=NW)

    def __set_main_canvas(self, root):
        """
        Initialize the main canvas of the GUI.
        :param root: The parent window.
        :return: None.
        """
        self.__main_canvas = Canvas(root, width=self.CANVAS_W,
                                    height=self.CANVAS_H,
                                    highlightthickness=self.HLTN)
        self.__boardIMG = PhotoImage(file=self.BOARD_IMG_PATH)
        self.__main_canvas.create_image(0, 0, anchor=NW, image=self.__boardIMG)
        self.__main_canvas.image = self.__boardIMG
        self.__main_canvas.pack(side=TOP, padx=60)

    def __set_insertion_frame(self, root):
        """
        Initialize the insertion frame of the GUI, and bind actions to the
        corresponding labels.
        :param root: The parent window.
        :return: None.
        """
        self.__insertion_frame = Frame(root, width=self.INS_W,
                                       height=self.INS_H, bg=self.INS_FRM_BGC,
                                       highlightthickness=self.HLTN)
        self.__insertion_frame.pack(side=TOP, padx=60)
        self.__optionsLST = []
        for i in range(WIDTH):
            self.__option = PhotoImage(file=self.RED_IMG_PATH)
            self.__optionsLST.append(Label(self.__insertion_frame,
                    image=self.__option, state="disabled", bg=self.INS_FRM_BGC,
                                                highlightthickness=self.HLTN))
            self.__optionsLST[i].image = self.__option
            self.__optionsLST[i].grid(row=0, column=i, ipadx=3)
            if not SERVER:
                self.__optionsLST[i].grid_remove()
            if HUMAN:
                self.__optionsLST[i].bind("<Enter>", lambda event, k=i:
                  self.__optionsLST[k].config(state="normal", cursor="hand2"))
                self.__optionsLST[i].bind("<Leave>", lambda event, k=i:
                  self.__optionsLST[k].config(state="disabled", cursor=None))
                self.__optionsLST[i].bind("<Button-1>", lambda event, k=i:
                    self.__optionsLST[k].config(command=self.move_turn(k)))
                self.__optionsLST[i].bind("<ButtonRelease-1>", lambda event,
                  k=i: self.__optionsLST[k].config(command=self.__send_msg(k)))

    def __set_status_frame(self, root):
        """
        Initialize the status frame of the GUI.
        :param root: The parent window.
        :return: None.
        """
        self.__status_frame = Frame(root, highlightthickness=self.HLTN,
                                    borderwidth=self.BW)
        self.__status_frame.pack(side=TOP, fill=X)
        status_bg = PhotoImage(file=self.STATUS_BG_IMG_PATH)
        self.__statusBG = Label(self.__status_frame, image=status_bg,
                            highlightthickness=self.HLTN, borderwidth=self.BW)
        self.__statusBG.image = status_bg
        self.__statusBG.place(x=0, y=0, anchor=NW)
        self.__colorIMG = PhotoImage(file=self.RED_SML_IMG_PATH)
        self.__statusIMG = Label(self.__status_frame, image=self.__colorIMG,
                            highlightthickness=self.HLTN, borderwidth=self.BW)
        self.__statusIMG.image = self.__colorIMG
        self.__statusIMG.pack(side=LEFT, pady=10)
        self.__txt_bg = PhotoImage(file=self.STATUS_TXT_RED_PATH)
        self.__statusTXT = Label(self.__status_frame, image=self.__txt_bg,
                            highlightthickness=self.HLTN, borderwidth=self.BW)
        self.__statusTXT.image = self.__txt_bg
        self.__statusTXT.pack(side=LEFT, pady=10)

    def __send_msg(self, col):
        """
        Send a message to the Server/Client. The message is just the column
        number that the current user playes. also update the insertion frame to
        fit the current game state.
        :param col: The column that was currently played. This is an int.
        :return: None.
        """
        for i in range(WIDTH):
            self.__optionsLST[i].grid_remove()
        self.__comm.send_message(col)

    def move_turn(self, col):
        """
        A sequence of actions to initiate as a human player move. Triggered
        when clicking the left mouse button.
        :param col: The column that the user clicked on.
        :return: None.
        """
        winning_seq, winner = self.__game.get_winner()
        if winner is None:
            if self.col_limit[col] < HEIGHT:
                self.insertion_col = col + 1
                self.col_limit[col] += 1
                self.__update_UI()
                self.__board = self.__game.make_move(self.insertion_col)
                if self.__board:
                    self.update_board(self.__board)
                winning_seq, winner = self.__game.get_winner()
                if winner is not None:
                    self.__check_winner()
            elif (SERVER and self.__game.get_current_player() ==
                   self.__game.PLAYER_ONE) or (not SERVER and
                   self.__game.get_current_player() == self.__game.PLAYER_TWO):
                messagebox.showinfo(self.FULL_COL_TITLE, self.FULL_COL_MSG)
        # else:
        #     self.__check_winner()

    def move_ai_turn(self):
        """
        A sequence of actions to initiate as an AI move.
        :return: None
        """
        winning_seq, winner = self.__game.get_winner()
        if winner is None:
            col = self.__ai.find_legal_move(self.__game, self.__game.make_move)
            self.insertion_col = col - 1
            self.col_limit[self.insertion_col] += 1
            self.__update_UI()
            self.__board = self.__game.get_board()
            if self.__board:
                self.update_board(self.__board)
                self.__send_msg(self.insertion_col)
            winning_seq, winner = self.__game.get_winner()
            if winner is not None:
                self.__check_winner()
        else:
            self.__send_msg(self.insertion_col)
            self.__check_winner()

    def __update_UI(self):
        """
        Update the Insertion frame and Status frame to fit the current game
        state.
        :return: None
        """
        if self.__game.get_current_player() == self.__game.PLAYER_ONE:
            self.__txt_bg.config(file=self.STATUS_TXT_YELLOW_PATH)
            self.__colorIMG.config(file=self.YELLOW_SML_IMG_PATH)
            for i in range(WIDTH):
                self.__option.config(file=self.YELLOW_IMG_PATH)
                self.__optionsLST[i].config(image=self.__option)
        else:
            self.__txt_bg.config(file=self.STATUS_TXT_RED_PATH)
            self.__colorIMG.config(file=self.RED_SML_IMG_PATH)
            for i in range(WIDTH):
                self.__option.config(file=self.RED_IMG_PATH)
                self.__optionsLST[i].config(image=self.__option)

    def __check_winner(self):
        """
        Check which player won or if it's a tie. Prompt a message accordingly.
        Also change the winning sequence color to white for easy recognition.
        :return: None
        """
        winning_seq, winner = self.__game.get_winner()
        if winning_seq:
            for coord in winning_seq:
                row, col = coord
                self.winning_dict[(row, col)].image.config(
                    file=self.WIN_IMG_PATH)
        response = ""
        if winner == self.__game.DRAW:
            response = messagebox.showinfo(self.FULL_BOARD_TITLE,
                                           self.FULL_BOARD_MSG)
        if winner == self.__game.PLAYER_ONE:
            response = messagebox.showinfo(self.END_GAME_MSG,
                                           self.RED_WINNER_MSG)
        if winner == self.__game.PLAYER_TWO:
            response = messagebox.showinfo(self.END_GAME_MSG,
                                           self.YELLOW_WINNER_MSG)
        if response == self.POP_RESPONSE:
            self.__root.quit()

    def update_board(self, board_mat):
        """
        Update the board graphics according to the last move, and check if
        someone won.
        :param board_mat: A 2D matrix representing the board status.
        :return: None
        """
        for row in range(HEIGHT):
            for col in range(WIDTH):
                if board_mat[row][col] == 0:
                    token = PhotoImage(file=self.RED_IMG_PATH)
                    self.update_lst.append(Label(self.__main_canvas,
                                    image=token, highlightthickness=self.HLTN,
                                                    bg=self.TOKEN_BG_COLOR))
                    self.winning_dict[(row, col)] = self.update_lst[-1]
                    self.winning_dict[(row, col)].image = token
                    self.update_lst[-1].image = token
                    self.update_lst[-1].place(x=self.board_dict[(row, col)][1],
                                     y=self.board_dict[(row, col)][0])
                if board_mat[row][col] == 1:
                    token = PhotoImage(file=self.YELLOW_IMG_PATH)
                    self.update_lst.append(Label(self.__main_canvas,
                                    image=token, highlightthickness=self.HLTN,
                                                    bg=self.TOKEN_BG_COLOR))
                    self.winning_dict[(row, col)] = self.update_lst[-1]
                    self.winning_dict[(row, col)].image = token
                    self.update_lst[-1].image = token
                    self.update_lst[-1].place(x=self.board_dict[(row, col)][1],
                                     y=self.board_dict[(row, col)][0])


if __name__ == "__main__":  # Run the Game.
    if 3 <= len(sys.argv) <= 4:
        ip = None
        ai = None
        port = int(sys.argv[2])
        if len(sys.argv) == 4:
            ip = sys.argv[3]
            SERVER = False
        if port < PORT_MIN or port > PORT_MAX or (sys.argv[1] != HUMAN_ARG and
                                                   sys.argv[1] != AI_ARG):
            sys.exit(ILLEGAL_ARGS)
    else:
        sys.exit(ERR_NUM_ARGS)
    root = Tk()
    root.resizable(False, False)
    game = Game()
    if sys.argv[1] == AI_ARG:
        HUMAN = False
        ai = AI(game, )
    board = game.get_board()
    if SERVER:
        comm = Communicator(root, port)
        if HUMAN:
            root.title(WIN_NAME_SRVR_HUMAN)
        else:
            root.title(WIN_NAME_SRVR_AI)
    else:
        comm = Communicator(root, port, ip=ip)
        if HUMAN:
            root.title(WIN_NAME_CLNT_HUMAN)
        else:
            root.title(WIN_NAME_CLNT_AI)
    gui = GUI(root, game, board, comm, ai)
    root.mainloop()