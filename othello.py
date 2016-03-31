# othello

# each side of the game board
size = 8
# pre-computed values
range_size = range(size)
size_m = size - 1

# direction vectors (delta_row, delta_colum)
directions = [(-1,-1), (-1,0), (-1,1),
              (0,-1),          (0,1),
              (1,-1),  (1,0),  (1,1)]

tuple_in_dir = lambda tuple,dir: (tuple[0]+dir[0], tuple[1]+dir[1])
tuple_valid = lambda tuple: (tuple[0]>=0 and tuple[0]<size
                             and tuple[1]>=0 and tuple[1]<size)

class game:
    """
    Implements the game of othello, this class provides the following:

    copy()            - return a deep copy of the game
    score()           - return the current game score
    terminal_test()   - is the game over?
    invert_game()     - inverts the board by interchanging black, white as well as player
    generate_moves()  - return a list of legal moves
    play_move(move)   - play a legal move in the game

    Board is represented by 1 for white and -1 for black
    """
    
    
    def get_color(self, tuple):

        return self.board[tuple[0]][tuple[1]]

    def set_color(self, tuple, playernum):

        self.board[tuple[0]][tuple[1]] = playernum

    def __init__(self, old_game = None):
        """Initiallize a new game of othello, optionally from an
        existing game."""
        if old_game is None:
            # initially an 8 by 8 square
            self.board = [[0 for j in range_size] for i in range_size]
            # with the middle four squares filled in
            # -1 is black +1 is white, 0 => empty
            self.board[3][3] = 1
            self.board[4][4] = 1
            self.board[3][4] = -1
            self.board[4][3] = -1
            # its black's move
            self.player = -1
        else:
            # copy all the pieces from the old game
            self.board = [[old_game.board[i][j] for j in range_size]
                          for i in range_size]
            # copy the next player num
            self.player = old_game.player

    def copy(self):
        """Make a deep copy of the game."""

        return game(self)

    def score(game):
        """The current game score w.r.t. player whose move it is.

        This is a very simple evaluation of the position for non-terminal positions.
        For terminal positions this will return the final 'score'."""
    
        # first compute the score with +ve for white and -ve for blacks
        score = 0
        for i in range_size:
            for j in range_size:
                score += game.board[i][j]

        # if white to play the score as is is correct, so multiply by 1,
        # and if black to play we need to flip the score around, hence
        # multiply by -1
        return score * game.player

    def terminal_test(self):
        """Is the game over?"""

        # first find an empty square
        for i in range_size:
            for j in range_size:
                if self.board[i][j] != 0:
                    continue
                # now we'll test if either player can put a piece in this square
                for player in [-1, 1]:
                    opp = -1 * player # compute this player's opponent
                    # look in every direction
                    for dir in directions:
                        t = tuple_in_dir((i,j), dir)
                        # till you find an opponent piece
                        if (not tuple_valid(t)) or (self.get_color(t) != opp):
                            continue
                        # now, skip all the opponent pieces
                        while self.get_color(t) == opp:
                            t = tuple_in_dir(t, dir)
                            if not tuple_valid(t):
                                break
                        else:
                            # finally, if we get one of player's piece then
                            # we can make the move
                            if self.get_color(t) == player:
                                return False

        return True

    def invert_game(self):
        """
        Inverts the board so as to interchange black and white as well as player
        """
        for i in range_size:
            for j in range_size:
                self.board[i][j] = -1*self.board[i][j]

        self.player = -1*self.player

    def generate_moves(self):
        """Return the list of legal moves where a move is a tuple.

        It returns a list of moves, if the game is not over. Otherwise, it
        returns an empty list. Note that a list with the singleton None is
        possible if the current player has no move but the game is not over.
        None is actually a valid move which rotates the turn to the other
        player and is only allowed if the current player has no legitimate
        move."""
        
        opp = -1 * self.player # opponent player num
        
        # A legal move is an empty square, s.t.
        # there is a contiguous straight line from this square consisting of
        # opponent squares followed by player's square.
        moves = []
        for i in range_size:
            for j in range_size:
                # find an empty square
                if self.board[i][j] != 0:
                    continue
                # look in every direction
                for dir in directions:
                    t = tuple_in_dir((i,j), dir)
                    # till you find an opponent piece
                    if (not tuple_valid(t)) or (self.board[t[0]][t[1]] != opp):
                        continue
                    # now, skip all the opponent pieces
                    while self.board[t[0]][t[1]] == opp:
                        t = tuple_in_dir(t, dir)
                        if not tuple_valid(t):
                            break
                    else:
                        # finally if we get one of our own pieces then
                        # make the move
                        if self.get_color(t) == self.player:
                            moves.append((i,j))
                            # no point looking in any other direction
                            break

        # if we don't have a move and the game is not over then
        # return the None move or "no move."
        if not moves and not self.terminal_test():
            moves = [None]
            
        return moves

    def play_move(self, move):
        """Make a move in the game. (The move is assumed to be valid!)"""

        # an empty move implies there was no move choice in this case the turn
        # rotates to the other player
        if move is None:
            self.player *= -1
            return
        
        self.set_color(move, self.player)

        opp = -1 * self.player # opponent player

        # look in all directions
        for dir in directions:
            t = tuple_in_dir(move, dir)
            # if we don't find an opponent piece then there is nothing to flip
            if (not tuple_valid(t)) or (self.get_color(t) != opp):
                continue
            # now keep skip over all the opponent pieces
            while self.get_color(t) == opp:
                t = tuple_in_dir(t, dir)
                # there is nothing to flip we have reached the end of the board
                # without seeing our own color piece
                if not tuple_valid(t):
                    break
            else:
                # now if we find our own piece then flip all these pieces
                if self.get_color(t) == self.player:
                    t = tuple_in_dir(move, dir)
                    while self.get_color(t) == opp:
                        self.set_color(t, self.player)
                        t = tuple_in_dir(t, dir)
        
        # finally swap the player #
        self.player *= -1


    
    def __str__(self):
        if self.player == -1:
            ret = "B"
        else:
            ret = "W"
        ret += "\n"
        for i in range_size:
            for j in range_size:
                if self.board[i][j] == 0:
                    ret += '. '
                elif self.board[i][j] == 1:
                    ret += 'W '
                elif self.board[i][j] == -1:
                    ret += 'B '
                else:
                    return None
            ret += "\n"
        
        return ret

def edge_eval(game):
    """
    A better evaluation function which gives more preference to squares
    on the edge of the board and on the corners.
    """

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
    score = 0
    for i in range_size:
        for j in range_size:
            # any piece gets a value of 1
            # an edge piece gets a value of 6
            # a corner piece gets a value of 11
            # subtract 10 for the four diagonal square near the corners
            # subtract 5 for the rows and cols near the edge
            # TODO: only charge the penalty when the edge or corner is not
            # occupied
            delta = 1 
            if i == 0 or i == size_m:
                delta += 5
            if j == 0 or j == size_m:
                delta += 5
            # penalty for putting a piece close to the edge
            if i == 1 or i == (size_m -1):
                delta -= 5
            if j == 1 or j == (size_m -1):
                delta -=5
            
            if game.board[i][j] == game.player:
                score += delta
            elif game.board[i][j] == opp:
                score -= delta

    return score