title PyWord Launcher
curl -O https://raw.githubusercontent.com/Behike/PyWord/main/addChapter.py
curl -O https://raw.githubusercontent.com/Behike/PyWord/main/config.py
curl -O https://raw.githubusercontent.com/Behike/PyWord/main/requirements.txt
curl -O https://raw.githubusercontent.com/Behike/PyWord/main/Style/default.css
curl -O https://github.com/Behike/PyWord/raw/main/Style/Cambria-Font.ttf
curl -O https://github.com/Behike/PyWord/raw/main/Style/Palatino%20Linotype.ttf

pip install -r requirements.txt
python .\addChapter.py
pause