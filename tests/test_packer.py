
import unittest
import os
import json
from packer import pack_multiple_items, rects_overlap, best_layout

class TestPacker(unittest.TestCase):
    def test_multi_pack_no_overlap(self):
        box_w, box_h = 200, 100
        items = [{'w':30,'h':20,'count':10},{'w':60,'h':30,'count':4}]
        placements = pack_multiple_items(box_w, box_h, items)
        # ensure some placements
        self.assertGreater(len(placements), 0)
        # check no overlap
        rects = [(p['x'],p['y'],p['w'],p['h']) for p in placements]
        for i in range(len(rects)):
            for j in range(i+1,len(rects)):
                self.assertFalse(rects_overlap(rects[i], rects[j]))

    def test_unlimited_count(self):
        box_w, box_h = 100, 50
        items = [{'w':30,'h':20,'count':0}]
        placements = pack_multiple_items(box_w, box_h, items)
        # expect a 3x2 grid = 6
        self.assertEqual(len(placements), 6)

    def test_single_type_count_zero(self):
        box_w, box_h = 100, 50
        item_w, item_h = 30, 20
        # count=None (unlimited) -> expect 6 placements
        best = best_layout(box_w, box_h, item_w, item_h, None)
        self.assertEqual(len(best), 6)

if __name__ == '__main__':
    unittest.main()
