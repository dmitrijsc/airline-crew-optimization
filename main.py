import random
from datetime import timedelta
from flight_data import FlightData
from member_data import MemberData
import time

from scheduler import run_solver, save_results

# random.seed(4321)

base_airports = ['VNO', 'RIX', 'TLL']

# Realtime data from the airline API
flight_data = FlightData(base_airports)
flight_data.read_flights()

# Emperical formula for pilot count based on the number of flights
start_time = flight_data.flights[0].depart - timedelta(hours=1)
pilot_count = int(len(flight_data.flights) / 5 / 2 * 0.5)

# Generate members
member_data = MemberData(base_airports)
member_data.generate_members(pilot_count, pilot_count, pilot_count * 4, start_time)

# Solver params
flights_count = 50
# solver_params = { 'flights': flights_count, 'members': flights_count // 2, 'seconds': flights_count * 2, 'verbose': True }
solver_params = { 'flights': flights_count, 'members': flights_count // 2, 'seconds': flights_count * 3, 'verbose': True }

# Run solver
outcome = run_solver('demo', base_airports, flight_data.flights, member_data.members, solver_params)

# Save results
save_results(outcome)



# print('Pilot count:', pilot_count)

# print the first 10 flights
# for flight in flight_data.flights[:5]:
#    print(f"{flight.orig} -> {flight.dest} ({flight.depart} - {flight.arrival}) ({flight.duration} min) {flight.flight_number}")

# print the number of flights
# print(len(flight_data.flights))

# for member in member_data.members[:15]:
#    print(f"{member.id} {member.name} {member.role} {member.base} {member.preferences})")

# print the number of members
# print(len(member_data.members))

# scheduler = Scheduler(base_airports, flight_data.flights, member_data.members, member_data.available_from)
# scheduler.assign_members_to_flights()

# result = None

# def update_best(best):
#     print("Best results", best.score)
#     global result
#     result = best