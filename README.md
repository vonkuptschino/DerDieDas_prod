# DerDieDas

## Building an application
I strongly recommend you to use virtual environment: 
```
python3 -m venv path/to/dir
source path/to/dir/bin/activate
```

There is also a list of modules you need to run the app.

```
pip install requests firebase python-firebase plyer docutils pygments  kivymd kivy3 kivy PyCryptodome requests_toolbelt sseclient gcloud python_jwt
```

Before building the application please install all the necessary libs and tools:
```
brew install --build-bottle sdl2 sdl2_image sdl2_ttf sdl2_mixer

pip install -U pyinstaller
```

Then just follow the instructions that are given in official docs. The spec-file is already corrected.
