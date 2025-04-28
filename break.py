import curses
import random

# Configuration
grid_size = 6              # 6×6 matrix
attempts_allowed = 3       # number of attempts
picks_per_attempt = 8      # picks per attempt
reference_len = 4          # reference sequence length


def generate_grid(n):
    return [[f"{random.choice('0123456789ABCDEF')}{random.choice('0123456789ABCDEF')}" for _ in range(n)] for _ in range(n)]


def pick_reference_positions(n, length):
    # Create a valid alternating-axis path of positions
    path = []
    visited = set()
    r, c = random.randrange(n), random.randrange(n)
    path.append((r, c))
    visited.add((r, c))
    for step in range(1, length):
        axis = 'col' if step % 2 == 1 else 'row'
        if axis == 'col':
            candidates = [(rr, c) for rr in range(n) if (rr, c) not in visited]
        else:
            candidates = [(r, cc) for cc in range(n) if (r, cc) not in visited]
        pos = random.choice(candidates)
        path.append(pos)
        visited.add(pos)
    return path


def make_new_grid_with_ref(n, ref_positions):
    # Generate a grid and place new random reference codes at ref_positions
    grid = generate_grid(n)
    ref_codes = []
    for (r, c) in ref_positions:
        code = f"{random.choice('0123456789ABCDEF')}{random.choice('0123456789ABCDEF')}"
        grid[r][c] = code
        ref_codes.append(code)
    return grid, ref_codes


def get_axis(prev, step):
    if step == 0:
        return None
    return 'col' if step % 2 == 1 else 'row'


def get_valid_picks(prev, step, visited):
    axis = get_axis(prev, step)
    n = grid_size
    if axis is None:
        return {(r, c) for r in range(n) for c in range(n) if (r, c) not in visited}
    r0, c0 = prev
    if axis == 'col':
        return {(r, c0) for r in range(n) if (r, c0) not in visited}
    return {(r0, c) for c in range(n) if (r0, c) not in visited}


def draw_single_box(stdscr, y, x, h, w, title=None):
    stdscr.addstr(y, x, '┌' + '─'*(w-2) + '┐')
    for i in range(1, h-1):
        stdscr.addstr(y+i, x, '│')
        stdscr.addstr(y+i, x+w-1, '│')
    stdscr.addstr(y+h-1, x, '└' + '─'*(w-2) + '┘')
    if title:
        stdscr.addstr(y, x+2, f' {title} ')


def draw_double_box(stdscr, y, x, h, w, title=None):
    stdscr.addstr(y, x, '╔' + '═'*(w-2) + '╗')
    for i in range(1, h-1):
        stdscr.addstr(y+i, x, '║')
        stdscr.addstr(y+i, x+w-1, '║')
    stdscr.addstr(y+h-1, x, '╚' + '═'*(w-2) + '╝')
    if title:
        stdscr.addstr(y, x+2, f' {title} ')


def draw(stdscr, grid, cursor, picks, attempts, reference):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    # Dimensions for centering
    grid_w = grid_size*5 + 2
    grid_h = grid_size*2 + 2
    info_w = max(60, reference_len*6 + picks_per_attempt*4)
    info_h = picks_per_attempt + 8
    total_w = grid_w + info_w + 6
    start_y = max(2, (h - grid_h)//2)
    start_x = max(2, (w - total_w)//2)

    # Header
    stdscr.addstr(start_y-2, start_x, "NET::TECH PROTOCOL", curses.A_BOLD)

    # Containers
    draw_single_box(stdscr, start_y, start_x, grid_h, grid_w, title=" GRID ")
    info_x = start_x + grid_w + 4
    draw_double_box(stdscr, start_y, info_x, info_h, info_w, title=" PROTOCOL ")

    # Color pairs
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)    # normal
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # axis
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)   # picked
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # cursor

    # Draw grid
    valid = get_valid_picks(picks[-1] if picks else None, len(picks), set(picks))
    for r in range(grid_size):
        for c in range(grid_size):
            y = start_y+1 + r*2
            x = start_x+1 + c*5
            code = grid[r][c]
            if (r, c) == cursor:
                attr = curses.color_pair(4) | curses.A_REVERSE | curses.A_BOLD
            elif (r, c) in picks:
                attr = curses.color_pair(3) | curses.A_BOLD
            elif (r, c) in valid:
                attr = curses.color_pair(2) | curses.A_UNDERLINE
            else:
                attr = curses.color_pair(1)
            stdscr.addstr(y, x, code, attr)

    # Info panel
    info_y = start_y + 2
    stdscr.addstr(info_y, info_x+2, f"[{attempts}]::> ATTEMPTS LEFT")
    slots = [grid[r][c] for (r,c) in picks] + ['__']*(picks_per_attempt-len(picks))
    stdscr.addstr(info_y+2, info_x+2, "BYTE [ " + ' | '.join(slots) + " ]")
    stdscr.addstr(info_y+4, info_x+2, ">>> SEQUENCE:  " + ' '.join(f"[{b}]" for b in reference))

    stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)
    attempts = attempts_allowed
    success = False

    # Reference positions for a guaranteed solvable path
    ref_positions = pick_reference_positions(grid_size, reference_len)

    while attempts > 0 and not success:
        # Scramble grid and update reference codes each attempt
        grid, reference = make_new_grid_with_ref(grid_size, ref_positions)

        picks = []
        visited = set()
        cursor = ref_positions[0]

        while len(picks) < picks_per_attempt:
            draw(stdscr, grid, cursor, picks, attempts, reference)
            key = stdscr.getch()
            r, c = cursor
            axis = get_axis(picks[-1] if picks else None, len(picks))

            def can_move(nr, nc):
                if axis is None:
                    return True
                r0, c0 = picks[-1]
                return (axis == 'col' and nc == c0) or (axis == 'row' and nr == r0)

            if key in (curses.KEY_UP, ord('k')):
                nr, nc = max(0, r-1), c
            elif key in (curses.KEY_DOWN, ord('j')):
                nr, nc = min(grid_size-1, r+1), c
            elif key in (curses.KEY_LEFT, ord('h')):
                nr, nc = r, max(0, c-1)
            elif key in (curses.KEY_RIGHT, ord('l')):
                nr, nc = r, min(grid_size-1, c+1)
            elif key in (curses.KEY_ENTER, 10, 13):
                valid = get_valid_picks(picks[-1] if picks else None, len(picks), visited)
                if cursor in valid:
                    picks.append(cursor)
                    visited.add(cursor)
                else:
                    curses.flash()
                continue
            elif key in (ord('q'), ord('Q')):
                return
            else:
                continue

            if can_move(nr, nc):
                cursor = (nr, nc)
            else:
                curses.flash()

        # Evaluate: check if all reference codes were picked
        picked_codes = {grid[r][c] for (r, c) in picks}
        if all(code in picked_codes for code in reference):
            success = True
        else:
            attempts -= 1

    # Final screen
    draw(stdscr, grid, cursor, picks, attempts, reference)
    h, w = stdscr.getmaxyx()
    msg = "*** HACK SUCCESSFUL! ***" if success else "*** HACK FAILED! GAME OVER ***"
    stdscr.addstr(h-2, 2, msg, curses.A_BOLD)
    stdscr.addstr(h-1, 2, "Press any key to exit.")
    stdscr.getch()

if __name__ == '__main__':
    curses.wrapper(main)
