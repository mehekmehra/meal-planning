from backend.pick_meals import PickMeals
from googleapiclient.discovery import build
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import date, timedelta, datetime
import csv

SCOPES = ['https://www.googleapis.com/auth/calendar']


class GCal():
    def __init__(self, num_weeks, first_time, calendar_name=None, user_email=None):
        """ Initializes an objct to interact with Google Calendar's API. Takes credentials from credentials.json.
            If the calendar does not exist, creates a new one and stores its id. 
            If the calendar already exists, pulls its id from user_info.csv.
            inputs
            ------
            num_weeks: number of weeks that should be scheduled as an integer.
            first_time: boolean representing if a new calendar should be created or not.
            calendar_name: name of the calendar (same as database name).
                           If no name is provided, pulls name from user_info.csv.
            user_email: gmail email of the user that the calendar will be shared with as a string.
                        If no email is provided, it pulls the name from user_info.csv.
        """
        self.num_weeks = num_weeks
        self.creds = service_account.Credentials.from_service_account_file(
                    'backend/credentials.json')
        self.service = build('calendar', 'v3', credentials=self.creds)

        # create new calendars and share them with first time users
        if first_time:
            self.calendar_id = self.create_calendar(calendar_name)
            self.db_name = calendar_name
            self.user_email = user_email
        # for returning users, just pull the saved calendar id
        else:
            with open("user_info.csv", mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    calendar_id = row[2]
                    db_name = row[0]
                    user_email = row[1]
            self.calendar_id = calendar_id
            self.db_name = db_name
            self.user_email = user_email

    def create_calendar(self, calendar_name):
        """ creates a new calendar with the inputted name. 
            inputs
            ------
            calendar_name: name of the calendar as a string.
            outputs
            -------
            calendar_id: the id of the calendar created.
        """
        new_calendar = {
                        'summary': calendar_name,
                        'timeZone': 'America/Los_Angeles'
                        }
        
        calendar = self.service.calendars().insert(body=new_calendar).execute()
        calendar_id = calendar["id"]

        self.share_calendar()
        return calendar_id
    
    def create_event(self, event_name, description, start, end):
        """ Creates a calendar event in the calendar associated with the object.
            inputs
            ------
            event_name: name of the calendar event as a string.
            description: description of the event.
                        (for this use case it will be the name of each dish followed by its ingredients list)
            start: the start date of the event as a datetime. 
            end: the end date of the event as a datetime.
            outputs
            -------
            event_id: the id of the event created.
        """
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
        """ Shares the calendar associated with the object with the email associated with the object.
        """
        rule = {
            'scope': {
                'type': 'user',
                'value': self.user_email,
            },
            'role': 'owner' 
        }

        self.service.acl().insert(calendarId=self.calendar_id, body=rule).execute()

    def get_sundays(self):
        """ Finds the dates of the next self.num_weeks Sundays.
        """
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
        """ Schedules the meals on the calendar for the number of weeks specified by self.num_weeks.
            Finds the dates to schedule on, picks the meals and schedules the events.
        """
        pm = PickMeals(self.db_name, self.num_weeks)
        meals_list = pm.meal_plan()
        sundays = self.get_sundays()

        for i in range(self.num_weeks):
            start_date = sundays[i]
            end_date = start_date + timedelta(days=1)

            description = self.process_week_meals(meals_list[i])

            self.create_event("This week's meals", description, start_date, end_date)


    def process_week_meals(self, week_meals):
        """ Writes the description for each calendar event based on the chosen meals.
            inputs
            ------
            week_meals: a list of tuples (meal, ingredients), where meal is the name of the meal and ingredients is
                        a list of ingredients.
            outputs
            -------
            description: the description as a string. 
                         For example: for ("example_meal", ["ingredient1", ingredient2"]). The output is:
                         "example_meal
                         Ingredients:
                         ingredient1
                         ingredient2"
        """
        description = ""
        for meal in week_meals:
            dish_name = meal[0]
            ingredients = meal[1]
            description += dish_name + "\n Ingredients: \n"
            for ingredient in ingredients:
                description += ingredient + "\n"
            description += "\n"
        return description
