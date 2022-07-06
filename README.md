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
