# Tic Tac Toe

import numpy as np
import pygame
import os

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800

WHITE=(255,255,255)
BLACK=(0,0,0)
GRAY=(180,180,180)

pygame.init()

current_path = os.getcwd()
asset_image_path = os.path.join(current_path, "assets/image")
asset_sound_path = os.path.join(current_path, "assets/sound")

font_basic=pygame.font.SysFont('FixedSys',40,True,False)
font_menu=pygame.font.SysFont('FixedSys',50,True,False)

pygame.display.set_caption('20191097 Project1')

screen=pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

clock=pygame.time.Clock()

#load many many assets
board = pygame.image.load(os.path.join(asset_image_path, "board.png"))
title = pygame.image.load(os.path.join(asset_image_path, "title.png"))
o_1 = pygame.image.load(os.path.join(asset_image_path, "o_1.png"))
o_2 = pygame.image.load(os.path.join(asset_image_path, "o_2.png"))
o_3 = pygame.image.load(os.path.join(asset_image_path, "o_3.png"))
x_1 = pygame.image.load(os.path.join(asset_image_path, "x_1.png"))
x_2 = pygame.image.load(os.path.join(asset_image_path, "x_2.png"))
x_3 = pygame.image.load(os.path.join(asset_image_path, "x_3.png"))
o_mouse = pygame.image.load(os.path.join(asset_image_path, "o_mouse.png"))
x_mouse = pygame.image.load(os.path.join(asset_image_path, "x_mouse.png"))
button_x = pygame.image.load(os.path.join(asset_image_path, "button_x.png"))
button_o = pygame.image.load(os.path.join(asset_image_path, "button_o.png"))
blank = pygame.image.load(os.path.join(asset_image_path, "blank.png"))
o_sound = pygame.mixer.Sound(os.path.join(asset_sound_path, 'o_sound.wav'))
x_sound = pygame.mixer.Sound(os.path.join(asset_sound_path, 'x_sound.wav'))
click_sound = pygame.mixer.Sound(os.path.join(asset_sound_path, 'click.wav'))

def whoGoesFirst():
    # Randomly choose the player who goes first.
        return np.random.choice(['computer','player'])

def makeMove(board, letter, move):
    board[move] = letter

def isWinner(bo, le):
    # Given a board and a player's letter, this function returns True if that player has won.
    # We use bo instead of board and le instead of letter so we don't have to type as much.
    return ((bo[7] == le and bo[8] == le and bo[9] == le) or # across the top
    (bo[4] == le and bo[5] == le and bo[6] == le) or # across the middle
    (bo[1] == le and bo[2] == le and bo[3] == le) or # across the bottom
    (bo[7] == le and bo[4] == le and bo[1] == le) or # down the left side
    (bo[8] == le and bo[5] == le and bo[2] == le) or # down the middle
    (bo[9] == le and bo[6] == le and bo[3] == le) or # down the right side
    (bo[7] == le and bo[5] == le and bo[3] == le) or # diagonal
    (bo[9] == le and bo[5] == le and bo[1] == le)) # diagonal

def getBoardCopy(board):
    # Make a copy of the board list and return it.
    boardCopy = []
    for i in board:
        boardCopy.append(i)
    return boardCopy

def isSpaceFree(board, move):
    # Return true if the passed move is free on the passed board.
    return board[move] == ' '

def isBoardFull(board):
    # Return True if every space on the board has been taken. Otherwise return False.
    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False
    return True



def getgametree(currentboard, letter):
    if letter == 'O':
        counterletter = 'X'
    else:
        counterletter = 'O'
    trees = [currentboard,[]]
    for i in range(1,10):
        branch = currentboard.copy()
        if not (isWinner(branch, letter) or isWinner(branch, counterletter)): #skip making gametree if game is already over
            if branch[i] == ' ': #make move in only empty spaces
                makeMove(branch, letter,i)
                branch[0]=str(evaluate(branch)) + letter
                trees[1].append(branch)

    for b in range(len(trees[1])):
        b_branch=trees[1][b]
        trees[1][b]=getgametree(b_branch, counterletter)
    return trees

