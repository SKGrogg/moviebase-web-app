# moviebase-web-app
This app began as a small final project for a Databases course, with the intention of creating a web API for a small database file that allows the user to add entries for two different entities (movies and reviews), and manipulate those entities in a variety of ways (edit fields, reassign fields, etc). Some of this lingering functionality is not inherently beneficial for the app itself (the real world reason of reassigning a review to another movie makes little sense), but remains as a remnant of that initial project.

After the course ended, I used the app as an opportunity to enhance my webscraping skills, adding functionality for automate inputs from URLs for movies and reviews that the user requests. This included incorporating the Beautiful Soup library into the app.

All this leads to the app as it current exits: A simple web application that allows users to compile movies and associated reviews. The site currently runs with a "moviebase.db" file to give new users an example of how a non-empty database looks on the app, but the intention would be for users to create their own database files for their respective collections.

### Please Note
The intial focus of this project was and remains back-end database interaction and the flow of the webpages into one another. User Interface was given little to no attention, hence the exceedingly simply design. 

### Going Forward
There is still work to be done on beefing up the scraping capabilities to add more reviews at once. There are still some untested input that may not have proper error handling. Finally, if time permits, revamping the UI would be a high priority.



# Setting Up Database and Launching Web App

The database needed for this web app to run is titled "moviebase.db". A populated copy of this file has been added to the p8 folder on my github. However, if you would like to construct a new copy of this, you can do so by going into the p3 folder of my github to download the files "create_db.sql" and "populate_db.sql". Again, when you run these in commandline/terminal, be sure to name the resulting db file "moviebase.db". The web app will not work with any other name.

Once you've ensured the database file is full, you can launch the web app through the commandline/terminal. The file for the web app is found in the p8 folder on my github, titled "final.py". In the terminal, run the file with the command "python3 final.py". The app will launch at URL "http://localhost:8080/". Go to this URL.

### Python Libraries
This web app relies on SQLite3 and Bottle python libraries to run. All tools needed are in the Piplock file. Please be sure to run the "pipenv shell" to ensure you have access to all these libraries

# Using The Web App

## Searching 
Once you've gone to http://localhost:8080/, you will find the main searchpage of the site. There are two search fields to enter: 1) A string search for a movie's name, 2) The minimum box office gross a movie made during its theatrical release. #1 uses a "LIKE '%{str}%' SQL search, so any movie containing the sequence of characters that the user inputs will be returned. Also note that the SQL commands have been paramterized on the backend, so searching with quotation marks and apostrophes will not cause an error. #2 uses a ">=" search, so any movie that has gross the amount or above that the user has put in will appear. Note that only integers are allowed for this field. The search field will not allow a alphabetical character to be input, and the form will not allow the user to submit if they try to input a float.

Please note that pressing the "Search" button without any inputs, or searches that return empty results will display a message indicating the results of those searches (essentially "You didn't put any search values" or "No results for your search", respectively) and instead displaying the top 20 movies in the Database. 

There is also a button on the search page, and all other non-search result pages (view_edit, delete confirmation, get_reviews, add_reviews, etc), to "See All Movies" in the database. This returns ALL movies, not just a limited result of 20. At the time the app is launched, this will be 24 movies, though this will change as the user adds and deletes movies.

## Notes on Expected Functionality and Error Handling
The app should work just as the project rubric describes. A few notes on what to expect in specific situations.

### Deleting A Movie and The Effect on Its Reviews
If a movie is deleted, its reviews (RelationY) are not deleted from the database. They remain in the database without an associated movie. As a result, they will still appear on the "Add A New Review" page, where a table of ALL reviews in the database will be shown, with the option to reassign that review to the current movie. A "LEFT OUTER JOIN" is used, so these reviews without an existing movie will appear at the top of the table with "None" values for movie_id and movie_name.

### Numeric Restrictions for Adding and Updating Movies
When adding a new movie, or updating an existing movie, there are restrictions on the integers a user can input. For "Year Released", a user cannot put in a value less than 1895, which was the first year films were widely shown to the public. For budget and gross, a user may not put in a negative value. If any of these restrictions are breached, the command will be aborted, and a message displayed to the user to alert them of which inputs were invalid, with a button to bring them back and try again.

### Empty Update Attempt Error
If a user tries to submit an empty update form for an existing movie, they will receive an error message stating that the form was empty and a button is given to go back and try the update again.

### Error Handling User Input Local URLs
The site is structed in a way that, once on the site, the User should never have to manually type in a URL at any time. However, if the user DOES try to go directly to an existing URL, this is handled in two ways. In the first case, if they try to go directly to a URL (i.e. '/movies/view_edit/') and do NOT include a movie_id at the end of the URL, a message will appear letting them know there was no movie_id to search for and buttons will allow them to go back to previous pages of the site. If a User tries to manually go to a URL with a movie_id that doesn't exist in the database (i.e. '/movies/view_edit/75'), a message will appear letting them know that the movie they've tried to find does not exist, and they are given buttons to go back.


### Misc. Error Handling
I've added extensive error handling for any and all cases I could project may occur. In all of these cases, an explanation for the User is displayed and further action is recommended. In the event a completely unanticipated error occurs, A generic message apologizes for the inconvenience is displayed, along with the error that occured, and links back to earlier webpages are displayed.


