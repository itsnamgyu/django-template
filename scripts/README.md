# Deploy on Apache using WSGI (Ubuntu 16.04, 18.04)

## Quick start

### Install requirements

- Apache 2
- Virtual environment (`venv` or equivalent)

```
sudo apt install apache2
sudo apt install apache2-dev
```

#### Install a virtual enviornment (Python 3.5+)

```
# start at root folder
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run script!

```bash
# start at root folder
# enable virtual environment
pip install mod-wsgi
export PROJECT_DIR=`pwd`
./scripts/install --host=mysite.com
```
