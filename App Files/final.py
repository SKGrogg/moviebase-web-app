from sqlite3.dbapi2 import OperationalError
from bottle import redirect, route, run, template, Bottle, post, get, request
import sqlite3
import requests
from bs4 import BeautifulSoup

con = sqlite3.connect('moviebase.db')
cur = con.cursor()

app = Bottle()


@route('/')
def homepage():

    #Give the User Two Options:
    #1. Search for a specific movie and/or based on how much money the movie made
        #If no results match their search, the top 20 movies in the database are returned
    #2. See a page with ALL movies in the Database

    num_movies = list(cur.execute("SELECT COUNT(*) FROM movies"))[0][0] 

    return f"""
    <h1>
    Welcome to Moviebase! 
    </h1>
    <h3>
    Please search for a movie below by inputing either a movie name, a minimum box office gross, or both!
    <br>
    Or, click the button below the search to see all {num_movies} movies in the Database!
    </h3>
    <br>
    <form action="/movies" method="POST">
            Movie Name: <input name="movie_name" type="text" />
            <br>
            <br>
            Minimum Box Office Gross*: <input name="min_box_office" type="number" />
            <input value="Search" type="submit" />
    </form>
    <br>
    <form action="/movies"> <input type="submit" value="See All Movies"/></form> <br>
    """


#Displays search results from homepage. If not results match, displays 20 movies in Database
#OR, if User presses "See All Movies" button, displays ALL movies in Database
@route('/movies')
@post('/movies')
def movies():

    try: 
        movie_name = request.forms.get('movie_name')
        min_box_office = request.forms.get('min_box_office')

        
        html = "<form action='/'> <input type='submit' value='Try a Different Search' /></form>\
            <h1><u>Movies</h1></u><br/>\
            <form action='/movies/add_movie'> <input type='submit' value='Add a New Movie'/></form>"


        #if no user input but "Search" button pressed
        if (movie_name == "") and (min_box_office == ""):
            html += '<h2><u>No input values in your search. Here are 20 movies in our database.</u></h2> <br>'
            html += "<table border='1'><tr><td><u> Movie Name</u></td>  <td><u>View / Edit</u></td>  <td><u>Delete</u></td>  <td><u>Show Reviews</u></td>  <td><u>Add New Reviews</u></td></tr>" 

            for row in cur.execute('SELECT * FROM movies LIMIT 20'):
                html += f'<tr> <td>{row[1]}</td>\
                    <td><form action=\"/movies/view_edit/{row[0]}\"> <input type=\"submit\" value=\"View/Edit {row[1]}\" /></form></td>\
                    <td><form action=\"/movies/delete/{row[0]}\"> <input type=\"submit\" value=\"Delete {row[1]}\" /></form></td>\
                    <td><form action=\"/movies/get_reviews/{row[0]}\"> <input type=\"submit\" value=\"Reviews for {row[1]}\" /></form></td>\
                    <td><form action=\"/movies/add_reviews/{row[0]}\"> <input type=\"submit\" value=\"Add Review for {row[1]}\" /></form></td></tr>'


        #If someone selects "See All Movies" button OR comes straight to this URL manually
        elif movie_name is None and min_box_office is None:
            num_movies = list(cur.execute("SELECT COUNT(*) FROM movies"))[0][0]
            html += f'<h2><u>All {num_movies} movies in database</u></h2> <br>'
            html += "<table border='1'><tr><td><u> Movie Name</u></td>  <td><u>View / Edit</u></td>  <td><u>Delete</u></td>  <td><u>Show Reviews</u></td>  <td><u>Add New Reviews</u></td></tr>" 

            for row in cur.execute('SELECT * FROM movies'):
                html += f'<tr> <td>{row[1]}</td>\
                    <td><form action=\"/movies/view_edit/{row[0]}\"> <input type=\"submit\" value=\"View/Edit {row[1]}\" /></form></td>\
                    <td><form action=\"/movies/delete/{row[0]}\"> <input type=\"submit\" value=\"Delete {row[1]}\" /></form></td>\
                    <td><form action=\"/movies/get_reviews/{row[0]}\"> <input type=\"submit\" value=\"Reviews for {row[1]}\" /></form></td>\
                    <td><form action=\"/movies/add_reviews/{row[0]}\"> <input type=\"submit\" value=\"Add Review for {row[1]}\" /></form></td></tr>'
        
        #if user inputs something in search
        else:
            
            sql_com = ""

            #Set SQL command and arguments based on user input
            if movie_name == "" and min_box_office != "":

                sql_com = f'SELECT movie_id, movie_name FROM movies WHERE gross >= ?'

                args = (min_box_office,)
            
            elif movie_name != "" and min_box_office == "":

                sql_com = f"SELECT movie_id, movie_name FROM movies WHERE movie_name LIKE ?"
                args = (f'%{movie_name}%',)

            else:

                sql_com = f"SELECT movie_id, movie_name FROM movies WHERE (movie_name LIKE ? AND gross >= ?)"
                args = (f'%{movie_name}%', min_box_office)

            #check to see if results are empty for search
            results = cur.execute(sql_com, args)

            counter = 0

            for row in results:
                counter +=1

            #if results are empty, return generic results
            if counter == 0:

                html += '<h2><u>No Movies Matched Your Search. Here are 20 movies in our database.</u></h2> <br>'
                html += "<table border='1'><tr><td><u> Movie Name</u></td>  <td><u>View / Edit</u></td>  <td><u>Delete</u></td>  <td><u>Show Reviews</u></td>  <td><u>Add New Reviews</u></td></tr>"
                
                for row in cur.execute('SELECT * FROM movies LIMIT 20'):
                    
                    html += f'<tr> <td>{row[1]}</td>\
                    <td><form action=\"/movies/view_edit/{row[0]}\"> <input type=\"submit\" value=\"View/Edit {row[1]}\" /></form></td>\
                    <td><form action=\"/movies/delete/{row[0]}\"> <input type=\"submit\" value=\"Delete {row[1]}\" /></form></td>\
                    <td><form action=\"/movies/get_reviews/{row[0]}\"> <input type=\"submit\" value=\"Reviews for {row[1]}\" /></form></td>\
                    <td><form action=\"/movies/add_reviews/{row[0]}\"> <input type=\"submit\" value=\"Add Review for {row[1]}\" /></form></td></tr>'

            #else, return actual results
            else:
                
                if movie_name == "" and min_box_office != "":
                    html += f'<h2><u>Movies With Box Office Gross >= ${min_box_office}</u></h2> <br>'

                elif movie_name != "" and min_box_office == "":
                    html += f"<h2><u>Movies With Names Like \"{movie_name}\"</u></h2> <br>"

                else:
                    html += f"<h2><u>Movies With Names Like \"{movie_name}\" and Box Office Gross >= ${min_box_office}</u></h2> <br>"
                
                html += "<table border='1'><tr><td><u> Movie Name</u></td>  <td><u>View / Edit</u></td>  <td><u>Delete</u></td>  <td><u>Show Reviews</u></td>  <td><u>Add New Reviews</u></td></tr>"

                for row in cur.execute(sql_com, args):
                    html += f'<tr> <td>{row[1]}</td>\
                    <td><form action=\"/movies/view_edit/{row[0]}\"> <input type=\"submit\" value=\"View/Edit {row[1]}\" /></form></td>\
                    <td><form action=\"/movies/delete/{row[0]}\"> <input type=\"submit\" value=\"Delete {row[1]}\" /></form></td>\
                    <td><form action=\"/movies/get_reviews/{row[0]}\"> <input type=\"submit\" value=\"Reviews for {row[1]}\" /></form></td>\
                    <td><form action=\"/movies/add_reviews/{row[0]}\"> <input type=\"submit\" value=\"Add Review for {row[1]}\" /></form></td></tr>'


        html += '</table>'

        return html

    #If unanticipated error occurs
    except Exception as e:

        return f"""
                <h2> Whoops, Something Went Wrong!</h2>
                <h3> {e} </h3>
                <h4> We apologize for the inconvenience. Please go back and try again. </h4>
                <br>
                <form action="/movies"> <input type="submit" value="See All Movies"/></form> 
                <br>
                <form action="/"> <input type="submit" value="Homepage" /></form>"""


