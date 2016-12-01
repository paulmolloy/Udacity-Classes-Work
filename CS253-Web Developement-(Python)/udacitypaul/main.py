#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2, cgi, re, jinja2, os, hmac
from string import letters

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

SECRET = 'imsosecret'
def render_str(template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a,**kw)

    def render_str(self, template, **params):
        return render_str(template, **params)
    
    def render(self, template, **kw):
        self.write(self.render_str(template,**kw))


months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']

#set of ignored characters
ignored_characters = [".","'", "," ,'"', "!", "?", " ", "-", "&", "<", ">" ]

#check if character should be ignored
def is_rot13able(string, ignored):
    if string not in  ignored:
        return True
    return False
    
#rot13 encodes and decodes text

def rot13(s):
        newstring =""
        for character in s:
                val = ord(character)
                
                #if character is a capital
                if val <91 and val > 64:
                    val = val +13
                    
                    
                    if val > 90:
                        val = val -26
                        
                #if character is lowercase
                else:
                    if val <123 and val > 96:
                        val = val + 13
                        if val > 122:
                            val = val -26
               
                rotcharacter = chr(val)
                if is_rot13able(character, ignored_characters):
                    newstring = newstring +rotcharacter
                else:
                    newstring = newstring + character
                    
        return newstring


        #SIGNUP UTILITY FUNCTIONS
user = "bob9ggggggggggggggggggggggggggggggggg7"

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASSWORD_RE =re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASSWORD_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
     return( (not email) or EMAIL_RE.match(email))

                          
            
#VALID DATE STUFF
month_abbvs = dict((m[:3].lower(), m) for m in months)

def valid_day(day):
        if day.isdigit() and int(day) in range(1,32):
            return int(day)
def valid_month(month):
    if month:
        #short_month = month[:3].lower()
        #return month_abbvs.get(short_month)
        cap_month = month.capitalize()
        if cap_month in months:
            return cap_month

def valid_year(year):
    if year.isdigit() and int(year)>=1900 and int(year)<=2020:
        return int(year)


                


form = """
    <form method="post">
        What is your birthday?
        <br/>
        <label> Month
            <input type="text" name = "month" placeholder ="month" value="%(month)s">
        </label>
        <label> Day
            <input type="text" name = "day" placeholder ="day" value="%(day)s">
        </label>
        <label> Year
            <input type="text" name = "year" placeholder ="year" value="%(year)s">
        </label>
        
        <div style="color: red">%(error)s</div>
        
        <br/>
        <br/>
        <input type= submit>
    </form>
"""

page = """
<form method="post">
<h1> Enter some text to ROT13: </h1>
<br/>
<textarea name = "text"   >%(text)s
</textarea>
<br/>
<br/>
<input type= "submit">
<br/>
</form>

"""



mainpage = """<!doctype html>
<html>
	<head>
		<title> Main Menu Paul's Udacity Project</title>
	</head>
	<body>
		<img src="https://lh3.ggpht.com/A0x3jzuH1qRkE10HcTiT4qQr_6iAqVg-CTsoIqxnoIFyv92V91WI3KqiVlOvLtfoMRg=w300" height="42" width="42" align ="left" hspace = "20";/>
		<h1>This is my Udacity project below is a list of things I've made so far.</h1>
	
		<p> This is the list</p>
		
		<table cellpadding= "20">
                    <tr>
                        <td> <a  STYLE="text-decoration: none" href='/rot13'> Rot 13 </a> </td>
                        <td> <a  STYLE="text-decoration: none" href='/signup'> Sign up </a> </td>
                        <td> <a  STYLE="text-decoration: none" href='/birthday'> Birthday </a> </td>
                        <td> <a  STYLE="text-decoration: none" href='/food'> Food </a> </td>
                        <td> <a  STYLE="text-decoration: none" href='/variablesub'> Variable Substitution </a> </td>
                        <td> <a  STYLE="text-decoration: none" href='/fizzbuzz'> Fizz Buzz </a> </td>
                        <td> <a  STYLE="text-decoration: none" href='/asciichan'> ASCII Chan </a> </td>
                    </tr>
                    <tr>
                        <td> <a  STYLE="text-decoration: none" href='/blog'> Blog </a> </td>
                        <td> <a  STYLE="text-decoration: none" href='/blog/newpost'> Post Blog Entry </a> </td>  
                        <td> <a  STYLE="text-decoration: none" href='/cookiepage'> Cookie Page </a> </td>
                        <td> <a href='/cookiepage'> <img src="https://s-media-cache-ak0.pinimg.com/236x/77/9b/9d/779b9dc3928c2dbc304bcf6702bef6df.jpg" alt="test" > </a> </td>

                        
                    </tr>
                    <tr>
                        <td>  </td>
                        <td>  </td>
                        <td>  </td>
                    </tr>
                </table>
                    
	</body>
</html>
"""

def escape_html(s):
    return cgi.escape(s, quote = True)

class MainHandler(Handler):
    def get(self):
        self.write(mainpage)


class BirthdayHandler(Handler):
    

    def write_form(self, error="", month="", day="", year=""):
        self.write(form % {"error": error,
                                        "month":escape_html(month),
                                        "day":escape_html(day),
                                        "year":escape_html(year)} )


    def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        self.write_form()
    def post(self):
        user_month = self.request.get('month')
        user_day = self.request.get('day')
        user_year = self.request.get('year')

        month = valid_month(user_month)
        day = valid_day(user_day)
        year = valid_year(user_year)

        if not (month and day and year):
            self.write_form("That doesnt look valid to me friend", user_month, user_day, user_year)
                            
        else:
            self.redirect("/thanks")
            
        
            

