turn_num = 0
Board = []
files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

#checkmate, fix move back capture not capture other word that dont make sentence, ascii chars

def create_game():
    global turn_num
    turn_num = 1
    Board[:] = [[Rook(['a', 8], 'black'), Knight(['b', 8], 'black'), Bishop(['c', 8], 'black'), Queen(['d', 8], 'black'),
          black_king, Bishop(['f', 8], 'black'), Knight(['g', 8], 'black'), Rook(['h', 8], 'black')],
         [Pawn([files[x], 7], 'black') for x in range(8)]]+[['-----' for _ in range(8)] for _ in range(4)]+[[Pawn([files[x], 2], 'white') for x in range(8)],
         [Rook(['a', 1], 'white'), Knight(['b', 1], 'white'), Bishop(['c', 1], 'white'), Queen(['d', 1], 'white'),
          white_king, Bishop(['f', 1], 'white'), Knight(['g', 1], 'white'), Rook(['h', 1], 'white')]]
    print_board()

def print_board():
    if not Board:
        print('start a game first u noob')
        return
    line = '        '
    for x in range(8):
        print('')
        print(8-x, ' ', Board[x])
        line = line + files[x] + '        '
    print('')
    print(line)

def play(move):
    global turn_num
    if turn_num == 0:
        print('create a game first u idiot')
        return
    location = [move[0], int(move[1])]
    destination = [move[2], int(move[3])]
    occupier = contents(destination)
    piece = contents(location)
    color = 'white' if turn_num % 2 else 'black'
    if piece != '-----' and piece.color == color and piece.can_move_to(destination):
        piece.move(destination)
        king = white_king if color == 'white' else black_king
        if under_threat_by(king.location, opposite(color)):
            piece.move(location)
            Board[y_loc(destination)][x_loc(destination)] = occupier
            print('bish i cant do dat')
        else:
            turn_num += 1
            print_board()
    else:
        print('bish i cant do dat')

def x_loc(square):
    return files.index(file(square))

def y_loc(square):
    return 8 - rank(square)

def file(square):
    return square[0]

def rank(square):
    return square[1]
        
def contents(square):
    return Board[y_loc(square)][x_loc(square)]

def contents_cell(x, y):
    return Board[y][x]

def under_threat_by(square, color):
    threats = []
    for row in Board:
        for piece in row:
            if piece != '-----' and piece.color == color and piece.is_guarding(square):
                threats.append(piece)
    return threats

def opposite(color):
    if color == 'white':
        return 'black'
    elif color == 'black':
        return 'white'
    else:
        print('this function is so obvious')

def sign(val):
    if val > 0:
        return 1
    elif val < 0:
        return -1
    else:
        return 0

class Piece:
    
    move_count = 0
    
    def __init__(self, starting_place, color, name = 'Nameless'):
        self.color = color
        self.location = starting_place
        self.name = name

    def can_move_to(self, destination):
        occupier = contents(destination)
        return self.is_guarding(destination) and (occupier == '-----' or occupier.color == opposite(self.color))
        
    def move(self, destination):
        x0, y0 = x_loc(self.location), y_loc(self.location)
        x1, y1 = x_loc(destination), y_loc(destination)
        if self.can_move_to(destination) == 'castles':
            direction = sign(x1-x0)
            rook_x = 7 if direction == 1 else 0
            rook = contents_cell(rook_x, y0)
            Board[y0][rook_x], Board[y0][x0 + direction] = '-----', rook
            rook.location = [files[files.index(file(destination)) + direction], rank(destination)]
        elif self.can_move_to(destination) == 'en passant':
            Board[y1+self.forward][x1] = '-----'
        Board[y0][x0], Board[y1][x1] = '-----', self
        self.location = destination
        self.move_count += 1

    def __repr__(self):
        # return self.color[0] + self.name + ' ' * (6 - len(self.name))
        piece_name = self.name + ' ' * (7 - len(self.name))
        return piece_name.upper() if self.color == 'white' else piece_name.lower()

