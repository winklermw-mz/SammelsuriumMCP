docker build -t my-mcp-server .
docker run -d --name my-mcp-server --network my-local-net -p 7999:7999 my-mcp-server