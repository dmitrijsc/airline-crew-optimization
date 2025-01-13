import random

from datetime import timedelta
from flight_data import FlightData
from member_data import MemberData
from scheduler import Scheduler

random.seed(4321)

# Realtime data from the airline API
flight_data = FlightData()
flight_data.read_flights()

# Emperical formula for pilot count based on the number of flights
start_time = flight_data.flights[0].depart - timedelta(hours=1)
pilot_count = int(len(flight_data.flights) / 5 / 2 * 0.5)

member_data = MemberData()
member_data.generate_members(pilot_count, pilot_count, pilot_count * 4, start_time)

print('Pilot count:', pilot_count)

# print the first 10 flights
for flight in flight_data.flights[:5]:
    print(f"{flight.orig} -> {flight.dest} ({flight.depart} - {flight.arrival}) ({flight.duration} min) {flight.flight_number}")

# print the number of flights
print(len(flight_data.flights))

for member in member_data.members[:15]:
    print(f"{member.id} {member.name} {member.role} {member.base} {member.preferences} (Available: {member_data.available_from[member.id]})")

# print the number of members
print(len(member_data.members))

scheduler = Scheduler(['VNO', 'RIX', 'TLL'], flight_data.flights, member_data.members, member_data.available_from)
scheduler.assign_members_to_flights()

