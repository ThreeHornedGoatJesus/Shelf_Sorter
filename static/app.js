document.addEventListener('DOMContentLoaded', () => {
  const items = [];
  const itemsList = document.getElementById('items-list');
  const canvas = document.getElementById('canvas');
  const ctx = canvas.getContext('2d');

  function renderBox(boxW, boxH, placements) {
    // scale to fit canvas
    const scale = Math.min(canvas.width / boxW, canvas.height / boxH);
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.strokeStyle = '#000'; ctx.strokeRect(0,0,boxW*scale,boxH*scale);
    placements.forEach(p => {
      ctx.fillStyle = 'rgba(0,100,200,0.5)';
      ctx.fillRect(p.x*scale, p.y*scale, p.w*scale, p.h*scale);
      ctx.strokeStyle = '#000'; ctx.strokeRect(p.x*scale,p.y*scale,p.w*scale,p.h*scale);
    });
  }

  function refreshItems() {
    itemsList.innerHTML = '';
    items.forEach((it, idx) => {
      const d = document.createElement('div');
      d.textContent = `${it.w}x${it.h} (x${it.count})`;
      itemsList.appendChild(d);
    });
  }

  document.getElementById('addItem').addEventListener('click', () => {
    const w = parseFloat(document.getElementById('item_w').value);
    const h = parseFloat(document.getElementById('item_h').value);
    const count = parseInt(document.getElementById('item_count').value,10)||1;
    items.push({w:h? w:0,h:h? h:0,count:count});
    refreshItems();
  });

  document.getElementById('packBtn').addEventListener('click', async () => {
    const boxW = parseFloat(document.getElementById('box_w').value);
    const boxH = parseFloat(document.getElementById('box_h').value);
    const payload = items.length ? {box:{w:boxW,h:boxH}, items: items} : {box:{w:boxW,h:boxH}, item: {w: parseFloat(document.getElementById('item_w').value), h: parseFloat(document.getElementById('item_h').value)}};
    const resp = await fetch('/pack', {method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify(payload)});
    const data = await resp.json();
    if (data.placements) {
      renderBox(boxW, boxH, data.placements);
      window.lastPlacements = {box:{w:boxW,h:boxH}, placements: data.placements};
    } else {
      alert('No placements returned');
    }
  });

  document.getElementById('exportJson').addEventListener('click', () => {
    if (!window.lastPlacements) { alert('No layout to export'); return; }
    const blob = new Blob([JSON.stringify(window.lastPlacements,null,2)], {type:'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href = url; a.download = 'placements.json'; a.click();
  });

  document.getElementById('exportCsv').addEventListener('click', () => {
    if (!window.lastPlacements) { alert('No layout to export'); return; }
    const rows = ['x,y,w,h,type'];
    window.lastPlacements.placements.forEach(p => rows.push([p.x,p.y,p.w,p.h,p.type||''].join(',')));
    const blob = new Blob([rows.join('\n')], {type:'text/csv'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href = url; a.download = 'placements.csv'; a.click();
  });

});
