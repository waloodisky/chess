board = [None]*64
y = 8
turn = "white"
checkmated = None
class Piece:
    def __init__(self, color, position):
        global board
        self.color = color
        self.position = position
        board[self.position] = self
        self.has_moved = False
        

    def move(self, new_position):
        global board
        if self == white_king and white_king.can_castle:
            if new_position == 6:
                right_white_rook.move(5)
                board[self.position] = None
                self.position = new_position
                board[self.position] = self
                self.has_moved = True
            elif new_position == 2:
                left_white_rook.move(3)
                board[self.position] = None
                self.position = new_position
                board[self.position] = self
                self.has_moved = True

        elif self == black_king and black_king.can_castle:
            if new_position == 58:
                right_black_rook.move(59)
                board[self.position] = None
                self.position = new_position
                board[self.position] = self
                self.has_moved = True
            elif new_position == 62:
                left_black_rook.move(61)
                board[self.position] = None
                self.position = new_position
                board[self.position] = self
                self.has_moved = True

        if new_position in self.legal_moves:
            board[self.position] = None
            self.position = new_position
            board[self.position] = self
            self.has_moved = True
            global turn
            if turn == "white":
                turn = "black"
            elif turn == "black":
                turn = "white"

    def friendly_fire(self, moves):
        placeholder = list(moves)
        for move in placeholder:
            if board[move] and board[move].color == self.color:
                moves.remove(move)
    
        
    
class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.type = "pawn"
        if self.color == "black":
            self.y = -8
        else:
            self.y = 8

    @property
    def legal_moves(self):
        moves=[]
        if not self.has_moved and not board[self.position+self.y] and not board[self.position+2*self.y]:
            moves.append(self.position+2*self.y)
        if not board[self.position+self.y]:
            moves.append(self.position+self.y)
        if self.position%8 != 7 and board[self.position+self.y+1]:
            moves.append(self.position+self.y+1)
        if self.position%8 != 0 and board[self.position+self.y-1]:
            moves.append(self.position+self.y-1)
        self.friendly_fire(moves)
        return moves
        
        
class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.type = "king"


    @property
    def in_check(self):
        for piece in board:
            if piece and piece.type != "king" and piece.color != self.color and self.position in piece.legal_moves:
                return True
                
    @property
    def can_castle(self):
        castle_right = False
        castle_left = False
        if not self.has_moved and not self.in_check:
            if self.color == "white":
                if not right_white_rook.has_moved and not board[5] and not board[6]:
                    castle_right = True
                    for square in [5,6,7]:
                        for piece in board:
                            if piece and piece.type != "king" and piece.color == "black":
                                if square in piece.legal_moves:
                                    castle_right = False

                if not left_white_rook.has_moved and not board[1] and not board[2] and not board[3]:
                    castle_left = True
                    for square in [0,1,2,3]:
                        for piece in board:
                            if piece and piece.type != "king" and piece.color == "black":
                                if square in piece.legal_moves:
                                    castle_left = False

                if castle_right and castle_left:
                    return "both"
                elif castle_left:
                    return "left"
                elif castle_right:
                    return "right"

            elif self.color == "black":
                if not right_black_rook.has_moved and not board[57] and not board[58] and not board[59]:
                    castle_right = True
                    for square in [56,57,58,59]:
                        for piece in board:
                            if piece and piece.type != "king" and piece.color == "white":
                                if square in piece.legal_moves:
                                    castle_right = False

                if not left_black_rook.has_moved and not board[61] and not board[62]:
                    castle_left = True
                    for square in [61,62,63]:
                        for piece in board:
                            if piece and piece.type != "king" and piece.color == "white":
                                if square in piece.legal_moves:
                                    castle_left = False

                if castle_right and castle_left:
                    return "both"
                elif castle_left:
                    return "left"
                elif castle_right:
                    return "right"
        
    @property
    def legal_moves(self):
        moves=[]
        
        if self.color == "white":
            if self.can_castle == "right":
                moves.append(6)
            elif self.can_castle == "left":
                moves.append(2)
            elif self.can_castle == "both":
                moves.append(2)
                moves.append(6)
        elif self.color == "black":
            if self.can_castle == "right":
                moves.append(58)
            elif self.can_castle == "left":
                moves.append(62)
            elif self.can_castle == "both":
                moves.append(58)
                moves.append(62)
        for move in [1,-1,8,-8,7,9,-7,-9]:
            if move in [1,9,-7] and self.position % 8 == 7:
                continue
            if move in [7,-9,-1] and self.position % 8 == 0:
                continue
            if 0 <= self.position+move <= 63:
                moves.append(self.position+move)
        self.friendly_fire(moves)
        return moves
    
    
