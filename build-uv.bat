@echo off

REM avoid error installing sniffio
set UV_LINK_MODE=copy

REM Create virtual environment
uv venv .venv

REM Install dependencies
uv sync --extra dev

REM Run tests
uv run pre-commit run --all-files

REM Build
uv run pyinstaller sigbox-lever-video.spec --clean 2> dist\build.log
tail dist\build.log
