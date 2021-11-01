### Create `venv`
```
python -m venv ipscan-env
```
### Activate `venv`
```
source ipscan-env/bin/activate
```
### Quit `venv`
```
deactivate
```
### Save pip requirements from venv
```
pip freeze > requirements.txt
```
### Install requirements in fresh env
```
python -m pip install -r requirements.txt
```
### start http server
```
python -m http.server 1234
```