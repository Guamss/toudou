# Toudou - the todo application

the project requirement :
* python 3.10 or above
* click
* sqlalchemy
* flask

which means you need to installed them using pip :
```bash
$ pip install click
$ pip install sqlalchemy
$ pip install flask
```

now that the project dependencies are installed with pip you need to setup the project itself :

```bash
$ pdm install           
$ pdm run toudou        # run the project
Usage: toudou [OPTIONS] COMMAND [ARGS]...

Options:
    --help  Show this message and exit.

Commands:
    complete
    create
    delete
    display
    display-all
    import-csv
    update
```

the web application can also be run like this :
```bash
pdm run flask --app toudou.views --debug run
```

Course & examples : [https://kathode.neocities.org](https://kathode.neocities.org)
