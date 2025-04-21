call poetry env use python
call poetry run python -m pip install --upgrade pip
call poetry install
call poetry run pre-commit run --all-files
call poetry run pyinstaller sigbox-lever-video.spec --clean 2> dist\build.log
tail dist\build.log
