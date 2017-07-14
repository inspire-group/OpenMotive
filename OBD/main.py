from guizero import App, ButtonGroup, PushButton, Text

def start():
    if mode_button.get() == 'A':
        print("\nStandard Mode")
        import ModeStandard
    else:
        print("\nSecure Mode")
        import ModeSecure

app = App(title = "OBD")

app_message = Text(app, text = "OBDII Secure and Private Connection",\
size = 20, font = "Times New Roman")
mode_message = Text(app, text = "Relay Mode", size = 14,\
font = "Times New Roman")
mode_button = ButtonGroup(app, options=[["Standard", "A"], ["Secure", "B"]],\
selected = "A", horizontal = True, align = "left")
start_button = PushButton(app, command = start, text = "Start")

app.display()
