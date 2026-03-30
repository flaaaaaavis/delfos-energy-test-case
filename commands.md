python -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip
pip install "fastapi[standard]"
pip install SQLAlchemy

pip install -r ./requirements.txt
pip freeze > ./requirements.txt

## para rodar:

python main.py

fastapi dev
