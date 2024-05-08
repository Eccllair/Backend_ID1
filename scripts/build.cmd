docker-compose up --build -d
python -m venv venv
.\venv\Scripts\activate
pip install -r .\requirements.txt
alembic init alembic
sleep 3000
python .\init_database.py