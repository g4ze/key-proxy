import pyautogui
import time
import pyperclip

def type_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Delay before starting typing
    time.sleep(5)

    for line in lines:
        for char in line.strip():
            if char == '<':
                # Use pyperclip to paste '<' symbol from the clipboard
                pyperclip.copy('<')
                pyautogui.hotkey('shift', ',')
            if char == '#':
                # Use pyperclip to paste '#' symbol from the clipboard
                pyperclip.copy('#')
                pyautogui.hotkey('shift', '3')
            else:
                pyautogui.write(char)
            
            time.sleep(0.1)  # Adjust this delay as needed

        pyautogui.press("enter")  # Press 'Enter' at the end of each line

if __name__ == "__main__":
    text_file_path = "./testfile.txt"  # Replace with the actual path to your text file
    type_text_from_file(text_file_path)