#Shows User current attributes of a movie, as well as allowing them to edit those attributes
@route('/movies/view_edit/')
@get('/movies/view_edit/<movie_id>')
def view_edit(movie_id=None):

    try:

        name  = list(cur.execute(f"SELECT movie_name FROM movies WHERE movie_id = {movie_id}"))[0][0]
        html = f"""
        <form action="/"> <input type="submit" value="Homepage" /></form>
        <form action="/movies"> <input type="submit" value="See All Movies"/></form> 
        <h1><u>View '{name}'</u></h1> <br> <table border='1'>
        """

        html += f"<tr><td><u> Database ID #</u></td>  <td><u> Movie Name </u></td>  <td><u>Year Released</u></td> \
        <td><u>Budget</u></td>  <td><u>Box Office Gross</u></td> <td><u>Genre</u></td> </tr>"

        for row in cur.execute(f'SELECT movie_id, movie_name, year_released, budget, gross, genre FROM movies WHERE movie_id = {movie_id}'):
            html += f'<tr><td>{row[0]}</td> <td>{row[1]}</td> <td>{row[2]}</td> <td>{row[3]}</td> <td>{row[4]}</td> <td>{row[5]}</td></tr>'


        html += '</table>'

        #Form to update attributes
        html += f"""
        <h1><u>Edit</u></h1>
        <h3> Not all fields required. Update only what you wish.</h3>
        <h4> For "Year Released",  any value below 1895 (the year of the first film) is not allowed. </h4>
        <h4> Please do not insert negative numbers into monetary fields fields (budget, gross). </h4>
        <form action="/movies/view_edit/{movie_id}" method="POST">
                New Movie Name: <input name="movie_name" type="text" />
                <br>New Year Released: <input name="year_released" type="number" />
                <br>New Budget: <input name="budget" type="number" />
                <br>New Box Office Gross: <input name="gross" type="number" />
                <br><label for="genre">Genre:</label>
                <select id="genre" name="genre">
                    <option value="No Update">No Update</option>
                    <option value="Comedy">Comedy</option>
                    <option value="Action">Action</option>
                    <option value="Adventure">Adventure</option>
                    <option value="Crime">Crime</option>
                    <option value="Western">Western</option>
                    <option value="Drama">Drama</option>
                    <option value="Romance">Romance</option>
                    <option value="Sci-Fi">Sci-Fi</option>
                    <option value="Horror">Horror</option>
                    <option value="Sports">Sports</option>
                    </select>
                <br><br><input value="Submit Updates" type="submit" />
            </form>
        """
        

        return html
    
    except: 

        try:
            #Check to see if invalid movie_id in URL
            #Should only be ann issue if someone tries to manually type in URL
            counter = 0

            for row in cur.execute(f'SELECT * FROM movies WHERE movie_id = {movie_id}'):
                counter +=1

            if counter == 0:
                return f"""
                <h2> Whoops, Something Went Wrong!</h2>
                <h4> The movie_id in your URL doesn't seem to exist in the Database. Please go back and try another movie. </h4>
                <form action="/movies"> <input type="submit" value="See All Movies"/></form> 
                <br>
                <form action="/"> <input type="submit" value="Homepage" /></form>
                """

        except Exception as e:
            #If someone comes to page manually without putting in a movie_id
            if movie_id is None:
                return f"""
                    <h2> Whoops, Something Went Wrong!</h2>
                    <h4> No movie_id to search. Please go back and try again. </h4>
                    <br>
                    <form action="/movies"> <input type="submit" value="See All Movies"/></form> 
                    <br>
                    <form action="/"> <input type="submit" value="Homepage" /></form>"""

            #Unknown error occurs
            
            return f"""
                <h2> Whoops, Something Went Wrong!</h2>
                <h3> {e} </h3>
                <h4> We apologize for the inconvenience. Please go back and try again. </h4>
                <br>
                <form action="/movies"> <input type="submit" value="See All Movies"/></form> 
                <br>
                <form action="/"> <input type="submit" value="Homepage" /></form>"""
    
