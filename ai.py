#############################################################
# FILE : ai.py
# WRITER : Shahaf Hermann , shahaf.hermann , 308156983
# EXERCISE : intro2cs ex12 2017-2018s
# DESCRIPTION: The AI class - determine the AI algorithm.
#############################################################

MSG_NO_POS_MOVE = "There are no possible Moves."


class AI:
    def __init__(self, game):
        """
        Initialize the AI object.
        :param game: Object of type Game, representing the current game played.
        """
        self.board = game.get_board()

    def find_legal_move(self, game, func, timeout=None):
        """
        Find a legal move to play. Raise exception if there are no allowed
        moves.
        :param game: Object of type Game, representing the current game played.
        :param func: the function from Game in charge of making a move.
        :param timeout:
        :return: Return the col that was found valid for making a move.
        """
        for col in range(game.WIDTH):
            temp = func(col)
            if temp:
                self.board = temp
                return col
        raise Exception(MSG_NO_POS_MOVE)
