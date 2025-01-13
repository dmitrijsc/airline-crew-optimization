from timefold import SolverFactory
from datetime import timedelta
# from flight_data import FlightData
# from member_data import MemberData

class Scheduler:
    def __init__(self, base_airports, flights, members, available_from):
        self.base_airports = base_airports
        self.flights = flights
        self.members = members
        self.members_available_from = available_from
        self.members_current_workhours = {member.id: 0 for member in members}

    def create_problem(self):
        # Define the problem using TimeFold AI
        pass

    def solve(self):
        solver_factory = SolverFactory()
        solver = solver_factory.create_solver()
        problem = self.create_problem()
        solution = solver.solve(problem)
        return solution

    def assign_members_to_flights(self):
        solution = self.solve()
        # Process the solution and assign members to flights
        pass

    def create_problem(self):

        problem = {
            'flights': self.flights,
            'members': self.members,
            'constraints': [
                # Constraint: Member must be available
                lambda flight, member: self.members_available_from[member.id] <= flight.depart,
                # Constraint: Prevent overwork
                lambda flight, member: 
                    flight.depart_airport not in self.base_airports or
                    self.members_current_workhours[member.id] + flight.duration * + 1 < member.max_daily_hours,
            ],
            'soft_constraints': [
                # Soft Constraint: Preference handling
                lambda flight, member: member.preferences is None or member.preferences in flight.depart.strftime('%p'),
                # Soft Constraint: Minimize number of members
                lambda flight, member: 1
            ]
        }

        return problem