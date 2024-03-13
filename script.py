import click
from src.key_proxy_gui import MyApp
@click.command()
def hello():
   click.echo(f'Spinning up your instance!!!')
   MyApp().run()

if __name__ == '__main__':
   hello()