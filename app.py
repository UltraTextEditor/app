from application.application import Application
import sys, os

app = Application("Slime", show_tabs=False)
app.get_entry()["borderwidth"] = 0
app.get_entry()["highlightthickness"] = 0
app.run()