#Updates user changes in the database, displays the updated attributes
@post('/movies/view_edit/<movie_id>')
def updated_view(movie_id):

    try:
        name = request.forms.get('movie_name')
        year = request.forms.get('year_released')
        budget = request.forms.get('budget')
        gross = request.forms.get('gross')
        genre = request.forms.get('genre')


        #Check to see if any input values are negative 
        num_check_vals = [year, budget, gross]
        num_check_attr  =['year_released', 'budget', 'gross']
        invalid_number = False
        invalid_list = [False, False, False]

        for i in range(0,3):
            if num_check_vals[i] != "":
                val = int(num_check_vals[i])    
                #If it's the year_released attribute
                if i == 0:
                    if val < 1895:
                        invalid_number = True
                        invalid_list[i] = True
                #otherwise, budget or gross
                else:
                    if val < 0:
                        invalid_number = True
                        invalid_list[i] = True
        
        #If negative numbers input, do not except update. Return error message and ask them to try again
        if invalid_number:

            name  = list(cur.execute(f"SELECT movie_name FROM movies WHERE movie_id = {movie_id}"))[0][0]

            html = f"""
            <h1><u>Update for '{name}' Cancelled</u></h1>
            <h3> It appears you put invalid values for the following attributes:</h3>
            """

            for i in range(0,3):
                if invalid_list[i]:
                    html += f"{num_check_attr[i]}: {num_check_vals[i]}<br> "
            
            html += f"""<h3> Please go back and try your update again.
                <br>
                <br>
                <form action="/movies/view_edit/{movie_id}" method="GET"> <input type="submit" value="Try Update Again" /></form>
                """

            return html


        #Valid Input. Continue
        input_list = [name, year, budget, gross, genre]

        attr_list = ['movie_name', 'year_released', 'budget', 'gross', 'genre']

        sql_com = "UPDATE movies SET "

        #tracking to ensure proper construction of string command
        first_update = True

        #list to be converted to tuple for execute
        arg_list = []

        for i in range(0,5):

            #if attribute was not updated, do not add to string
            if input_list[i] == "" or input_list[i] == "No Update":
                continue
            
            #If attribute was updated, add to string
            else:

                #if no other updates have been added to list, no comma needed
                if first_update:

                    first_update = False

                    #if it's a string input, add quotes
                    if i == 0 or i == 4:
                        sql_com += f"{attr_list[i]} = ?"
                        arg_list.append(f'{input_list[i]}')

                    #if it's an integer, no quotes
                    else:
                        sql_com += f"{attr_list[i]} = ?"
                        arg_list.append(input_list[i])

                #comma needed in command string
                else:

                    #if it's a string input, add quotes
                    if i == 0 or i == 4:
                        sql_com += f", {attr_list[i]} = ?"
                        arg_list.append(f'{input_list[i]}')

                    #if it's an integer, no quotes
                    else:
                        sql_com += f", {attr_list[i]} = ?"
                        arg_list.append(input_list[i])
        
        sql_com += f" WHERE movie_id = {movie_id}"

        args = tuple(arg_list)
        cur.execute(sql_com, args)
        con.commit()

        #Create html to display with updated values
        name  = list(cur.execute(f"SELECT movie_name FROM movies WHERE movie_id = {movie_id}"))[0][0]

        html = f"""
        <form action="/"> <input type="submit" value="Homepage" /></form>
        <form action="/movies"> <input type="submit" value="See All Movies"/></form> 
        <h1><u>View '{name}'(Updated)</u></h1> <br> <table border='1'>
        """

        html += f"<tr><td><u> Database ID #</u></td>  <td><u> Movie Name </u></td>  <td><u>Year Released</u></td> \
        <td><u>Budget</u></td>  <td><u>Box Office Gross</u></td> <td><u>Genre</u></td> </tr>"

        for row in cur.execute(f'SELECT movie_id, movie_name, year_released, budget, gross, genre FROM movies WHERE movie_id = {movie_id}'):
            html += f'<tr><td>{row[0]}</td> <td>{row[1]}</td> <td>{row[2]}</td> <td>{row[3]}</td> <td>{row[4]}</td> <td>{row[5]}</td></tr>'


        html += '</table>'

        html += f"""
        <br>
        <form action="/movies/view_edit/{movie_id}" method="GET"> <input type="submit" value="Update Again" /></form>
        """

        return html
    
    #If no updates are made but "Update" button is pressed, an error is thrown. This displays an error message and bring user back to view/edit
    except OperationalError:

        return f"""
        <h2> Whoops, Something Went Wrong!</h2>
        <h4> It looks like you pressed "Update" without making any updates. Please go back and try again.</h4>
        <br>
        <form action="/movies/view_edit/{movie_id}" method="GET"> <input type="submit" value="Try Update Again" /></form>
        <br>
        <form action="/movies"> <input type="submit" value="See All Movies"/></form> 
        <br>
        <form action="/"> <input type="submit" value="Homepage" /></form>"""
        
    #Unanticipated Error
    except Exception as e:
        return f"""
        <h2> Whoops, Something Went Wrong!</h2>
        <h3> {e} </h3>
        <h4> We apologize for the inconvenience. Please go back.</h4>
        <br>
        <form action="/movies"> <input type="submit" value="See All Movies"/></form> 
        <br>
        <form action="/"> <input type="submit" value="Homepage" /></form>"""
        
