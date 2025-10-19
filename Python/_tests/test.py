import tkinter as tk
from tkinter import messagebox
import random
import time
from copy import deepcopy

# --- Chess Piece Symbols ---
pieces = {
    'bR':'♜','bN':'♞','bB':'♝','bQ':'♛','bK':'♚','bP':'♟',
    'wR':'♖','wN':'♘','wB':'♗','wQ':'♕','wK':'♔','wP':'♙',
    '  ':' '
}

# --- Initial Board Setup ---
initial_board = [
    ['bR','bN','bB','bQ','bK','bB','bN','bR'],
    ['bP']*8,
    ['  ']*8,
    ['  ']*8,
    ['  ']*8,
    ['  ']*8,
    ['wP']*8,
    ['wR','wN','wB','wQ','wK','wB','wN','wR']
]

# --- Game State ---
board = [row[:] for row in initial_board]
current_player = 'w'
selected_piece = None
selected_coords = None
player_view_flipped = False
mode = "2P"
castling_rights = {'wK': True,'wQ': True,'bK': True,'bQ': True}
king_positions = {'w':(7,4),'b':(0,4)}

# --- Tkinter setup ---
root = tk.Tk()
root.title("Chess Game")
root.geometry("600x650")
root.resizable(False, False)

frame = tk.Frame(root)
frame.pack(expand=True, fill='both')
buttons = [[None for _ in range(8)] for _ in range(8)]

# --- Move Helpers ---
def in_bounds(i,j):
    return 0<=i<8 and 0<=j<8

def is_check(player,temp_board=None):
    if temp_board is None:
        temp_board = board
    ki,kj = king_positions[player]
    enemy = 'b' if player=='w' else 'w'
    for i in range(8):
        for j in range(8):
            piece = temp_board[i][j]
            if piece != '  ' and piece[0]==enemy:
                for move in generate_moves(piece,(i,j),temp_board,ignore_check=True):
                    if move==(ki,kj):
                        return True
    return False

def is_checkmate(player):
    for i in range(8):
        for j in range(8):
            piece=board[i][j]
            if piece!='  ' and piece[0]==player:
                for move in generate_moves(piece,(i,j)):
                    temp_board = deepcopy(board)
                    make_move_on_board((i,j),move,temp_board)
                    temp_king_pos = deepcopy(king_positions)
                    if piece[1]=='K':
                        temp_king_pos[player] = move
                    if not is_check(player,temp_board):
                        return False
    return is_check(player)

