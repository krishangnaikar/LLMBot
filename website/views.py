from flask import Blueprint, render_template, request, url_for, session, redirect
import SlackBot.privateGPT as private
import login_classes
import time

views = Blueprint(__name__, "views")

SESSION_TIMEOUT = 1800

session_start_times = {}

@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get username and password from the POST request
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        potential_id = login_classes.users.login(username, password)
        if potential_id == False:
            return {'username':False}#render_template('login.html')
        else:
            session['session_id'] = potential_id
            session['username'] = username
            session_start_times[username] = time.time()
            session['permission'] = login_classes.users.get_user_by_username(username).permission

        return {'username':username}#redirect(url_for('views.chat'), code=302)
    else:
        return render_template('login.html')

@views.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get username and password from the POST request
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        login_classes.users.new_user(username, password)
        session['username'] = login_classes.users.get_user_by_username(username).username
        session['session_id'] = login_classes.SessionId().get_latest_session_id()
        session_start_times[username] = time.time()
        session['permission'] = login_classes.users.get_user_by_username(username).permission
        return {'username':username}
    else:
        return render_template('register.html')

@views.route('/chat', methods=['GET', 'POST'])
def chat():

    print(session)
    try:
        if 'username' not in session:
            return redirect('/login')
    except Exception:
        return redirect('/login')

    username = session.get('username')

    if username in session_start_times:
        session_start_time = session_start_times[username]
        if time.time() - session_start_time > SESSION_TIMEOUT:
            del session['username']
            del session_start_times[username]
            return 'Session expired. Please log in again.'

    return render_template('index.html', username=session.get('username'), sessionid=session.get('session_id'), permission=session.get('permission'))

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@views.route('/query', methods=['POST'])
def query():
    if request.method == 'POST':
        print("POST Request")
        query = request.form['query']
        permission = request.form['permission']
        result = private.main(query, permission)
        return render_template('result.html', query=result[0], answer=result[1])
