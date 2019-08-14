* [ ]  **lab 12-part 2 exercise**

| File Name | What it does |
| ------ | ------ |
| decorator_1.py | There are two functions and wrapper functions prints out some sentences before and after the other function is called |
| decorator_timer.py |Outputs the time a function takes to execute. The function sums up numbers from 0 to 10000| 
| headline.py | Shows a headline from BBC rss feed (title, published time, and summary) without the use of template |
| headlines.py | Shows headlines from BBC rss feed with the use of template|
| headlines_if.py | Shows a headline from BBC rss feed filtered by a certain word with the use of template. The script pass the article to template via render_template.| 
| hello_world.py | Prints out Hello, World! |
| hello_world_with_templates.py | Prints out hello, world! via render_template  |
| if_name_test.py | prints out __name__ which is a value that gets as string of  __main__ | 
| macros.py | A websites that shows different information depends on which routes it goes |
| random_headline.py | Chooses one headline randomly from BBC articles using randint function |
| random_letters.py | Prints out random word that is between 0 to 32 in ascii code. | 
| show_time.py | if the route is '/time', prints out current time with datetime function. | 
| show_time_with_filter.py | if the route is '/time', prints out date and time in a specific format with datetimefilter function. It uses show_time_with_filter.html template. | 
| url_for.py | Redirects users to url_for('home') when users go to /login | 
| url_for_using_vs_url_for.py | Redirectts users to vs_url_for('home') prefix to /usr/253 when users go to /login | 
| username.py | When a user goes to /username, it shows the user profile for that user| 
| vs_url_for.py | Returns to prefix url |
| whats_my_name.py | Prints out __name__ of the file, when the code run by interpreter | 

**Usage**


   **URL** : [http://doc.gold.ac.uk/usr/340/](http://doc.gold.ac.uk/usr/340/)
* Set last line in mytwits_mysql.py (debug=False) to run it without debug
* If you want to test it our without registration, put id = dan1, password = password1 in /login 
* I’ve imported abort(401) for avoiding to make a user edit and delete other users’ twits and image
* The landing page(/) is for creating/updating/deleting/reading twits
* Go to /gallery for creating/updating/deleting/reading images
* Go to /register to create a new account
* There are three tables in the mysql database (users, twits, images). Primary keys for each is user_id, twit_id, image_id. Foreign key for twits and images is user_id. If you want to check the database structure, command `sudo mysql -u root` in CMD , put password and command `SELECT * FROM <table_name>` or `DESCRIBE <table_name>`
* Check out my [git history](https://gitlab.doc.gold.ac.uk/skim037/database-and-the-web-term2/commits/master)

**Requirement**
1.	it is a flask app -__YES__
2.	there is more than one route and more than one view – __YES__
**This is the accessible route for my app**
* / ,(Line 173) : renders “index.html” which is a landing page.
* /<username> ,(Line 178) : displays the latest twit where username=username
* /add_twit ,(Line 183) : using flask-wtform, adds a twit
* /edit_twit ,(Line 196) : using flask-wtform, edits a existing twit
* /delete_twit ,(Line 225): remove a twit
* /login ,(Line 240): using flask-wtform and flask-login, validates user information and put it in a session
* /logout ,(Line 251): removes the user from the session if it’s there
* /register ,(Line 260) : using flask-wtform, gets new user’s information and post it to database
* /gallery ,(Line 283) : displays all the images in the ‘images’ table from database
* /w ,(Line 289) : render “upload.html” template which is a page to let user upload image
* /upload ,(Line 295) : get image information from “upload.html”, post it in database with description
* /add_image ,(Line 330) : adds image using flask-form. 
* /edit_image ,(Line 343) : edits image 
* /delete_image ,(Line 379) : delete image

** assigned route for api **
* /api ,(Line 161): shows all twits, you can edit twits by passing arguments
* /api/<int:twit_id> ,(Line 162): shows twits that twit_id is corresponding with the passing argument. You can edit it as well
* /image_api ,(Line 163): shows all images, you can edit twits by passing arguments
* /image_api/<int:image_id>, (Line 164): shows urls of the images that image_id is corresponding with the passing argument. You can edit it as well

3.	the html is rendered using jinja templates -__YES__
all the html files in the templates is rendered using jinja templates
4.	the jinja templates include some control structure(S) e.g. if/else, for/endfor – __YES__
* mytwits_mysql.html : for/endfor (Line 5~13)
* add_image.html : if/endif (Line 11~18)
* gallery.html : for/endfor (Line 4~12)
* add_twit_mysql.html : if/endif (Line 11~18)
* edit_image.html : if/endif (Line 11~18)
* index.html : if/endif (Line 13~19), for/endfor (Line 4~10)
* register.html : if/endif (Line 12~19, 24~31, 48~55) for/endfor is inseide if phrase
* edit_twit_mysql.html : if/endif (Line 11~18)
* timeline.html : for/endfor (Line 4~12)
* login.html : if/endfor (Line 12~19, 24~32, 37~44)
* base.html : if/endif (Line 25~32) for/endfor (Line 18~23)

5.	it includes one or more forms – __YES__
in forms.py, addTwitForm, editTwitForm, loginForm, RegistrationForm, UploadForm, editImageForm
6.	the forms have some validation -__YES__
For form, I used flask-wtform for form validation.
For login, I used flask-login for login/session validation
7.	there are useful feedback messages to the user – __YES__
* For password when login, flask-login form has error handling (in mytwits_mysql.py line 340, forms.py line 21 & login.html line 15, 28, 40) 

*  When the static file is already made, upload() prints error message in mytwits_mysql.py line 304
*  All the forms is basically offering error handling

8.	it has a database backend that implements CRUD operations (the database can be mysql or mongodb) -YES I’ve used SQLAlchemy.
9.	the create & update operations take input data from a form or forms – YES, throughout the app(/add_twit, /edit_twit, /upload, /edit_image) in mytwits_mysql.py
10.	there is user authentication (i.e. logins) – __YES__ (in user.py line 10)
11.	the login process uses sessions -__YES__ I’ve used flask-login, and it uses session
12.	passwords should be stored as hashes – __YES__ it uses hash and salt and it encrypted with sha-512. (passwordhelper.py )
13.	there is a way to logout – __YES__ there is /logout route
14.	there is a basic api i.e. content can be accessed as json via http methods – __YES__, please refer to number 4 above
15.	it should be clear how to access the api (this could include comments in code) __YES__, please refer to number 4 above
<extensions>
16.	using wtforms is not required but is recommended – __YES__ all forms is in forms.py
17.	use of flask-login is not required but is recommended – __YES__ flask-login is connected in mytwits_mysql.py line 36
18.	using a salt is not required but is recommended – __YES__, salt is generated in passwordhelper.py line 9
19.	additional credit will be given for an api that implements get,post,push and delete - __YES__ in mytwits_mysql.py line 50~163
20.	use of flask-restful is not required but is recommended – __YES__ I’ve set flask-restful api for not only twits but also images in mytwits_mysql.py line 50~163
21.	using sqlalchemy is not required but will attract credit -__YES__, I’ve used SQLAlchemy database model is in models.py and connects it in mytwits_mysql.py line 42

