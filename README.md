# PPTMaker
Flask Powered Web Application which takes Topic &amp; Slide Count &amp; Automatically Generates a Presentable PPT.

## Website
[makeit.witeso.com](https://makeit.witeso.com)

## Technologies Used
- Flask
- Celery
- Redis
- HTML
- CSS
- Bootstrap
- Javascript
- OpenAi API
- Unsplash API

## Installation
```
## Windows
pip install virtualenv
virtualenv venv
venv\Scripts\activate
pip install -r requirements.txt

## Linux
pip install virtualenv
virtualenv venv
venv/bin/activate
pip install -r requirements.txt
```

## Installation & Run
```
# Install Redis on Linux [Redis Not Available on Windows 11]
sudo apt install redis-server 
sudo systemctl start redis-server
sudo systemctl enable redis-server
sudo service redis-server status 
```

```
pip install -r requirements.txt

# Run in Terminal - 1
python app.py

# Run in Terminal - 2
celery -A app.celery worker --loglevel=info
```

```
UNSPLASH_ACCESS_KEY='btnHAFhjy2uuVUWDUYGOMd_lHwJr3AVQNV4AyPPNqLc'
from pyunsplash import PyUnsplash
import requests

pu = PyUnsplash(api_key=UNSPLASH_ACCESS_KEY)
photos = pu.photos(type_='random', count=1, featured=True, query="bugatti")
[photo] = photos.entries
response = requests.get(photo.link_download, {"client_id": UNSPLASH_ACCESS_KEY}, allow_redirects=True)
open('../bugatti.png', 'wb').write(response.content)
```
