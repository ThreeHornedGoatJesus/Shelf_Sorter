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
