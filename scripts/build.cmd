python -m venv venv
.\venv\Scripts\activate
pip install -r .\requirements.txt
docker-compose up --build -d
sleep 3000
python .\init_database.py