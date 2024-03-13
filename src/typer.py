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
