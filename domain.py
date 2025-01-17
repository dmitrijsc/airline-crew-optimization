from typing import List
from timefold.solver import SolverStatus
from timefold.solver.domain import *
from timefold.solver.score import HardSoftDecimalScore
from datetime import datetime, date

from typing import Annotated

from member_data import Member
from flight_data import Flight

class MemberEntity:

    id: Annotated[int, PlanningId]
    member: Annotated[Member | None, PlanningVariable]
    rest_until: Annotated[datetime | None, None]
    available_from: Annotated[datetime | None, None]
    assigned: Annotated[bool | None, None]
    workhours: Annotated[int | None, None]
    preference: Annotated[str | None, None]
    max_daily_hours: Annotated[int | None, None]
    min_rest_hours: Annotated[int | None, None]
    base: Annotated[str | None, None]

    def __init__(self, member: Member):
        self.id = member.id
        self.member = member
        self.rest_until = member.available_from
        self.available_from = member.available_from
        self.assigned = False
        self.workhours = 0
        self.preferences = member.preferences
        self.max_daily_hours = member.max_daily_hours
        self.min_rest_hours = member.min_rest_hours
        self.base = member.base

@planning_entity
class FlighAssignmentEntity:

    id: Annotated[str, PlanningId]
    
    orig: Annotated[str, None]
    dest: Annotated[str, None]
    depart: Annotated[datetime, None]
    arrive: Annotated[datetime, None]
    duration: Annotated[int, None]

    member: Annotated[MemberEntity | None, PlanningVariable]
    
    def __init__(self):
        self.id = None
        self.member = None

    def __init__(self, flight: Flight, member: MemberEntity):
        
        self.id: Annotated[str, PlanningId] = flight.flight_number
        self.depart = flight.depart
        self.arrive = flight.arrival
        self.orig = flight.orig
        self.dest = flight.dest
        self.duration = flight.duration

        self.member : Annotated[MemberEntity | None, PlanningVariable] = member
    
    def get_id(self):
        return self.flight_number

@planning_solution
class FlightScheduleSolution:
    members: Annotated[list[MemberEntity], ProblemFactCollectionProperty, ValueRangeProvider]
    assignments: Annotated[list[FlighAssignmentEntity], PlanningEntityCollectionProperty]
    score: Annotated[HardSoftDecimalScore | None, PlanningScore]
    solver_status: SolverStatus | None

    def __init__(self):
        # self.flights = []
        self.members = []
        self.assignments = []
        self.score = None
        self.solver_status = None