def evaluate(currentboard):
    if isWinner(currentboard, computerLetter):
        heuristic = 5
    elif isWinner(currentboard, playerLetter):
        heuristic = 0
    elif isBoardFull(currentboard):
        heuristic = 2
    else:
        heuristic = ' '
    return heuristic

def choose(tree):
    heus=[]
    for branches in tree[1]:
        heus.append(branches[0][0][0])
    if heus != [] and ' ' not in heus:
        if tree[0][0][1]==computerLetter:#previous turn was player
            tree[0][0]=str(min(heus)) + computerLetter
        elif tree[0][0][1]==playerLetter:#previous turn was com
            tree[0][0]=str(max(heus)) + playerLetter
    return heus

def get_all_heus(tree):
    tree2=tree.copy()
    if ' ' not in choose(tree2) and len(choose(tree2))>0:
        choose(tree)
    else:
        for subtree in tree[1]:
            get_all_heus(subtree)

def get_com_move(gametree):
    possibles=[]
    for i in range(len(gametree[1])):#tree(branch[])
        if gametree[0][0][0] == gametree[1][i][0][0][0]:
            possibles.append(gametree[1][i][0])#branches
    print(possibles)
    commove=possibles[np.random.randint(0,len(possibles))]
    return commove

def is_on_mouse(x, y, width, height): #If mouse is on the rect, return True
    m_pos = pygame.mouse.get_pos()
    m_x = m_pos[0]
    m_y = m_pos[1]
    if m_x > x and m_x < x + width:
        if m_y > y and m_y < y + height:
            return True
        else:
            return False
    else:
        return False

def interactive_text(text, x, y): #If text is on the mouse, text color becomes black. Not on, text color is gray.
    text_gray = font_menu.render(text, True, GRAY)
    text_black = font_menu.render(text, True, BLACK)
    text_width = text_black.get_rect()[2]
    text_height = text_black.get_rect()[3]
    if is_on_mouse(x, y, text_width, text_height):
        screen.blit(text_black, [x, y])
        return True
    else:
        screen.blit(text_gray, [x, y])
        return False

def get_random_ox_img(ox): #get the random image of o and x
    if ox == 'O':
        img = np.random.choice([o_1, o_2, o_3])
    elif ox == 'X':
        img = np.random.choice([x_1, x_2, x_3])
    else:
        img = blank
    return img

def tile_finder(): #tell mouse is on which tile
    tile_pos=[[0,400],[200,400],[400,400],[0,200],[200,200],[400,200],[0,0],[200,0],[400,0]] # lefttop position of each tiles. 
    for i in range(9):
        tx=tile_pos[i][0]
        ty=tile_pos[i][1]
        if is_on_mouse(tx,ty,200,200):
            return i + 1

def ox_mouse(ox):
    if is_on_mouse(0,0,600,600):
        m_pos = pygame.mouse.get_pos()
        m_x = m_pos[0]
        m_y = m_pos[1]
        if ox == 'X':
            screen.blit(x_mouse,[m_x-x_mouse.get_width()/2, m_y-x_mouse.get_height()/2])
        if ox == 'O':
            screen.blit(o_mouse,[m_x-o_mouse.get_width()/2, m_y-o_mouse.get_height()/2])      