class Pawn(Piece):

    def __init__(self, starting_place, color):
        Piece.__init__(self, starting_place, color, 'Pawn')
        self.forward = 1 if self.color == 'white' else -1
        self.passable = []

    def is_guarding(self, square):
        x0, y0 = x_loc(self.location), y_loc(self.location)
        x1, y1 = x_loc(square), y_loc(square)
        return y0 - self.forward == y1 and abs(x0 - x1) == 1
        
    def can_move_to(self, destination):
        """En passant tests.

        >>> create_game()
        [bRook  , bKnight, bBishop, bQueen , bKing  , bBishop, bKnight, bRook  ]
        [bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  ]
        ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
        ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
        ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
        ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
        [wPawn  , wPawn  , wPawn  , wPawn  , wPawn  , wPawn  , wPawn  , wPawn  ]
        [wRook  , wKnight, wBishop, wQueen , wKing  , wBishop, wKnight, wRook  ]
        >>> play('e2e4')
        [bRook  , bKnight, bBishop, bQueen , bKing  , bBishop, bKnight, bRook  ]
        [bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  ]
        ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
        ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
        ['-----', '-----', '-----', '-----', wPawn  , '-----', '-----', '-----']
        ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
        [wPawn  , wPawn  , wPawn  , wPawn  , '-----', wPawn  , wPawn  , wPawn  ]
        [wRook  , wKnight, wBishop, wQueen , wKing  , wBishop, wKnight, wRook  ]
        >>> play('c7c5')
        [bRook  , bKnight, bBishop, bQueen , bKing  , bBishop, bKnight, bRook  ]
        [bPawn  , bPawn  , '-----', bPawn  , bPawn  , bPawn  , bPawn  , bPawn  ]
        ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
        ['-----', '-----', bPawn  , '-----', '-----', '-----', '-----', '-----']
        ['-----', '-----', '-----', '-----', wPawn  , '-----', '-----', '-----']
        ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
        [wPawn  , wPawn  , wPawn  , wPawn  , '-----', wPawn  , wPawn  , wPawn  ]
        [wRook  , wKnight, wBishop, wQueen , wKing  , wBishop, wKnight, wRook  ]
        >>> play('e4e5')
        [bRook  , bKnight, bBishop, bQueen , bKing  , bBishop, bKnight, bRook  ]
        [bPawn  , bPawn  , '-----', bPawn  , bPawn  , bPawn  , bPawn  , bPawn  ]
        ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
        ['-----', '-----', bPawn  , '-----', wPawn  , '-----', '-----', '-----']
        ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
        ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
        [wPawn  , wPawn  , wPawn  , wPawn  , '-----', wPawn  , wPawn  , wPawn  ]
        [wRook  , wKnight, wBishop, wQueen , wKing  , wBishop, wKnight, wRook  ]
        >>> play('d7d5')
        [bRook  , bKnight, bBishop, bQueen , bKing  , bBishop, bKnight, bRook  ]
        [bPawn  , bPawn  , '-----', '-----', bPawn  , bPawn  , bPawn  , bPawn  ]
        ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
        ['-----', '-----', bPawn  , bPawn  , wPawn  , '-----', '-----', '-----']
        ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
        ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
        [wPawn  , wPawn  , wPawn  , wPawn  , '-----', wPawn  , wPawn  , wPawn  ]
        [wRook  , wKnight, wBishop, wQueen , wKing  , wBishop, wKnight, wRook  ]
        >>> play('e5d6')
        [bRook  , bKnight, bBishop, bQueen , bKing  , bBishop, bKnight, bRook  ]
        [bPawn  , bPawn  , '-----', '-----', bPawn  , bPawn  , bPawn  , bPawn  ]
        ['-----', '-----', '-----', wPawn  , '-----', '-----', '-----', '-----']
        ['-----', '-----', bPawn  , '-----', '-----', '-----', '-----', '-----']
        ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
        ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
        [wPawn  , wPawn  , wPawn  , wPawn  , '-----', wPawn  , wPawn  , wPawn  ]
        [wRook  , wKnight, wBishop, wQueen , wKing  , wBishop, wKnight, wRook  ]
        >>> create_game()
        [bRook  , bKnight, bBishop, bQueen , bKing  , bBishop, bKnight, bRook  ]
        [bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  ]
        ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
        ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
        ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
        ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
        [wPawn  , wPawn  , wPawn  , wPawn  , wPawn  , wPawn  , wPawn  , wPawn  ]
        [wRook  , wKnight, wBishop, wQueen , wKing  , wBishop, wKnight, wRook  ]
        >>> play('d2d4')
        [bRook  , bKnight, bBishop, bQueen , bKing  , bBishop, bKnight, bRook  ]
        [bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  ]
        ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
        ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
        ['-----', '-----', '-----', wPawn  , '-----', '-----', '-----', '-----']
        ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
        [wPawn  , wPawn  , wPawn  , '-----', wPawn  , wPawn  , wPawn  , wPawn  ]
        [wRook  , wKnight, wBishop, wQueen , wKing  , wBishop, wKnight, wRook  ]
        >>> play('b8c6')
        [bRook  , '-----', bBishop, bQueen , bKing  , bBishop, bKnight, bRook  ]
        [bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  ]
        ['-----', '-----', bKnight, '-----', '-----', '-----', '-----', '-----']
        ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
        ['-----', '-----', '-----', wPawn  , '-----', '-----', '-----', '-----']
        ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
        [wPawn  , wPawn  , wPawn  , '-----', wPawn  , wPawn  , wPawn  , wPawn  ]
        [wRook  , wKnight, wBishop, wQueen , wKing  , wBishop, wKnight, wRook  ]
        >>> play('d4d5')
        [bRook  , '-----', bBishop, bQueen , bKing  , bBishop, bKnight, bRook  ]
        [bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  ]
        ['-----', '-----', bKnight, '-----', '-----', '-----', '-----', '-----']
        ['-----', '-----', '-----', wPawn  , '-----', '-----', '-----', '-----']
        ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
        ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
        [wPawn  , wPawn  , wPawn  , '-----', wPawn  , wPawn  , wPawn  , wPawn  ]
        [wRook  , wKnight, wBishop, wQueen , wKing  , wBishop, wKnight, wRook  ]
        >>> play('e7e5')
        [bRook  , '-----', bBishop, bQueen , bKing  , bBishop, bKnight, bRook  ]
        [bPawn  , bPawn  , bPawn  , bPawn  , '-----', bPawn  , bPawn  , bPawn  ]
        ['-----', '-----', bKnight, '-----', '-----', '-----', '-----', '-----']
        ['-----', '-----', '-----', wPawn  , bPawn  , '-----', '-----', '-----']
        ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
        ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
        [wPawn  , wPawn  , wPawn  , '-----', wPawn  , wPawn  , wPawn  , wPawn  ]
        [wRook  , wKnight, wBishop, wQueen , wKing  , wBishop, wKnight, wRook  ]
        >>> play('d5e6')
        [bRook  , '-----', bBishop, bQueen , bKing  , bBishop, bKnight, bRook  ]
        [bPawn  , bPawn  , bPawn  , bPawn  , '-----', bPawn  , bPawn  , bPawn  ]
        ['-----', '-----', bKnight, '-----', wPawn  , '-----', '-----', '-----']
        ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
        ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
        ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
        [wPawn  , wPawn  , wPawn  , '-----', wPawn  , wPawn  , wPawn  , wPawn  ]
        [wRook  , wKnight, wBishop, wQueen , wKing  , wBishop, wKnight, wRook  ]
        """
        x0, y0 = x_loc(self.location), y_loc(self.location)
        x1, y1 = x_loc(destination), y_loc(destination)
        occupier = contents(destination)
        if self.is_guarding(destination):
            if occupier == '-----':
                en_occupier = contents_cell(x1, y1+self.forward)
                if en_occupier != '-----' and en_occupier.color == opposite(self.color) and turn_num-1 in en_occupier.passable:
                    return 'en passant'
                else:
                    return False
            else:
                return occupier.color == opposite(self.color)
        elif y0 - self.forward == y1 and x0 == x1:
            return occupier == '-----'
        elif y0 - 2*self.forward == y1 and x0 == x1 and not self.move_count:
            self.passable.append(turn_num)
            return occupier == '-----' and contents_cell(x0, y0 - self.forward) == '-----'
        else:
            return False

