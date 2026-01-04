Windows Installer & Releases

This project automatically creates a GitHub Release and attaches build artifacts when a tag matching `v*` is pushed (e.g. `v0.1.0`). The release includes:

- `packer-<VERSION>-windows.zip` — zip containing `packer.exe` and `packer-gui.exe` (built by PyInstaller)
- `packer-<VERSION>-installer.exe` — NSIS-based installer containing the executables

CI behavior

- The workflow `.github/workflows/release.yml` runs on tag pushes (`v*`). It installs dependencies, runs tests, builds the executables and the NSIS installer, then creates a GitHub Release and uploads the ZIP and the installer.

Build a local installer (development / USB testing)

1. Create a clean venv and install deps:

   - python -m venv .venv
   - .\.venv\Scripts\Activate.ps1
   - python -m pip install -r requirements.txt pyinstaller

2. Build the executables:

   - powershell -ExecutionPolicy Bypass -File .\build_exe.ps1

   This produces `dist\packer.exe` and `dist\packer-gui.exe` and a versioned ZIP `packer-<VERSION>-windows.zip`.

3. Install NSIS (e.g., with Chocolatey):

   - choco install nsis -y

4. Build the installer:

   - powershell -ExecutionPolicy Bypass -File .\scripts\build_installer.ps1

   The script reads `VERSION` and produces `installer\dist\packer-<VERSION>-installer.exe`.

Notes

- Code signing of installers and executables is recommended for production releases. This requires a code signing certificate and adding signing steps to CI (not included by default).
- If you want me to add automatic code signing (using a secure key stored in GitHub Secrets), say so and I can add that as a follow-up.
