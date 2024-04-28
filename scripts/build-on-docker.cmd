docker build . -t fastapi_app:latest
docker-compose up --build -d
sleep 3000
python .\init_database.py