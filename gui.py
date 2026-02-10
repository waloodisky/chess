import pygame
import os
import logic
import ctypes 


if os.name == "nt":
    ctypes.windll.user32.SetProcessDPIAware() #solves pygame windows scale bug
pygame.init()
screen_height = pygame.display.Info().current_h
height = 600
heights = [360,480,600,720,840,960,1080,1200,1320,1440,1560,1680,1800,1920,2040,2160]
scale_factor = height/240
square_length = height//8
window = pygame.display.set_mode((height,height))
running = True
clock = pygame.time.Clock()


alternative_board = False
selected = None
rects = []
for rect in range(64):
    rects.append(pygame.Rect(rect%8*square_length,height-square_length-(rect//8*square_length),square_length,square_length))


black_king = pygame.transform.smoothscale_by(pygame.image.load(os.path.join('assets\\black_king.png')).convert_alpha(),scale_factor*0.25)
white_king = pygame.transform.smoothscale_by(pygame.image.load(os.path.join('assets', 'white_king.png')).convert_alpha(),scale_factor*0.25)
black_pawn = pygame.transform.smoothscale_by(pygame.image.load(os.path.join('assets', 'black_pawn.png')).convert_alpha(),scale_factor*0.25)
white_pawn = pygame.transform.smoothscale_by(pygame.image.load(os.path.join('assets', 'white_pawn.png')).convert_alpha(),scale_factor*0.25)
black_knight = pygame.transform.smoothscale_by(pygame.image.load(os.path.join('assets', 'black_knight.png')).convert_alpha(),scale_factor*0.25)
white_knight = pygame.transform.smoothscale_by(pygame.image.load(os.path.join('assets', 'white_knight.png')).convert_alpha(),scale_factor*0.25)
black_bishop = pygame.transform.smoothscale_by(pygame.image.load(os.path.join('assets', 'black_bishop.png')).convert_alpha(),scale_factor*0.25)
white_bishop = pygame.transform.smoothscale_by(pygame.image.load(os.path.join('assets', 'white_bishop.png')).convert_alpha(),scale_factor*0.25)
black_rook = pygame.transform.smoothscale_by(pygame.image.load(os.path.join('assets', 'black_rook.png')).convert_alpha(),scale_factor*0.25)
white_rook = pygame.transform.smoothscale_by(pygame.image.load(os.path.join('assets', 'white_rook.png')).convert_alpha(),scale_factor*0.25)
black_queen = pygame.transform.smoothscale_by(pygame.image.load(os.path.join('assets', 'black_queen.png')).convert_alpha(),scale_factor*0.25)
white_queen = pygame.transform.smoothscale_by(pygame.image.load(os.path.join('assets', 'white_queen.png')).convert_alpha(),scale_factor*0.25)
board = pygame.transform.scale_by(pygame.image.load(os.path.join('assets', 'board.png')).convert_alpha(),scale_factor)
board2 = pygame.transform.scale_by(pygame.image.load(os.path.join('assets', 'board2.png')).convert_alpha(),scale_factor)




def change_resolution(more_or_less):
    global height, scale_factor, square_length, board, rects, selected, black_king, white_king, black_pawn, white_pawn, black_knight, white_knight, black_bishop, white_bishop, black_rook, white_rook, black_queen, white_queen, board2
    if more_or_less == "more" and heights[heights.index(height)+1]<screen_height:
        height = heights[heights.index(height)+1]
    elif more_or_less == "less" and heights[heights.index(height)-1]>=360:
        if heights.index(height) == 0:
            return
        else:
            height = heights[heights.index(height)-1]
    else:
        return
    window = pygame.display.set_mode((height,height))
    scale_factor = height/240
    square_length = height/8
    black_king = pygame.transform.smoothscale_by(pygame.image.load(os.path.join('assets', 'black_king.png')).convert_alpha(),scale_factor*0.25)
    white_king = pygame.transform.smoothscale_by(pygame.image.load(os.path.join('assets', 'white_king.png')).convert_alpha(),scale_factor*0.25)
    black_pawn = pygame.transform.smoothscale_by(pygame.image.load(os.path.join('assets', 'black_pawn.png')).convert_alpha(),scale_factor*0.25)
    white_pawn = pygame.transform.smoothscale_by(pygame.image.load(os.path.join('assets', 'white_pawn.png')).convert_alpha(),scale_factor*0.25)
    black_knight = pygame.transform.smoothscale_by(pygame.image.load(os.path.join('assets', 'black_knight.png')).convert_alpha(),scale_factor*0.25)
    white_knight = pygame.transform.smoothscale_by(pygame.image.load(os.path.join('assets', 'white_knight.png')).convert_alpha(),scale_factor*0.25)
    black_bishop = pygame.transform.smoothscale_by(pygame.image.load(os.path.join('assets', 'black_bishop.png')).convert_alpha(),scale_factor*0.25)
    white_bishop = pygame.transform.smoothscale_by(pygame.image.load(os.path.join('assets', 'white_bishop.png')).convert_alpha(),scale_factor*0.25)
    black_rook = pygame.transform.smoothscale_by(pygame.image.load(os.path.join('assets', 'black_rook.png')).convert_alpha(),scale_factor*0.25)
    white_rook = pygame.transform.smoothscale_by(pygame.image.load(os.path.join('assets', 'white_rook.png')).convert_alpha(),scale_factor*0.25)
    black_queen = pygame.transform.smoothscale_by(pygame.image.load(os.path.join('assets', 'black_queen.png')).convert_alpha(),scale_factor*0.25)
    white_queen = pygame.transform.smoothscale_by(pygame.image.load(os.path.join('assets', 'white_queen.png')).convert_alpha(),scale_factor*0.25)
    board = pygame.transform.scale_by(pygame.image.load(os.path.join('assets', 'board.png')).convert_alpha(),scale_factor)
    board2 = pygame.transform.scale_by(pygame.image.load(os.path.join('assets', 'board2.png')).convert_alpha(),scale_factor)
    selected = None
    rects = []
    for rect in range(64):
        rects.append(pygame.Rect(rect%8*square_length,height-square_length-(rect//8*square_length),square_length,square_length))


def draw_pieces():
    for piece in logic.board:
        if piece:
            if piece.type == "pawn":
                if piece.color == "white":
                    window.blit(white_pawn, (piece.position%8*square_length,height-square_length-(piece.position//8*square_length)))
                else:
                    window.blit(black_pawn, (piece.position%8*square_length,height-square_length-(piece.position//8*square_length)))
            if piece.type == "rook":
                if piece.color == "white":
                    window.blit(white_rook, (piece.position%8*square_length,height-square_length-(piece.position//8*square_length)))
                else:
                    window.blit(black_rook, (piece.position%8*square_length,height-square_length-(piece.position//8*square_length)))
            if piece.type == "knight":
                if piece.color == "white":
                    window.blit(white_knight, (piece.position%8*square_length,height-square_length-(piece.position//8*square_length)))
                else:
                    window.blit(black_knight, (piece.position%8*square_length,height-square_length-(piece.position//8*square_length)))
            if piece.type == "bishop":
                if piece.color == "white":
                    window.blit(white_bishop, (piece.position%8*square_length,height-square_length-(piece.position//8*square_length)))
                else:
                    window.blit(black_bishop, (piece.position%8*square_length,height-square_length-(piece.position//8*square_length)))
            if piece.type == "queen":
                if piece.color == "white":
                    window.blit(white_queen, (piece.position%8*square_length,height-square_length-(piece.position//8*square_length)))
                else:
                    window.blit(black_queen, (piece.position%8*square_length,height-square_length-(piece.position//8*square_length)))
            if piece.type == "king":
                if piece.color == "white":
                    window.blit(white_king, (piece.position%8*square_length,height-square_length-(piece.position//8*square_length)))
                else:
                    window.blit(black_king, (piece.position%8*square_length,height-square_length-(piece.position//8*square_length)))

def detect_input():
    global running, selected, alternative_board, selected
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for rect in rects:
                    if rect.collidepoint(event.pos):
                        previous_selected=selected
                        selected = int(rect.x//square_length+(height-square_length-rect.y)//square_length*8)
                        if selected is not None and previous_selected is not None and logic.board[previous_selected] and selected in logic.board[previous_selected].legal_moves:
                            logic.board[previous_selected].move(selected)
                            selected = None
                            print(f"stalemate: {logic.is_stalemate()}")
                        if selected and logic.board[selected] and logic.board[selected].color != logic.turn:
                            selected = None
                        elif selected and not logic.board[selected]:
                            selected = None
                            
                        


        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F2:
                change_resolution("more")
            elif event.key == pygame.K_F1:
                change_resolution("less")
            elif event.key == pygame.K_b:
                alternative_board = not alternative_board
            elif event.key == pygame.K_ESCAPE:
                selected = None


def draw_legal_moves():
    if selected is not None and logic.board[selected]:
        for move in logic.board[selected].legal_moves:
                pygame.draw.circle(window, "red", (move%8*square_length+square_length/2, height-square_length/2-(move//8*square_length)), square_length/10)

                


while running:
    window.fill("gray")
    if alternative_board:
        window.blit(board2,(0,0))
    else:
        window.blit(board,(0,0))

    if selected is not None:
        pygame.draw.rect(window, "yellow", (selected%8*square_length, height-square_length-(selected//8*square_length), square_length, square_length))

    draw_pieces()
        
    detect_input() 

    draw_legal_moves()
    
    

    pygame.display.flip()
    
    clock.tick(60)


pygame.quit()
