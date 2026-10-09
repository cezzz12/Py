from pathlib import Path
from ui.ui import UserInterface

def main():
    filename = str(Path(__file__).resolve().parent / 'flights')
    ui= UserInterface(filename)
    ui.runUi()

if __name__ == "__main__":
    main()