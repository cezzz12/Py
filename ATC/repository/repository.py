from domain.domain import Flight,FlightException,FlightValidator

class FlightRepository:
    def __init__(self, filename):
        self.filename = filename
        self.flights = []
        for flight in self.readFile():
            id, departure_city, departure_time, arrival_city, arrival_time = (
                flight[0], flight[1], flight[2], flight[3], flight[4]
            )
            new_flight = Flight(id, departure_city, departure_time, arrival_city, arrival_time)
            FlightValidator().validate(new_flight)
            self.flights.append(new_flight)

    def readFile(self):
        with open(self.filename,'r') as file:
            return [line.strip().split(',') for line in file.readlines()]
    def writeFile(self):
        with open(self.filename,'w') as file:
            for flight in self.flights:
                file.write(str(flight)+ '/n')

    def add(self,new_flight):
        for flight in self.flights:
            if (flight.departure_time == new_flight.departure_time and
                    flight.departure_city == new_flight.departure_city):
                raise FlightException("Airport can only handle one departure at a time")
            if (flight.arrival_time == new_flight.arrival_time and
                    flight.arrival_city == new_flight.arrival_city):
                raise FlightException("Airport can only handle one arrival at a time")
        self.flights.append(new_flight)
        self.writeFile()

    def remove(self, id):
        flight = self.findFlightById(id)
        if flight:
            self.flights.remove(flight)
            self.writeFile()
            return True
        return False

    def getFlights(self):
        return self.flights.copy()

    def findFlightById(self,id):
        for flight in self.flights:
            if flight.id == id:
                return flight
        return None