#Deletes movie from Database, displays message confirming deletion
@route('/movies/delete/')
@route('/movies/delete/<movie_id>')
def delete(movie_id=None):

    try:

        #Get name to display in confirmation message before deleting
        name  = list(cur.execute(f"SELECT movie_name FROM movies WHERE movie_id = {movie_id}"))[0][0]

        #Updating review foreign key to NULL for deleted movie
        cur.execute(f"UPDATE reviews SET movie_id = NULL WHERE movie_id = {movie_id}")

        # Delete the movie
        cur.execute(f"DELETE FROM movies WHERE movie_id = {movie_id}")
        con.commit()

        return f"""
        <h1><u> Delete</u><h1>
        <h3> '{name}' Deleted From Database</h3>
        <form action="/movies"> <input type="submit" value="Back To All Movies" /></form>
        <form action="/"> <input type="submit" value="Homepage" /></form>
        """

    except Exception as e:

        #if someone tries to come directly to this address, send them back to homepage
        if movie_id == None:
            return f"""
            <h2> Whoops, Something Went Wrong!</h2>
            <h4> No movie_id to search. Please go back. </h4>
            <br>
            <form action="/movies"> <input type="submit" value="See All Movies"/></form> 
            <br>
            <form action="/"> <input type="submit" value="Homepage" /></form>
            """


        #Check to make sure movie_id exists. If not, add a link back to homepage
        counter = 0

        for row in cur.execute(f'SELECT * FROM movies WHERE movie_id = {movie_id}'):
            counter +=1

        if counter == 0:
            return f"""
            <h2> Whoops, Something Went Wrong!</h2>
            <h4> This movie_id is not in our database. Please go back and try another movie. </h4>
            <form action="/movies"> <input type="submit" value="See All Movies"/></form> 
            <br>
            <form action="/"> <input type="submit" value="Homepage" /></form>
            """

        #If we've gotten here, an unanticipated error has occurred.
        return f"""
            <h2> Whoops, Something Went Wrong!</h2>
            <h3 >{e} </h3>
            <h4> We apologize for the inconvenience. Please go back and try another movie. </h4>
            <form action="/movies"> <input type="submit" value="See All Movies"/></form> 
            <br>
            <form action="/"> <input type="submit" value="Homepage" /></form>
            """


#Get reviews for a specified movies
@route('/movies/get_reviews/')
@get('/movies/get_reviews/<movie_id>')
def get_reviews(movie_id=None):

    try: 
    
        #get movie_name to display
        name  = list(cur.execute(f"SELECT movie_name FROM movies WHERE movie_id = {movie_id}"))[0][0]

        html = f"""
        <form action="/"> <input type="submit" value="Homepage" /></form>
        <form action="/movies"> <input type="submit" value="See All Movies"/></form> 
        <h1><u>Reviews for '{name}' </u></h1>
        <form action="/movies/add_reviews/{movie_id}"> <input type="submit" value="Add a New Review"/></form> 
        <br>
        """

        html += f"<table border='1'> <tr><td><u> Review ID </u></td> <td><u> Critic Name </u></td> <td><u> Review Summary </u></td> </tr>"

        for row in cur.execute(f'SELECT review_id, critic_name, review_text FROM movies INNER JOIN reviews USING (movie_id)\
            INNER JOIN critics USING (critic_id) WHERE movies.movie_id = {movie_id}'):
            html += f'<tr><td>{row[0]}</td> <td>{row[1]}</td> <td>{row[2]}</td></tr>'

        html += '</table>'


        return html

    except:

        try:
            #Check to see if invalid movie_id in URL
            #Should only be ann issue if someone tries to manually type in URL
            counter = 0

            for row in cur.execute(f'SELECT * FROM movies WHERE movie_id = {movie_id}'):
                    counter +=1

            if counter == 0:
                return f"""
                <h2> Whoops, Something Went Wrong!</h2>
                <h4> The movie_id in your URL doesn't seem to exist in the Database. Please go back and try another movie. </h4>
                <form action="/movies"> <input type="submit" value="See All Movies"/></form> 
                <br>
                <form action="/"> <input type="submit" value="Homepage" /></form>
                """

        except Exception as e:

            #If someone comes to page manually without putting in a movie_id
            if movie_id is None:
                return f"""
                    <h2> Whoops, Something Went Wrong!</h2>
                    <h4> No movie_id to search. Please go back and try again. </h4>
                    <br>
                    <form action="/movies"> <input type="submit" value="See All Movies"/></form> 
                    <br>
                    <form action="/"> <input type="submit" value="Homepage" /></form>"""

            #Unknown error occurs
                
            return f"""
                <h2> Whoops, Something Went Wrong!</h2>
                <h3> {e} </h3>
                <h4> We apologize for the inconvenience. Please go back and try again. </h4>
                <br>
                <form action="/movies"> <input type="submit" value="See All Movies"/></form> 
                <br>
                <form action="/"> <input type="submit" value="Homepage" /></form>"""

