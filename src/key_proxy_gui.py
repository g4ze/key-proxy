import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.modalview import ModalView


class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MyBoxLayout, self).__init__(**kwargs)
        self.orientation = "vertical"

        # Widget for support link
        self.support_widget = Button(
            text="WELCOME! Reach developer by clicking here!",
            size_hint=(1, 0.1),
            background_color=(0.5, 0.5, 0.5, 1),
            color=(1, 1, 1, 1),
        )
        self.support_widget.bind(on_press=self.open_support_link)

        self.add_widget(self.support_widget)

        self.text_input = TextInput(
            hint_text="Paste your text here:",
            size_hint=(1, 0.8),
            background_color=(0, 0, 0, 1),
            foreground_color=(1, 1, 1, 1),
        )
        self.add_widget(self.text_input)
        self.countdown_input = TextInput(
            hint_text="Enter countdown duration (in seconds):",
            size_hint=(1, 0.1),
            background_color=(0, 0, 0, 1),
            foreground_color=(1, 1, 1, 1),
        )
        self.add_widget(self.countdown_input)

        self.button_execute = Button(
            text="Start", size_hint=(1, 0.1), background_color=(0, 2, 0, 2)
        )
        self.button_execute.bind(on_press=self.start_execution)
        self.add_widget(self.button_execute)

    def start_execution(self, instance):
        text = self.text_input.text
        if not self.countdown_input.text or not self.countdown_input.text.isdigit():
            self.countdown_input.text = "5"

        # Save the text to a file
        file_path = os.path.join(os.getcwd(), "output.txt")
        try:
            with open(file_path, "w") as file:
                file.write(text)
            print("Text saved to output.txt")
        except Exception as e:
            print(f"Error saving text to file: {e}")

        self.show_countdown()

    def show_countdown(self):
        self.countdown_view = ModalView(
            size_hint=(0.5, 0.3), size_hint_max_x=400, size_hint_max_y=100
        )
        self.countdown_label = Label(
            text=f"Starting in {int(self.countdown_input.text)}s", font_size=20
        )
        self.countdown_view.add_widget(self.countdown_label)
        self.countdown_view.open()

        # Schedule the update_countdown method after showing the countdown view
        Clock.schedule_interval(self.update_countdown, 1)

    def update_countdown(self, dt):
        countdown_value = int(
            self.countdown_label.text.split()[-1][0]
        )  # Extract the countdown value
        if countdown_value > 1:
            self.countdown_label.text = f"Starting in {countdown_value - 1}s"
        else:
            Clock.unschedule(self.update_countdown)
            self.countdown_view.dismiss()  # Close the countdown popup
            self.execute_script()

    def execute_script(self):
        print("Starting the script...")
        try:
            start = KeyProxy(
                file_path="output.txt", delay=int(self.countdown_input.text)
            )
            start.type_text_from_file()
            print("Script execution completed!")
            self.show_success_popup()
        except Exception as e:
            print(f"Error executing script: {e}")

    def show_success_popup(self):
        self.success_view = ModalView(
            size_hint=(0.7, 0.3), size_hint_max_x=400, size_hint_max_y=100
        )
        self.success_label = Label(text="Script execution completed!", font_size=20)
        self.success_view.add_widget(self.success_label)
        self.success_view.open()

    def open_support_link(self, instance):
        import webbrowser

        print("Opening support link...")
        webbrowser.open("https://github.com/g4ze/key-proxy")


class MyApp(App):
    def build(self):
        Window.size = (400, 300)
        self.title = "Key-Proxy"
        return MyBoxLayout()


import pyautogui
import time
import pyperclip


class KeyProxy:
    def __init__(self, file_path, delay=5):
        self.file_path = file_path
        self.delay = delay

    def type_text_from_file(self):

        with open(self.file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        print("reading file...")

        # Delay before starting typing
        time.sleep(self.delay)

        for line in lines:
            for char in line.strip():
                if char == "<":
                    # Use pyperclip to paste '<' symbol from the clipboard
                    pyperclip.copy("<")
                    pyautogui.hotkey("shift", ",")
                if char == "#":
                    # Use pyperclip to paste '#' symbol from the clipboard
                    pyperclip.copy("#")
                    pyautogui.hotkey("shift", "3")
                else:
                    pyautogui.write(char)

                time.sleep(0.1)  # Adjust this delay as needed

            pyautogui.press("enter")  # Press 'Enter' at the end of each line


if __name__ == "__main__":
    MyApp().run()
