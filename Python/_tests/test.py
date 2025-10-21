import tkinter as tk
from tkinter import messagebox
import random
from copy import deepcopy
import threading
import time
import sys

# ----------------------------
# Config
# ----------------------------
HARD_TIME_LIMIT = 6.0   # seconds for Hard AI per move (increase to make it stronger)
HARD_MAX_DEPTH = 6      # maximum depth to attempt with iterative deepening
MEDIUM_DEPTH = 4        # medium ply depth fallback
# ----------------------------

# --- Chess Piece Symbols ---
pieces = {
    'bR':'♜','bN':'♞','bB':'♝','bQ':'♛','bK':'♚','bP':'♟',
    'wR':'♖','wN':'♘','wB':'♗','wQ':'♕','wK':'♔','wP':'♙',
    '  ': ''
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
current_player = 'w'          # 'w' or 'b' (white moves first)
selected_piece = None
selected_coords = None
player_view_flipped = False
mode = "AI"                   # default to AI vs Human
ai_difficulty = "Hard"        # default difficulty
king_positions = {'w':(7,4),'b':(0,4)}
game_over = False

# Castling rights: True if rook/king hasn't moved (K = kingside, Q = queenside)
castling_rights = {'wK': True, 'wQ': True, 'bK': True, 'bQ': True}

# AI run state
ai_running = False
ai_thread = None
ai_abort = False

# Transposition table (string-keyed)
transposition_table = {}

# -------------------------
# Helpers
# -------------------------
def in_bounds(i,j):
    return 0 <= i < 8 and 0 <= j < 8

def find_king(player, temp_board):
    key = player + 'K'
    for i in range(8):
        for j in range(8):
            if temp_board[i][j] == key:
                return (i,j)
    return None

def make_move_on_board(start, end, temp_board, update_castling=True):
    """Apply move on given board. Pawn auto-promotes to Q.
       Handles castling rook movement if king moves two squares.
    """
    si,sj = start
    ei,ej = end
    piece = temp_board[si][sj]
    # move piece
    temp_board[ei][ej] = piece
    temp_board[si][sj] = '  '

    # castle handling: if king moved two squares horizontally, move rook
    if piece != '  ' and piece[1] == 'K' and abs(sj - ej) == 2:
        if ej > sj:
            # kingside: rook from h-file -> f-file
            rook_start = (si, 7)
            rook_end = (si, ej - 1)
        else:
            # queenside: rook from a-file -> d-file
            rook_start = (si, 0)
            rook_end = (si, ej + 1)
        rs, cs = rook_start
        re, ce = rook_end
        rook_piece = temp_board[rs][cs]
        # move rook if present
        if rook_piece != '  ' and rook_piece[1] == 'R':
            temp_board[re][ce] = rook_piece
            temp_board[rs][cs] = '  '

    # pawn promotion
    if piece != '  ' and piece[1] == 'P':
        if (piece[0] == 'w' and ei == 0) or (piece[0] == 'b' and ei == 7):
            temp_board[ei][ej] = piece[0] + 'Q'

    # Optionally updating castling rights should be done externally if needed.
    # But callers can pass update_castling=True to update rights on this board if it's the main board.

# Non-recursive attack detection to prevent recursion with generate_moves
def is_square_attacked(square, by_player, temp_board):
    """
    Return True if the square (i,j) is attacked by any piece of by_player.
    Handles pawn, knight, sliding pieces and king adjacency.
    """
    i,j = square
    attacker = by_player

    # pawn attacks
    if attacker == 'w':
        # white pawn at (i+1, j±1) attacks (i,j)
        for dj in (-1, 1):
            pi, pj = i+1, j+dj
            if in_bounds(pi,pj) and temp_board[pi][pj] == 'wP':
                return True
    else:
        # black pawn at (i-1, j±1)
        for dj in (-1, 1):
            pi, pj = i-1, j+dj
            if in_bounds(pi,pj) and temp_board[pi][pj] == 'bP':
                return True

    # knights
    knight_moves = [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
    for di,dj in knight_moves:
        ni,nj = i+di, j+dj
        if in_bounds(ni,nj) and temp_board[ni][nj] != '  ' and temp_board[ni][nj][0] == attacker and temp_board[ni][nj][1] == 'N':
            return True

    # sliding pieces (orthogonal and diagonal)
    directions = [
        (-1,0,('R','Q')), (1,0,('R','Q')), (0,-1,('R','Q')), (0,1,('R','Q')),
        (-1,-1,('B','Q')), (1,1,('B','Q')), (1,-1,('B','Q')), (-1,1,('B','Q'))
    ]
    for di,dj,types in directions:
        ni, nj = i+di, j+dj
        while in_bounds(ni,nj):
            p = temp_board[ni][nj]
            if p == '  ':
                ni += di; nj += dj
                continue
            if p[0] == attacker and p[1] in types:
                return True
            # blocked by any piece
            break

    # king adjacency
    for di in (-1,0,1):
        for dj in (-1,0,1):
            if di==0 and dj==0: continue
            ni,nj = i+di, j+dj
            if in_bounds(ni,nj) and temp_board[ni][nj] != '  ' and temp_board[ni][nj][0] == attacker and temp_board[ni][nj][1] == 'K':
                return True

    return False

def is_check(player, temp_board=None):
    """True if player's king is attacked on temp_board."""
    if temp_board is None:
        temp_board = board
    king_pos = find_king(player, temp_board)
    if king_pos is None:
        # missing king -> treat as 'in check' for search
        return True
    enemy = 'b' if player == 'w' else 'w'
    return is_square_attacked(king_pos, enemy, temp_board)

def generate_moves(piece, pos, temp_board=None, ignore_check=False):
    """
    Generate pseudo-legal moves for piece at pos on temp_board.
    If ignore_check==False filter out moves that leave own king in check.
    Includes castling logic for the king based on castling_rights (uses global rights).
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
        # en-passant not implemented

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

        # Castling (king-side & queen-side) - only if rights exist and squares are clear and not in check
        if color == 'w':
            own_rank = 7
            rights_k = castling_rights.get('wK', False)
            rights_q = castling_rights.get('wQ', False)
        else:
            own_rank = 0
            rights_k = castling_rights.get('bK', False)
            rights_q = castling_rights.get('bQ', False)

        # only attempt castling if king is on starting square and not currently in check
        king_start_col = 4
        if j == king_start_col and not is_check(color, temp_board):
            # kingside: squares between king and rook must be empty and not attacked
            if rights_k:
                if temp_board[own_rank][5] == '  ' and temp_board[own_rank][6] == '  ':
                    # check that squares the king moves through are not attacked
                    if (not is_square_attacked((own_rank,5), enemy, temp_board) and
                        not is_square_attacked((own_rank,6), enemy, temp_board)):
                        # rook present at h-file?
                        if temp_board[own_rank][7] != '  ' and temp_board[own_rank][7][1] == 'R' and temp_board[own_rank][7][0] == color:
                            moves.append((own_rank, 6))  # kingside castle target
            # queenside:
            if rights_q:
                if temp_board[own_rank][3] == '  ' and temp_board[own_rank][2] == '  ' and temp_board[own_rank][1] == '  ':
                    if (not is_square_attacked((own_rank,3), enemy, temp_board) and
                        not is_square_attacked((own_rank,2), enemy, temp_board)):
                        if temp_board[own_rank][0] != '  ' and temp_board[own_rank][0][1] == 'R' and temp_board[own_rank][0][0] == color:
                            moves.append((own_rank, 2))  # queenside castle target

    # Filter illegal moves that leave own king in check
    if not ignore_check:
        legal = []
        for m in moves:
            tmp = deepcopy(temp_board)
            make_move_on_board((i,j), m, tmp)
            # After a castling move, ensure king isn't in check
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
    """Smarter evaluation: material + mobility + center control + king safety."""
    score = 0.0
    center_squares = {(3,3), (3,4), (4,3), (4,4)}
    for i, row in enumerate(temp_board):
        for j, p in enumerate(row):
            if p == '  ':
                continue
            base = piece_values.get(p[1], 0)
            color_factor = 1 if p[0] == 'w' else -1
            val = base

            # central control
            if (i, j) in center_squares:
                val += 0.2

            # mobility bonus (ignore_check to be cheaper)
            val += 0.02 * len(generate_moves(p, (i, j), temp_board, ignore_check=True))

            # king safety penalty (fewer friendly defenders near king is bad)
            if p[1] == 'K':
                allies_near = 0
                for di in (-1,0,1):
                    for dj in (-1,0,1):
                        ni, nj = i+di, j+dj
                        if in_bounds(ni,nj) and temp_board[ni][nj] != '  ' and temp_board[ni][nj][0] == p[0]:
                            allies_near += 1
                val -= (8 - allies_near) * 0.3

            score += color_factor * val

    return score

# -------------------------
# Minimax / negamax with alpha-beta, TT and time cutoff
# -------------------------
def board_key(temp_board, side_to_move):
    # compact key for transposition table
    return (tuple(''.join(r) for r in temp_board), side_to_move)

def move_order_key(temp_board, start, end):
    # heuristic: captures (value captured higher first), promotions, then quiet
    si,sj = start
    ei,ej = end
    captured = temp_board[ei][ej]
    cap_value = 0
    if captured != '  ':
        cap_value = piece_values.get(captured[1], 0)
    moving = temp_board[si][sj]
    prom = 1 if (moving[1]=='P' and ( (moving[0]=='w' and ei==0) or (moving[0]=='b' and ei==7))) else 0
    return (-cap_value, -prom)

def minimax_tt(temp_board, depth, alpha, beta, side_to_move, stop_time, tt):
    """
    Returns (score, best_move) from White's perspective (positive favors White).
    side_to_move: 'w' or 'b'.
    Uses simple transposition table (tt) keyed by board_key.
    Will raise TimeoutError if time exceeded.
    """
    if time.time() > stop_time:
        raise TimeoutError

    key = board_key(temp_board, side_to_move)
    if key in tt and tt[key]['depth'] >= depth:
        return tt[key]['score'], tt[key].get('best_move', None)

    moves = get_all_moves_for_player(temp_board, side_to_move)
    if depth == 0 or not moves:
        if not moves:
            if is_check(side_to_move, temp_board):
                # side_to_move is checkmated -> very bad for that side
                score = (-9999 if side_to_move == 'w' else 9999)
                return score, None
            else:
                return 0, None
        return evaluate_board(temp_board), None

    best_move = None
    # ordering
    moves_sorted = sorted(moves, key=lambda s: move_order_key(temp_board, s[0], s[1]))
    if side_to_move == 'w':
        max_eval = -99999
        for start,end in moves_sorted:
            if time.time() > stop_time:
                raise TimeoutError
            t = deepcopy(temp_board)
            # make move (castling will be handled by make_move_on_board)
            make_move_on_board(start, end, t)
            # small anticipation: after making this move, look at a sample of opponent replies to penalize risky moves
            try:
                val, _ = minimax_tt(t, depth-1, alpha, beta, 'b', stop_time, tt)
            except TimeoutError:
                raise
            # opponent response sampling (light-weight)
            if depth <= 2 and val != 0:
                pass  # avoid double counting at shallow levels
            # update
            if val > max_eval:
                max_eval = val
                best_move = (start, end)
            alpha = max(alpha, val)
            if beta <= alpha:
                break
        tt[key] = {'depth': depth, 'score': max_eval, 'best_move': best_move}
        return max_eval, best_move
    else:
        min_eval = 99999
        for start,end in moves_sorted:
            if time.time() > stop_time:
                raise TimeoutError
            t = deepcopy(temp_board)
            make_move_on_board(start, end, t)
            try:
                val, _ = minimax_tt(t, depth-1, alpha, beta, 'w', stop_time, tt)
            except TimeoutError:
                raise
            if val < min_eval:
                min_eval = val
                best_move = (start, end)
            beta = min(beta, val)
            if beta <= alpha:
                break
        tt[key] = {'depth': depth, 'score': min_eval, 'best_move': best_move}
        return min_eval, best_move

# -------------------------
# AI orchestration (threaded)
# -------------------------
def ai_worker(board_snapshot, difficulty, apply_callback):
    """
    Runs in background thread. When done, calls apply_callback(start,end) via root.after.
    """
    global ai_abort, transposition_table

    moves = get_all_moves_for_player(board_snapshot, 'b')
    if not moves:
        root.after(1, lambda: apply_callback(None, None, board_snapshot))
        return

    # Easy: random
    if difficulty == "Easy":
        start,end = random.choice(moves)
        root.after(1, lambda: apply_callback(start, end, board_snapshot))
        return

    # Medium: prefer captures; else shallow search
    if difficulty == "Medium":
        capture_moves = [m for m in moves if board_snapshot[m[1][0]][m[1][1]] != '  ']
        if capture_moves:
            start,end = random.choice(capture_moves)
            root.after(1, lambda: apply_callback(start, end, board_snapshot))
            return
        try:
            tt = {}
            _, best = minimax_tt(board_snapshot, MEDIUM_DEPTH, -99999, 99999, 'b', time.time()+1.0, tt)
            if best is None:
                start,end = random.choice(moves)
            else:
                start,end = best
        except TimeoutError:
            start,end = random.choice(moves)
        root.after(1, lambda: apply_callback(start, end, board_snapshot))
        return

    # Hard: iterative deepening with time limit and light anticipation
    stop_time = time.time() + HARD_TIME_LIMIT
    best_move_overall = None
    tt = {}
    try:
        for depth in range(1, HARD_MAX_DEPTH+1):
            if ai_abort:
                break
            if time.time() > stop_time:
                break
            try:
                score, best = minimax_tt(board_snapshot, depth, -99999, 99999, 'b', stop_time, tt)
                if best:
                    best_move_overall = best
                # continue deeper if time remains
            except TimeoutError:
                break
    except Exception as e:
        print("AI worker unexpected exception:", e, file=sys.stderr)

    if best_move_overall is None:
        best_move_overall = random.choice(moves)
    start,end = best_move_overall
    root.after(1, lambda: apply_callback(start, end, board_snapshot))

# -------------------------
# GUI & gameplay functions
# -------------------------
def move_piece(start, end):
    global king_positions, castling_rights
    si,sj = start
    ei,ej = end
    piece = board[si][sj]
    # apply move (this will handle rook movement for castling)
    make_move_on_board((si,sj), (ei,ej), board)
    # update king pos if moved
    if piece != '  ' and piece[1] == 'K':
        king_positions[piece[0]] = (ei,ej)
        # moving king removes both castling rights for that color
        if piece[0] == 'w':
            castling_rights['wK'] = False
            castling_rights['wQ'] = False
        else:
            castling_rights['bK'] = False
            castling_rights['bQ'] = False

    # if rook moved or rook captured, update castling rights
    # rook original positions: white a1=(7,0) and h1=(7,7), black a8=(0,0) and h8=(0,7)
    # If rook moved from its original square, revoke corresponding right.
    if piece != '  ' and piece[1] == 'R':
        if (si, sj) == (7,7):
            castling_rights['wK'] = False
        if (si, sj) == (7,0):
            castling_rights['wQ'] = False
        if (si, sj) == (0,7):
            castling_rights['bK'] = False
        if (si, sj) == (0,0):
            castling_rights['bQ'] = False

    # If a rook was captured on original rook square, revoke corresponding right
    # check destination square where capture might have happened (we already moved)
    # But we need to check previous occupant at dest: handled before move in some callers; for robustness, check board state:
    # if white rook captured at starting black rook squares:
    # We'll do a simple scan: if rook not present at rook starting squares, rights revoked earlier or should be kept false.
    if board[7][7] != 'wR':
        castling_rights['wK'] = False
    if board[7][0] != 'wR':
        castling_rights['wQ'] = False
    if board[0][7] != 'bR':
        castling_rights['bK'] = False
    if board[0][0] != 'bR':
        castling_rights['bQ'] = False

    # pawn promotion handled inside make_move_on_board

def apply_ai_move(start, end, board_snapshot):
    """
    Runs on main thread. Applies the provided move (computed on snapshot).
    """
    global game_over, ai_running, ai_abort
    ai_running = False
    ai_abort = False

    if start is None or end is None:
        if is_check('b'):
            messagebox.showinfo("Checkmate", "White wins!")
        else:
            messagebox.showinfo("Stalemate", "Draw by stalemate.")
        game_over = True
        return

    # Sanity: verify move still legal on current board; if not, pick random legal
    legal_moves = get_all_moves_for_player(board, 'b')
    if ((start,end) not in legal_moves):
        if not legal_moves:
            if is_check('b'):
                messagebox.showinfo("Checkmate", "White wins!")
            else:
                messagebox.showinfo("Stalemate", "Draw by stalemate.")
            game_over = True
            return
        start,end = random.choice(legal_moves)

    move_piece(start, end)
    update_board()

    if is_checkmate('w'):
        messagebox.showinfo("Checkmate", "AI wins!")
        game_over = True
        return

    switch_player()

def start_ai_thread():
    """Start background AI worker if not already running."""
    global ai_running, ai_thread, ai_abort
    if ai_running or game_over:
        return
    ai_running = True
    ai_abort = False
    board_snapshot = deepcopy(board)
    difficulty = ai_difficulty
    def target():
        ai_worker(board_snapshot, difficulty, apply_ai_move)
    ai_thread = threading.Thread(target=target, daemon=True)
    ai_thread.start()

def switch_player():
    global current_player, player_view_flipped, ai_abort
    current_player = 'b' if current_player == 'w' else 'w'
    # flip view only if user toggles option
    if flip_var.get():
        global player_view_flipped
        player_view_flipped = not player_view_flipped
    update_board()
    if mode == 'AI' and current_player == 'b' and not game_over:
        root.after(120, start_ai_thread)

# -------------------------
# Tkinter UI
# -------------------------
root = tk.Tk()
root.title("Chess Game")
root.geometry("640x700")
root.resizable(False, False)

frame = tk.Frame(root)
frame.pack(expand=True, fill='both', padx=8, pady=8)

buttons = [[None for _ in range(8)] for _ in range(8)]

def update_board():
    """Safely redraw all pieces on the board without collapsing columns."""
    global buttons

    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            button = buttons[r][c]

            # Always display something so Tkinter keeps column width stable
            display_symbol = pieces.get(piece, " ")
            if display_symbol == " ":
                # Use a transparent placeholder (like a non-breaking space)
                button.config(text=" ")  # U+00A0 non-breaking space
            else:
                button.config(text=display_symbol)

            # Color squares consistently
            color = "#EEEED2" if (r + c) % 2 == 0 else "#769656"
            button.config(bg=color, activebackground=color)

    # Lock column widths so they never shrink
    for c in range(8):
        root.grid_columnconfigure(c, minsize=64, weight=1)
    for r in range(8):
        root.grid_rowconfigure(r, minsize=64, weight=1)

    root.update_idletasks()
    
def on_click(i, j):
    global selected_piece, selected_coords, current_player, game_over
    if game_over or (mode == 'AI' and current_player == 'b') or ai_running:
        # if AI's turn or running, ignore clicks
        return

    # translate displayed coords to logical board coords
    ri, rj = (7 - i, 7 - j) if player_view_flipped else (i, j)
    piece = board[ri][rj]

    if selected_piece:
        legal = generate_moves(selected_piece, selected_coords, None, ignore_check=False)
        if (ri, rj) in legal:
            # perform move; if castling occurs, move_piece will handle rook
            move_piece(selected_coords, (ri, rj))
            update_board()
            # check for checkmate/stalemate
            if is_checkmate('b' if current_player=='w' else 'w'):
                messagebox.showinfo("Checkmate", f"{current_player.upper()} wins!")
                game_over = True
                selected_piece = None
                selected_coords = None
                return
            switch_player()
        # either succeeded or failed -> deselect
        selected_piece = None
        selected_coords = None
        update_board()
    else:
        # select piece
        if piece != '  ' and piece[0] == current_player:
            selected_piece = piece
            selected_coords = (ri, rj)
            # highlight selection (map back to display coords)
            di,dj = (7-selected_coords[0], 7-selected_coords[1]) if player_view_flipped else selected_coords
            try:
                buttons[di][dj].config(bg='yellow')
            except Exception:
                pass

# create board buttons
for i in range(8):
    for j in range(8):
        bg = 'white' if (i + j) % 2 == 0 else 'gray'
        btn = tk.Button(
            frame,
            text=pieces.get(board[i][j], ""),
            font=("Arial", 28),
            bg=bg,
            command=lambda i=i, j=j: on_click(i, j)
        )
        btn.grid(row=i, column=j, sticky='nsew', padx=0, pady=0)
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
    global board, current_player, player_view_flipped, king_positions, game_over, selected_piece, selected_coords, ai_running, ai_abort, transposition_table, castling_rights
    board[:] = [row[:] for row in initial_board]
    current_player = 'w'
    player_view_flipped = False
    king_positions = {'w':(7,4),'b':(0,4)}
    game_over = False
    selected_piece = None
    selected_coords = None
    ai_running = False
    ai_abort = True
    transposition_table = {}
    # reset castling rights
    castling_rights = {'wK': True, 'wQ': True, 'bK': True, 'bQ': True}
    update_board()
    # if vs AI and black to move (shouldn't be), schedule AI
    if mode == 'AI' and current_player == 'b':
        root.after(120, start_ai_thread)

game_menu.add_command(label="2 Players", command=set_mode_2p)
game_menu.add_command(label="Vs AI", command=set_mode_ai)
game_menu.add_checkbutton(label="Flip Board", variable=flip_var)
game_menu.add_command(label="Reset Game", command=reset_game)

ai_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="AI Difficulty", menu=ai_menu)
for diff in ["Easy","Medium","Hard"]:
    ai_menu.add_command(label=diff, command=lambda d=diff:set_difficulty(d))

# show current defaults
update_board()

# If default mode is AI and human is white, nothing to do.
# If you want AI to start as white, set current_player = 'b' and call start_ai_thread() after mainloop starts.
# --- ADD THIS SECTION near the bottom, just before root.mainloop() ---

# -------------------------
# CASTLING BUTTONS
# -------------------------
castle_frame = tk.Frame(root)
castle_frame.pack(pady=10)

def attempt_castle(side):
    """Try to perform castling for the current player manually via button."""
    global board, current_player
    if game_over or (mode == 'AI' and current_player == 'b') or ai_running:
        return

    color = current_player
    own_rank = 7 if color == 'w' else 0
    if side == 'K':  # kingside
        target = (own_rank, 6)
    else:  # queenside
        target = (own_rank, 2)

    king_pos = find_king(color, board)
    legal = generate_moves(color + 'K', king_pos, board)
    if target in legal:
        move_piece(king_pos, target)
        update_board()
        switch_player()
    else:
        messagebox.showinfo("Castling", f"{color.upper()} cannot castle {('kingside' if side=='K' else 'queenside')} now.")

castle_k_btn = tk.Button(castle_frame, text="Castle Kingside", font=("Arial", 12), command=lambda: attempt_castle('K'))
castle_q_btn = tk.Button(castle_frame, text="Castle Queenside", font=("Arial", 12), command=lambda: attempt_castle('Q'))
castle_k_btn.pack(side="left", padx=8)
castle_q_btn.pack(side="left", padx=8)

def update_castle_buttons():
    """Enable/disable castling buttons based on turn."""
    if game_over:
        castle_k_btn.config(state='disabled')
        castle_q_btn.config(state='disabled')
        return
    if mode == 'AI' and current_player == 'b':
        castle_k_btn.config(state='disabled')
        castle_q_btn.config(state='disabled')
    else:
        castle_k_btn.config(state='normal')
        castle_q_btn.config(state='normal')

# hook it into your board update
old_update_board = update_board
def update_board_with_castle():
    old_update_board()
    update_castle_buttons()

update_board = update_board_with_castle
update_board()

root.mainloop()
