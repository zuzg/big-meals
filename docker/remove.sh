docker rm -f $(docker container ls -aq -f name=^/cas[0-9]*$)
