@echo off
python -m pip install --upgrade pip
pip install -r requirements.txt pyinstaller
pyinstaller --onefile packer.py --name packer
if exist dist\packer.exe (
  echo Built: dist\packer.exe
) else (
  echo Build failed
)
