REM delete old build, dist, egg
python setup.py sdist bdist_wheel
twine upload dist/*