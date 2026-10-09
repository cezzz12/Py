from repository.repository import BoardRepository
from service.service import GameService
from ui.ui import ConsoleUI


def main():
    # Initialize the game components
    repository = BoardRepository()
    service = GameService(repository)

    # Let user choose interface
    while True:
        print("\nConnect Four")
        print("1. Console Interface")
        print("2. Graphical Interface")
        print("3. Exit")

        try:
            choice = int(input("Choose interface (1-3): "))
            if choice == 1:
                ui = ConsoleUI(service)
                ui.play_game()
            elif choice == 2:
                from gui import GUI
                ui = GUI(service)
                ui.run()
            elif choice == 3:
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


if __name__ == "__main__":
    main()