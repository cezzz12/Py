from fileinput import filename

from domain.domain import Flight,FlightValidator,FlightException
from repository.repository import FlightRepository

class FlightService:
    def __init__(self,filename):
        self.repository = FlightRepository(filename)
        self.filename=filename
        self.FlightValidator = FlightValidator()
        self.ServiceValidator=ServiceValidator()


    def addFlight(self,new_flight):
        try:
            self.FlightValidator.validate(new_flight)
            self.ServiceValidator.validate(new_flight, self.filename)
            self.repository.add(new_flight)
        except FlightException as error:
            print(error)

    def DeleteFlightById(self, id):
        if self.repository.remove(id):
            print("Flight deleted successfully")
        else:
            print("Flight not found")

    def SortAirportByActivity(self):
        flights = self.repository.getFlights()
        count = {}
        for flight in flights:
            count[flight.departure_city] = count.get(flight.departure_city, 0) + 1
            count[flight.arrival_city] = count.get(flight.arrival_city, 0) + 1
        sorted_airports = sorted(count.items(), key=lambda x: x[1], reverse=True)
        for airport in sorted_airports:
            print(f"{airport[0]}: {airport[1]} operations")



class ServiceValidator:
    def validate(self, new_flight, filename):
        repository = FlightRepository(filename)
        for flight in repository.getFlights():
            if str(flight.id) == str(new_flight.id):
                raise FlightException('Flight already exists')

class ServiceException(Exception):
    pass

