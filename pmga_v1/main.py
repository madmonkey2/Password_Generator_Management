from pathlib import Path
from tkinter import *


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

NAVY  = '#0A043C'
WHITE = '#FFFFFF'
BLACK = '#000000'
GREEN = '#00FF00'

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class MainMenu():
    def __init__(self):
        self.window = Tk()
        self.window.title("Password Generator & App Management (Team 9)")
        icon = PhotoImage(file='icon_logo.png')
        self.window.iconphoto(True, icon)
        self.window.geometry("563x457")
        self.window.config(bg=NAVY)

    def callGenerator(self):
        from generator import PasswordGeneratorUI
        self.destroy()
        PasswordGeneratorUI().render()

    def callManager(self):
        from login import Login
        self.destroy()
        Login().render()

    def render(self):
        canvas = Canvas(self.window, bg = NAVY, height = 457, width = 563, bd = 0, highlightthickness = 0, relief = "ridge")

        canvas.place(x = 0, y = 0)
        self.generator_image = PhotoImage(file=relative_to_assets("generator.png"))

        generator_button = Button(
            image=self.generator_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.callGenerator,
            relief="flat"
        )
        generator_button.place( x=122.0, y=356.0, width=319.0, height=30.0)

        self.manager_image = PhotoImage(file=relative_to_assets("manager.png"))

        manager_button = Button(
            image=self.manager_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.callManager,
            relief="flat"
        )
        manager_button.place( x=122.0, y=297.0, width=319.0, height=30.0)

        self.window.resizable(False, False)
        self.window.mainloop()

    def destroy(self):
        self.window.destroy()


if __name__ == "__main__":
    MainMenu().render()
