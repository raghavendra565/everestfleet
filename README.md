## Time Spent
I roughly spend 4 hours to complete this project

## Assumptions
I did't considered any assumptions on my own. I have done the project as outlined in the readme file

## Next Steps
If I had some time
1. I would be doing the swagger documentations more meaning full and cleaner.
2. I would be doing testing my django app by learning testing.
3. I would add serializers for response and input model.

### Features
1. swagger documentation which provides easy interface to execute APIs
2. Provided all the query params as outlined in the requirements
## How to Use

After cloning the project,
To execute the custom command run the below command
1. python manage.py import_house_data --file_path "path to the csv file containing FleetDailyTrips data"

To run the project
1. create virtual env and activate env
2. install the requirements using requirements.txt file
3. run the project
4. in the browser open "http://localhost:8000". it will redirect to swagger documentation "http://localhost:8000/cached/swagger/"
5. In the swagger documentation you will see the get api. you can execute the API by providing inputs as mentioned.