class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.type = "knight"

    @property
    def legal_moves(self):
        moves=[]
        if self.position>47:
            if self.position%8>5:
                moves.append(self.position-10)
            elif self.position%8<2:
                moves.append(self.position-6)
            else:
                moves.append(self.position-10)
                moves.append(self.position-6)
            if self.position%8==7:
                moves.append(self.position-17)
            elif self.position%8==0:
                moves.append(self.position-15)
            else:
                moves.append(self.position-15)
                moves.append(self.position-17)
            if self.position<56:
                if self.position%8>5:
                    moves.append(self.position+6)
                elif self.position%8<2:
                 moves.append(self.position+10)
                else:
                   moves.append(self.position+10)
                   moves.append(self.position+6)

        elif self.position<16:
            if self.position%8>5:
                moves.append(self.position+6)
            elif self.position%8<2:
                moves.append(self.position+10)
            else:
                moves.append(self.position+10)
                moves.append(self.position+6)
            if self.position%8==7:
                moves.append(self.position+15)
            elif self.position%8==0:
                moves.append(self.position+17)
            else:
                moves.append(self.position+15)
                moves.append(self.position+17)
            if self.position>7:
                if self.position%8>5:
                    moves.append(self.position-10)
                elif self.position%8<2:
                 moves.append(self.position-6)
                else:
                   moves.append(self.position-10)
                   moves.append(self.position-6)

        else:
            if self.position%8==7:
                moves.append(self.position+15)
                moves.append(self.position+6)
                moves.append(self.position-10)
                moves.append(self.position-17)
            elif self.position%8==6:
                moves.append(self.position+6)
                moves.append(self.position+17)
                moves.append(self.position+15)
                moves.append(self.position-10)
                moves.append(self.position-17)
                moves.append(self.position-15)
            elif self.position%8==0:
                moves.append(self.position+17)
                moves.append(self.position+10)
                moves.append(self.position-6)
                moves.append(self.position-15)
            elif self.position%8==1:
                moves.append(self.position+10)    
                moves.append(self.position+17)
                moves.append(self.position+15)
                moves.append(self.position-17)
                moves.append(self.position-15)
                moves.append(self.position-6)
            else:
                moves.append(self.position+17)
                moves.append(self.position+15)
                moves.append(self.position+6)
                moves.append(self.position+10)
                moves.append(self.position-15)
                moves.append(self.position-17)
                moves.append(self.position-6)
                moves.append(self.position-10)
 

        self.friendly_fire(moves)
        return moves
    

class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.type = "bishop"

    @property
    def legal_moves(self):
        moves=[]
        #up right
        for move in range(9, 72, 9):
            if 0 <= self.position+move <= 63 and self.position %8 != 7:
                moves.append(self.position+move)
                if (self.position+move) %8 == 7:
                    break
                if board[self.position+move]:
                    break
        #up left
        for move in range(7, 63, 7):
            if 0 <= self.position+move <= 63 and self.position %8 != 0:
                moves.append(self.position+move)
                if (self.position+move) %8 == 0:
                    break
                if board[self.position+move]:
                    break
        #down left
        for move in range(-9, -72, -9):
            if 0 <= self.position+move <= 63 and self.position %8 != 0:
                moves.append(self.position+move)
                if (self.position+move) %8 == 0:
                    break
                if board[self.position+move]:
                    break
        #down right
        for move in range(-7, -63, -7):
            if 0 <= self.position+move <= 63 and self.position %8 != 7:
                moves.append(self.position+move)
                if (self.position+move) %8 == 7:
                    break
                if board[self.position+move]:
                    break
        self.friendly_fire(moves)    
        return moves
    
