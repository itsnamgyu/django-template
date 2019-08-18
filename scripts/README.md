# Deploy on Apache using WSGI (Ubuntu 16.04, 18.04)

## Quick start

### Install requirements

- Apache 2
- Virtual environment (`venv` or equivalent)
- mod-wsgi Python package

```
sudo apt install apache2
sudo apt install apache2-dev
```

#### Set up a virtual environment (Python 3.5+)

```
# start at root folder
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install mod-wsgi
```

### Run script!

```bash
# start at root folder
source venv/bin/activate # enable virtual environment
export PROJECT_DIR=`pwd`
./scripts/install --host=mysite.com
```

#### Start apache service

Make sure to restart Apache service using

```bash
sudo apachectl restart
```

*May return error status if Apache is already running*
