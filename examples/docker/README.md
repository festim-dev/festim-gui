# Docker Bundle

Docker bundle aims to provide an easy step to bundle and deploy your application
into a Docker image that can easily be deployed in the cloud as a service and
will naturally support multi-users.

## Building image

```sh
docker build -t festim-gui -f ./examples/docker/Dockerfile .
```

## Run image

```sh
docker run -it --rm -p 8080:80 festim-gui
```

Then connect to `http://localhost:8080/`.
