import os
import time
import json
import random
import pathlib
import requests
import threading
from typing import Tuple
from datetime import datetime
from multiprocessing import freeze_support

from firebase import firebase
from plyer import uniqueid
from plyer.utils import platform


from kivy.clock import Clock, mainthread
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout

from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDRoundFlatButton




COLORS_DARK = {
    "der": (0, 0, 1, 1),
    "die": (1, 0, 0, 1),
    "das": (0, 1, 0, 1),
    "base": (1, 1, 1, 1),
}

COLORS_LIGHT = {
    "der": (0, 0, 1, 1),
    "die": (1, 0, 0, 1),
    "das": (0, 1, 0, 1),
    "base": (0, 0, 0, 1),
}


class MainScreen(GridLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.firebase = firebase.FirebaseApplication('https://derdiedas-17e3e.firebaseio.com/', None)
        self._errors_file = pathlib.Path.home() / pathlib.Path(".derdiedas/errors.json")
        self._substantive_file = pathlib.Path.cwd() / pathlib.Path("substantive.json")
        self._user_id = uniqueid.id
        self.color_table = COLORS_DARK
        self._build_layout()

    def _build_layout(self):
        self.rows = 4
        self.padding = 20

        self.start_button = MDRaisedButton(
            size_hint=(0.5, 1.0),
            font_size=50,
            text="Start"
        )

        self.start_button.bind(on_press=self.on_start)
        self.add_widget(self.start_button)

        self.word_label = MDLabel(
            text="H",
            font_style="H3",
            theme_text_color="Primary",
            halign="center"
        )

        self.answers_layout = FloatLayout()
        self.der_button = MDRoundFlatButton(
            size_hint=(0.2, 0.3),
            pos_hint={"x": 0.1, "y": 0.25},
            text_color=self.color_table["der"],
            text="der",
            font_size=30,
        )
        self.der_button.bind(on_press=self.on_answer)

        self.die_button = MDRoundFlatButton(
            size_hint=(0.2, 0.3),
            pos_hint={"center_x": 0.5, "y": 0.25},
            text_color=self.color_table["die"],
            text="die",
            font_size=30,
        )
        self.die_button.bind(on_press=self.on_answer)

        self.das_button = MDRoundFlatButton(
            size_hint=(0.2, 0.3),
            pos_hint={"x": 0.7, "y": 0.25},
            text_color=self.color_table["das"],
            text="das",
            font_size=30,
        )
        self.das_button.bind(on_press=self.on_answer)

        self.answers_layout.add_widget(self.der_button)
        self.answers_layout.add_widget(self.die_button)
        self.answers_layout.add_widget(self.das_button)

    def _get_word(self) -> Tuple[str, str]:
        return random.sample(self._words.items(), 1)[0]

    def _save_error(self, error: str):
        if not self._errors_file.exists():
            errors = {}
        else:
            with self._errors_file.open("r") as f:
                errors = json.load(f)

        with self._errors_file.open("w") as f:
            errors[error] = errors.get(error, 0) + 1
            json.dump(errors, f, indent=4)

    def _push_errors(self):
        if not self._errors_file.exists():
            errors = {}
            self._errors_file.parent.mkdir(exist_ok=True, parents=True)
        else:
            with self._errors_file.open("r") as f:
                errors = json.load(f)
        
        self.firebase.put(f"/users/{self._user_id}", "errors", errors)

    @mainthread
    def _next_word(self):
        self.word_label.color = self.color_table["base"]
        word, art = self._get_word()

        self.word_label.text = word
        self.right_art = art

    @mainthread
    def on_start(self, button):
        self.remove_widget(button)
        self.add_widget(self.word_label)
        threading.Thread(target=self._load_data).start()

    def _load_data(self):
        self.word_label.text = "Loading..."
        try:
            self._words = self.firebase.get("/substantive/", None)
            self.firebase.put(f"/users/{self._user_id}", "session", datetime.utcnow())
        except  requests.exceptions.RequestException as e:
            with self._substantive_file.open("r") as f:
                self._words = json.loads(f.read())
        else:
            self._push_errors()

        self._after_load()

    @mainthread
    def _after_load(self):
        self.add_widget(self.answers_layout)
        self.word_label.text, self.right_art = self._get_word()

    @mainthread
    def on_answer(self, button):
        self.word_label.color = self.color_table[self.right_art.lower()]

        if button.text.lower() != self.right_art.lower():
            toast(self.right_art.upper())
            self._save_error(self.word_label.text)
        else:
            self._next_word()


class DerDieDasApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        return MainScreen()


if __name__ == "__main__":
    freeze_support()
    DerDieDasApp().run()
