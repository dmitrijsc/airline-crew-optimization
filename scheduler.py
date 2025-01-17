from timefold.solver import SolverManager, SolverFactory, SolutionManager, SolverStatus
from timefold.solver.config import (SolverConfig, ScoreDirectorFactoryConfig,
                                    TerminationConfig, Duration)

from domain import FlighAssignmentEntity, MemberEntity, FlightScheduleSolution
from constraints import define_constraints
from random import choice

import time

from flight_data import Flight
from member_data import Member

def solvers(seconds = 250):

    solver_config = SolverConfig(
        solution_class=FlightScheduleSolution,
        entity_class_list=[FlighAssignmentEntity],
        score_director_factory_config=ScoreDirectorFactoryConfig(
            constraint_provider_function=define_constraints
        ),
        termination_config=TerminationConfig(
            spent_limit=Duration(seconds=seconds),
        ),   
    )

    solver_factory = SolverFactory.create(solver_config)
    solver_manager = SolverManager.create(solver_factory)
    solution_manager = SolutionManager.create(solver_manager)

    return solution_manager, solver_manager

def generate_schedule(base_airports, flights: list[Flight], members: list[Member], counts):

    schedule = FlightScheduleSolution()
    departure_flight_members = {}

    for member in members[0:counts['members']]:
        member_entity = MemberEntity(member)
        schedule.members.append(member_entity)

    for flight in flights[0:counts['flights']]:
        
        member = choice(schedule.members)

        # If flight is a return flight, check if the departure flight has already 
        # been assigned to a member
        if flight.flight_number.endswith('R'):
            dep_flight_number = flight.flight_number[:-1]
            #if dep_flight_number in departure_flight_members:
            #    member = departure_flight_members[dep_flight_number]
        else:
            departure_flight_members[flight.flight_number] = member

        assignment = FlighAssignmentEntity(flight, member)
        schedule.assignments.append(assignment)

    return schedule


def report_progress(best):
    print("Best results", best.score)

def run_solver(id, base_airports, flights, members, params):

    schedule = generate_schedule(base_airports, flights, members, params)

    start_time = time.time()
    solution_manager, solver_manager = solvers(params['seconds'])
    solver_job = solver_manager.solve(id, schedule, lambda best: report_progress(best))    

    for idx in range(params['seconds'] * 6):
        time.sleep(5)
        status = solver_manager.get_solver_status(id)

        if params['verbose']:
            print(idx, "Solver status", status)

        if status != SolverStatus.SOLVING_ACTIVE:
            break

    end_time = time.time()
    result = solver_job.get_final_best_solution()

    if params['verbose']:   
        print("Time taken", end_time - start_time, result is not None)
        print("Best score", result.score)

    if result is None:
        return None

    return {
        'time': end_time - start_time,
        'params': params,
        'score': result.score,
        'original_assignments': schedule.assignments,
        'optimized_assignments': result.assignments,
    }

def save_results(outcome):

    if outcome is None or outcome['optimized_assignments'] is None:
        return

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    
    print(f"Time taken: {outcome['time']} seconds")
    print(f"Params: {outcome['params']}")
    print(f"Score: {outcome['score']}")
    print(f"Results saved to results-{timestamp}.txt")

    with open(f"results-{timestamp}.txt", "w") as f:

        f.write(f"Time taken: {outcome['time']} seconds\n")
        f.write(f"Params: {outcome['params']}\n")
        f.write(f"Score: {outcome['score']}\n")
        f.write("\n")

        for assignment in outcome['original_assignments']:
            f.write(f"{assignment.id}\t{assignment.depart.strftime('%d-%m %H:%M')} {assignment.orig} {assignment.dest} {assignment.member.id}\n")

        f.write("\n\n")

        for assignment in outcome['optimized_assignments']:
            f.write(f"{assignment.id}\t{assignment.depart.strftime('%d-%m %H:%M')} {assignment.orig} {assignment.dest} {assignment.member.id}\n")

