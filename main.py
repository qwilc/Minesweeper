# This is a sample Python script.
from game import Game
from gui import GUI
from game_modes import Mode


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# TODOs:
    # don't remove flags at end, show accurate/inaccurate flags
    # best times - literally just a file with the info for the top ten would work
    # what does the time do when it gets really large? like, left it open for a week
    # should I have the question mark option?
    # would be nice if first click always opened up a lot of squares,
    #       but maybe that'll come when we figure out the no-guess version

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    game = Game(Mode.EASY)
    game.peek()
    # game.play_game()
    GUI(game).display()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