@route('/movies/add_reviews/')
@get('/movies/add_reviews/<movie_id>')
def add_reviews(movie_id=None):

    try:
        
        #get movie name to display
        name  = list(cur.execute(f"SELECT movie_name FROM movies WHERE movie_id = {movie_id}"))[0][0]

        html = f"""
        <form action="/"> <input type="submit" value="Homepage"/></form> 
        <form action="/movies"> <input type="submit" value="See All Movies"/></form> 
        <h1><u>Manually Add Review for '{name}'</u></h1>"""

        #Form to add a new review for this movies
        html += f"""
        <form action="/movies/add_reviews/complete/{movie_id}" method="POST">
                <label for="review_text">Type Your Review:</label>
                <textarea id="review_text" name="review_text" rows="4" cols="50" required></textarea>
                <br>
                <br>
                <br>
                Critic Name: <input name="critic_name" type="text" required>
                <br><br><input value="Submit Review" type="submit" />
        </form>
        """

        html += f"""
                <h1><u>Automatically Add Reviews from Rotten Tomatoes</u></h1>
                <h4>Please note: Current functionality limited to 20 reviews automatically added. Check back soon for updates!</h4>
                <form action="/movies/add_reviews/rt/complete/{movie_id}" method="POST">
                Rotten Tomatoes URL: <input name="url" type="text" required/>
                <br>
                <br>Max Number of Reviews to Add: <input name="num" type="number"/>
                <br><input value="Submit Request" type="submit"/>
                <br>
                </form>
                """

        #Displays all reviews with the option to change that to the current movie

        html += '<h1><u>Change Old Review </u></h1>'
        html += f"<h4>You may select a review below so that it now is assigned to '{name}'</h4> <br>"
        html += f"<table border='1'><tr> <td><u> Movie ID </u></td> <td><u> Movie Name </u></td>\
            <td><u> Review ID </u></td> <td><u> Critic Name </u></td> \
            <td><u> Review Summary </u></td>\
                <td><u> Switch Review </u></td> </tr>"

        for row in cur.execute(f'SELECT movie_id, movie_name, review_id, critic_name, review_text FROM critics INNER JOIN reviews USING (critic_id)\
            LEFT OUTER JOIN movies USING (movie_id) ORDER BY movie_id'):
            html += f"<tr><td>{row[0]}</td> <td>{row[1]}</td> <td>{row[2]}</td><td>{row[3]}</td>\
                <td>{row[4]}</td>\
                <td><form action='/movies/add_reviews/complete/{movie_id}/{row[2]}'> <input type='submit' value='Switch This Review'/></form> </td>"

        #back buttons
        html+= f"""
        </table>
        """
        
        return html

    except:

        try:
            #Check to see if invalid movie_id in URL
            #Should only be ann issue if someone tries to manually type in URL
            counter = 0

            for row in cur.execute(f'SELECT * FROM movies WHERE movie_id = {movie_id}'):
                    counter +=1

            if counter == 0:
                return f"""
                <h2> Whoops, Something Went Wrong!</h2>
                <h4> The movie_id in your URL doesn't seem to exist in the Database. Please go back and try another movie. </h4>
                <form action="/movies"> <input type="submit" value="See All Movies"/></form> 
                <br>
                <form action="/"> <input type="submit" value="Homepage" /></form>
                """

        except Exception as e:
            
            #If someone comes to page manually without putting in a movie_id
            if movie_id is None:
                return f"""
                    <h2> Whoops, Something Went Wrong!</h2>
                    <h4> No movie_id to search. Please go back and try again. </h4>
                    <br>
                    <form action="/movies"> <input type="submit" value="See All Movies"/></form> 
                    <br>
                    <form action="/"> <input type="submit" value="Homepage" /></form>"""

            #Unknown error occurs
                
            return f"""
                <h2> Whoops, Something Went Wrong!</h2>
                <h3> {e} </h3>
                <h4> We apologize for the inconvenience. Please go back and try again. </h4>
                <br>
                <form action="/movies"> <input type="submit" value="See All Movies"/></form> 
                <br>
                <form action="/"> <input type="submit" value="Homepage" /></form>"""

@route('/movies/add_reviews/rt')
@get('/movies/add_reviews/rt/<movie_id>')
def add_reviews_rt(movie_id=None):
    try:

        name  = list(cur.execute(f"SELECT movie_name FROM movies WHERE movie_id = {movie_id}"))[0][0]

        html = f"""
        <form action="/"> <input type="submit" value="Homepage"/></form> 
        <form action="/movies"> <input type="submit" value="See All Movies"/></form> 
        <h1><u>Add Review(s) for '{name}' From Rotten Tomatoes</u></h1>
        <h4>Please note: Current functionality limited to 20 reviews automatically added. Check back soon for updates!</h4>"""

        #Form to add a new review for this movies
        html += f"""
        <form action="/movies/add_reviews/rt/complete/{movie_id}" method="POST">
                Rotten Tomatoes URL: <input name="url" type="text" required/>
                <br>Max Number of Reviews to Add: <input name="num" type="number"/>
                <<br><input value="Submit Review" type="submit"/>
        </form>
        """
    except:

        try:
            #Check to see if invalid movie_id in URL
            #Should only be ann issue if someone tries to manually type in URL
            counter = 0

            for row in cur.execute(f'SELECT * FROM movies WHERE movie_id = {movie_id}'):
                    counter +=1

            if counter == 0:
                return f"""
                <h2> Whoops, Something Went Wrong!</h2>
                <h4> The movie_id in your URL doesn't seem to exist in the Database. Please go back and try another movie. </h4>
                <form action="/movies"> <input type="submit" value="See All Movies"/></form> 
                <br>
                <form action="/"> <input type="submit" value="Homepage" /></form>
                """

        except Exception as e:
            
            #If someone comes to page manually without putting in a movie_id
            if movie_id is None:
                return f"""
                    <h2> Whoops, Something Went Wrong!</h2>
                    <h4> No movie_id to search. Please go back and try again. </h4>
                    <br>
                    <form action="/movies"> <input type="submit" value="See All Movies"/></form> 
                    <br>
                    <form action="/"> <input type="submit" value="Homepage" /></form>"""

            #Unknown error occurs
                
            return f"""
                <h2> Whoops, Something Went Wrong!</h2>
                <h3> {e} </h3>
                <h4> We apologize for the inconvenience. Please go back and try again. </h4>
                <br>
                <form action="/movies"> <input type="submit" value="See All Movies"/></form> 
                <br>
                <form action="/"> <input type="submit" value="Homepage" /></form>"""



