## Commands to build this project:

```sh
Install dependencies
> pip install -r requirements.txt

Database initialization, migration (sqlite3 in here)
> flask db init
> flask db migrate -m "orders table"
> flask db upgrade

Finally, run:
> python importer.py (development version, don't do this in production)
```