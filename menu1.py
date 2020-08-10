from random import randint
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

form_data = {
    "TB": "Value1",
}


class myclass(Frame):
    def __init__(self, screen):
        super(myclass, self).__init__(
            screen,
            screen.height * 2 // 3,
            screen.width * 2 // 3,
            data=form_data,
            hover_focus=True,
            title="PROXIMITY",
        )
        layout = Layout([1, 1, 1])
        self.add_layout(layout)
        layout.add_widget(Button("Create server", self._createserver), 0)
        layout.add_widget(Button("Join server", self._view), 1)
        layout.add_widget(Button("Quit", self._quit), 2)
        self.fix()

    def _view(self):
        self.save()
        self._scene.add_effect(PopUpDialog(self._screen, "Hello", ["OK"]))

    def _createserver(self):
        self.save()
        os.system("python3 server.py")
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
            screen.height * 2 // 3,
            screen.width * 2 // 3,
            data=form_data,
            hover_focus=True,
            title="PROXIMITY",
        )
        layout = Layout([1, 1, 1])
        self.add_layout(layout)
        layout.add_widget(
            Text(label="Enter username", name="TB", on_change=self._on_change), 0
        )
        layout.add_widget(Button("View", self._view), 1)
        layout.add_widget(Button("Quit", self._quit), 2)
        self.fix()

    def _on_change(self):
        global form_data
        self.save()
        for key, value in self.data.items():
            form_data[key] = value

    def _view(self):
        global form_data
        self.save()
        message = "Hi , {}".format(form_data["TB"])
        self._scene.add_effect(PopUpDialog(self._screen, message, ["OK"]))

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
    ]
    screen.play(scenes, stop_on_resize=True)


Screen.wrapper(demo)