class Knight(Piece):

    def __init__(self, starting_place, color):
        Piece.__init__(self, starting_place, color, 'Knight')

    def is_guarding(self, square):
        x0, y0 = x_loc(self.location), y_loc(self.location)
        x1, y1 = x_loc(square), y_loc(square)
        dx, dy = abs(x0 - x1), abs(y0 - y1)
        return dx == 2 and dy == 1 or dx == 1 and dy == 2

class Bishop(Piece):

    def __init__(self, starting_place, color):
        Piece.__init__(self, starting_place, color, 'Bishop')

    def is_guarding(self, square):
        x0, y0 = x_loc(self.location), y_loc(self.location)
        x1, y1 = x_loc(square), y_loc(square)
        dx, dy = abs(x0 - x1), abs(y0 - y1)
        if dx == dy and dx != 0:
            return all(contents_cell(x0 + n*sign(x1-x0), y0 + n*sign(y1-y0)) == '-----' for n in range(1, dx))
        else:
            return False

class Rook(Piece):

    def __init__(self, starting_place, color):
        Piece.__init__(self, starting_place, color, 'Rook')

    def is_guarding(self, square):
        x0, y0 = x_loc(self.location), y_loc(self.location)
        x1, y1 = x_loc(square), y_loc(square)
        dx, dy = abs(x0 - x1), abs(y0 - y1)
        if dx > 0 and dy == 0:
            return all(contents_cell(x0 + n*sign(x1-x0), y0) == '-----' for n in range(1, dx))
        elif dy > 0 and dx == 0:
            return all(contents_cell(x0, y0 + n*sign(y1-y0)) == '-----' for n in range(1, dy))
        else:
            return False