class ThanksHandler(Handler):
    def get(self):
            self.write("Thanks! Thats a totally rad date!")


class Rot13Handler(Handler) :

    def writerot_form(self, text=""):
        self.write(page  % {
                                            "text": escape_html(text)} )
    def get (self):
            self.writerot_form()

    def post (self):
            #user_newstring = self.request.get('rotval')
            text = rot13(self.request.get('text'))
            
            self.writerot_form( text)

class SignUpHandler(Handler):
                
        def get (self):
                self.render("signup-form.html")

        def post (self):
            have_error = False
            user_name = self.request.get('username')
            user_password = self.request.get('password')
            user_verify = self.request.get('verify')
            user_email = self.request.get('email')

            params = dict(username = user_name, email = user_email)

            if not valid_username(user_name):
                params['error_username'] = "That's not a valid username."
                have_error = True

            if not valid_password(user_password):
                params['error_password'] = "That's not a valid password."
                have_error = True

            elif user_password != user_verify:
                params['error_verify'] = "Your passwords didnt match."
                have_error = True

            if not valid_email(user_email):
                params['error_email'] = " That's not a valid email."
                have_error = True

            if have_error:
                self.render('signup-form.html', **params)
            else:
                self.redirect('/welcome?username='+ user_name)            

class WelcomeHandler(Handler):
        def get(self):
                username= self.request.get('username')
                self.write("Welcome " + username)




class FoodHandler(Handler):
    def get(self):

        items = self.request.get_all("food")
        self.render("shopping_list.html" , items = items )
        
        
class VariableSubHandler(Handler):
    def get(self):
        self.render("variablesub.html" , animal1 = self.request.get("animal1") , animal2 = self.request.get("animal2") )


        
class FizzBuzzHandler(Handler):
    def get(self):
        n = self.request.get('n', 0)
        n = n and int(n)
        self.render("fizzbuzz.html", n = n)


class Art(db.Model):
    title = db.StringProperty(required = True)
    art = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class AsciiChanHandler(Handler):

    def render_front(self, title="", art= "", error=""):
        arts = db.GqlQuery(" SELECT * FROM Art"
                            " ORDER BY created DESC")
        self.render("front.html", title = title, art = art, error =error, arts=arts)


    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")

        if title and art:
            a = Art(title = title, art = art)
            a.put()

            self.redirect("/asciichan")
        else:
            error = " We need both a title and some artwork!"
            self.render_front(title, art, error)

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)


class Post(db.Model):
    subject = db.StringProperty(required =True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p =self)

class BlogHandler(Handler):
    def get(self):
        posts = db.GqlQuery("select * from Post order by created desc limit 10")
        self.render('blog.html', posts = posts)

class PostPage(Handler):
    def get(self, blog_id):
        key = db.Key.from_path('Post', int(blog_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        self.render("permalink.html", post = post)

class PostBlogHandler(Handler):
   

    def get(self): 
        self.render("newpost.html")

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")

        if subject and content:
            p = Post(parent = blog_key(), subject = subject, content = content)
            p.put()
            self.redirect("/blog/%s" % str(p.key().id()))

        else:
            error = " We need both a title and a blog post!"
            self.render("newpost.html", subject = subject, content = content, error = error)
            
def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()

def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
    val = h.split('|')[0]
    if h == make_secure_val(val):
        return val



class CookiePageHandler(Handler):
    def get(self):
        self.response.headers['Content-Type'] = 'text-plain'
        visits = 0
        visit_cookie_str = self.request.cookies.get('visits')
        if visit_cookie_str:
            cookie_val = check_secure_val(visit_cookie_str)
            if cookie_val:
                visits = int(cookie_val)

        visits += 1
        new_cookie_val = make_secure_val(str(visits))
        
        self.response.headers.add_header('Set-Cookie', 'visits=%s' % new_cookie_val)
        if visits > 100000:
            self.write("You are the best ever!!! You've visited %s times!" % visits)
        else:
            self.write("You've been here %s times!" % visits)
        
class BlogSignUpHandler(Handler):

        def get (self):
            self.render("signup-form.html")

        def post (self):
            have_error = False
            user_name = self.request.get('username')
            user_password = self.request.get('password')
            user_verify = self.request.get('verify')
            user_email = self.request.get('email')

            params = dict(username = user_name, email = user_email)

            if not valid_username(user_name):
                params['error_username'] = "That's not a valid username."
                have_error = True

            if not valid_password(user_password):
                params['error_password'] = "That's not a valid password."
                have_error = True

            elif user_password != user_verify:
                params['error_verify'] = "Your passwords didnt match."
                have_error = True

            if not valid_email(user_email):
                params['error_email'] = " That's not a valid email."
                have_error = True

            if have_error:
                self.render('signup-form.html', **params)
            else:
                self.redirect('/blog/welcome?username='+ user_name)

       
class BlogWelcomeHandler(Handler):
    def get(self):
            username= self.request.get('username')
            self.write("Welcome " + username)
                



app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/thanks', ThanksHandler),
     ('/rot13', Rot13Handler), ('/signup', SignUpHandler) ,
      ('/welcome', WelcomeHandler) , ('/birthday', BirthdayHandler) ,
       ('/food', FoodHandler) , ('/variablesub', VariableSubHandler),
        ('/fizzbuzz', FizzBuzzHandler), ('/asciichan', AsciiChanHandler),
         ('/blog/?', BlogHandler), ('/blog/newpost', PostBlogHandler),
         ('/blog/([0-9]+)', PostPage), ('/cookiepage',CookiePageHandler),
         ('/blog/signup', BlogSignUpHandler), ('/blog/welcome', BlogWelcomeHandler)
], debug=True)
