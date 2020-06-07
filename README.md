# DerDieDas

## Building an application
I strongly recommend you to use virtual environment:
```
python3 -m venv path/to/dir
source path/to/dir/bin/activate
```
There is also a list of modules you need to run the app. Install them in your virtualenv.
```
pip install requests firebase python-firebase plyer docutils pygments  kivymd kivy3 kivy PyCryptodome requests_toolbelt sseclient gcloud python_jwt multiprocessing
```
Install PYInstaller and follow the instructions from the official docs. Small tipp: to build a 'closed compilation' exe-file delete the `COLL`-block from `derdiedas.spec`.
