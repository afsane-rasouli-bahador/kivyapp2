import os
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton
from kivy.properties import StringProperty, NumericProperty
import datetime
from datetime import date
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.behaviors import CommonElevationBehavior
from models import User, Session, Task


os.system('clear')
Window.size = (350, 580)

class LoginScreen(Screen):
    pass

class SignupScreen(Screen):
    pass

class ForgetPasswordScreen(Screen):
    pass

class MyScreenManager(ScreenManager):
    pass

class TodoCard(CommonElevationBehavior, MDFloatLayout):
    title = StringProperty()
    description = StringProperty()
    task_id = NumericProperty()

class LoginPage(MDApp):
    current_user_id = None
    def build(self):
        self.session = Session()
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(Builder.load_file('pre-splash.kv'))
        self.screen_manager.add_widget(Builder.load_file('login.kv'))
        self.screen_manager.add_widget(Builder.load_file('signup.kv'))
        self.screen_manager.add_widget(Builder.load_file('forget_password.kv'))
        self.screen_manager.add_widget(Builder.load_file('todo.kv'))
        self.screen_manager.add_widget(Builder.load_file('AddTodo.kv'))
        return self.screen_manager
    
    def on_start(self):
        Clock.schedule_once(self.show_login, 5)

    def show_login(self, *args):
        self.screen_manager.current = 'login'

    def show_signup(self):
        self.screen_manager.current = 'signup'

    def show_forgetpass(self):
        self.screen_manager.current = 'forget_password'

    def show_todocard(self):
        self.screen_manager.current = 'todo'
        self.set_time_todo()

    def show_error(self, message):
        dialog = MDDialog(text=message, buttons=[MDRectangleFlatButton(text='OK', on_release=lambda _: dialog.dismiss())])
        dialog.open()


    def login(self, username, password):
        user = self.session.query(User).filter_by(username=username).first()
        if user and user.check_password(password):
            self.current_user_id = user.id
            print("Login successful")
            self.load_user_tasks(user.id)
            self.show_todocard()
            
        else:
            print("Login failed: Incorrect username or password")
            self.show_error("Incorrect username or password")


    def load_user_tasks(self, user_id):
        tasks = self.session.query(Task).filter_by(user_id=user_id).all()
        for task in tasks:
            task_card = TodoCard(task_id=str(task.id), title=task.title, description=task.description)
            if task.is_completed:
                task_card.ids.description_text.text = f'[s]{task.description}[/s]'
                task_card.ids.bar.md_bg_color = (0, 179/255, 0, 1)
            else:
                task_card.ids.description_text.text = task.description
                task_card.ids.bar.md_bg_color = (226/255, 0, 48/255, 1)
            self.root.get_screen('todo').todo_list.add_widget(task_card)



    def signup(self, username, password, email=None, phone=None):
        if not username or not password:
            self.show_error("Username and password are required")
            return
        user = User(username=username, email=email, phone=phone)
        user.set_password(password)
        self.session.add(user)
        try:
            self.session.commit()
            print("Signup successful")
            # Optionally switch to the login screen
            self.show_login()
        except Exception as e:
            self.session.rollback()
            print(f"Signup failed: {str(e)}")
            self.show_error("Signup failed: Username may already exist")


    def check_username(self, username):
        user = self.session.query(User).filter_by(username=username).first()
        if user:
            self.screen_manager.current = 'forget_password'
        else:
            self.show_error("Username not found")

    def reset_password(self, new_password, confirm_password):
        if new_password != confirm_password:
            self.show_error("Passwords do not match")
            return
        user = self.session.query(User).filter_by(username=self.current_username).first()
        if user:
            user.set_password(new_password)
            self.session.commit()
            self.show_login()
            self.show_error("Password reset successful")
        else:
            self.show_error("User not found")
    
    def set_time_todo(self):
        today = date.today()
        wd = date.weekday(today)
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        year = str(datetime.datetime.now().year)
        month = str(datetime.datetime.now().strftime('%b'))
        day = str(datetime.datetime.now().strftime('%d'))
        self.root.get_screen('todo').ids.date.text = f'{days[wd]}, {day} {month} {year}'

    def add_todo(self, title, description, user_id):
        if not title or not description:
            self.show_error("Title and description are required")
            return
        if len(title) > 20:
            self.show_error("Title length should be <= 20")
            return
        if len(description) > 60:
            self.show_error("Description length should be <= 60")
            return
        if self.current_user_id is None:
            self.show_error("No user is currently logged in.")
            return
    
        new_task = Task(title=title, description=description, user_id=user_id)
        self.session.add(new_task)
        self.session.commit()

        new_card = TodoCard(task_id=new_task.id, title=title, description=description)
        new_card.ids.checkbox.bind(active=lambda instance, value: self.on_complete(new_task.id, value, new_card.ids.description_text, new_card.ids.bar))
        try:
            self.root.get_screen('todo').todo_list.add_widget(new_card)
            self.root.get_screen('add_todo').ids.title.text = ''
            self.root.get_screen('add_todo').ids.description.text = ''
        except Exception as e:
            self.session.rollback()
            error_message = f"Failed to add task: {str(e)}"
            print(error_message)
            self.show_error(error_message)



    def on_complete(self, task_id, value, description_widget, bar):
        task = self.session.query(Task).filter_by(id=task_id).first()
        if task:
            task.is_completed = value
            try:
                self.session.commit()
                print(f"Task {task_id} completion status updated to {value}.")

                # Updating UI based on the completion status
                if value:
                    if '[s]' not in description_widget.text:
                        description_widget.text = f'[s]{description_widget.text}[/s]'
                    bar.md_bg_color = (0, 179/255, 0, 1)  # Green for completed
                else:
                    description_widget.text = description_widget.text.replace('[s]', '').replace('[/s]', '')
                    bar.md_bg_color = (226/255, 0, 48/255, 1)  # Red for not completed

            except Exception as e:
                self.session.rollback()
                self.show_error(f"Failed to update task status due to: {str(e)}")  # Using a generic error display method
        else:
            print(f"Task with ID {task_id} not found.")
            self.show_error(f"Task with ID {task_id} not found.")

if __name__ == '__main__':
    LoginPage().run()
