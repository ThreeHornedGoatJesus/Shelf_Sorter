#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json, csv, os
from packer import pack_multiple_items, best_layout
from typing import List, Dict

try:
    from PIL import Image
    from PIL import Image as PilImage
    from PIL import ImageOps
except Exception:
    PilImage = None

class PackerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Packer (local GUI)')
        self.geometry('1000x600')
        self.items: List[Dict] = []
        self.create_widgets()

    def create_widgets(self):
        frm = ttk.Frame(self)
        frm.pack(fill='both', expand=True)

        ctrl = ttk.Frame(frm)
        ctrl.pack(side='left', fill='y', padx=10, pady=10)

        ttk.Label(ctrl, text='Box width').grid(row=0, column=0, sticky='w')
        self.box_w = tk.DoubleVar(value=200)
        ttk.Entry(ctrl, textvariable=self.box_w).grid(row=0, column=1)

        ttk.Label(ctrl, text='Box height').grid(row=1, column=0, sticky='w')
        self.box_h = tk.DoubleVar(value=100)
        ttk.Entry(ctrl, textvariable=self.box_h).grid(row=1, column=1)

        ttk.Separator(ctrl, orient='horizontal').grid(row=2, column=0, columnspan=2, pady=8, sticky='ew')

        ttk.Label(ctrl, text='Item W').grid(row=3, column=0, sticky='w')
        self.item_w = tk.DoubleVar(value=30)
        ttk.Entry(ctrl, textvariable=self.item_w).grid(row=3, column=1)

        ttk.Label(ctrl, text='Item H').grid(row=4, column=0, sticky='w')
        self.item_h = tk.DoubleVar(value=20)
        ttk.Entry(ctrl, textvariable=self.item_h).grid(row=4, column=1)

        ttk.Label(ctrl, text='Count (0 = unlimited)').grid(row=5, column=0, sticky='w')
        self.item_count = tk.IntVar(value=10)
        ttk.Entry(ctrl, textvariable=self.item_count).grid(row=5, column=1)

        ttk.Button(ctrl, text='Add Item', command=self.add_item).grid(row=6, column=0, columnspan=2, pady=6, sticky='ew')
        ttk.Button(ctrl, text='Pack', command=self.pack_items).grid(row=7, column=0, columnspan=2, pady=6, sticky='ew')

        ttk.Button(ctrl, text='Load items', command=self.load_items).grid(row=8, column=0, columnspan=2, pady=6, sticky='ew')
        ttk.Button(ctrl, text='Save items', command=self.save_items).grid(row=9, column=0, columnspan=2, pady=6, sticky='ew')

        ttk.Button(ctrl, text='Export JSON', command=self.export_json).grid(row=10, column=0, columnspan=2, pady=6, sticky='ew')
        ttk.Button(ctrl, text='Export CSV', command=self.export_csv).grid(row=11, column=0, columnspan=2, pady=6, sticky='ew')
        ttk.Button(ctrl, text='Save Image', command=self.save_image).grid(row=12, column=0, columnspan=2, pady=6, sticky='ew')

        ttk.Separator(ctrl, orient='horizontal').grid(row=13, column=0, columnspan=2, pady=8, sticky='ew')
        ttk.Label(ctrl, text='Items list').grid(row=14, column=0, columnspan=2)
        self.items_listbox = tk.Listbox(ctrl, height=10)
        self.items_listbox.grid(row=15, column=0, columnspan=2, sticky='ew')
        ttk.Button(ctrl, text='Remove selected', command=self.remove_selected).grid(row=16, column=0, columnspan=2, pady=6, sticky='ew')

        # canvas area
        canvas_frame = ttk.Frame(frm)
        canvas_frame.pack(side='left', fill='both', expand=True)
        self.canvas = tk.Canvas(canvas_frame, bg='white')
        self.canvas.pack(fill='both', expand=True, padx=10, pady=10)

        self.placements = []

    def add_item(self):
        w = float(self.item_w.get())
        h = float(self.item_h.get())
        cnt = self.item_count.get()
        self.items.append({'w': w, 'h': h, 'count': cnt})
        self.items_listbox.insert('end', f"{w}x{h} (x{cnt})")

    def remove_selected(self):
        sel = self.items_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        self.items_listbox.delete(idx)
        del self.items[idx]

    def pack_items(self):
        box_w = float(self.box_w.get())
        box_h = float(self.box_h.get())
        if self.items:
            placements = pack_multiple_items(box_w, box_h, self.items)
            self.placements = placements
            self.draw_placements(box_w, box_h, placements)
            messagebox.showinfo('Packed', f'Placed {len(placements)} items')
        else:
            # single-item mode from inputs
            w = float(self.item_w.get())
            h = float(self.item_h.get())
            cnt = self.item_count.get()
            if cnt == 0:
                cnt = None
            best = best_layout(box_w, box_h, w, h, cnt)
            placements = [{'x': x, 'y': y, 'w': w, 'h': h, 'type': 0} for (x, y, w, h) in best]
            self.placements = placements
            self.draw_placements(box_w, box_h, placements)
            messagebox.showinfo('Packed', f'Placed {len(placements)} items')

    def draw_placements(self, box_w, box_h, placements):
        self.canvas.delete('all')
        cw = self.canvas.winfo_width() or int(self.canvas['width'])
        ch = self.canvas.winfo_height() or int(self.canvas['height'])
        scale = min(cw / box_w, ch / box_h)
        # draw box
        self.canvas.create_rectangle(0, 0, box_w * scale, box_h * scale, outline='black')
        colors = ['lightblue','lightgreen','orange','pink','lightgrey','lightyellow']
        for p in placements:
            x = p['x'] * scale
            y = p['y'] * scale
            w = p['w'] * scale
            h = p['h'] * scale
            color = colors[p.get('type',0) % len(colors)]
            self.canvas.create_rectangle(x, y, x + w, y + h, fill=color, outline='black')

    def save_image(self):
        if PilImage is None:
            messagebox.showerror('Missing dependency', 'Pillow is required to save PNG. Install pillow in your environment.')
            return
        path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG','*.png')])
        if not path:
            return
        # export via postscript
        ps = filedialog.asksaveasfilename(defaultextension='.ps', filetypes=[('PostScript','*.ps')], title='Temporary PostScript (internal)')
        try:
            ps = path + '.ps'
            self.canvas.postscript(file=ps)
            img = PilImage.open(ps)
            img.save(path, 'png')
            os.remove(ps)
            messagebox.showinfo('Saved', f'Saved image to {path}')
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def export_json(self):
        if not self.placements:
            messagebox.showwarning('No layout', 'No placements to export')
            return
        path = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[('JSON','*.json')])
        if not path:
            return
        data = {'box': {'w': float(self.box_w.get()), 'h': float(self.box_h.get())}, 'placements': self.placements}
        with open(path, 'w', encoding='utf8') as f:
            json.dump(data, f, indent=2)
        messagebox.showinfo('Saved', f'Wrote {path}')

    def export_csv(self):
        if not self.placements:
            messagebox.showwarning('No layout', 'No placements to export')
            return
        path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV','*.csv')])
        if not path:
            return
        with open(path, 'w', newline='', encoding='utf8') as f:
            w = csv.writer(f)
            w.writerow(['x','y','w','h','type'])
            for p in self.placements:
                w.writerow([p['x'], p['y'], p['w'], p['h'], p.get('type','')])
        messagebox.showinfo('Saved', f'Wrote {path}')

    def load_items(self):
        path = filedialog.askopenfilename(filetypes=[('JSON','*.json'),('CSV','*.csv')])
        if not path:
            return
        if path.lower().endswith('.json'):
            with open(path,'r',encoding='utf8') as f:
                data = json.load(f)
                self.items = data
        else:
            items = []
            with open(path,'r',encoding='utf8') as f:
                r = csv.DictReader(f)
                for row in r:
                    c = int(row.get('count',1))
                    if c == 0:
                        c = None
                    items.append({'w': float(row['w']), 'h': float(row['h']), 'count': c})
            self.items = items
        self.items_listbox.delete(0,'end')
        for it in self.items:
            self.items_listbox.insert('end', f"{it['w']}x{it['h']} (x{it.get('count',1)})")

    def save_items(self):
        path = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[('JSON','*.json')])
        if not path:
            return
        with open(path,'w',encoding='utf8') as f:
            json.dump(self.items, f, indent=2)
        messagebox.showinfo('Saved', f'Wrote {path}')

if __name__ == '__main__':
    app = PackerGUI()
    app.mainloop()
