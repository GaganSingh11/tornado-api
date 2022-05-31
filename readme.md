# Test API using Tornado

### First Clone this repo using git

```
git clone https://github.com/GaganSingh11/tornado-api.git
```
Once cloned the repo then make sure that you are inside the tornado-api repo

```
$ cd tornado-api
```

### Setup the local environment for development purposes.

- This project uses some features which are only available in python3 so please install python3.10 or higher in your system

  - [python download](https://www.python.org/downloads/)

- Once the python3.10+ is setup in your system, highly recommend to use virtual env instead of global python interpreter. [venv](https://docs.python.org/3/library/venv.html)

> To create virtual python environment

```
$python3 -m venv venv
```
> To activate virtual env

```
$ source venv/bin/activate
```

> Now, install requirements using pip

```
(venv)$ pip install -r requirements.txt
```
> Once everything setup to check if the project is setup correctly by running the server
```
(venv)$ python3 app/main.py
```

### API Routes

- Test API `/tests`:

  - Get
    - 200
      - response body:
        ```json
        {
        "tests": [
            {
                "test_number": 19,
                "test_string": "boolen fixed",
                "test_boolen": false
            },
            {
                "test_number": 1,
                "test_string": "First test",
                "test_boolen": false
            },
            {
                "test_number": 400,
                "test_string": "third test",
                "test_boolen": false
            }
            ]

        }
        ```
    
  - POST
    - 200
      - response body:
        ```json
        {
        "test": {
            "test_number": 400,
            "test_string": "third test",
            "test_boolen": false
            }
        }
        ```


- Test API `/tests/<id>`:
  - GET
    - 200
      - response body:
        ```json
        {
        "test": {
            "test_number": 400,
            "test_string": "third test",
            "test_boolen": false
            }
        }
        ```




