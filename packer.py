#!/usr/bin/env python3
import argparse
import json
import csv
import sys
from typing import List, Tuple, Optional, Dict

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


def greedy_row_pack(box_w: float, box_h: float, item_w: float, item_h: float, max_items: Optional[int] = None) -> List[Rect]:
    placements: List[Rect] = []
    y = 0.0
    while y + min(item_h, item_w) <= box_h:
        remaining_width = box_w
        x = 0.0
        while True:
            if max_items is not None and len(placements) >= max_items:
                return placements
            placed = False
            if item_w <= remaining_width and item_h <= (box_h - y):
                placements.append((x, y, item_w, item_h))
                x += item_w
                remaining_width -= item_w
                placed = True
            elif item_h <= remaining_width and item_w <= (box_h - y):
                placements.append((x, y, item_h, item_w))
                x += item_h
                remaining_width -= item_h
                placed = True
            if not placed:
                break
        y += item_h
        if max_items is not None and len(placements) >= max_items:
            break
    return placements


def best_layout(box_w: float, box_h: float, item_w: float, item_h: float, max_items: Optional[int] = None):
    candidates = []
    p_grid = grid_pack(box_w, box_h, item_w, item_h, max_items)
    candidates.append(p_grid)
    p_grid_rot = grid_pack(box_w, box_h, item_h, item_w, max_items)
    p_grid_rot_norm = [(x, y, item_w, item_h) for (x, y, w, h) in p_grid_rot]
    candidates.append(p_grid_rot_norm)
    p_greedy = greedy_row_pack(box_w, box_h, item_w, item_h, max_items)
    candidates.append(p_greedy)
    best = max(candidates, key=lambda p: len(p))
    return best


# --- multi-item support helpers ---

def rects_overlap(a: Rect, b: Rect) -> bool:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return not (ax + aw <= bx or bx + bw <= ax or ay + ah <= by or by + bh <= ay)


def can_place(x: float, y: float, w: float, h: float, box_w: float, box_h: float, placed: List[Rect]) -> bool:
    if x + w > box_w or y + h > box_h:
        return False
    r = (x, y, w, h)
    for p in placed:
        if rects_overlap(r, p):
            return False
    return True


