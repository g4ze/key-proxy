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
        self.text_input = TextInput(
            hint_text="Paste your text here:", size_hint=(1, 0.8),
            background_color=(0, 0, 0, 1),
            foreground_color=(1, 1, 1, 1)
        )
        self.add_widget(self.text_input)
        self.countdown_input = TextInput(
            hint_text="Enter countdown duration (in seconds):", size_hint=(1, 0.1),
            background_color=(0, 0, 0, 1),
            foreground_color=(1, 1, 1, 1),
            )
        self.add_widget(self.countdown_input)

        self.button_execute = Button(text="Start", size_hint=(1, 0.1), background_color=(0, 2, 0, 2))
        self.button_execute.bind(on_press=self.start_execution)
        self.add_widget(self.button_execute)

    def start_execution(self, instance):
        text = self.text_input.text
        if not self.countdown_input.text or not self.countdown_input.text.isdigit():
            self.countdown_input.text = "5"
        # Save the text to a file
        with open("src/output.txt", "w") as file:
            file.write(text)

        print("Text saved to output.txt")
        
        self.show_countdown()

    def show_countdown(self):
        self.countdown_view = ModalView(size_hint=(0.5, 0.3), size_hint_max_x=400, size_hint_max_y=100)
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
        from starter import Starter
        print("Starting the script...")
        starter = Starter(file_path="src/output.txt", delay=0)
        starter.start()
        print("Script execution completed!")
        self.show_success_popup()
    def show_success_popup(self):
        self.success_view = ModalView(size_hint=(0.7, 0.3), size_hint_max_x=400, size_hint_max_y=100)
        self.success_label = Label(
            text="Script execution completed!", font_size=20
        )
        self.success_view.add_widget(self.success_label)
        self.success_view.open()



class MyApp(App):
    def build(self):
        Window.size = (400, 300)
        self.title = "Key-Proxy"
        return MyBoxLayout()



    
