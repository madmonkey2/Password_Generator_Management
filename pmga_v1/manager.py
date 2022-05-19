from pathlib import Path
from tkinter import *
from tkinter import messagebox

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class DetailRow():
    def __init__(self, parent, canvas, y, site, password, email):
        self.parent = parent
        self.site = StringVar()
        self.site.set(site)
        self.password = StringVar()
        self.password.set("*" * 8)
        self.hide = True
        self.email = email

        self.site_label = Label(canvas, fg="#000000", bg="#FFFFFF", width=20, height=1, textvariable=self.site)
        self.site_label.place(x=39.0, y=y)

        self.password_label = Label(canvas, fg="#000000", bg="#FFFFFF", width=18, height=1, textvariable=self.password)
        self.password_label.place(x=230.0, y=y)

        self.unhide_image = PhotoImage(file=relative_to_assets("unhide.png"))
        self.unhide_button = Button(
            image=self.unhide_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.unhide(password),
            relief="flat"
        )
        self.unhide_button.place(x=405.0, y=y, width=30.0, height=23.0)

        self.clipboard_image = PhotoImage(file=relative_to_assets("clipboard.png"))
        self.clipboard_button = Button(
            image=self.clipboard_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.clipboard(password),
            relief="flat"
        )
        self.clipboard_button.place(x=440.0, y=y, width=30.0, height=23.0)

        self.update_image = PhotoImage(file=relative_to_assets("update.png"))
        self.update_button = Button(
            image=self.update_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.update,
            relief="flat"
        )
        self.update_button.place(x=475.0, y=y, width=30.0, height=23.0)

        self.delete_image = PhotoImage(file=relative_to_assets("delete.png"))
        self.delete_button = Button(
            image=self.delete_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.delete,
            relief="flat"
        )
        self.delete_button.place(x=510.0, y=y, width=30.0, height=23.0)

    def clipboard(self, password):
        import pyperclip
        pyperclip.copy(password.decode())
        messagebox.showwarning(
            title="Copied to Clipboard",
            message="Password copied to clipboard!"
        )

    def unhide(self, password):
        if self.hide:
            self.password.set(password.decode("utf-8"))
            self.hide = False
        else:
            self.password.set("*" * 8)
            self.hide = True
        self.password_label.update()

    def update(self):
        from generator import PasswordGeneratorUI
        self.parent.destroy()
        PasswordGeneratorUI(self.email, self.site.get()).render()

    def delete(self):
        confirm = messagebox.askyesno(
            title="Password Delete",
            message=f"Are you sure you want to delete Password for {self.site.get()}"
        )
        if confirm:
            import yaml
            new_data = {}
            with open('data.yaml', 'r') as data_file:
                data = yaml.safe_load(data_file)
                for site, data in data.items():
                    if site != self.site.get() or data['email'] != self.email:
                        new_data.update({
                            site: {
                                'email': data['email'],
                                'password': data['password']
                            }
                        })
            with open('data.yaml', 'w') as data_file:
                yaml.safe_dump(new_data, data_file, indent=4)

            from login import Login
            self.parent.destroy()
            Login().render()


class ManagerUI():
    def __init__(self, data):
        self.window = Tk()
        self.window.title("Password Generator & App Management (Team 9)")

        self.window.geometry("563x457")
        self.window.configure(bg="#0A043C")

        self.data = data
        self.email = StringVar()
        self.email.set(self.data[0]["email"])

    def main_menu(self):
        from main import MainMenu
        self.destroy()
        MainMenu().render()

    def render(self):
        canvas = Canvas(
            self.window,
            bg="#0A043C",
            height=457,
            width=563,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        canvas.place(x=0, y=0)

        email = Label(canvas, fg="#000000", bg="#FFFFFF", width=55, height=1, textvariable=self.email)
        email.place(x=40.0, y=22.0)

        height = 104
        for details in self.data:
            DetailRow(self, canvas, height, details['website'], details['password'], details['email'])
            height += 30

        menu_image = PhotoImage(file=relative_to_assets("menu_button.png"))
        menu_button = Button(
            image=menu_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.main_menu,
            relief="flat"
        )
        menu_button.place(x=204.0, y=400.0, width=155.0, height=30.0)

        self.window.resizable(False, False)
        self.window.mainloop()

    def destroy(self):
        self.window.destroy()


if __name__ == "__main__":
    ManagerUI([{'email': 'Team9_email@gmail.com', 'password': b'6Xlq6$jt', 'website': 'abc.com'},
               {'email': 'Team9_email@gmail.com', 'password': b'uzU6!5(el', 'website': 'lmn.com'},
               {'email': 'Team9_email@gmail.com', 'password': b'ef70e*yl', 'website': 'xyz.com'}]).render()
