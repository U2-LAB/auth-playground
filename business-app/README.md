# Auth-portal

## Buisness app
Simple business app that will use OAuth system.

### Setup virtual environment
1. Create venv
```bash
cd business-app
python -m venv env
```
2. Install dependencies
```bash
source ./env/bin/activate
pip install -r requirements.txt
```
3. Update *env/bin/activate* file with variables
```bash
# env/bin/activate

deactivate(){
    ...
    unset DJANGO_SECRET_KEY
    unset DJANGO_DB_NAME
    unset DJANGO_DB_USER
    unset DJANGO_DB_PASSWORD
}
...
export DJANGO_SECRET_KEY='YOUR_SECRET_DJANGO_KEY' # Can be found in settings.py
export DJANGO_DB_NAME='YOUR_DB_NAME'
export DJANGO_DB_USER='YOUR_DB_USER'
export DJANGO_DB_PASSWORD='YOUR_DB_USER_PASSWORD'
```
### Run app
1. Build frontend
```bash
cd src/frontend
npm run build
```
2. Run django server
```bash
cd ..
./manage.py runserver
```
3. Go to Browser to *localhost:8000*