done=False
play_multi, play_single = False, False
playing = False
selecting_shape = False
back_to_menu = False
board_coords = [[0,0],[30,430],[230,430],[430,430],[30,230],[230,230],[430,230],[30,30],[230,30],[430,30]]
player_input = 0
theBoard = [' '] * 10 #reset board
turn = whoGoesFirst()
lastclick = pygame.time.get_ticks()
one_game_end=True
replay=False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.MOUSEBUTTONDOWN and quit == True: #quit the game at the title
            done = True

        if event.type == pygame.MOUSEBUTTONDOWN and singleplay == True: #click singleplay at title
            play_single = True
            playing = True
            selecting_shape = True #go to selecting shape page
            gamemode = 'single'
            singleplay = False #no singplay button in selecting time. So become False.
            lastclick=pygame.time.get_ticks()
            click_sound.play()

        if event.type == pygame.MOUSEBUTTONDOWN and multiplay == True: #click multiplay at title
            play_multi = True
            playing = True
            selecting_shape = True #go to selecting shape page
            gamemode = 'multi'
            multiplay = False #no multiplay button in selecting time. So become False.
            lastclick=pygame.time.get_ticks()
            click_sound.play()

        if event.type == pygame.MOUSEBUTTONDOWN and back_to_menu == True: #click multiplay at title
            player_input = 0
            theBoard = [' '] * 10 #reset board
            turn = whoGoesFirst()
            play_multi, play_single, playing = False, False, False #go to title
            back_to_menu = False #cause no back to menu button in title.
            click_sound.play()

        if event.type == pygame.MOUSEBUTTONDOWN and replay == True: #click multiplay at title
            player_input = 0
            theBoard = [' '] * 10 #reset board
            turn = whoGoesFirst()
            one_game_end=False
            replay = False
            lastclick = pygame.time.get_ticks()
            click_sound.play()

        if selecting_shape == True: # shape selecting
            if event.type == pygame.MOUSEBUTTONDOWN and is_on_mouse(40,350,button_o.get_rect()[2],button_o.get_rect()[3]):
                if pygame.time.get_ticks() > lastclick + 350:
                    shapes = ['O','X'] #player1, 2(COM)
                    one_game_end=False
                    selecting_shape = False  #select completed
                    lastclick = pygame.time.get_ticks()
                    click_sound.play()
             
            if event.type == pygame.MOUSEBUTTONDOWN and is_on_mouse(350,350,button_x.get_rect()[2],button_x.get_rect()[3]):
                if pygame.time.get_ticks() > lastclick + 350:
                    shapes = ['X','O'] #player1, 2(COM)
                    one_game_end=False
                    selecting_shape = False #shape completed
                    lastclick = pygame.time.get_ticks()
                    click_sound.play()


        if one_game_end == False and turn[0]=='p': #get player input
            if event.type == pygame.MOUSEBUTTONDOWN and tile_finder() != None:
                if isSpaceFree(theBoard, tile_finder()):
                    if pygame.time.get_ticks() > lastclick + 350:
                        player_input = tile_finder()
                        lastclick = pygame.time.get_ticks()



    if playing == False and play_multi == False and play_single == False:  #title display
        screen.fill(WHITE)
        screen.blit(title, [23, 150])
        singleplay = interactive_text('single play', 200, 300) #whether singlplay button is clicked
        multiplay = interactive_text('multi play', 200, 400) #whether multiplay button is clicked
        quit = interactive_text('quit', 250, 500) #whether quit button is clicked

    if playing == True:
        if selecting_shape == True: #show shape selecting UI
            now = pygame.time.get_ticks()
            screen.fill(WHITE)
            if play_multi:
                screen.blit(font_menu.render('multiplay', True, BLACK), [200, 160])
            if play_single:
                screen.blit(font_menu.render('singleplay', True, BLACK), [200, 160])

            screen.blit(font_menu.render('select shape', True, BLACK), [180, 200])
            screen.blit(button_o, [40, 350])
            screen.blit(button_x, [350, 350])
            back_to_menu = interactive_text('back to menu', 20, 750)

        else: #select completed. Let's go to game!   
            screen.fill(WHITE) 
            screen.blit(board,[0,0])     

            for i in range(1,10):
                    ox_img = get_random_ox_img(theBoard[i])
                    ox_img_coords = board_coords[i]
                    screen.blit(ox_img, ox_img_coords)


            #Single play
            if play_single and one_game_end==False:
                playerLetter, computerLetter = shapes
                turn_message = font_basic.render('Now turn: ' + turn, True, BLACK)
                screen.blit(turn_message, [150,620])
                ox_mouse(playerLetter)

                if turn == 'player':
                    if player_input != 0:
                        move = player_input
                        player_input=0
                        if isSpaceFree(theBoard, move):
                            makeMove(theBoard, playerLetter, move)
                            if playerLetter=='O':
                                o_sound.play()
                            else:
                                x_sound.play()
                            if isWinner(theBoard, playerLetter):
                                winner=turn
                                one_game_end = True
                            else:
                                if isBoardFull(theBoard):
                                    winner='draw'
                                    one_game_end = True
                                else:
                                    turn = 'computer'

                else:
                    if lastclick + 800 < pygame.time.get_ticks():
                        # Computer's turn.
                        theBoard[0]=' '+playerLetter
                        treeofgame=getgametree(theBoard,computerLetter)
                        for i in range(len(treeofgame[1])):
                            get_all_heus(treeofgame)
                        move = get_com_move(treeofgame)
                        theBoard=move
                        if computerLetter=='O':
                                o_sound.play()
                        else:
                                x_sound.play()
                        if isWinner(theBoard, computerLetter):
                            winner=turn
                            one_game_end = True
                        else:
                            if isBoardFull(theBoard):
                                winner='draw'
                                one_game_end = True
                            else:
                                turn = 'player'
                                
            elif play_single and one_game_end:
                if winner=='player':
                    screen.blit(font_basic.render('You Win!!', True, BLACK),[200,640])
                elif winner=='computer':
                    screen.blit(font_basic.render('You Lose...', True, BLACK),[200,640])
                elif winner=='draw':
                    screen.blit(font_basic.render('Draw.', True, BLACK),[200,640])
                replay=interactive_text("Replay",100,670)
                back_to_menu=interactive_text("Back to menu", 250,670)

            if play_multi and one_game_end==False:
                player1Letter, player2Letter = shapes
                if turn=='computer':
                    turn='player2'
                elif turn=='player':
                    turn='player1'
                turn_message = font_basic.render('Now turn: ' + turn, True, BLACK)
                screen.blit(turn_message, [150,620])
                
                if turn=='player1':
                    ox_mouse(player1Letter)
                    if player_input != 0:
                        move = player_input
                        player_input=0
                        if isSpaceFree(theBoard, move):
                            makeMove(theBoard, player1Letter, move)
                            if player1Letter=='O':
                                o_sound.play()
                            else:
                                x_sound.play()

                            if isWinner(theBoard, player1Letter):
                                winner=turn
                                one_game_end = True
                            else:
                                if isBoardFull(theBoard):
                                    winner='draw'
                                    one_game_end = True
                                else:
                                    turn = 'player2'
                if turn=='player2':
                    ox_mouse(player2Letter)
                    if player_input != 0:
                        move = player_input
                        player_input=0
                        if isSpaceFree(theBoard, move):
                            makeMove(theBoard, player2Letter, move)
                            if player2Letter=='O':
                                o_sound.play()
                            else:
                                x_sound.play()

                            if isWinner(theBoard, player2Letter):
                                winner=turn
                                one_game_end = True
                            else:
                                if isBoardFull(theBoard):
                                    winner='draw'
                                    one_game_end = True
                                else:
                                    turn = 'player1'

            elif play_multi and one_game_end:
                if winner != 'draw':
                    screen.blit(font_basic.render(turn + ' Win', True, BLACK),[200,640])
                else:
                    screen.blit(font_basic.render('Draw.', True, BLACK),[200,640])
                replay=interactive_text("Replay",100,670)
                back_to_menu=interactive_text("Back to menu", 250,670)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