#this page handles both adding a new review and reassigning and old review
#if new review, <review_id> is none
@post('/movies/add_reviews/complete/<movie_id>')
@get('/movies/add_reviews/complete/<movie_id>/<review_id>')
def updated_reviews(movie_id, review_id=None):

    try:
        #if adding a new review
        if review_id is None:

            try:
                review_text = request.forms.get('review_text')
                critic_name = request.forms.get('critic_name')

                #Check to see if critic_name already exists in critics table (RELATION-Z)

                critic_result = list(cur.execute(f"SELECT * FROM critics WHERE critic_name = ? LIMIT 1", (f'{critic_name}',)))
                    
                #If critic doesn't exist, add critic to RELATION-Z
                if critic_result == []:   
                    cur.execute(f"INSERT INTO critics (critic_name) VALUES (?)", (f'{critic_name}',))
                    con.commit()

                #get critic_id
                critic_id = list(cur.execute(f"SELECT * FROM critics WHERE critic_name = ? LIMIT 1", (f"{critic_name}",)))[0][0]

                #add the review with the movie and critic IDs
                args = (f'{review_text}', movie_id, critic_id)
                cur.execute(f"INSERT INTO reviews (review_text, movie_id, critic_id) VALUES (?,?,?)", args)
                con.commit()

            #In case something crashes during the database access
            except Exception as e:
                return f"""
                    <h2> Whoops, Something Went Wrong!</h2>
                    <h3> {e} </h3>
                    <h4> We apologize for the inconvenience. Please go back and try again. </h4>
                    <br>
                    <form action="/movies"> <input type="submit" value="See All Movies"/></form> 
                    <br>
                    <form action="/"> <input type="submit" value="Homepage" /></form>"""

        
        #else, updating an old review
        else:
            cur.execute(f"UPDATE reviews SET movie_id = {movie_id} WHERE review_id = {review_id}")
            con.commit()
  
    except Exception as e:

        return f"""
            <h2> Whoops, Something Went Wrong!</h2>
            <h3> {e} </h3>
            <h4> We apologize for the inconvenience. Please go back and try again. </h4>
            <br>
            <form action="/movies"> <input type="submit" value="See All Movies"/></form> 
            <br>
            <form action="/"> <input type="submit" value="Homepage" /></form>"""

    #redirect back to all reviews for the movie so they cannot accidentally resubmit form
    redirect(f'/movies/get_reviews/{movie_id}')

#Adds reviews scraped from Rotten Tomatoes
@post("/movies/add_reviews/rt/complete/<movie_id>")
def post_reviews_rt(movie_id=None):

    try:

        url = request.forms.get('url')
        num = request.forms.get('num')

        if num == "":
            num = 20
        elif int(num) > 20:
            num = 20

        num = int(num)

        revs = rt_scrape(url, num, movie_id)

        if revs == []:
            raise ReviewException


        for i in range(len(revs)):

                try:
                    
                    critic_name = revs[i][0]
                    review_text = revs[i][1]

                    #Check to see if review already exists

                    review_result = list(cur.execute(f"SELECT * FROM reviews WHERE review_text = ? LIMIT 1", (f'{review_text}',)))

                    if review_result != []:   
                        continue

                    #Check to see if critic_name already exists in critics table 

                    critic_result = list(cur.execute(f"SELECT * FROM critics WHERE critic_name = ? LIMIT 1", (f'{critic_name}',)))

                    #If critic doesn't exist, add critic to RELATION-Z
                    if critic_result == []:   
                        cur.execute(f"INSERT INTO critics (critic_name) VALUES (?)", (f'{critic_name}',))
                        con.commit()

                    #get critic_id
                    critic_id = list(cur.execute(f"SELECT * FROM critics WHERE critic_name = ? LIMIT 1", (f"{critic_name}",)))[0][0]

                    
                    #add the review with the movie and critic IDs
                    args = (f'{review_text}', movie_id, critic_id)
                    cur.execute(f"INSERT INTO reviews (review_text, movie_id, critic_id) VALUES (?,?,?)", args)
                    con.commit()

                except:
                    continue

    except Exception as e:

        return f"""
            <h2> Whoops, Something Went Wrong!</h2>
            <h3> {e} </h3>
            <h4> We apologize for the inconvenience. Please go back and try again. </h4>
            <br>
            <form action="/movies"> <input type="submit" value="See All Movies"/></form> 
            <br>
            <form action="/"> <input type="submit" value="Homepage" /></form>"""
    #redirect back to all reviews for the movie so they cannot accidentally resubmit form
    redirect(f'/movies/get_reviews/{movie_id}')

            

