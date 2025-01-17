import random
from datetime import datetime, timedelta

class Member:

    def __init__(self, id, name, role, base, max_daily_hours, min_rest_hours, preferences, available_from):
        self.id = id
        self.name = name
        self.role = role
        self.base = base
        self.max_daily_hours = max_daily_hours
        self.min_rest_hours = min_rest_hours
        self.preferences = preferences
        self.available_from = available_from

    def get_id(self):
        return self.id

class MemberData:

    _RANDOM_PREFERENCE_MORNING = 13
    _RANDOM_PREFERENCE_NIGHT = 17

    def __init__(self, base_airports):
        self.base_airports = base_airports
        self.members = []
        # self.available_from = {}

    def generate_members(self, num_pilots, num_copilots, num_crew_members, start_date):

        roles = {
            'Pilot': { 'MaxDailyHours': 10, 'MinRestHours': 12},
            'Copilot': { 'MaxDailyHours': 12, 'MinRestHours': 12},
            'Crew Member': { 'MaxDailyHours': 8, 'MinRestHours': 10}
        }
        
        id_counter = 1
        
        def generate_member(role, id_counter):
            
            base = random.choice(self.base_airports)
            max_daily_hours = roles[role]['MaxDailyHours']
            min_rest_hours = roles[role]['MinRestHours']
            preference = None
            available_from = start_date + timedelta(hours=-1)

            if random.random() < 0.4:
                available_from = start_date + timedelta(minutes=random.randint(0, 600))

            if id_counter % self._RANDOM_PREFERENCE_MORNING == 0:
                preference = 'Morning'
            elif id_counter % self._RANDOM_PREFERENCE_NIGHT == 0:
                preference = 'Night'
            return Member(
                id=id_counter,
                name=f'{role} {id_counter}',
                role=role,
                base=base,
                max_daily_hours=max_daily_hours,
                min_rest_hours=min_rest_hours,
                preferences=preference,
                available_from = available_from
            )
        
        for _ in range(num_pilots):
            self.members.append(generate_member('Pilot', id_counter))
            id_counter += 1
        
        for _ in range(num_copilots):
            self.members.append(generate_member('Copilot', id_counter))
            id_counter += 1
        
        for _ in range(num_crew_members):
            self.members.append(generate_member('Crew Member', id_counter))
            id_counter += 1

        # self.generate_member_wait_times(start_date + timedelta(hours=-1))

    # def generate_member_wait_times(self, availe_from_datetime):

    #     self.available_from = {}
        
    #     for member in self.members:
    #         self.available_from[member.id] = availe_from_datetime

    #     for member in self.members:
    #         if random.random() < 0.4:
    #             self.available_from[member.id] = availe_from_datetime + timedelta(minutes=random.randint(0, 600))
