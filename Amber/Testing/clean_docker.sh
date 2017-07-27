docker rm --force $(docker ps --all --quiet)
docker rmi --force $(docker images --all --quiet)