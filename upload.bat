REM will prompt for passwaord unless staored locally in a config file
python setup.py sdist bdist_wheel
twine upload dist/*

REM Cleaning up...
rd build /Q/S
rd dist /Q/S
rd boo.egg-info /Q/S