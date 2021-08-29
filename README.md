# Pokemon API

This is a API to retrive the data from the pokemon database that are in the **Pokemon.json** file that are on the root of the project.
So after you download the project, you should create a Virtual Environment for them, using the command:

```
python3 -m venv /path/to/new/virtual/environment
```

After you created the Virtual Environment you should activate it using the command:

```
source /path/to/new/virtual/environment/bin/activate
```

and then run the command to install the packages that are on the **requirements.txt**:

```
pip install -r requirements.txt
```

After that go the **app** folder and run the command:

```
uvicorn main:app
```

if you want change the code and you want to apply your changes after you save it, use the command:

```
uvicorn main:app --reload
```

After you run your application go to the folder app in other windows and run the script **from_json_to_db.py** using the command:

```
python from_json_to_db.py
```

After you execute this script your database will be filled.

To run the tests go to the **tests** folder and run the command:

```
pytest
```

#NOTE
On tests do not forget to change the path to your project.
If you want to change the port of your application just use the **--port** and there's others parameters for the uvicorn you can check on the documentation.
To be updated.....