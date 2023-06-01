docker run --name cas1 -p 9042:9042 -e HEAP_NEWSIZE=1M -e MAX_HEAP_SIZE=1024M -e CASSANDRA_CLUSTER_NAME=BigMeals -d cassandra:latest
docker run --name cas2 -e CASSANDRA_SEEDS="$(docker inspect --format='{{.NetworkSettings.IPAddress}}' cas1)" -e HEAP_NEWSIZE=1M -e MAX_HEAP_SIZE=1024M -e CASSANDRA_CLUSTER_NAME=BigMeals -d cassandra:latest
docker run --name cas3 -e CASSANDRA_SEEDS="$(docker inspect --format='{{.NetworkSettings.IPAddress}}' cas1)" -e HEAP_NEWSIZE=1M -e MAX_HEAP_SIZE=1024M -e CASSANDRA_CLUSTER_NAME=BigMeals -d cassandra:latest

docker inspect --format='{{.NetworkSettings.IPAddress}}' cas1
