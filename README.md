# skeleton

## Setup

```
virtualenv env
. env/bin/activate
pip install -r requirements.txt
```

## Run

Start up the app and pass in a port

```
python main.py --port=999
```

## Ping the app

Once the app is running, curl to it to make sure it's up.

(Replace 999 with a valid port)

```
curl -i http://localhost:999/ping
```
