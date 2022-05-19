from pathlib import Path
from tkinter import *
from tkinter import messagebox
import yaml



NAVY  = '#0A043C'
WHITE = '#FFFFFF'
BLACK = '#000000'
GREEN = '#00FF00'

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class Login():
    def __init__(self):
        self.window = Tk()
        self.window.title("Password Generator & App Management (Team 9)")

        self.window.geometry("563x457")
        self.window.configure(bg = NAVY)

    def login(self):
        user_email = self.email_entry.get().strip()
        if user_email:
            try:
                with open("data.yaml", "r") as data_file:
                    data = yaml.safe_load(data_file)
                    user_data = []
                    for website in data.keys():
                        if data[website]['email'] == user_email:
                            data[website]['website'] = website
                            user_data.append(data[website])

                if user_data:
                    from manager import ManagerUI
                    self.destroy()
                    ManagerUI(user_data).render()
                else:
                    messagebox.showerror(
                        title = "Error",
                        message = "Email not found"
                        )
            except FileNotFoundError:
                messagebox.showwarning(
                title='Oops',
                message="No User found. First create password using password generator."
            )
            except Exception as e:
                print(e)
        else:
            messagebox.showwarning(
                title='Oops',
                message="Please Enter Your Email Address"
            )

    def main_menu(self):
        from main import MainMenu
        self.destroy()
        MainMenu().render()


    def render(self):
        canvas = Canvas( self.window, bg = NAVY, height = 457, width = 563, bd = 0, highlightthickness = 0, relief = "ridge")

        canvas.place(x = 0, y = 0)
        login_button_image = PhotoImage(file=relative_to_assets("login_button.png"))

        login_button = Button(
            image=login_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.login,
            relief="flat"
        )
        login_button.place( x=300.0, y=373.0, width=155.0, height=30.0)

        menu_image = PhotoImage(file=relative_to_assets("menu_button.png"))
        menu_button = Button(
            image=menu_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.main_menu,
            relief="flat"
        )
        menu_button.place( x=100.0, y=373.0, width=155.0, height=30.0)

        email_field_image = PhotoImage(file=relative_to_assets("email_field.png"))
        email_field_label = Label(
            image=email_field_image,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        email_field_label.place( x=72.0, y=318.0, width=419.0, height=46.0)

        self.email_entry = Entry(
            bd=0,
            bg=WHITE,
            highlightthickness=0,
            font=("Arial", 20),
        )

        self.email_entry.place( x=140.0, y=325.0, width=328.0, height=26.0 )
        self.email_entry.insert(0, 'Team9_email@gmail.com')
        self.window.resizable(False, False)
        self.window.mainloop()


    def destroy(self):
        self.window.destroy()


if __name__ == "__main__":
    Login().render()
