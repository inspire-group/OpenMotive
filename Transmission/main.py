from guizero import App, ButtonGroup, PushButton, Text

def start():
    if mode_button.get() == 'A':
        print("\Sports Mode")
        import ModeSports
    else:
        print("\Efficiency Mode")
        import ModeEfficiency

app = App(title = "Transmission")

app_message = Text(app, text = "Vehicle Transmission Sports and\
 Efficiency Application", size = 20, font = "Times New Roman")
mode_message = Text(app, text = "Mode", size = 14,\
font = "Times New Roman")
mode_button = ButtonGroup(app, options=[["Sports", "A"], ["Efficiency", "B"]],\
selected = "A", horizontal = True, align = "left")
start_button = PushButton(app, command = start, text = "Start")

app.display()
