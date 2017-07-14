from guizero import App, ButtonGroup, Combo, PushButton, Text, TextBox
from ModeRaspi import ModeRaspi
from ModeCloud import ModeCloud
from ModeBoth import ModeBoth

def find_license():
    lps = plate_textbox.get().upper().split(", ")
    if len(lps) == 1 and lps[0] == "": return
    alpr = None
    if mode_button.get() == "R":
        alpr = ModeRaspi(footage = (footage_button.get() == "F"))
        print("Raspberry Pi Mode")
    elif mode_button.get() == "C":
        alpr = ModeCloud(footage = (footage_button.get() == "F"))
        print("Cloud Mode")
    else:
        alpr = ModeBoth(footage = (footage_button.get() == "F"))
        print("Both Mode")
    alpr.add(lps)
    results = alpr.find()
    for lp in results:
        print("\nFound vehicle " + lp[0] + ", confidence = " + lp[1])

app = App(title = "AMBER")

app_message = Text(app, text = "AMBER License Plate Detection",\
size = 20, font = "Times New Roman")

mode_message = Text(app, text = "Computation Mode", size = 14,\
font = "Times New Roman")
mode_button = ButtonGroup(app, options=[["Raspberry Pi", "R"], ["Cloud", "C"],\
["Both", "B"]], selected = "R", horizontal = True, align = "left")

plate_message = Text(app, text = "License Plate Number", size = 14,\
font = "Times New Roman")
plate_textbox = TextBox(app)
footage_button = ButtonGroup(app, options=[["Camera", "C"], ["Footage", "F"]],\
selected = "C", horizontal = True, align = "left")
plate_button = PushButton(app, command = find_license, text = "Find Vehicle")

app.display()
