from timefold.solver.score import (constraint_provider, ConstraintFactory, Joiners, HardSoftDecimalScore, ConstraintCollectors)
from datetime import datetime, date, timedelta

from domain import MemberEntity, FlighAssignmentEntity

def is_member_available(shift: FlighAssignmentEntity):

    isAvailable = shift.member.available_from is None or shift.member.available_from <= shift.depart
    # isRestComplete = shift.member.rest_until is None or shift.member.rest_until <= shift.depart

    return isAvailable # and isRestComplete

def is_member_overbooked(group):

    # Sort shifts by departure time
    sorted_shifts = sorted(group, key=lambda shift: shift.depart)    
    
    # Get first departure and last arrival
    max_consecutive_hours = sorted_shifts[0].member.max_daily_hours
    first_depart = sorted_shifts[0].depart
    last_arrive = max(shift.arrive for shift in sorted_shifts)
    
    # Calculate total time span in hours
    time_span = (last_arrive - first_depart).total_seconds() / 3600
    
    return time_span > max_consecutive_hours

def count_invalid_departure_airports(group):

    sorted_shifts = sorted(group, key=lambda shift: shift.depart)

    last_airport = sorted_shifts[0].member.base
    count = 0

    for shift in sorted_shifts:

        if shift.orig != last_airport:
            count += 1

        else:
            last_airport = shift.dest

    return count

def count_shift_overlap(group):

    sorted_shifts = sorted(group, key=lambda shift: shift.depart)
    
    last_date = sorted_shifts[0].depart
    last_flight = sorted_shifts[0].id

    count = 0

    for shift in sorted_shifts:
        
        if shift.depart <= last_date and shift.id != last_flight:
            count += 1

        else:
            last_date = shift.depart
            last_flight = shift.id

    return count

def is_member_time_overlap(group):

    sorted_shifts = sorted(group, key=lambda shift: shift.depart)
    
    last_date = sorted_shifts[0].depart - timedelta(hours=1)

    for shift in sorted_shifts:
        
        if shift.depart <= last_date:
            return False

        last_date = shift.arrive

    return True

def count_member_shifts(group):
    return len(group)

def is_member_preference_met(shift: FlighAssignmentEntity):
    if shift.member.preferences is None:
        return False
    if shift.member.preferences == 'Morning' and shift.depart.hour >= 12:
        return True
    if shift.member.preferences == 'Night' and shift.depart.hour < 12:
        return True
    return 0

def is_vacay(flight: FlighAssignmentEntity, member: MemberEntity):
    return member.assigned
    

def constraint_member_availability(constraint_factory: ConstraintFactory):
    return (constraint_factory.for_each(FlighAssignmentEntity)
            .filter(lambda shift: not is_member_available(shift))
            .penalize(HardSoftDecimalScore.ONE_HARD)
            .as_constraint("Requirement: Availability")
            )

def constraint_member_preferences(constraint_factory: ConstraintFactory):
    return (constraint_factory.for_each(FlighAssignmentEntity)
            .filter(lambda shift: not is_member_preference_met(shift))
            .penalize(HardSoftDecimalScore.ONE_SOFT)
            .as_constraint("Preference missing: preferred shift")
            )

def constraint_member_workload(constraint_factory: ConstraintFactory):
    return (constraint_factory.for_each(FlighAssignmentEntity)
            .group_by(lambda shift: shift.member.id, ConstraintCollectors.to_list())
            .filter(lambda id, group: is_member_overbooked(group))
            .penalize(HardSoftDecimalScore.ONE_HARD)
            .as_constraint("Requirement: Workload")
            )

def constraint_departure_airport(constraint_factory: ConstraintFactory):
    return (constraint_factory.for_each(FlighAssignmentEntity)
            .group_by(lambda shift: shift.member.id, ConstraintCollectors.to_list())
            .filter(lambda id, group: count_invalid_departure_airports(group) > 0)
            .penalize(HardSoftDecimalScore.ONE_HARD, lambda id, group: count_invalid_departure_airports(group))
            .as_constraint("Requirement: Departure airport")
            )

def constraint_dispatch_overlap(constraint_factory: ConstraintFactory):
    return (constraint_factory.for_each(FlighAssignmentEntity)
            .group_by(lambda shift: shift.member.id, ConstraintCollectors.to_list())
            .filter(lambda id, group: count_shift_overlap(group) > 0)
            .penalize(HardSoftDecimalScore.ONE_HARD, lambda id, group: count_shift_overlap(group))
            .as_constraint("Requirement: Flight overlap")
            )

def constraint_minimize_members(constraint_factory: ConstraintFactory):
    return (constraint_factory.for_each(FlighAssignmentEntity)
            .group_by(lambda shift: shift.member.id,  ConstraintCollectors.to_list())
            .filter(lambda id, group: len(group) < 3)
            .penalize(HardSoftDecimalScore.ONE_SOFT)
            .as_constraint("Preference: Minimize number of members")
            )

@constraint_provider
def define_constraints(constraint_factory: ConstraintFactory):
    return [
        constraint_member_availability(constraint_factory),
        constraint_member_workload(constraint_factory),
        constraint_departure_airport(constraint_factory),
        constraint_dispatch_overlap(constraint_factory),
        constraint_member_preferences(constraint_factory),
        constraint_minimize_members(constraint_factory)
    ]