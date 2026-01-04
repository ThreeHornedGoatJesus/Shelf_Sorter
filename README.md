Rectangular Packer

Small Python tool to compute how many identical rectangles (items) fit inside a larger rectangle (box).

Usage examples:

```bash
python packer.py --box 100 50 --item 30 20 --count 100 --visualize --out layout.png
```

Options:
- `--box W H` : box width and height
- `--item W H` : item width and height
- `--count N` : optional maximum number of items available
- `--visualize` : write a PNG image of the layout (requires `matplotlib`)

Windows executable (CI build)

- A GitHub Actions workflow is included at `.github/workflows/build-windows.yml` that builds a one-file Windows executable using PyInstaller and uploads it as an artifact named `packer-windows`.
- To run the workflow: push to `main` or trigger `Run workflow` in the Actions tab on GitHub. Download the `packer.exe` from the workflow artifacts.

Build locally on Windows

PowerShell:

```powershell
.\build_exe.ps1
```

Command prompt:

```bat
build_exe.bat
```

Notes

- Building the executable requires Python and PyInstaller. The CI build uses `windows-latest` runner and Python 3.11.
## Multi-item input and exports

You can provide a CSV or JSON file with item types and counts (columns: `w,h,count`), and the tool will attempt to pack items greedily largest-first. Examples are in the `examples/` folder.

Examples:

```powershell
# CSV input
python packer.py --box 200 100 --items-file examples\items.csv --visualize --out examples\layout_multi.png --output-json examples\placements.json --output-csv examples\placements.csv

# JSON input
python packer.py --box 200 100 --items-file examples\items.json --visualize --out examples\layout_multi.png --output-json examples\placements.json --output-csv examples\placements.csv
```

Flags:
- `--items-file PATH` : CSV or JSON file with items (CSV headers: w,h,count)
- `--output-json PATH` : write placements summary to JSON file
- `--output-csv PATH` : write placements to CSV file

Note: multi-item packing currently uses a simple greedy placement; for denser/optimal packing, I can add heuristic bin-packing (guillotine, skyline) later.

Local GUI

You can run the local GUI (Tkinter) which requires no additional web server:

```powershell
python gui.py
```

Alternatively, the CI and local build scripts now build a `packer-gui.exe` alongside `packer.exe`.
