import py5
import numpy as np


cell_side_length = 10  # MODIFY THIS TO ADJUST THE SIZE OF CELLS


screen_width, screen_height = 800, 800
cells_x = screen_width // cell_side_length
cells_y = screen_height // cell_side_length
cells = np.zeros((cells_x, cells_y))
time = 0


def setup():
    py5.size(screen_width, screen_height)
    py5.rect_mode(py5.CENTER)


def draw():
    global time, cells
    py5.background(0)
    for i in range(cells_x):
        for j in range(cells_y):
            cells[i, j] = py5.remap(py5.noise(i * 0.05, j * 0.05, time), 0, 1, -1, 1)

    for i in range(cells_x):
        for j in range(cells_y):
            py5.fill(py5.remap(cells[i, j], 0, 1, 0, 255))
            py5.no_stroke()
            py5.rect(
                cell_side_length * i,
                cell_side_length * j,
                cell_side_length,
                cell_side_length,
            )

    for i in range(cells_x - 1):
        for j in range(cells_y - 1):
            draw_contours(i, j)

    time += 6.0 / 97.0


def draw_contours(i, j):
    global cells
    py5.stroke(256, 0, 0)
    tl, tr, bl, br = (
        (i, j, cells[i, j]),
        (i + 1, j, cells[i + 1, j]),
        (i, j + 1, cells[i, j + 1]),
        (i + 1, j + 1, cells[i + 1, j + 1]),
    )
    on_tl = int(tl[2] > 0)
    on_tr = int(tr[2] > 0)
    on_bl = int(bl[2] > 0)
    on_br = int(br[2] > 0)
    # marching_squares = {0b0000: None, 0b0010: py5.lerp()}
    x = (on_tl << 3) | (on_tr << 2) | (on_bl << 1) | (on_br)
    if x == 0b0010:
        py5.line(*ip(tl, bl), *ip(bl, br))
    elif x == 0b0001:
        py5.line(*ip(tr, br), *ip(br, bl))
    elif x == 0b0011:
        py5.line(*ip(tl, bl), *ip(tr, br))
    elif x == 0b0100:
        py5.line(*ip(tl, tr), *ip(tr, br))
    elif x == 0b0110:
        py5.line(*ip(tl, tr), *ip(tl, bl))
        py5.line(*ip(br, tr), *ip(br, bl))
    elif x == 0b0101:
        py5.line(*ip(tl, tr), *ip(bl, br))
    elif x == 0b0111:
        py5.line(*ip(tl, tr), *ip(tl, bl))
    elif x == 0b1000:
        py5.line(*ip(tl, tr), *ip(tl, bl))
    elif x == 0b1010:
        py5.line(*ip(tl, tr), *ip(bl, br))
    elif x == 0b1001:
        py5.line(*ip(tl, bl), *ip(bl, br))
        py5.line(*ip(tl, tr), *ip(tr, br))
    elif x == 0b1011:
        py5.line(*ip(tl, tr), *ip(tr, br))
    elif x == 0b1100:
        py5.line(*ip(tl, bl), *ip(tr, br))
    elif x == 0b1110:
        py5.line(*ip(tr, br), *ip(br, bl))
    elif x == 0b1101:
        py5.line(*ip(tl, bl), *ip(bl, br))


def ip(a, b):
    ax, ay, a_val = a
    bx, by, b_val = b

    return cell_side_length * (b_val * ax - a_val * bx) / (
        b_val - a_val
    ), cell_side_length * (b_val * ay - a_val * by) / (b_val - a_val)


py5.run_sketch()
