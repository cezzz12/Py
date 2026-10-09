from service.service import FlightService
from domain.domain import Flight
class UserInterface:
    EXIT = 0
    ADD_OPTION = 1
    DELETE_OPTION = 2
    LIST_AIRPORT_OPTION = 3
    LIST_FREE_TIME = 4

    def __init__(self, filename):
        self.filename = filename
        self.service = FlightService(filename)

    def __PrintMenu(self):
        print("Menu")
        print("1.ADD")
        print("2.DELETE")
        print("3.LIST_AIRPORT")
        print("4.FREE_TIME")
        print("0.Exit")

    def runUi(self):
        while True:
            self.__PrintMenu()
            try:
                option = int(input("Enter your option: "))
                if option == self.EXIT:
                    break
                elif option == self.ADD_OPTION:
                    id = input("Enter flight id: ")
                    departure_city = input("Enter departure city: ")
                    departure_time = input("Enter departure time: ")
                    arrival_city = input("Enter arrival city: ")
                    arrival_time = input("Enter arrival time: ")
                    new_flight = Flight(id, departure_city, departure_time, arrival_city, arrival_time)
                    self.service.addFlight(new_flight)
                elif option == self.DELETE_OPTION:
                    id = input("Enter flight id: ")
                    self.service.DeleteFlightByID(id)
                elif option == self.LIST_AIRPORT_OPTION:
                    self.service.SortAirportByActivity()
            except ValueError:
                print("Invalid option!")
            except Exception as e:
                print(f"Error: {e}")