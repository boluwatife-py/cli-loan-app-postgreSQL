from asciimatics.widgets import Frame, ListBox, Layout, Divider, Text, Button, TextBox, Widget, Label, PopUpDialog
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
import sys
import fn
    

class LoanAppUI(Frame):
    def __init__(self, screen):
        super(LoanAppUI, self).__init__(screen,
                                       screen.height * 2 // 3,
                                       screen.width * 2 // 3,
                                       title="Loan App",
                                       hover_focus=True,
                                       can_scroll=False)
        
        layout = Layout([1], fill_frame=True)
        self.add_layout(layout)
        
        
        layout.add_widget(Text("Email or Phone:", "identifier"))
        layout.add_widget(Text("Pin (4 digits):", "pin"))
        self.error_label = Label("")
        layout.add_widget(self.error_label)
        layout.add_widget(Button("Login", self._login))
        layout.add_widget(Divider())
        
        layout2 = Layout([1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Sign Up", self._signup), 0)
        layout2.add_widget(Button("Admin", self._admin), 1)
        layout2.add_widget(Button("Quit", self._quit), 2)
        
        self.fix()

    def _login(self):
        self.save()
        identifier = self.data.get("identifier", "").strip()
        pin = self.data.get("pin", "").strip()
        
        if fn.is_valid_email(identifier):
            identiifier_type = 'email'
        elif fn.is_valid_phone_number(identifier):
            identiifier_type = 'phone-number'

    def _signup(self):
        # Logic for signup
        self.save()
        # Transition to the signup screen
        raise NextScene("Sign Up")

    def _admin(self):
        # Logic for admin access
        self.save()
        # Transition to the admin dashboard
        raise NextScene("Admin Dashboard")

    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")


class LoanDashboard(Frame):
    def __init__(self, screen):
        super(LoanDashboard, self).__init__(screen,
                                          screen.height * 2 // 3,
                                          screen.width * 2 // 3,
                                          title="Loan Dashboard",
                                          hover_focus=True,
                                          can_scroll=False)
        # Add loan dashboard content
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        
        layout.add_widget(Text("Welcome to your Loan Dashboard", "welcome"))
        layout.add_widget(Divider())
        
        layout2 = Layout([1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Apply for Loan", self._apply_loan), 0)
        layout2.add_widget(Button("Logout", self._logout), 1)
        
        self.fix()

    def _apply_loan(self):
        # Logic for loan application
        pass

    def _logout(self):
        # Logic for logging out
        raise NextScene("Login")

class SignUp(Frame):
    def __init__(self, screen):
        super(SignUp, self).__init__(screen,
                                     screen.height * 2 // 3,
                                     screen.width * 2 // 3,
                                     title="Sign Up",
                                     hover_focus=True,
                                     can_scroll=False)
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        
        layout.add_widget(Text("Email or Phone:", "email_or_phone"))
        layout.add_widget(Text("Password:", "password"))
        layout.add_widget(Divider())
        
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Sign Up", self._sign_up), 0)
        layout2.add_widget(Button("Cancel", self._cancel), 3)
        
        self.fix()

    def _sign_up(self):
        # Logic for signing up a user
        pass

    def _cancel(self):
        raise NextScene("Login")

class AdminDashboard(Frame):
    def __init__(self, screen):
        super(AdminDashboard, self).__init__(screen,
                                            screen.height * 2 // 3,
                                            screen.width * 2 // 3,
                                            title="Admin Dashboard",
                                            hover_focus=True,
                                            can_scroll=False)
        # Add admin dashboard content
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        
        layout.add_widget(Text("Admin Control Panel", "admin_panel"))
        layout.add_widget(Divider())
        
        layout2 = Layout([1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("View Users", self._view_users), 0)
        layout2.add_widget(Button("Logout", self._logout), 1)
        
        self.fix()

    def _view_users(self):
        # Logic for viewing users
        pass

    def _logout(self):
        raise NextScene("Login")

def demo(screen, scene):
    scenes = [
        Scene([LoanAppUI(screen)], -1, name="Login"),
        Scene([LoanDashboard(screen)], -1, name="Loan Dashboard"),
        Scene([SignUp(screen)], -1, name="Sign Up"),
        Scene([AdminDashboard(screen)], -1, name="Admin Dashboard")
    ]
    
    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)

last_scene = None
while True:
    try:
        Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene
