import game2
import othello

class benchPlayer(object):
    """
    Reinforcement Learning in The Game Of Othello - By Michiel Van Der Ree and Marco Wiering(IEEE member)
    http://www.ai.rug.nl/~mwiering/GROUP/ARTICLES/paper-othello.pdf
    A better evaluation function which gives more preference to squares
    on the edge of the board and on the corners.
    """
    def __init__(self):
        pass

    def get_evaluation_score(self,game):
        # if the game is over, give a 1000 point bonus to the winning player
        if game.terminal_test():
            score = game.score()
            if score > 0:
                return 1000
            elif score < 0:
                return -1000
            else:
                return 0
            

        opp = -1 * game.player # the opponent
        board_values = [[80,-26,24,-1,-5,28,-18,76],
    					[-23,-39,-18,-9,-6,-8,-39,-1],
    					[46,-16,4,1,-3,6,-20,52],
    					[-13,-5,2,-1,4,3,-12,-2],
    					[5,-6,1,-2,-3,0,-9,-5],
    					[48,-13,12,5,0,5,-24,41],
    					[-27,-53,-11,-1,-11,-16,-58,-15],
    					[87,-25,27,-1,5,36,-3,100]]
        score = 0
        for i in othello.range_size:
            for j in othello.range_size:
                # any piece gets a value of 1
                # an edge piece gets a value of 6
                # a corner piece gets a value of 11
                # subtract 10 for the four diagonal square near the corners
                # subtract 5 for the rows and cols near the edge
                # TODO: only charge the penalty when the edge or corner is not
                # occupied
                delta = board_values[i][j]
                
                if game.board[i][j] == game.player:
                    score += delta
                elif game.board[i][j] == opp:
                    score -= delta

        return score

    def play_next_move(self, game_orig):
        """
        Find the best move in the game

        Returns a tuple (estimated value, operator)
        The game must support the following functions:
        
        copy() to make a deep copy of the game
        terminal_test() to determine whether the game is over
        """
        best = None

        # try each move
        for move in game_orig.generate_moves():
            g = game_orig.copy()
            g.play_move(move)
            # evaluate the position and choose the best move
            # NOTE: the minimax function computes the value for the current
            # player which is the opponent so we need to invert the value
            val = -1 * self.get_evaluation_score(g)
            # update the best operator so far
            if best is None or val > best[0]:
                best = (val, move)
        return best