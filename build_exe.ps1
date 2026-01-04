# Build packer.exe locally on Windows using PyInstaller
python -m pip install --upgrade pip
pip install -r requirements.txt pyinstaller
pyinstaller --onefile packer.py --name packer
if (Test-Path .\dist\packer.exe) { Write-Host "Built: .\dist\packer.exe" } else { Write-Error "Build failed" }
