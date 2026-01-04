#!/usr/bin/env python3
import argparse
import math
import sys
from typing import List, Tuple, Optional


Rect = Tuple[float, float, float, float]


def grid_pack(box_w: float, box_h: float, item_w: float, item_h: float, max_items: Optional[int] = None) -> List[Rect]:
    cols = int(box_w // item_w)
    rows = int(box_h // item_h)
    placements: List[Rect] = []
    for r in range(rows):
        for c in range(cols):
            if max_items is not None and len(placements) >= max_items:
                return placements
            x = c * item_w
            y = r * item_h
            placements.append((x, y, item_w, item_h))
    return placements


def try_both_orientations(box_w, box_h, item_w, item_h, max_items=None):
    p1 = grid_pack(box_w, box_h, item_w, item_h, max_items)
    p2 = grid_pack(box_w, box_h, item_h, item_w, max_items)
    if len(p2) > len(p1):
        # rotate placements back to original orientation (x,y,width,height) where width=item_w,height=item_h
        # We transformed by swapping item_w/item_h when packing; now rotate each rect 90deg inside the cell
        # For simplicity, return p2 but swap w/h
        return [(x, y, item_w, item_h) for (x, y, w, h) in p2]
    return p1


def greedy_row_pack(box_w: float, box_h: float, item_w: float, item_h: float, max_items: Optional[int] = None) -> List[Rect]:
    placements: List[Rect] = []
    y = 0.0
    while y + min(item_h, item_w) <= box_h:
        remaining_width = box_w
        x = 0.0
        # choose row height as the smaller of remaining vertical space and the smaller item dimension
        row_height = item_h
        # fill the row greedily by choosing the orientation that fits and yields one more item in this row
        while True:
            if max_items is not None and len(placements) >= max_items:
                return placements
            placed = False
            # try unrotated if fits
            if item_w <= remaining_width and item_h <= (box_h - y):
                placements.append((x, y, item_w, item_h))
                x += item_w
                remaining_width -= item_w
                placed = True
            elif item_h <= remaining_width and item_w <= (box_h - y):
                # place rotated
                placements.append((x, y, item_h, item_w))
                x += item_h
                remaining_width -= item_h
                placed = True
            if not placed:
                break
        # move to next row
        y += item_h
        if max_items is not None and len(placements) >= max_items:
            break
    return placements


def best_layout(box_w: float, box_h: float, item_w: float, item_h: float, max_items: Optional[int] = None):
    candidates = []
    p_grid = grid_pack(box_w, box_h, item_w, item_h, max_items)
    candidates.append(p_grid)
    p_grid_rot = grid_pack(box_w, box_h, item_h, item_w, max_items)
    # normalize rotation placements to original item dims for interpretation
    p_grid_rot_norm = [(x, y, item_w, item_h) for (x, y, w, h) in p_grid_rot]
    candidates.append(p_grid_rot_norm)
    p_greedy = greedy_row_pack(box_w, box_h, item_w, item_h, max_items)
    candidates.append(p_greedy)
    # pick longest
    best = max(candidates, key=lambda p: len(p))
    return best


def visualize(placements: List[Rect], box_w: float, box_h: float, out_path: str):
    try:
        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle
    except Exception:
        print("matplotlib not available; install it to enable visualization", file=sys.stderr)
        return
    fig, ax = plt.subplots()
    ax.set_xlim(0, box_w)
    ax.set_ylim(0, box_h)
    ax.set_aspect('equal')
    ax.add_patch(Rectangle((0, 0), box_w, box_h, fill=False, edgecolor='black', lw=1))
    for (x, y, w, h) in placements:
        ax.add_patch(Rectangle((x, y), w, h, facecolor='C0', edgecolor='black', alpha=0.6))
    ax.invert_yaxis()
    plt.savefig(out_path, bbox_inches='tight')
    plt.close(fig)


def parse_args():
    p = argparse.ArgumentParser(description='Pack identical rectangles in a box and return best layout')
    p.add_argument('--box', nargs=2, type=float, required=True, metavar=('W', 'H'), help='Box width and height')
    p.add_argument('--item', nargs=2, type=float, required=True, metavar=('W', 'H'), help='Item width and height')
    p.add_argument('--count', type=int, default=None, help='Maximum number of items available')
    p.add_argument('--visualize', action='store_true', help='Save an image of the layout (requires matplotlib)')
    p.add_argument('--out', type=str, default='layout.png', help='Output image path')
    return p.parse_args()


def main():
    args = parse_args()
    box_w, box_h = args.box
    item_w, item_h = args.item
    max_items = args.count
    best = best_layout(box_w, box_h, item_w, item_h, max_items)
    placed = len(best)
    print(f'Placed: {placed} item(s)')
    if max_items is not None:
        print(f'Available: {max_items}')
    # show rows/cols estimate
    cols_est = int(box_w // item_w)
    rows_est = int(box_h // item_h)
    print(f'Estimate grid (no-rotation): {cols_est} x {rows_est} = {cols_est*rows_est}')
    # print first few placements
    for i, (x, y, w, h) in enumerate(best[:50]):
        print(f'{i+1:3d}: x={x:.2f}, y={y:.2f}, w={w:.2f}, h={h:.2f}')
    if args.visualize:
        visualize(best, box_w, box_h, args.out)
        print(f'Layout image written to {args.out}')


if __name__ == '__main__':
    main()
