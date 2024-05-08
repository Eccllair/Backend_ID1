docker build . -t fastapi_app:latest
docker-compose up --build -d
python3 ./build.py