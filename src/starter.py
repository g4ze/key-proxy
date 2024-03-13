from typer import KeyProxy


class Starter:
    def __init__(self, delay: int, file_path="src/output.txt"):
        self.file_path = file_path
        self.delay = delay

    def start(self):
        print("Starting the script...")
        key_proxy = KeyProxy(self.file_path, self.delay)
        key_proxy.type_text_from_file()


if __name__ == "__main__":
    starter = Starter()
    starter.start()
