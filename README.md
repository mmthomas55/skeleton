# skeleton

## Setup

```
$ pyvenv ./env
$ . env/bin/activate
$ pip install -r requirements.txt
```


## Set up CoreOS with etcd

In order to test this POC, you will need to have CoreOS running so you can update config
variables in etcd and have the application use them.
I used Vagrant to run CoreOS across 3 nodes on a VM with VirtualBox.

Clone this project and follow the setup instuctions
[coreos-vagrant](https://coreos.com/os/docs/latest/booting-on-vagrant.html)
Once you have CoreOS up and running, you can set up the config structure with values to work with
this project.

For my example, the application is skeleton and the environment is mthomas.

```
# create directories
$ curl -L http://172.17.8.101:2379/v2/keys/skeleton -XPUT -d dir=true
$ curl -L http://172.17.8.101:2379/v2/keys/skeleton/mthomas -XPUT -d dir=true

# create port and debug keys within skeleton/mthomas directory
$ curl -L http://172.17.8.101:2379/v2/keys/skeleton/mthomas/port -XPUT -d value=80
$ curl -L http://172.17.8.101:2379/v2/keys/skeleton/mthomas/debug -XPUT -d value=True

# See values for available environment
$ curl -L http://172.17.8.101:2379/v2/keys/skeleton/mthomas
```

### Config Structure

The commands above set up the directory structure in the following format:
```
$ curl -L http://172.17.8.101:2379/v2/keys/skeleton/mthomas | python -m json.tool
{
    "action": "get",
    "node": {
        "createdIndex": 66250,
        "dir": true,
        "key": "/skeleton/mthomas",
        "modifiedIndex": 66250,
        "nodes": [
            {
                "createdIndex": 85833,
                "key": "/skeleton/mthomas/debug",
                "modifiedIndex": 85833,
                "value": "True"
            },
            {
                "createdIndex": 66289,
                "key": "/skeleton/mthomas/port",
                "modifiedIndex": 66289,
                "value": "80"
            }
        ]
    }
}
```


## Run
Start up the app and pass in environment (defaults to mthomas).

Environment will need to correspond to an etcd subdirectory for the skeleton app.

The port will come from the etcd config!

```
$ python main.py --env=mthomas
```


## Ping the app

Once the app is running, curl to it to make sure it's up.

(Replace 80 with a valid port from the etcd config)

```
$ curl -i http://localhost:80/ping
```

## Publish to PyPi
The package version is set in `skeleton/__init__.py`.

In order to publish a package to PyPi, you will need to set up a pypirc file
with credentials in your home directory.  Here's a sample of what my pypirc
looks like when publishing to a pypi server called `internal`.
```
[distutils]
index-servers =
  internal

[internal]
repository: http://someserver:8080
username: xxxxxxx
password: xxxxxxx
```

First, you need to publish the tarball for distribution.
```
$ python setup.py sdist
```

Next, you will need to register your PyPi server, in my case `internal`.
```
$ python setup.py register -r internal
```

Now you can publish the `skeleton` package (sdist) to PyPi.
```
$ python setup.py sdist upload -r internal
```

### Install Package from PyPi
To install the `skeleton` package from the `internal` PyPi server, add the
following line to the top of your requrements file.  Replace
`http://someserver:8080` with the actual hostname of the PyPi server (specified
in your `~/.pypirc`).

```
-i http://someserver:8080/simple/
```
