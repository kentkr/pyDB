import readline
import logging
from .commands import CommandExecutor

logger = logging.getLogger(__name__)


class Input:
    def __init__(self) -> None:
        self.history = self.load_history()


    def load_history(self) -> None:
        try:
            readline.read_history_file('history.txt')
        except FileNotFoundError:
            pass


    def save_history(self) -> None:
        readline.write_history_file('history.txt')


    def receive_input(self) -> None:
        user_input = ''
        try:
            while True:
                if not user_input:
                    line = input('> ')
                else:
                    line = input('\\ ')
                user_input += line + '\n'
                if ';' in line:
                    logger.info(f'Command input: {user_input.strip()}')
                    readline.add_history(user_input.strip())
                    CommandExecutor(user_input).execute()
                    user_input = ''
        except (KeyboardInterrupt, EOFError) as e:
            if isinstance(e, KeyboardInterrupt):
                print('\n')
                self.receive_input()
            if isinstance(e, EOFError):
                self.save_history()


def main():
    logging.basicConfig(filename='pyDB.log', level=logging.INFO, format='[%(levelname)s]%(asctime)s::%(name)s %(message)s')

    logger.info('pyDB entry')
    Input().receive_input()
    logger.info('pyDB exit')


if __name__ == "__main__":
    main()

