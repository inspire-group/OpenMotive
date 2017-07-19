from guizero import App, ButtonGroup, PushButton, Text
import ModeSports, ModeEfficiency

def start():
    if mode_button.get() == 'A' and type_button.get() == 'A':
        print('\nSports Mode - Training')
    elif mode_button.get() == 'A' and type_button.get() == 'B':
        print('\nSports Mode - Testing')
    elif mode_button.get() == 'B' and type_button.get() == 'A':
        print('\nEfficiency Mode - Training')
    elif mode_button.get() == 'B' and type_button.get() == 'B':
        print('\nEfficiency Mode - Testing')

app = App(title = "Transmission")

app_message = Text(app, text = "Vehicle Transmission Sports and\
 Efficiency Application", size = 20, font = "Times New Roman")
mode_message = Text(app, text = "Mode", size = 14,\
font = "Times New Roman")
mode_button = ButtonGroup(app, options=[["Sports", "A"], ["Efficiency", "B"]],\
selected = "A", horizontal = True, align = "left")
type_message = Text(app, text = "Type", size = 14,\
font = "Times New Roman")
type_button = ButtonGroup(app, options=[["Train", "A"], ["Test", "B"]],\
selected = "A", horizontal = True, align = "left")
start_button = PushButton(app, command = start, text = "Start")

app.display()
