# AJAX Flask Contact Form One Page App

A super simple AJAX flask contact me page. Using python 2.7 and flask 0.10.1
  - Responsive
  - Using CSS3 form validation and some very basic server side validation
  - AJAX form submission via jquery
  - Can be configured to send contact form information off via email with mandrillapp api to a designated email address. Stores messages via an sqlite database for redundancy
  - Includes uwsgi conf, nginx conf, upstart conf

See it here [matt.sammar.co](https://matt.sammar.co)

###Getting it going - ubuntu...
- Sign up for mandrill app account and add your key in the contact_app.py file to send emails. You can also choose to use an smtp implementation. A code comment is left for how this done in contact_app.py. Messages are stored in a simple sqlite database for some redundancy. This version in master uses the mandrill api, mostly because I wanted to check out how it worked, and the analytics it offers. More information at http://mandrill.com/
- Install nginx, uwsgi and pip then...
```sh
$ sudo apt-get update && sudo apt-get install nginx && sudo apt-get install uwsgi
$ pip install -r requirements.txt
```
- Run the init.py script to create your sqlite3 database and initialize the logging file
```sh
$ python init.py
```
- Test you can run the flask app via the command line
```sh
$ python contact_app.py
```
- Configure nginx-contact-page.conf and enable it (change locations to your installation). Restart nginx
- Configure uwsgi in the contact-page-uwsgi.ini file (change locations to your installation)
- Check permissions and users are correct at this moment too
- Run it via the command line to test uwsgi is working
```sh
$ uwsgi --ini ..../uwsgi-contact-one-pager.ini
```
- Add uwsgi as an upstart service by editing and copying over upstart-contact-page.ini to /etc/init/ Don't forget to reload with 'initctl reload'. Start the service and you should be good to go. When in doubt, check the logs.
