
import unittest
import os
import json
from packer import pack_multiple_items, rects_overlap

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

if __name__ == '__main__':
    unittest.main()
