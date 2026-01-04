import os
from flask import Flask, render_template, request, jsonify
from packer import pack_multiple_items, best_layout

base_dir = os.path.dirname(__file__)
template_dir = os.path.join(base_dir, 'templates')
static_dir = os.path.join(base_dir, 'static')
app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pack', methods=['POST'])
def pack_api():
    data = request.get_json() or {}
    box = data.get('box', {})
    box_w = float(box.get('w', 100))
    box_h = float(box.get('h', 50))
    items = data.get('items')

    if items:
        # items: list of {w,h,count}
        placements = pack_multiple_items(box_w, box_h, items)
        return jsonify({'placements': placements, 'count': len(placements)})

    item = data.get('item')
    count = data.get('count')
    if not item:
        return jsonify({'error': 'no item or items provided'}), 400
    item_w = float(item.get('w'))
    item_h = float(item.get('h'))
    placements = best_layout(box_w, box_h, item_w, item_h, count)
    # convert to dicts
    placements_dicts = [{'x':x,'y':y,'w':w,'h':h,'type':0} for (x,y,w,h) in placements]
    return jsonify({'placements': placements_dicts, 'count': len(placements_dicts)})

if __name__ == '__main__':
    app.run(debug=True)
