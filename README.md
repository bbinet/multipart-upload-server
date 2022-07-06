# tornado-upload
multipart/form-data upload server for Tornado

## Install Tornado
```
sudo apt install python3-pip python3-setuptools python3-magic
python -m pip install -U pip
python -m pip install -U wheel
python -m pip install tornado
```

## Start WEB Server using Tornado
```
git clone https://github.com/nopnop2002/multipart-upload-server
cd multipart-upload-server/tornado
python upload.py
```

## Upload file using curl
```
curl -X POST -F upfile=@tornado/tornado-web-service.jpg http://localhost:8080/upload_multipart

ls -l tornado/uploaded/
-rw-rw-r-- 1 nop nop 13189  5月 21 08:58 tornado-web-service.jpg
```

## Docker build

To create the image `bbinet/tornado-upload`, execute the following command in the
`docker-tornado-upload` folder:

    docker build -t bbinet/tornado-upload .

You can now push the new image to the public registry:
    
    docker push bbinet/tornado-upload


## Docker run

Then, when starting your tornado-upload container, you will want to bind ports `80`
from the tornado-upload container to a host external port.
The tornado-upload container will read its configuration from the `/config/tornado-upload.cfg`
file, so make sure this file is available to docker as a volume.

For example:

    $ docker pull bbinet/tornado-upload

    $ docker run --name tornado-upload \
        -v $(pwd)/data:/app/uploaded \
        -p 80:8080 \
        bbinet/tornado-upload
