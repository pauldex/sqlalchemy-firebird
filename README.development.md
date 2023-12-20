# Development notes

Support for 32/64 bit Python 2.7, 3.6+ on Windows/Linux/Mac.

* Use `firebird-driver` and/or `fdb`
    * Python >= 3.8
    * SQLAlchemy 1.4 or 2.0

* Use `fdb`
    * Python == 3.7 and SQLAlchemy 2.0
    * Python >= 3.6 and SQLAlchemy 1.4


# Windows environment


## Install Python

You may install Python with [Chocolatey](https://chocolatey.org/install):

```powershell
choco install python -y
```


## Install Visual Studio Code

We strongly recommend Visual Studio Code for development. You may install it with:

```powershell
choco install vscode -y
```


## Initial checkout

Clone this repository into a local folder on your computer and, from the root folder, run 

```
python -m venv .venv
.venv/Scripts/activate
pip install .[dev]
pip install fdb
```

This will create a Python virtual environment on `.venv` subfolder and install all required components.

Open the project folder with VSCode. It should detect the virtual environment automatically and use it. Please refer to [Visual Studio Code documentation on Python](https://code.visualstudio.com/docs/languages/python) for more information.


## Prepare the test infrastructure

Run the following Powershell script

```
.\rebuild-test-environment.ps1
```

This will create a `sqlalchemy-firebird-tests` under your `$env:TEMP` folder containing:
  - The binaries for each supported Firebird version
  - An empty database for each Firebird version

The script also adds a `[db]` section to your `setup.cfg` file like the following:

```ini
[db]
default = firebird+firebird://SYSDBA@/<temp>\sqlalchemy-firebird-tests\FIREBIRD.FB50.FDB?charset=UTF8&fb_client_library=<temp>\sqlalchemy-firebird-tests\fb50\fbclient.dll

firebird_fb50 = firebird+firebird://SYSDBA@/<temp>\sqlalchemy-firebird-tests\FIREBIRD.FB50.FDB?charset=UTF8&fb_client_library=<temp>\sqlalchemy-firebird-tests\fb50\fbclient.dll
firebird_fb40 = firebird+firebird://SYSDBA@/<temp>\sqlalchemy-firebird-tests\FIREBIRD.FB40.FDB?charset=UTF8&fb_client_library=<temp>\sqlalchemy-firebird-tests\fb40\fbclient.dll
firebird_fb30 = firebird+firebird://SYSDBA@/<temp>\sqlalchemy-firebird-tests\FIREBIRD.FB30.FDB?charset=UTF8&fb_client_library=<temp>\sqlalchemy-firebird-tests\fb30\fbclient.dll

fdb_fb30 = firebird+fdb://SYSDBA@/<temp>\sqlalchemy-firebird-tests\FDB.FB30.FDB?charset=UTF8&fb_library_name=<temp>\sqlalchemy-firebird-tests\fb30\fbclient.dll
fdb_fb25 = firebird+fdb://SYSDBA@/<temp>\sqlalchemy-firebird-tests\FDB.FB25.FDB?charset=UTF8&fb_library_name=<temp>\sqlalchemy-firebird-tests\fb25\fbclient.dll
```


## Running the tests

Run the following Powershell script

```
.\run-all-tests.ps1
```

This will start 5 different processes, each one running a different combination of driver/Firebird version supported.



## Debugging the tests

SQLAlchemy has a complex test infrastructure which unfortunately is not completely functional from VSCode test runner.

To run a specific test under VSCode debugger this repository already provides a `.vscode/launch.json` file preconfigured.

E.g. to run the test `test_get_table_names` with `firebird-driver` and Firebird 5.0 you must set `pytest` arguments as:

```json
"args": ["./test/test_suite.py::NormalizedNameTest", "-k", "test_get_table_names", "--db", "firebird_fb50"],
```

Now run the code (`F5`) and the debugger should work as expected (e.g. set a breakpoint and it should stop).

Comments: 

- Running the script `.\run-tests.ps1` will run the tests specified in `launch.json` out of VSCode.

- Use `.\run-tests.ps1 -All` to run all tests for the currently configured `--db` in in `launch.json`.
  - Or `.\run-tests.ps1 -All -Db <db>` to override the database in `launch.json`.


## Debugging SQLAlchemy code

Sooner or later you probably will need to debug SQLAlchemy code. Fortunately, this is easy as

```powershell
$sqlAlchemyFolder = '/temp/sqlalchemy'    # Replace with your desired location for SQLAlchemy repository

# Clone SQLAlchemy repository
git clone https://github.com/sqlalchemy/sqlalchemy.git $sqlAlchemyFolder

# [From your 'sqlalchemy-firebird' root folder, inside virtual environment]
pip install -e $sqlAlchemyFolder
```

The `launch.json` file already has the required `"justMyCode": false` configuration which allows you to step into SQLAlchemy source files during debugging.
