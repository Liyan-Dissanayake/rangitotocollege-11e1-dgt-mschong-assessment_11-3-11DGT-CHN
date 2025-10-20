import tkinter as tk
from tkinter import messagebox
import random
from copy import deepcopy

# --- Chess Piece Symbols ---
pieces = {
    'bR':'♜','bN':'♞','bB':'♝','bQ':'♛','bK':'♚','bP':'♟',
    'wR':'♖','wN':'♘','wB':'♗','wQ':'♕','wK':'♔','wP':'♙',
    '  ':' '
}

# --- Piece Values for AI (material) ---
piece_values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 1000}

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
current_player = 'w'          # 'w' or 'b'
selected_piece = None
selected_coords = None
player_view_flipped = False
mode = "2P"                  # "2P" or "AI"
ai_difficulty = "Easy"
king_positions = {'w':(7,4),'b':(0,4)}
game_over = False

# --- Helpers ---
def in_bounds(i,j):
    return 0 <= i < 8 and 0 <= j < 8

def find_king(player, temp_board):
    key = player + 'K'
    for i in range(8):
        for j in range(8):
            if temp_board[i][j] == key:
                return (i,j)
    return None

def make_move_on_board(start, end, temp_board):
    """Apply move on given board. Pawn auto-promotes to Q."""
    si,sj = start
    ei,ej = end
    piece = temp_board[si][sj]
    temp_board[ei][ej] = piece
    temp_board[si][sj] = '  '
    # pawn promotion
    if piece[1] == 'P':
        if (piece[0] == 'w' and ei == 0) or (piece[0] == 'b' and ei == 7):
            temp_board[ei][ej] = piece[0] + 'Q'

def is_check(player, temp_board=None):
    """True if player's king is attacked on temp_board."""
    if temp_board is None:
        temp_board = board
    king_pos = find_king(player, temp_board)
    if king_pos is None:
        # missing king -> treat as 'in check' (used by search)
        return True
    ki,kj = king_pos
    enemy = 'b' if player=='w' else 'w'
    # Check if any enemy move (raw attacks) hits the king position
    for i in range(8):
        for j in range(8):
            p = temp_board[i][j]
            if p != '  ' and p[0] == enemy:
                for mv in generate_moves(p, (i,j), temp_board, ignore_check=True):
                    if mv == (ki,kj):
                        return True
    return False

def generate_moves(piece, pos, temp_board=None, ignore_check=False):
    """
    Generate pseudo-legal moves for piece at pos on temp_board.
    If ignore_check==False filter out moves that leave own king in check.
    """
    if temp_board is None:
        temp_board = board
    i,j = pos
    color = piece[0]
    enemy = 'b' if color=='w' else 'w'
    p_type = piece[1]
    moves = []

    # Pawn
    if p_type == 'P':
        step = -1 if color == 'w' else 1
        start_row = 6 if color == 'w' else 1
        # forward one
        ni, nj = i+step, j
        if in_bounds(ni,nj) and temp_board[ni][nj] == '  ':
            moves.append((ni,nj))
            # forward two
            ni2 = i + 2*step
            if i == start_row and in_bounds(ni2,nj) and temp_board[ni2][nj] == '  ':
                moves.append((ni2,nj))
        # captures
        for dj in (-1, 1):
            ci, cj = i + step, j + dj
            if in_bounds(ci,cj) and temp_board[ci][cj] != '  ' and temp_board[ci][cj][0] == enemy:
                moves.append((ci,cj))
        # (en-passant not implemented)

    # Knight
    elif p_type == 'N':
        knight_moves = [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
        for di,dj in knight_moves:
            ni,nj = i+di, j+dj
            if in_bounds(ni,nj) and (temp_board[ni][nj] == '  ' or temp_board[ni][nj][0] == enemy):
                moves.append((ni,nj))

    # Bishop / Rook / Queen (sliders)
    elif p_type in ('B','R','Q'):
        if p_type == 'B':
            directions = [(-1,-1),(-1,1),(1,-1),(1,1)]
        elif p_type == 'R':
            directions = [(-1,0),(1,0),(0,-1),(0,1)]
        else:  # Q
            directions = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]

        for di,dj in directions:
            ni,nj = i+di, j+dj
            while in_bounds(ni,nj):
                if temp_board[ni][nj] == '  ':
                    moves.append((ni,nj))
                elif temp_board[ni][nj][0] == enemy:
                    moves.append((ni,nj))
                    break
                else:
                    # own piece blocks
                    break
                ni += di; nj += dj

    # King
    elif p_type == 'K':
        for di in (-1,0,1):
            for dj in (-1,0,1):
                if di==0 and dj==0: continue
                ni,nj = i+di, j+dj
                if in_bounds(ni,nj) and (temp_board[ni][nj] == '  ' or temp_board[ni][nj][0] == enemy):
                    moves.append((ni,nj))
        # castling not implemented here (would require additional state & checks)

    # Filter illegal moves that leave own king in check
    if not ignore_check:
        legal = []
        for m in moves:
            tmp = deepcopy(temp_board)
            make_move_on_board((i,j), m, tmp)
            if not is_check(color, tmp):
                legal.append(m)
        return legal

    return moves

