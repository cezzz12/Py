from domain.domain import Route, RouteValidator, RouteException


class RouteRepository:
    def __init__(self, filename):
        self.filename = filename
        self.routes = []
        for route in self.readFile():
            number, departure_city, departure_time, arrival_city, arrival_time, number_of_available_tickets = (
                int(route[0]), route[1], route[2], route[3], route[4], int(route[5]))
            new_route = Route(number, departure_city, departure_time, arrival_city, arrival_time, number_of_available_tickets)
            RouteValidator().validate(new_route)
            self.routes.append(new_route)

    def readFile(self):
        with open(self.filename, 'r') as file:
            return [line.strip().split(',') for line in file.readlines()]

    def writeFile(self):
        with open(self.filename, 'w') as file:
            for route in self.routes:
                file.write(str(route) + '\n')

    def add(self, new_route):
        self.routes.append(new_route)
        self.writeFile()

    def getRoutes(self):
        return self.routes

    def findRouteByNumber(self, number):
        for route in self.routes:
            if route.number == number:
                return route

class RepositoryException(Exception):
    pass

