# Meal Planning App
Have you ever had trouble deciding what to cook for yourself for dinner? Well, I have, so this is me making my computer figure out what I should meal prep.


Planning out what dishes you should meal prep each week can get a little tedious, especially when you have other things to worry about like college or a full time job. This app tries to address that problem by picking two full meals (side and protein or one all-inclusive meal) to prepare each week and adding them directly to a Google calendar with the ingredients listed. The meals for the week are scheduled for every Sunday, so you can refer to the ingredients, buy them, and make the meals, without having to think about it. 

## Running the App
### Set Up
To run the app locally, first set up a `venv` and run `pip install -r requirements.txt`. This will install all of the required packages in the environment. 

To set up the Google Calendar API:
1. Go to the [Google Cloud Console](https://console.cloud.google.com/) and create a new project. 
2. With the project selected, go to the API & Services dashboard and enable the Google Calendar API.
3. Then, navigate to IAM & Admin > Service Accounts and create a service account with a role of at minimum Project Editor.
4. After the service account is created, click on the email and go to the Keys tab.
5. Click on Add Key and Create New Key.
6. Then, select JSON as the file type. This will download a JSON file with your credentials.
7. Rename the JSON file to `credentials.json` and put it in the `backend` folder.

This completes the setup. Since this uses a service account, your personal Google Calendar does not get accessed. Instead, the service account creates its own calendar, which it populates with events and shares with your desired account.

### Running the App
After completing the set up, you can run the app by running:

``` python3 app.py```

and opening http://127.0.0.1:5000/ in the browser. The entire framework runs locally and has not been deployed yet. 

To schedule meals, simply follow the webpage. If it is your first time or you want to create a new calendar with a new database, you can click on `First Time User` and enter the necessary information. You can then navigate to the `Scheduling Meals` page and add your meals to the database. Once you have populated the database, you can enter how many weeks you want to schedule meals for and click on the `Make Meal Schedule` button. This will populate the calendar with meal prep events. If you have set up your calendar already, you can select `Returning User` on the homepage and go directly to the `Scheduling Meals` page. 

### Images
Homepage:
![homepage](https://github.com/mehekmehra/meal-planning/blob/main/demo-images/home.png)
First Time User Page:
![first_time](https://github.com/mehekmehra/meal-planning/blob/main/demo-images/first_time.png)
Scheduling Meals Page:
![schedule_meal](https://github.com/mehekmehra/meal-planning/blob/main/demo-images/schedule.png)


Calendar Update:
![calendar](https://github.com/mehekmehra/meal-planning/blob/main/demo-images/calendar.png)
Single Calendar Event (these dishes are very much made up):
![event](https://github.com/mehekmehra/meal-planning/blob/main/demo-images/event.png)

## Details About the Project
This is entirely a personal project that I worked on because I was bored and I wanted to make my life a little easier. I also wanted to try working with things I do not get to use as much and put together some skills I gained working on other projects. The webpage UI is built using HTML, CSS, and Javascript. I have mostly worked on primarily backend work, so getting to work on frontend helped me refresh my knowledge of HTML, CSS, and Javascript and think a little bit more about the usability of my projects. To link the frontend and backend, I used Flask. This was my first time working with Flask, so there was a learning curve to figuring out how to send information back and forth between the frontend and backend. The backend is built in Python since I am most familiar with it, so it was a nice base for all of the new things I worked with. To set up my meal databases, I used the SQLite package and got to apply some of the SQL knowledge that I gained while interning at Amazon and working on a data analysis project. For this project, I also wanted to use the Google Calendar API because it worked well with the scheduling I was trying to do and would integrate well into my day-to-day use. I have never worked with any of Google's APIs, so this was an interesting learning experience for me.

There are a few next steps for this project. First, deploying the webpage. However, to do this I would have to make several large changes including finding a way to host and store the databases, adding security measures for how personal data is stored and communicated within the framework, and actually hosting the webpage. Second, adding more room for personalization. For example, the app works to my requirements of picking 2 meals for each week but other users may have different requirements. Third, users can only access and modify one calendar at a time. I retain the information for the previous calendars, but there currently is no way to access them. Fourth, options to delete calendars or databases. The functionality to delete single meals exists but not entire calendars or databases. There is also no way to access this functionality from the UI. 
