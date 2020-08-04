import urwid
import os 
from pyfiglet import figlet_format
import pyfiglet

choices = ["Create Server","Join Server"]

def menu(title, choices):
    body = [urwid.Text(title), urwid.Divider()]
    for c in choices:
        button = urwid.Button(c)
        urwid.connect_signal(button, 'click', item_chosen, c)
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def item_chosen(button, choice):
    
    done = urwid.Button(u'Ok')
    if choice == 'Create Server':
        response = urwid.Text([u'Creating Server ', u'\n'])
        my_name = urwid.Edit('Enter a username \n')

        urwid.connect_signal(done, 'click', start_server)

    else:
        response = urwid.Text([u'Joining Server ', u'\n'])
        urwid.connect_signal(done, 'click', join_server)
    main.original_widget = urwid.Filler(urwid.Pile([response,urwid.AttrMap(done, None, focus_map='reversed')]))

def start_server(button):
    os.system("python3 server.py")

def join_server(button):
    os.system("python3 client.py")


welcomeText = pyfiglet.figlet_format('Proximity')
txt = urwid.Text(welcomeText,'center')
fill = urwid.Filler(txt, 'top')
main = urwid.Padding(menu(u'Menu', choices), left=2, right=2)
top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
    align='center', width=('relative', 60),
    valign='middle', height=('relative', 60),
    min_width=20, min_height=9)
top2 = urwid.Pile([fill,top])
urwid.MainLoop(top2, palette=[('reversed', 'standout', '')]).run()
#loop = urwid.MainLoop(fill)
#loop.run()