def pack_multiple_items(box_w: float, box_h: float, items: List[Dict]) -> List[Dict]:
    """Pack multiple item types. Items: list of dicts {'w','h','count','id'(optional)}
    Returns list of placements with fields x,y,w,h,type_id
    Simple greedy scan algorithm: place largest-first and scan rows/cols for fit."""
    # expand items with ids and sort by area desc
    expanded = []
    for i, it in enumerate(items):
        count = int(it.get('count', 1))
        for _ in range(count):
            expanded.append({'w': float(it['w']), 'h': float(it['h']), 'type': i})
    expanded.sort(key=lambda x: x['w'] * x['h'], reverse=True)

    placements = []  # dicts with x,y,w,h,type
    step = 1.0
    for item in expanded:
        w = item['w']; h = item['h']
        placed_flag = False
        for y in [round(i * step, 6) for i in range(int((box_h // step) + 1))]:
            if y + min(w, h) > box_h:
                break
            for x in [round(i * step, 6) for i in range(int((box_w // step) + 1))]:
                # try unrotated
                if can_place(x, y, w, h, box_w, box_h, [(p['x'], p['y'], p['w'], p['h']) for p in placements]):
                    placements.append({'x': x, 'y': y, 'w': w, 'h': h, 'type': item['type']})
                    placed_flag = True
                    break
                # try rotated
                if can_place(x, y, h, w, box_w, box_h, [(p['x'], p['y'], p['w'], p['h']) for p in placements]):
                    placements.append({'x': x, 'y': y, 'w': h, 'h': w, 'type': item['type']})
                    placed_flag = True
                    break
            if placed_flag:
                break
        # if couldn't place item, skip it
    return placements


# --- exports ---

def export_json(path: str, box_w: float, box_h: float, placements: List[Dict]):
    data = {
        'box': {'w': box_w, 'h': box_h},
        'placements': placements,
        'count': len(placements)
    }
    with open(path, 'w', encoding='utf8') as f:
        json.dump(data, f, indent=2)


def export_csv(path: str, placements: List[Dict]):
    with open(path, 'w', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(['x','y','w','h','type'])
        for p in placements:
            writer.writerow([p['x'], p['y'], p['w'], p['h'], p.get('type', '')])


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
    colors = ['C0','C1','C2','C3','C4','C5','C6','C7','C8','C9']
    for p in placements:
        x = p['x'] if isinstance(p, dict) else p[0]
        y = p['y'] if isinstance(p, dict) else p[1]
        w = p['w'] if isinstance(p, dict) else p[2]
        h = p['h'] if isinstance(p, dict) else p[3]
        t = p.get('type', 0) if isinstance(p, dict) else 0
        ax.add_patch(Rectangle((x, y), w, h, facecolor=colors[t % len(colors)], edgecolor='black', alpha=0.6))
    ax.invert_yaxis()
    plt.savefig(out_path, bbox_inches='tight')
    plt.close(fig)


def parse_items_file(path: str) -> List[Dict]:
    if path.lower().endswith('.json'):
        with open(path, 'r', encoding='utf8') as f:
            data = json.load(f)
            # expect list of objects {w,h,count}
            return data
    else:
        # assume CSV with headers w,h,count
        items = []
        with open(path, 'r', encoding='utf8') as f:
            reader = csv.DictReader(f)
            for r in reader:
                items.append({'w': float(r['w']), 'h': float(r['h']), 'count': int(r.get('count', 1))})
        return items


def parse_args():
    p = argparse.ArgumentParser(description='Pack identical rectangles in a box and return best layout')
    p.add_argument('--box', nargs=2, type=float, required=True, metavar=('W', 'H'), help='Box width and height')
    p.add_argument('--item', nargs=2, type=float, help='Item width and height (single-type pack)')
    p.add_argument('--items-file', type=str, help='CSV or JSON file containing multiple item types')
    p.add_argument('--count', type=int, default=None, help='Maximum number of items available (single-type)')
    p.add_argument('--visualize', action='store_true', help='Save an image of the layout (requires matplotlib)')
    p.add_argument('--out', type=str, default='layout.png', help='Output image path')
    p.add_argument('--output-json', type=str, help='Write placements to JSON file')
    p.add_argument('--output-csv', type=str, help='Write placements to CSV file')
    return p.parse_args()


def main():
    args = parse_args()
    box_w, box_h = args.box

    if args.items_file:
        items = parse_items_file(args.items_file)
        placements = pack_multiple_items(box_w, box_h, items)
        print(f'Placed {len(placements)} total items from {len(items)} types')
        if args.output_json:
            export_json(args.output_json, box_w, box_h, placements)
            print(f'Wrote JSON to {args.output_json}')
        if args.output_csv:
            export_csv(args.output_csv, placements)
            print(f'Wrote CSV to {args.output_csv}')
        if args.visualize:
            visualize(placements, box_w, box_h, args.out)
            print(f'Layout image written to {args.out}')
        # print a small summary
        counts = {}
        for p in placements:
            counts[p['type']] = counts.get(p['type'], 0) + 1
        for t, c in counts.items():
            print(f'Type {t}: {c}')
        return

    if not args.item:
        print('Error: either --item or --items-file must be supplied', file=sys.stderr)
        sys.exit(1)

    item_w, item_h = args.item
    max_items = args.count
    best = best_layout(box_w, box_h, item_w, item_h, max_items)
    placed = len(best)
    print(f'Placed: {placed} item(s)')
    if max_items is not None:
        print(f'Available: {max_items}')
    cols_est = int(box_w // item_w)
    rows_est = int(box_h // item_h)
    print(f'Estimate grid (no-rotation): {cols_est} x {rows_est} = {cols_est*rows_est}')
    for i, (x, y, w, h) in enumerate(best[:50]):
        print(f'{i+1:3d}: x={x:.2f}, y={y:.2f}, w={w:.2f}, h={h:.2f}')
    if args.output_json:
        export_json(args.output_json, box_w, box_h, [{'x':x,'y':y,'w':w,'h':h} for (x,y,w,h) in best])
        print(f'Wrote JSON to {args.output_json}')
    if args.output_csv:
        export_csv(args.output_csv, [{'x':x,'y':y,'w':w,'h':h} for (x,y,w,h) in best])
        print(f'Wrote CSV to {args.output_csv}')
    if args.visualize:
        visualize([{'x':x,'y':y,'w':w,'h':h,'type':0} for (x,y,w,h) in best], box_w, box_h, args.out)
        print(f'Layout image written to {args.out}')


if __name__ == '__main__':
    main()
