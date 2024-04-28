docker build . -t fastapi_app:latest
docker run -d -p 8000:8000 fastapi_app
docker-compose up --build -d
sleep 3000
python .\init_database.py