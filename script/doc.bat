cd ..
pdoc3 --html boo -o docs --force
move docs\boo\*.* docs 
git commit -am"documentation update"
git push
cd script