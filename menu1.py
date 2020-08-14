from asciimatics.screen import Screen
from asciimatics.widgets import (
    Frame,
    ListBox,
    Layout,
    Divider,
    Text,
    Button,
    TextBox,
    Widget,
    PopUpDialog,
)
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
import os
import subprocess
import socket
import threading
import os
import signal
from sys import platform
import base64

form_data = {"username": "", "passkey": ""}


class myclass(Frame):
    def __init__(self, screen):
        super(myclass, self).__init__(
            screen,
            screen.height * 3 // 4,
            screen.width * 3 // 4,
            data=form_data,
            hover_focus=True,
            title="PROXIMITY",
        )
        layout = Layout([1, 1, 1])
        self.add_layout(layout)
        layout.add_widget(Button("Create server", self._createserver), 0)
        layout.add_widget(Button("Join server", self._joinserver), 1)
        layout.add_widget(Button("Quit", self._quit), 2)
        self.fix()

    def _joinserver(self):
        self.save()
        raise NextScene("menu3")

    def _createserver(self):
        self.save()
        raise NextScene("menu2")

    def _quit(self):
        self._scene.add_effect(
            PopUpDialog(
                self._screen, "Are you sure?", ["Yes", "No"], on_close=self._quit_on_yes
            )
        )

    @staticmethod
    def _quit_on_yes(selected):
        # Yes is the first button
        if selected == 0:
            raise StopApplication("User requested exit")


class myclass2(Frame):
    def __init__(self, screen):
        super(myclass2, self).__init__(
            screen,
            screen.height * 3 // 4,
            screen.width * 3 // 4,
            data=form_data,
            hover_focus=True,
            title="PROXIMITY",
        )
        layout = Layout([1, 1, 1])
        self.add_layout(layout)
        layout.add_widget(
            Text(label="Username", name="username", on_change=self._on_change), 0
        )
        layout.add_widget(Button("Enter", self._enter), 1)
        layout.add_widget(Button("Quit", self._quit), 2)
        self.fix()

    def _on_change(self):
        global form_data
        self.save()
        value = self.data["username"]
        form_data["username"] = value

    def _view(self):
        global form_data
        self.save()
        message = "Hi , {}".format(form_data["username"])
        self._scene.add_effect(PopUpDialog(self._screen, message, ["OK"]))

    def _enter(self):

        if platform == "linux" or platform == "linux2":
            subprocess.call(
                ["gnome-terminal", "-x", f'python server.py {self.data["username"]}']
            )
        if platform == "win32":
            subprocess.call(
                f"start /wait python server.py {self.data['username']}", shell=True
            )
        else:
            os._exit(1)
        raise StopApplication("Exit this")

    def _quit(self):
        self._scene.add_effect(
            PopUpDialog(
                self._screen, "Are you sure?", ["Yes", "No"], on_close=self._quit_on_yes
            )
        )

    @staticmethod
    def _quit_on_yes(selected):

        if selected == 0:
            raise StopApplication("User requested exit")


class myclass3(Frame):
    def __init__(self, screen):
        super(myclass3, self).__init__(
            screen,
            screen.height * 3 // 4,
            screen.width * 3 // 4,
            data=form_data,
            hover_focus=True,
            title="PROXIMITY",
        )
        layout = Layout([1, 1, 1])
        self.add_layout(layout)
        layout.add_widget(
            Text(label="Passkey", name="passkey", on_change=self._on_change), 0,
        )
        layout.add_widget(Button("View", self._view), 1)
        layout.add_widget(Button("Quit", self._quit), 2)
        self.fix()

    def _on_change(self):
        global form_data
        self.save()
        value = self.data["passkey"]
        form_data["passkey"] = value

    def _view(self):
        global form_data
        self.save()

        if platform == "linux" or platform == "linux2":
            subprocess.call(
                ["gnome-terminal", "-x", f'python client.py {self.data["passkey"]}']
            )
        if platform == "win32":
            subprocess.call(
                f"start /wait python client.py {self.data['passkey']}", shell=True
            )
        else:
            os._exit(1)
        raise StopApplication("Exit this")

    def _quit(self):
        self._scene.add_effect(
            PopUpDialog(
                self._screen, "Are you sure?", ["Yes", "No"], on_close=self._quit_on_yes
            )
        )

    @staticmethod
    def _quit_on_yes(selected):
        # Yes is the first button
        if selected == 0:
            raise StopApplication("User requested exit")


def demo(screen):

    scenes = [
        Scene([myclass(screen)], -1, name="menu1"),
        Scene([myclass2(screen)], -1, name="menu2"),
        Scene([myclass3(screen)], -1, name="menu3"),
    ]
    screen.play(scenes, stop_on_resize=True)


Screen.wrapper(demo)

