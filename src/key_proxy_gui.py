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
    stop_key = "ctrl+alt+x"
    start_key = "ctrl+alt+s"
    def __init__(self, **kwargs):
        super(MyBoxLayout, self).__init__(**kwargs)
        self.orientation = "horizontal"
        self.size = (800, 600)  # Set a fixed size for the layout

        # Left box for text input
        left_box = BoxLayout(orientation="vertical", size_hint_x=0.5, size=(400, 600))

        self.text_input = TextInput(
            hint_text="Paste your text here:",
            size_hint_y=0.8,
            background_color=(0, 0, 0, 1),
            foreground_color=(1, 1, 1, 1),
        )
        left_box.add_widget(self.text_input)

        self.add_widget(left_box)

        # Right box for buttons
        right_box = BoxLayout(orientation="vertical", size_hint_x=0.5, size=(400, 600))

        # Widget for support link
        self.support_widget = Button(
            text="WELCOME! Reach developer by clicking here!",
            size_hint_y=None, height=100,
            background_color=(0.5, 0.5, 0.5, 1),
            color=(1, 1, 1, 1),
        )
        self.support_widget.bind(on_press=self.open_support_link)
        right_box.add_widget(self.support_widget)

        # Duration input box
        duration_input_box = BoxLayout(orientation="horizontal", size_hint_y=None, height=50)
        duration_label = Label(text="duration:", color=(1, 1, 1, 1), size_hint_x=None, width=150)
        self.countdown_input = TextInput(
            hint_text="Enter countdown duration (in seconds):",
            text="5",
            background_color=(0, 0, 0, 1),
            foreground_color=(1, 1, 1, 1),
        )
        duration_input_box.add_widget(duration_label)
        duration_input_box.add_widget(self.countdown_input)
        right_box.add_widget(duration_input_box)

        # Hot-key-start input box
        hotkey_input_box = BoxLayout(orientation="horizontal", size_hint_y=None, height=50)
        hotkey_label = Label(text="hot-key to start:", color=(1, 1, 1, 1), size_hint_x=None, width=150)
        self.hotkey_input = TextInput(
            hint_text="Enter hot-key to stop countdown",
            text="ctrl+alt+s",
            background_color=(0, 0, 0, 1),
            foreground_color=(1, 1, 1, 1),
        )
        hotkey_input_box.add_widget(hotkey_label)
        hotkey_input_box.add_widget(self.hotkey_input)
        right_box.add_widget(hotkey_input_box)

        # Hot-key-stop input box
        hotkey_input_box = BoxLayout(orientation="horizontal", size_hint_y=None, height=50)
        hotkey_label = Label(text="hot-key to stop:", color=(1, 1, 1, 1), size_hint_x=None, width=150)
        self.hotkey_input = TextInput(
            hint_text="Enter hot-key to stop countdown",
            text="ctrl+alt+x",
            background_color=(0, 0, 0, 1),
            foreground_color=(1, 1, 1, 1),
        )
        hotkey_input_box.add_widget(hotkey_label)
        hotkey_input_box.add_widget(self.hotkey_input)
        right_box.add_widget(hotkey_input_box)

        self.button_execute = Button(
            text="Start", size_hint_y=None, height=100,
            background_color=(0, 2, 0, 2)
        )
        self.button_execute.bind(on_press=self.start_execution)
        right_box.add_widget(self.button_execute)

        self.add_widget(right_box)
        


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
        Window.size = (700, 400)
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