class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.type = "rook"

    @property
    def legal_moves(self):
        moves=[]
        #up
        for move in range(8, 64, 8):
            if 0 <= self.position+move <= 63:
                moves.append(self.position+move)
                if board[self.position+move]:
                    break
        #down
        for move in range(-8, -64, -8):
            if 0 <= self.position+move <= 63:
                moves.append(self.position+move)
                if board[self.position+move]:
                    break
        #right
        for move in range(1, 8, 1):
            if 0 <= self.position+move <= 63 and self.position %8 != 7:
                moves.append(self.position+move)
                if (self.position+move) %8 == 7:
                    break
                if board[self.position+move]:
                    break
        #left
        for move in range(-1, -8, -1):
            if 0 <= self.position+move <= 63 and self.position %8 != 0:
                moves.append(self.position+move)
                if (self.position+move) %8 == 0:
                    break
                if board[self.position+move]:
                    break
        self.friendly_fire(moves)
        return moves
    






class Queen(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.type = "queen"

    @property
    def legal_moves(self):
        moves=[]
        #up right
        for move in range(9, 72, 9):
            if 0 <= self.position+move <= 63 and self.position %8 != 7:
                moves.append(self.position+move)
                if (self.position+move) %8 == 7:
                    break
                if board[self.position+move]:
                    break
        #up left
        for move in range(7, 63, 7):
            if 0 <= self.position+move <= 63 and self.position %8 != 0:
                moves.append(self.position+move)
                if (self.position+move) %8 == 0:
                    break
                if board[self.position+move]:
                    break
        #down left
        for move in range(-9, -72, -9):
            if 0 <= self.position+move <= 63 and self.position %8 != 0:
                moves.append(self.position+move)
                if (self.position+move) %8 == 0:
                    break
                if board[self.position+move]:
                    break
        #down right
        for move in range(-7, -63, -7):
            if 0 <= self.position+move <= 63 and self.position %8 != 7:
                moves.append(self.position+move)
                if (self.position+move) %8 == 7:
                    break
                if board[self.position+move]:
                    break
        #up
        for move in range(8, 64, 8):
            if 0 <= self.position+move <= 63:
                moves.append(self.position+move)
                if board[self.position+move]:
                    break
        #down
        for move in range(-8, -64, -8):
            if 0 <= self.position+move <= 63:
                moves.append(self.position+move)
                if board[self.position+move]:
                    break
        #right
        for move in range(1, 8, 1):
            if 0 <= self.position+move <= 63 and self.position %8 != 7:
                moves.append(self.position+move)
                if (self.position+move) %8 == 7:
                    break
                if board[self.position+move]:
                    break
        #left
        for move in range(-1, -8, -1):
            if 0 <= self.position+move <= 63 and self.position %8 != 0:
                moves.append(self.position+move)
                if (self.position+move) %8 == 0:
                    break
                if board[self.position+move]:
                    break
        self.friendly_fire(moves)
        return moves


white_king = King("white", 4)
black_king = King("black", 60)
left_white_rook = Rook("white", 0,)
right_white_rook = Rook("white", 7)
left_black_rook = Rook("black", 63)
right_black_rook = Rook("black", 56) 
board_tempelate = [left_white_rook, Knight("white", 1), Bishop("white", 2), Queen("white", 3), white_king, Bishop("white", 5), Knight("white", 6), right_white_rook, 
         Pawn("white", 8), Pawn("white", 9), Pawn("white", 10), Pawn("white", 11), Pawn("white", 12), Pawn("white", 13), Pawn("white", 14), Pawn("white", 15), 
         None, None, None, None, None, None, None, None,  
         None, None, None, None, None, None, None, None,  
         None, None, None, None, None, None, None, None,  
         None, None, None, None, None, None, None, None, 
         Pawn("black", 48), Pawn("black", 49), Pawn("black", 50), Pawn("black", 51), Pawn("black", 52), Pawn("black", 53), Pawn("black", 54), Pawn("black", 55), 
         right_black_rook, Knight("black", 57), Bishop("black", 58), Queen("black", 59), black_king, Bishop("black", 61), Knight("black", 62), left_black_rook]


        
def is_stalemate():
    for king in [white_king,black_king]:
        if not king.legal_moves and not king.in_check:
            for piece in board:
                if piece and piece.color == king.color and piece.legal_moves:
                    return True
