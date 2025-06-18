# Build the Python sub app container
echo "Building Python sub app container..."
docker build -t my-redis-app .

# Start Python sub app
echo "Start Python sub app"
docker run -e MODE=pubsub -e REDIS_URL=redis://192.168.0.8:6379 my-redis-app