class Queen(Piece):

    def __init__(self, starting_place, color):
        Piece.__init__(self, starting_place, color, 'Queen')
        
    def is_guarding(self, square):
        return Rook.is_guarding(self, square) or Bishop.is_guarding(self, square)

class King(Piece):
    """Castle check.

    >>> create_game()
    [bRook  , bKnight, bBishop, bQueen , bKing  , bBishop, bKnight, bRook  ]
    [bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  ]
    ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
    [wPawn  , wPawn  , wPawn  , wPawn  , wPawn  , wPawn  , wPawn  , wPawn  ]
    [wRook  , wKnight, wBishop, wQueen , wKing  , wBishop, wKnight, wRook  ]
    >>> Board[0][1:4] = 3*['-----']
    >>> Board[7][5:7] = 2*['-----']
    >>> play('e1g1')
    [bRook  , '-----', '-----', '-----', bKing  , bBishop, bKnight, bRook  ]
    [bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  ]
    ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
    [wPawn  , wPawn  , wPawn  , wPawn  , wPawn  , wPawn  , wPawn  , wPawn  ]
    [wRook  , wKnight, wBishop, wQueen , '-----', wRook  , wKing  , '-----']
    >>> play('e8c8')
    ['-----', '-----', bKing  , bRook  , '-----', bBishop, bKnight, bRook  ]
    [bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  ]
    ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
    [wPawn  , wPawn  , wPawn  , wPawn  , wPawn  , wPawn  , wPawn  , wPawn  ]
    [wRook  , wKnight, wBishop, wQueen , '-----', wRook  , wKing  , '-----']
    >>> create_game()
    [bRook  , bKnight, bBishop, bQueen , bKing  , bBishop, bKnight, bRook  ]
    [bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  ]
    ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
    [wPawn  , wPawn  , wPawn  , wPawn  , wPawn  , wPawn  , wPawn  , wPawn  ]
    [wRook  , wKnight, wBishop, wQueen , wKing  , wBishop, wKnight, wRook  ]
    >>> play('e2e4')
    [bRook  , bKnight, bBishop, bQueen , bKing  , bBishop, bKnight, bRook  ]
    [bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  ]
    ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', wPawn  , '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
    [wPawn  , wPawn  , wPawn  , wPawn  , '-----', wPawn  , wPawn  , wPawn  ]
    [wRook  , wKnight, wBishop, wQueen , wKing  , wBishop, wKnight, wRook  ]
    >>> play('b8c6')
    [bRook  , '-----', bBishop, bQueen , bKing  , bBishop, bKnight, bRook  ]
    [bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  ]
    ['-----', '-----', bKnight, '-----', '-----', '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', wPawn  , '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
    [wPawn  , wPawn  , wPawn  , wPawn  , '-----', wPawn  , wPawn  , wPawn  ]
    [wRook  , wKnight, wBishop, wQueen , wKing  , wBishop, wKnight, wRook  ]
    >>> play('f1b5')
    [bRook  , '-----', bBishop, bQueen , bKing  , bBishop, bKnight, bRook  ]
    [bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  ]
    ['-----', '-----', bKnight, '-----', '-----', '-----', '-----', '-----']
    ['-----', wBishop, '-----', '-----', '-----', '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', wPawn  , '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
    [wPawn  , wPawn  , wPawn  , wPawn  , '-----', wPawn  , wPawn  , wPawn  ]
    [wRook  , wKnight, wBishop, wQueen , wKing  , '-----', wKnight, wRook  ]
    >>> play('d7c6')
    bish i cant do dat
    >>> play('g1f3')
    bish i cant do dat
    >>> play('b7b6')
    [bRook  , '-----', bBishop, bQueen , bKing  , bBishop, bKnight, bRook  ]
    [bPawn  , '-----', bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  ]
    ['-----', bPawn  , bKnight, '-----', '-----', '-----', '-----', '-----']
    ['-----', wBishop, '-----', '-----', '-----', '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', wPawn  , '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
    [wPawn  , wPawn  , wPawn  , wPawn  , '-----', wPawn  , wPawn  , wPawn  ]
    [wRook  , wKnight, wBishop, wQueen , wKing  , '-----', wKnight, wRook  ]
    >>> play('b5d7')
    bish i cant do dat
    >>> play('b5c6')
    [bRook  , '-----', bBishop, bQueen , bKing  , bBishop, bKnight, bRook  ]
    [bPawn  , '-----', bPawn  , bPawn  , bPawn  , bPawn  , bPawn  , bPawn  ]
    ['-----', bPawn  , wBishop, '-----', '-----', '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', wPawn  , '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
    [wPawn  , wPawn  , wPawn  , wPawn  , '-----', wPawn  , wPawn  , wPawn  ]
    [wRook  , wKnight, wBishop, wQueen , wKing  , '-----', wKnight, wRook  ]
    >>> play('b7c6')
    bish i cant do dat
    >>> play('d7c6')
    [bRook  , '-----', bBishop, bQueen , bKing  , bBishop, bKnight, bRook  ]
    [bPawn  , '-----', bPawn  , '-----', bPawn  , bPawn  , bPawn  , bPawn  ]
    ['-----', bPawn  , bPawn  , '-----', '-----', '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', wPawn  , '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
    [wPawn  , wPawn  , wPawn  , wPawn  , '-----', wPawn  , wPawn  , wPawn  ]
    [wRook  , wKnight, wBishop, wQueen , wKing  , '-----', wKnight, wRook  ]
    >>> play('g1f3')
    [bRook  , '-----', bBishop, bQueen , bKing  , bBishop, bKnight, bRook  ]
    [bPawn  , '-----', bPawn  , '-----', bPawn  , bPawn  , bPawn  , bPawn  ]
    ['-----', bPawn  , bPawn  , '-----', '-----', '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', wPawn  , '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', '-----', wKnight, '-----', '-----']
    [wPawn  , wPawn  , wPawn  , wPawn  , '-----', wPawn  , wPawn  , wPawn  ]
    [wRook  , wKnight, wBishop, wQueen , wKing  , '-----', '-----', wRook  ]
    >>> play('c8a6')
    [bRook  , '-----', '-----', bQueen , bKing  , bBishop, bKnight, bRook  ]
    [bPawn  , '-----', bPawn  , '-----', bPawn  , bPawn  , bPawn  , bPawn  ]
    [bBishop, bPawn  , bPawn  , '-----', '-----', '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', wPawn  , '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', '-----', wKnight, '-----', '-----']
    [wPawn  , wPawn  , wPawn  , wPawn  , '-----', wPawn  , wPawn  , wPawn  ]
    [wRook  , wKnight, wBishop, wQueen , wKing  , '-----', '-----', wRook  ]
    >>> play('e1e2')
    bish i cant do dat
    >>> play ('e1g1')
    bish i cant do dat
    >>> play('d2d3')
    [bRook  , '-----', '-----', bQueen , bKing  , bBishop, bKnight, bRook  ]
    [bPawn  , '-----', bPawn  , '-----', bPawn  , bPawn  , bPawn  , bPawn  ]
    [bBishop, bPawn  , bPawn  , '-----', '-----', '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', wPawn  , '-----', '-----', '-----']
    ['-----', '-----', '-----', wPawn  , '-----', wKnight, '-----', '-----']
    [wPawn  , wPawn  , wPawn  , '-----', '-----', wPawn  , wPawn  , wPawn  ]
    [wRook  , wKnight, wBishop, wQueen , wKing  , '-----', '-----', wRook  ]
    >>> play('g8f6')
    [bRook  , '-----', '-----', bQueen , bKing  , bBishop, '-----', bRook  ]
    [bPawn  , '-----', bPawn  , '-----', bPawn  , bPawn  , bPawn  , bPawn  ]
    [bBishop, bPawn  , bPawn  , '-----', '-----', bKnight, '-----', '-----']
    ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', wPawn  , '-----', '-----', '-----']
    ['-----', '-----', '-----', wPawn  , '-----', wKnight, '-----', '-----']
    [wPawn  , wPawn  , wPawn  , '-----', '-----', wPawn  , wPawn  , wPawn  ]
    [wRook  , wKnight, wBishop, wQueen , wKing  , '-----', '-----', wRook  ]
    >>> play('e1g1')
    [bRook  , '-----', '-----', bQueen , bKing  , bBishop, '-----', bRook  ]
    [bPawn  , '-----', bPawn  , '-----', bPawn  , bPawn  , bPawn  , bPawn  ]
    [bBishop, bPawn  , bPawn  , '-----', '-----', bKnight, '-----', '-----']
    ['-----', '-----', '-----', '-----', '-----', '-----', '-----', '-----']
    ['-----', '-----', '-----', '-----', wPawn  , '-----', '-----', '-----']
    ['-----', '-----', '-----', wPawn  , '-----', wKnight, '-----', '-----']
    [wPawn  , wPawn  , wPawn  , '-----', '-----', wPawn  , wPawn  , wPawn  ]
    [wRook  , wKnight, wBishop, wQueen , '-----', wRook  , wKing  , '-----']
    """
    
    def __init__(self, starting_place, color):
        Piece.__init__(self, starting_place, color, 'King')

    def is_guarding(self, square):
        x0, y0 = x_loc(self.location), y_loc(self.location)
        x1, y1 = x_loc(square), y_loc(square)
        dx, dy = abs(x0 - x1), abs(y0 - y1)
        return dx <= 1 and dy <= 1

    def can_move_to(self, destination):
        if under_threat_by(destination, opposite(self.color)):
            return False
        elif self.is_guarding(destination):
            occupier = contents(destination)
            return occupier == '-----' or occupier.color == opposite(self.color)
        else:
            return self.can_castle(destination)

    def can_castle(self, destination):
        x0, y0 = x_loc(self.location), y_loc(self.location)
        x1, y1 = x_loc(destination), y_loc(destination)
        dx, direction = abs(x1 - x0), sign(x1 - x0)
        if abs(dx) == 2 and y0 == y1:
            intermediate = [files[files.index(file(destination)) - direction], rank(destination)]
            if not under_threat_by(self.location, opposite(self.color)) and not under_threat_by(intermediate, opposite(self.color)):
                rook = contents_cell(7 if direction == 1 else 0, y0)
                if isinstance(rook, Rook) and not rook.move_count and not self.move_count:
                    return 'castles'
                else:
                    return False
                
white_king = King(['e', 1], 'white')
black_king = King(['e', 8], 'black')
