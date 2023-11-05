
set +x
docker build ./client -t iot-hw2-client-img
docker build ./server -t iot-hw2-server-img

docker compose up -d 
