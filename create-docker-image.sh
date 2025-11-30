docker build -t winklermw-mz/mymcp .
docker run -d --name MyMCP --network my-local-net -v /Users/markus/Documents:/documents -p 7999:7999 winklermw-mz/mymcp