#Form to add a new movie
#Only Name Required
@get('/movies/add_movie')
def add_movie():

    #Form to update
    html = f"""
    <form action="/"> <input type="submit" value="Homepage" /></form>
    <form action="/movies"> <input type="submit" value="See All Movies"/></form> 
    <h1><u>Add a New Movie</u></h1>
    <form action="/movies/add_movie/wiki"> <input type="submit" value="Add Movie From Wikipedia"/></form> 
    <h3>Only a movie's name is required. All other attributes are optional. </h3>
    <h4> For "Year Released",  any value below 1895 (the year of the first film) is not allowed. </h4>
    <h4>Please do not insert negative numbers into monetary fields (budget, gross). </h4>
    <form action="/movies/add_movie" method="POST">
            Movie Name: <input name="movie_name" type="text" required/>
            <br>Year Released: <input name="year_released" type="number" />
            <br>Budget: <input name="budget" type="number" />
            <br>Box Office Gross: <input name="gross" type="number" />
            <br><label for="genre">Genre:</label>
            <select id="genre" name="genre">
                <option value=""></option>
                <option value="Comedy">Comedy</option>
                <option value="Action">Action</option>
                <option value="Adventure">Adventure</option>
                <option value="Crime">Crime</option>
                <option value="Western">Western</option>
                <option value="Drama">Drama</option>
                <option value="Romance">Romance</option>
                <option value="Sci-Fi">Sci-Fi</option>
                <option value="Sports">Sports</option>
                <option value="Horror">Horror</option>
                </select>
            <br><br><input value="Add Movie" type="submit" />
        </form>
        <br><br>
    """

    return html


#Input Wikipedia URL to add movie
@get('/movies/add_movie/wiki')
def add_movie_wiki():

    html = f"""
    <form action="/"> <input type="submit" value="Homepage" /></form>
    <form action="/movies"> <input type="submit" value="See All Movies"/></form> 
    <h1><u>Add a New Movie From Wikipedia</u></h1>
    <h3>Please Insert the complete URL from the film's Wikipedia Page.</h3>
    <form action="/movies/add_movie/wiki" method="POST">
            Wikipedia URL: <input name="url" type="text" required/>
    <br><br><input value="Add Movie" type="submit" />
    </form>
    """

    return html
#Adds new movie and redirects to view_edit page for that movie
@post('/movies/add_movie')
def add_movie():
    
    try:
        name = request.forms.get('movie_name')
        year = request.forms.get('year_released')
        budget = request.forms.get('budget')
        gross = request.forms.get('gross')
        genre = request.forms.get('genre')

        #Check to see if any input values are negative 
        num_check_vals = [year, budget, gross]
        num_check_attr  =['year_released', 'budget', 'gross']
        invalid_number = False
        invalid_list = [False, False, False]

        for i in range(0,3):
            if num_check_vals[i] != "":
                val = int(num_check_vals[i])    
                #If it's the year_released attribute
                if i == 0:
                    if val < 1895:
                        invalid_number = True
                        invalid_list[i] = True
                #otherwise, budget or gross
                else:
                    if val < 0:
                        invalid_number = True
                        invalid_list[i] = True
        
        #If negative numbers input, do not except update. Return error message and ask them to try again
        if invalid_number:

            html = f"""
            <h1><u>'{name}' Not Added</u></h1>
            <h3> It appears you put invalid values for the following attributes:</h3>
            """

            for i in range(0,3):
                if invalid_list[i]:
                    html += f"{num_check_attr[i]}: {num_check_vals[i]}<br>"
            
            html += f"""<h3> Please go back and try to add the movie again.
                <br>
                <br>
                <form action="/movies/add_movie" method="GET"> <input type="submit" value="Add A New Movie" /></form>
                """

            return html


        #Valid Input. Add Movie
        input_list = [name, year, budget, gross, genre]

        attr_list = ['movie_name', 'year_released', 'budget', 'gross', 'genre']

        sql_com = "INSERT INTO movies "
        attr_str = "("
        vals_str = "("

        first_update = True

        #list to be converted to tuple for execute
        arg_list = []

        for i in range(0,5):

        #if attribute was includes
            if input_list[i] == "":
                continue
            else:
                #if no other updates have been added to list
                if first_update:

                    first_update = False

                    #if it's a string input, add quotes
                    if i == 0 or i == 4:
                        attr_str += f"{attr_list[i]}"
                        vals_str += "?"
                        arg_list.append(f'{input_list[i]}')
                    #if it's an integer, no quotes
                    else:
                        attr_str += f"{attr_list[i]}"
                        vals_str += "?"
                        arg_list.append(input_list[i])

                else:
                    #if it's a string input, add quotes
                    if i == 0 or i == 4:
                        attr_str += f", {attr_list[i]}"
                        vals_str += ", ?"
                        arg_list.append(f'{input_list[i]}')
                    #if it's an integer, no quotes
                    else:
                        attr_str+= f", {attr_list[i]}"
                        vals_str += ", ?"
                        arg_list.append(input_list[i])
            
        attr_str += ")"
        vals_str += ")"

        sql_com = sql_com + attr_str + " VALUES " + vals_str


        args = tuple(arg_list)
        cur.execute(sql_com, args)
        con.commit()
    
    except:
        return f"""
            <h2> Whoops, Something Went Wrong!</h2>
            <h3> {e} </h3>
            <h4> We apologize for the inconvenience. Please go back and try again. </h4>
            <br>
            <form action="/movies"> <input type="submit" value="See All Movies"/></form> 
            <br>
            <form action="/"> <input type="submit" value="Homepage" /></form>"""

    #Because movie_id is autoincrememted, the MAX(movie_id) will be the newest
    movie_id  = list(cur.execute(f"SELECT movie_id FROM movies WHERE movie_id = (SELECT MAX(movie_id) FROM movies)"))[0][0]

    #redirect to view_edit page for this new movie
    redirect(f'/movies/view_edit/{movie_id}')

