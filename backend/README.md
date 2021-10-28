# Introverts Backend

## Executing 

```bash
$ docker build -t ffm .
[+] Building 7.7s (11/11) FINISHED                                                                                                           
 => [internal] load build definition from Dockerfile                                                                                    0.0s
 => => transferring dockerfile: 37B                                                                                                     0.0s
 => [internal] load .dockerignore                                                                                                       0.0s
 => => transferring context: 34B                                                                                                        0.0s
 => [internal] load metadata for docker.io/library/python:3.8                                                                           0.2s
 => [1/6] FROM docker.io/library/python:3.8@sha256:69947d7cb1febaff7782fe6bcabb1b2943f947b892431ca8cde8782bdfb6d9fb                     0.0s
 => [internal] load build context                                                                                                       0.0s
 => => transferring context: 359B                                                                                                       0.0s
 => CACHED [2/6] WORKDIR /code                                                                                                          0.0s
 => CACHED [3/6] COPY ./requirements.txt /code/requirements.txt                                                                         0.0s
 => CACHED [4/6] RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt                                                     0.0s
 => [5/6] RUN set -xe     && apt-get update -q     && apt-get install -y -q     graphviz                                                7.0s
 => [6/6] COPY ./app /code/app                                                                                                          0.0s
 => exporting to image                                                                                                                  0.3s 
 => => exporting layers                                                                                                                 0.3s 
 => => writing image sha256:9c587994dccee32e15a1175a75bcb8bbc4aee0db89b54f623e67e7ce2ec51990                                            0.0s 
 => => naming to docker.io/library/ffm                                                                                                  0.0s 
                                                                                                                                             
Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them

$ docker run -it --name ffm_container -p8080:80 ffm
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
```

## Accessing OpenAPI

Open `http://127.0.0.1:8080/docs`