def get_all_moves_for_player(temp_board, player):
    moves = []
    for i in range(8):
        for j in range(8):
            p = temp_board[i][j]
            if p != '  ' and p[0] == player:
                for m in generate_moves(p, (i,j), temp_board, ignore_check=False):
                    moves.append(((i,j), m))
    return moves

def is_checkmate(player):
    """True if player has no legal moves and is in check."""
    moves = get_all_moves_for_player(board, player)
    if moves:
        return False
    return is_check(player, board)

def evaluate_board(temp_board):
    """Simple evaluation: material + tiny mobility bonus. Positive favors White."""
    score = 0.0
    for row in temp_board:
        for p in row:
            if p != '  ':
                v = piece_values.get(p[1], 0)
                score += v if p[0] == 'w' else -v
    # small mobility bonus:
    white_moves = sum(len(generate_moves(p,(i,j),temp_board,ignore_check=True))
                      for i,row in enumerate(temp_board) for j,p in enumerate(row) if p!='  ' and p[0]=='w')
    black_moves = sum(len(generate_moves(p,(i,j),temp_board,ignore_check=True))
                      for i,row in enumerate(temp_board) for j,p in enumerate(row) if p!='  ' and p[0]=='b')
    score += 0.01 * (white_moves - black_moves)
    return score

# --- Minimax with alpha-beta, explicit side-to-move ---
def minimax(temp_board, depth, alpha, beta, side_to_move):
    """
    side_to_move: 'w' or 'b'
    returns (best_score, best_move) where best_move is ((si,sj),(ei,ej)) or None.
    Score always measured from White's perspective (positive = good for White).
    """
    # terminal
    moves = get_all_moves_for_player(temp_board, side_to_move)
    if depth == 0 or not moves:
        # if no moves => checkmate or stalemate
        if not moves:
            if is_check(side_to_move, temp_board):
                # side_to_move is checkmated -> very bad for that side
                return (-9999 if side_to_move == 'w' else 9999), None
            else:
                return 0, None
        return evaluate_board(temp_board), None

    best_move = None
    if side_to_move == 'w':
        max_eval = -99999
        for start,end in moves:
            t = deepcopy(temp_board)
            make_move_on_board(start, end, t)
            val, _ = minimax(t, depth-1, alpha, beta, 'b')
            if val > max_eval:
                max_eval = val
                best_move = (start, end)
            alpha = max(alpha, val)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = 99999
        for start,end in moves:
            t = deepcopy(temp_board)
            make_move_on_board(start, end, t)
            val, _ = minimax(t, depth-1, alpha, beta, 'w')
            if val < min_eval:
                min_eval = val
                best_move = (start, end)
            beta = min(beta, val)
            if beta <= alpha:
                break
        return min_eval, best_move

# --- GUI & gameplay functions ---
def move_piece(start, end):
    global king_positions, game_over
    si,sj = start
    ei,ej = end
    piece = board[si][sj]
    captured = board[ei][ej]
    # move
    board[ei][ej] = piece
    board[si][sj] = '  '
    # update king pos if moved
    if piece[1] == 'K':
        king_positions[piece[0]] = (ei,ej)
    # pawn promotion
    if piece[1] == 'P':
        if (piece[0] == 'w' and ei == 0) or (piece[0] == 'b' and ei == 7):
            board[ei][ej] = piece[0] + 'Q'
    # don't rely on capturing the king; checkmate detection used elsewhere
    return

def switch_player():
    global current_player, player_view_flipped
    current_player = 'b' if current_player == 'w' else 'w'
    if flip_var.get():
        # only flip view if the option is set
        global player_view_flipped
        player_view_flipped = not player_view_flipped
    update_board()
    if mode == 'AI' and current_player == 'b' and not game_over:
        root.after(350, ai_move)

