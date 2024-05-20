from backend.pick_meals import PickMeals
import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import date, timedelta, datetime
import os
import pickle

SCOPES = ['https://www.googleapis.com/auth/calendar']

class GCal():
    def __init__(self, num_weeks, db_name, first_time, user_email, calendar_name=None):
        self.creds = service_account.Credentials.from_service_account_file(
                    'credentials.json')
        self.service = build('calendar', 'v3', credentials=self.creds)

        # create new calendars and share them with first time users
        if first_time:
            if calendar_name:
                self.calendar_id = self.create_calendar(calendar_name)
            else:
                self.calendar_id = self.create_calendar("meal_planning")
        
        # for returning users, just pull the saved calendar id
        else:
            file = open("calendar_id.txt", 'w')
            calendar_id = file.read()
            self.calendar_id = calendar_id
        
        self.num_weeks = num_weeks
        self.db_name = db_name
        self.user_email = user_email

    def create_calendar(self, calendar_name):
        new_calendar = {
                        'summary': calendar_name,
                        'timeZone': 'America/Los_Angeles'
                        }
        
        calendar = self.service.calendars().insert(body=new_calendar).execute()
        file = open("calendar_id.txt", 'w')
        file.write(calendar["id"])
        file.close()

        self.share_calendar()
        return calendar['id']
    
    def create_event(self, event_name, description, start, end):
        event = {
                'summary': event_name,
                'description': description,
                'start': {
                    'dateTime': start.isoformat() + 'T00:00:00-07:00',
                    'timeZone': 'America/Los_Angeles',
                },
                'end': {
                    'dateTime': end.isoformat() + 'T00:00:00-07:00',
                    'timeZone': 'America/Los_Angeles',
                },
            }
        created_event = self.service.events().insert(calendarId=self.calendar_id, body=event).execute()
        return created_event['id']
    
    def share_calendar(self):
        rule = {
            'scope': {
                'type': 'user',
                'value': self.user_email,
            },
            'role': 'owner' 
        }

        self.service.acl().insert(calendarId=self.calendar_id, body=rule).execute()

    def get_sundays(self):
        # get today's date
        curr_date = date.today()
        # shift to the first sunday
        sunday_date = timedelta(days=6 - curr_date.weekday()) + curr_date

        sundays = [sunday_date]

        for _ in range(self.num_weeks - 1):
            sunday_date += timedelta(days=7)
            sundays += [sunday_date]

        return sundays
    
    def schedule_meals(self):
        pm = PickMeals(self.db_name, self.num_weeks)
        meals_list = pm.meal_plan()
        sundays = self.get_sundays()

        for i in range(self.num_weeks):
            start_date = sundays[i]
            end_date = start_date + timedelta(days=1)

            description = self.process_week_meals(meals_list[i])

            self.create_event("This week's meals", description, start_date, end_date)


    def process_week_meals(self, week_meals):
        description = ""
        for meal in week_meals:
            dish_name = meal[0]
            ingredients = meal[1]
            description += dish_name + "\n Ingredients: \n"
            for ingredient in ingredients:
                description += ingredient + "\n"
            description += "\n"
        return description