#Adds new movie from Wikipedia and redirects to view_edit page for that movie
@post('/movies/add_movie/wiki')
def add_movie_wiki():

    try:
        url = request.forms.get('url')
        movie_name, year, budget, gross = wiki_scrape(url)

        #Check to see if movie already exists

        movie_result = list(cur.execute(f"SELECT * FROM movies WHERE movie_name = ? LIMIT 1", (f'{movie_name}',)))

        if movie_result != []:   
            
            return f"""
            <h2> Whoops, Something Went Wrong!</h2>
            <h3> Looks like you're trying to add a movie that's already in the database. </h3>
            <h4> Please go back and try again. </h4>
            <br>
            <form action="/movies"> <input type="submit" value="See All Movies"/></form> 
            <br>
            <form action="/"> <input type="submit" value="Homepage" /></form>"""


        input_list = [movie_name, year, budget, gross]

        attr_list = ['movie_name', 'year_released', 'budget', 'gross']

        sql_com = "INSERT INTO movies "
        attr_str = "("
        vals_str = "("

        first_update = True

        #list to be converted to tuple for execute
        arg_list = []

        for i in range(0,4):

        #if attribute was includes
            if input_list[i] == "" or input_list[i] == None:
                continue
            else:
                #if no other updates have been added to list
                if first_update:

                    first_update = False

                    #if it's a string input, add quotes
                    if i == 0 or i == 4:
                        attr_str += f"{attr_list[i]}"
                        vals_str += "?"
                        arg_list.append(f'{input_list[i]}')
                    #if it's an integer, no quotes
                    else:
                        attr_str += f"{attr_list[i]}"
                        vals_str += "?"
                        arg_list.append(input_list[i])

                else:
                    #if it's a string input, add quotes
                    if i == 0 or i == 4:
                        attr_str += f", {attr_list[i]}"
                        vals_str += ", ?"
                        arg_list.append(f'{input_list[i]}')
                    #if it's an integer, no quotes
                    else:
                        attr_str+= f", {attr_list[i]}"
                        vals_str += ", ?"
                        arg_list.append(input_list[i])
            
        attr_str += ")"
        vals_str += ")"

        sql_com = sql_com + attr_str + " VALUES " + vals_str


        args = tuple(arg_list)
        cur.execute(sql_com, args)
        con.commit()
    
    except:
        return f"""
            <h2> Whoops, Something Went Wrong!</h2>
            <h3> {e} </h3>
            <h4> We apologize for the inconvenience. Please go back and try again. </h4>
            <br>
            <form action="/movies"> <input type="submit" value="See All Movies"/></form> 
            <br>
            <form action="/"> <input type="submit" value="Homepage" /></form>"""

    #Because movie_id is autoincrememted, the MAX(movie_id) will be the newest
    movie_id  = list(cur.execute(f"SELECT movie_id FROM movies WHERE movie_id = (SELECT MAX(movie_id) FROM movies)"))[0][0]

    #redirect to view_edit page for this new movie
    redirect(f'/movies/view_edit/{movie_id}')

def wiki_scrape(url):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    movie_name = None
    year = None
    budget = None
    gross = None
    rt_url = None

    if soup.find(id="firstHeading") != None:
        movie_name = soup.find(id="firstHeading")
    
    infobox = soup.find('table', {'class': 'infobox'})


    box_len = len(infobox.find_all('th', class_="infobox-label"))
    for i in range(box_len):
        tag = soup.find_all("th", class_="infobox-label")[i]

        #Find Budget
        if tag.text == "Budget" or tag.text == "Box office":
            temp = soup.find_all("td", class_="infobox-data")[i]
            temp = temp.text

            #convert string to int
            temp = temp.split()
            num = ""
            for c in temp[0]:
                if (ord(c) >= 48 and ord(c) <= 57) or c == '.':
                    num = num + c
                elif c == '[' or c == ']':
                    break
            num = float(num)

            if temp[-1][0] == "m":
                num = num *1000000
            elif temp[-1][0] == "b":
                num = num *1000000000
            elif temp[-1][0] == "t":
                num = num *1000

            if tag.text == "Budget":
                budget = str(num)
            else:
                gross = str(num)

        if tag.text == "Release dates":
            temp = soup.find_all("td", class_="infobox-data")[i]
            temp = temp.text
            temp = temp.split()
            for x in temp:
                if len(x) == 4:
                    if x[0] == '2' or x[0] == '1':
                        temp = x
                        break
            year = temp



    return movie_name.string, year, budget, gross


def rt_scrape(url, num, movie_id):

    url =  url+"/reviews?type=top_critics"

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    review_table = soup.find(class_="review_table")
    num_revs = len(review_table)

    if num_revs < num:
        num = num_revs

    i = 0
    ret = []
    
    while i <= num:
        try:
            row = soup.find_all(class_="row review_table_row")[i]
            review_text = row.find(class_="the_review").text.strip()
            if review_text == "":
                i=+1
                continue
            critic_name = row.find(class_="unstyled bold articleLink").text
            ret.append([critic_name, review_text])
            i += 1
        except IndexError:
            break
    
    return ret

class ReviewException(Exception):
    f"""
            <h2> Whoops, Something Went Wrong!</h2>
            <h3> We were unable to find the reviews for this movie. </h3>
            <h4> We apologize for the inconvenience. Please go back and input reviews manually. </h4>
            <br>
            <form action="/movies"> <input type="submit" value="See All Movies"/></form> 
            <br>
            <form action="/"> <input type="submit" value="Homepage" /></form>
    """

run(host='localhost', port=8080, debug=True)