# Run multi-item example. If packer.exe exists (from CI), use it; otherwise try python.
$exe = Join-Path $PWD 'dist\packer.exe'
if (Test-Path $exe) {
  & $exe --box 200 100 --items-file examples\items.json --visualize --out examples\layout_multi.png --output-json examples\placements.json --output-csv examples\placements.csv
} else {
  python packer.py --box 200 100 --items-file examples\items.json --visualize --out examples\layout_multi.png --output-json examples\placements.json --output-csv examples\placements.csv
}