def generate_moves(piece,pos,temp_board=None,ignore_check=False):
    if temp_board is None:
        temp_board = board
    i,j = pos
    color = piece[0]
    enemy = 'b' if color=='w' else 'w'
    p_type = piece[1]
    moves=[]
    
    if p_type=='P':
        step = -1 if color=='w' else 1
        if in_bounds(i+step,j) and temp_board[i+step][j]=='  ':
            moves.append((i+step,j))
            if (i==6 and color=='w') or (i==1 and color=='b'):
                if temp_board[i+2*step][j]=='  ':
                    moves.append((i+2*step,j))
        for dj in [-1,1]:
            if in_bounds(i+step,j+dj) and temp_board[i+step][j+dj]!='  ' and temp_board[i+step][j+dj][0]==enemy:
                moves.append((i+step,j+dj))

    elif p_type=='N':
        knight_moves=[(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
        for di,dj in knight_moves:
            ni,nj = i+di,j+dj
            if in_bounds(ni,nj) and (temp_board[ni][nj]=='  ' or temp_board[ni][nj][0]==enemy):
                moves.append((ni,nj))

    elif p_type=='R':
        directions=[(-1,0),(1,0),(0,-1),(0,1)]
    elif p_type=='B':
        directions=[(-1,-1),(-1,1),(1,-1),(1,1)]
    elif p_type=='Q':
        directions=[(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
    elif p_type=='K':
        for di in [-1,0,1]:
            for dj in [-1,0,1]:
                if di==0 and dj==0: continue
                ni,nj=i+di,j+dj
                if in_bounds(ni,nj) and (temp_board[ni][nj]=='  ' or temp_board[ni][nj][0]==enemy):
                    moves.append((ni,nj))
        if not ignore_check:
            # Castling
            if color=='w':
                if castling_rights['wK']:
                    if temp_board[7][5]=='  ' and temp_board[7][6]=='  ':
                        tmp=deepcopy(temp_board); tmp[7][4]='  '; tmp[7][5]='wK'
                        if not is_check(color,tmp): moves.append((7,6))
                if castling_rights['wQ']:
                    if temp_board[7][3]=='  ' and temp_board[7][2]=='  ' and temp_board[7][1]=='  ':
                        tmp=deepcopy(temp_board); tmp[7][4]='  '; tmp[7][3]='wK'
                        if not is_check(color,tmp): moves.append((7,2))
            else:
                if castling_rights['bK']:
                    if temp_board[0][5]=='  ' and temp_board[0][6]=='  ':
                        tmp=deepcopy(temp_board); tmp[0][4]='  '; tmp[0][5]='bK'
                        if not is_check(color,tmp): moves.append((0,6))
                if castling_rights['bQ']:
                    if temp_board[0][3]=='  ' and temp_board[0][2]=='  ' and temp_board[0][1]=='  ':
                        tmp=deepcopy(temp_board); tmp[0][4]='  '; tmp[0][3]='bK'
                        if not is_check(color,tmp): moves.append((0,2))
    # Sliding pieces
    if p_type in ['R','B','Q']:
        for di,dj in directions:
            ni,nj=i+di,j+dj
            while in_bounds(ni,nj):
                if temp_board[ni][nj]=='  ':
                    moves.append((ni,nj))
                elif temp_board[ni][nj][0]==enemy:
                    moves.append((ni,nj))
                    break
                else:
                    break
                ni+=di; nj+=dj

    # Filter illegal moves leaving king in check
    if not ignore_check:
        legal=[]
        for move in moves:
            tmp=deepcopy(temp_board)
            make_move_on_board((i,j),move,tmp)
            tmp_king_pos=deepcopy(king_positions)
            if p_type=='K':
                tmp_king_pos[color]=move
            if not is_check(color,tmp):
                legal.append(move)
        return legal
    return moves

def make_move_on_board(start,end,temp_board):
    piece = temp_board[start[0]][start[1]]
    temp_board[end[0]][end[1]] = piece
    temp_board[start[0]][start[1]] = '  '
    # Castling rook
    if piece[1]=='K':
        if start[1]==4 and end[1]==6:
            temp_board[start[0]][7],temp_board[start[0]][5]='  ',piece[0]+'R'
        elif start[1]==4 and end[1]==2:
            temp_board[start[0]][0],temp_board[start[0]][3]='  ',piece[0]+'R'

def move_piece_animation(start,end):
    si,sj=start; ei,ej=end
    piece=board[si][sj]; steps=5
    board[si][sj]='  '
    for step in range(1,steps+1):
        interm_i = si + (ei-si)*step/steps
        interm_j = sj + (ej-sj)*step/steps
        update_board(temp_piece=(piece,interm_i,interm_j))
        root.update(); time.sleep(0.05)
    board[ei][ej]=piece
    # Castling rook
    if piece[1]=='K':
        if sj==4 and ej==6: board[ei][7],board[ei][5]='  ',piece[0]+'R'
        elif sj==4 and ej==2: board[ei][0],board[ei][3]='  ',piece[0]+'R'
    update_board()

def move_piece(start,end):
    global king_positions,castling_rights
    piece=board[start[0]][start[1]]
    move_piece_animation(start,end)
    if piece[1]=='K':
        king_positions[piece[0]]=end
        castling_rights[piece[0]+'K']=False
        castling_rights[piece[0]+'Q']=False
    if piece[1]=='R':
        if start==(7,0): castling_rights['wQ']=False
        if start==(7,7): castling_rights['wK']=False
        if start==(0,0): castling_rights['bQ']=False
        if start==(0,7): castling_rights['bK']=False

# --- GUI ---
def update_board(temp_piece=None):
    for i in range(8):
        for j in range(8):
            di,dj=(7-i,7-j) if player_view_flipped else (i,j)
            bg='white' if (i+j)%2==0 else 'gray'
            txt=pieces[board[i][j]]
            if temp_piece:
                p,pi,pj=temp_piece
                if int(round(pi))==i and int(round(pj))==j: txt=pieces[p]
            buttons[di][dj].config(text=txt,bg=bg)

def on_click(i,j):
    global selected_piece,selected_coords,current_player
    ri,rj=(7-i,7-j) if player_view_flipped else (i,j)
    piece=board[ri][rj]
    if selected_piece:
        if (ri,rj) in generate_moves(selected_piece,selected_coords):
            move_piece(selected_coords,(ri,rj))
            if is_checkmate('b' if current_player=='w' else 'w'):
                messagebox.showinfo("Checkmate",f"{current_player.upper()} wins!")
            switch_player()
        selected_piece=None; selected_coords=None; update_board()
    else:
        if piece!='  ' and piece[0]==current_player:
            selected_piece=piece; selected_coords=(ri,rj)

def switch_player():
    global current_player, player_view_flipped
    current_player='b' if current_player=='w' else 'w'
    if flip_var.get(): player_view_flipped=not player_view_flipped
    update_board()
    if mode=='AI' and current_player=='b':
        root.after(500, ai_move)

def ai_move():
    moves=[]
    for i in range(8):
        for j in range(8):
            piece=board[i][j]
            if piece!='  ' and piece[0]=='b':
                for move in generate_moves(piece,(i,j)):
                    moves.append(((i,j),move))
    if moves:
        start,end=random.choice(moves)
        move_piece(start,end)
        if is_checkmate('w'): messagebox.showinfo("Checkmate","AI wins!")
        switch_player()

# --- Build board buttons ---
for i in range(8):
    for j in range(8):
        bg='white' if (i+j)%2==0 else 'gray'
        btn=tk.Button(frame,text=pieces[board[i][j]],font=("Arial",32),bg=bg,
                      command=lambda i=i,j=j:on_click(i,j))
        btn.grid(row=i,column=j,sticky='nsew')
        buttons[i][j]=btn

for i in range(8):
    frame.rowconfigure(i,weight=1)
    frame.columnconfigure(i,weight=1)

# --- Menu ---
menu = tk.Menu(root)
root.config(menu=menu)
game_menu=tk.Menu(menu,tearoff=0)
menu.add_cascade(label="Game",menu=game_menu)
flip_var=tk.BooleanVar(value=True)

def set_mode_2p(): global mode; mode='2P'; reset_game()
def set_mode_ai(): global mode; mode='AI'; reset_game()
def toggle_flip(): pass # already handled by flip_var
def reset_game():
    global board,current_player,player_view_flipped,king_positions,castling_rights
    board=[row[:] for row in initial_board]
    current_player='w'
    player_view_flipped=False
    king_positions={'w':(7,4),'b':(0,4)}
    castling_rights={'wK':True,'wQ':True,'bK':True,'bQ':True}
    update_board()
    if mode=='AI' and current_player=='b': root.after(500,ai_move)

game_menu.add_command(label="2 Players", command=set_mode_2p)
game_menu.add_command(label="Vs AI", command=set_mode_ai)
game_menu.add_checkbutton(label="Flip Board", variable=flip_var)
game_menu.add_command(label="Reset Game", command=reset_game)

update_board()
root.mainloop()
