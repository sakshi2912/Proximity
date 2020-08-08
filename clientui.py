import urwid
import os

my_val = ''
def exit_on_q(key):
    global my_val
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()
    else:
        os.system(f"python3 client.py {my_val}")
        raise urwid.ExitMainLoop()

class QuestionBox(urwid.Filler):
    def keypress(self, size, key):
        global my_val
        if key != 'enter':
            return super(QuestionBox, self).keypress(size, key)
        self.original_widget = urwid.Text(
            u"Welcome to the server ,\n%s.\n\nPress Q to exit." %
            edit.edit_text)
        my_val = edit.edit_text


edit = urwid.Edit(u"Enter passkey\n")
fill = QuestionBox(edit)
loop = urwid.MainLoop(fill, unhandled_input=exit_on_q)
loop.run()