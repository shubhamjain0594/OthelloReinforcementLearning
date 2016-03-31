import game2
import othello

"""
"""
class standardWPCPlayer(object):
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
        board_values = [[1.00,-0.25, 0.10, 0.05, 0.05, 0.10,-0.25, 1.00],
        [-0.25,-0.25, 0.01, 0.01, 0.01, 0.01,-0.25,-0.25],
        [ 0.10, 0.01, 0.05, 0.02, 0.02, 0.05, 0.01, 0.10],
        [ 0.05, 0.01, 0.02, 0.01, 0.01, 0.02, 0.01, 0.05],
        [ 0.05, 0.01, 0.02, 0.01, 0.01, 0.02, 0.01, 0.05],
        [ 0.10, 0.01, 0.05, 0.02, 0.02, 0.05, 0.01, 0.10],
        [-0.25,-0.25, 0.01, 0.01, 0.01, 0.01,-0.25,-0.25],
        [ 1.00,-0.25, 0.10, 0.05, 0.05, 0.10,-0.25, 1.00]]
        score = 0
        for i in othello.range_size:
            for j in othello.range_size:
                """
                To calculate the board evaluation we multiply each piece by 1 if piece is black else by -1 if piece is white and we maximize for black and minimize for white
                """
                delta = board_values[i][j]*(game.board[i][j]*-1)
                score += delta

        return score*game.player

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
            # black maximizes the score and white minimizes
            val = self.get_evaluation_score(g)
            # update the best operator so far
            if best is None or val > best[0]:
                best = (val, move)
        return best