docker build -t winklermw-mz/mymcp .
docker run -d --name MyMCP --network my-local-net -v /Users/markus/Documents:/documents -p 8002:8002 winklermw-mz/mymcp