# --- AI move ---
def ai_move():
    global ai_difficulty, game_over
    # collect moves for black
    moves = get_all_moves_for_player(board, 'b')
    if not moves:
        # no moves; checkmate or stalemate will be handled after
        if is_check('b'):
            messagebox.showinfo("Checkmate", "White wins!")
        else:
            messagebox.showinfo("Stalemate", "Draw by stalemate.")
        game_over = True
        return

    if ai_difficulty == "Easy":
        start,end = random.choice(moves)

    elif ai_difficulty == "Medium":
        # prefer captures if available otherwise 1-ply lookahead
        capture_moves = [m for m in moves if board[m[1][0]][m[1][1]] != '  ']
        if capture_moves:
            start,end = random.choice(capture_moves)
        else:
            _,best = minimax(board, 1, -99999, 99999, 'b')
            if best is None:
                start,end = random.choice(moves)
            else:
                start,end = best

    else:  # Hard
        depth = 3
        _,best = minimax(board, depth, -99999, 99999, 'b')
        if best is None:
            start,end = random.choice(moves)
        else:
            start,end = best

    move_piece(start, end)
    update_board()
    # check for checkmate/stalemate after move
    if is_checkmate('w'):
        messagebox.showinfo("Checkmate", "AI wins!")
        game_over = True
        return
    # switch back to human
    switch_player()

# --- Tkinter UI ---
root = tk.Tk()
root.title("Chess Game")
root.geometry("600x650")
root.resizable(False, False)

frame = tk.Frame(root)
frame.pack(expand=True, fill='both')

buttons = [[None for _ in range(8)] for _ in range(8)]

def update_board(temp_piece=None):
    for i in range(8):
        for j in range(8):
            di,dj = (7-i,7-j) if player_view_flipped else (i,j)
            bg = 'white' if (i+j)%2==0 else 'gray'
            txt = pieces[board[i][j]]
            if temp_piece:
                p,pi,pj=temp_piece
                if int(round(pi))==i and int(round(pj))==j:
                    txt = pieces[p]
            buttons[di][dj].config(text=txt, bg=bg)

def on_click(i,j):
    global selected_piece, selected_coords, current_player, game_over
    if game_over:
        return
    ri,rj = (7-i,7-j) if player_view_flipped else (i,j)
    piece = board[ri][rj]
    if selected_piece:
        # try to move
        legal = generate_moves(selected_piece, selected_coords, None, ignore_check=False)
        if (ri,rj) in legal:
            move_piece(selected_coords, (ri,rj))
            update_board()
            # check for checkmate/stalemate
            if is_checkmate('b' if current_player=='w' else 'w'):
                messagebox.showinfo("Checkmate", f"{current_player.upper()} wins!")
                game_over = True
                return
            switch_player()
        selected_piece = None
        selected_coords = None
        update_board()
    else:
        # select piece
        if piece != '  ' and piece[0] == current_player:
            selected_piece = piece
            selected_coords = (ri,rj)

# create board buttons
for i in range(8):
    for j in range(8):
        bg = 'white' if (i+j)%2==0 else 'gray'
        btn = tk.Button(frame, text=pieces[board[i][j]], font=("Arial", 32), bg=bg,
                        command=lambda i=i,j=j: on_click(i,j))
        btn.grid(row=i, column=j, sticky='nsew')
        buttons[i][j] = btn
for i in range(8):
    frame.rowconfigure(i, weight=1)
    frame.columnconfigure(i, weight=1)

# Menu
menu = tk.Menu(root)
root.config(menu=menu)
game_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Game", menu=game_menu)
flip_var = tk.BooleanVar(value=True)

def set_mode_2p():
    global mode
    mode = "2P"
    reset_game()
def set_mode_ai():
    global mode
    mode = "AI"
    reset_game()
def set_difficulty(level):
    global ai_difficulty
    ai_difficulty = level
    messagebox.showinfo("AI Difficulty", f"Difficulty set to {level}")
def reset_game():
    global board, current_player, player_view_flipped, king_positions, game_over, selected_piece, selected_coords
    board[:] = [row[:] for row in initial_board]
    current_player = 'w'
    player_view_flipped = False
    king_positions = {'w':(7,4),'b':(0,4)}
    game_over = False
    selected_piece = None
    selected_coords = None
    update_board()

game_menu.add_command(label="2 Players", command=set_mode_2p)
game_menu.add_command(label="Vs AI", command=set_mode_ai)
game_menu.add_checkbutton(label="Flip Board", variable=flip_var)
game_menu.add_command(label="Reset Game", command=reset_game)

ai_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="AI Difficulty", menu=ai_menu)
for diff in ["Easy","Medium","Hard"]:
    ai_menu.add_command(label=diff, command=lambda d=diff:set_difficulty(d))

update_board()
root.mainloop()
