from flask import Blueprint, render_template, request, session, redirect, jsonify
import privateGPT as private

try:
    import login_classes
except ModuleNotFoundError:
    import website.login_classes
import time

views = Blueprint(__name__, "views")
# Time to session timeout in milliseconds
SESSION_TIMEOUT = 1800 # 30 mins

session_start_times = {}

# /login route
@views.route('/login', methods=['GET', 'POST'])
def login():
    # Calling via POST method (requesting using code)
    if request.method == 'POST':
        # Get username and password from the POST request
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        # Check if valid user
        potential_id = login_classes.users.login(username, password)
        if potential_id == False:
            return {'username':False}#render_template('login.html')
        else:
            # Logging in and creating new session
            session['session_id'] = potential_id
            session['username'] = username
            session_start_times[username] = time.time()
            session['permission'] = login_classes.users.get_user_by_username(username).permission

        return {'username':username}#redirect(url_for('views.chat'), code=302)
    else:
        # going to localhost/login via browser
        return render_template('login.html')

# /register route
@views.route('/register', methods=['GET', 'POST'])
def register():
    # Calling via POST method (requesting using code)
    if request.method == 'POST':
        # Get username and password from the POST request
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        # Creating new username and password
        login_classes.users.new_user(username, password)

        # Creating new session
        session['username'] = login_classes.users.get_user_by_username(username).username
        session['session_id'] = login_classes.SessionId().get_latest_session_id()
        session_start_times[username] = time.time()
        session['permission'] = login_classes.users.get_user_by_username(username).permission
        return {'username':username}
    else:
        # going to localhost/register via browser
        return render_template('register.html')

# logout button
@views.route('/logout', methods=['POST'])
def logout():
    # Erasing session
    session.clear()
    return jsonify(success=True), 200

# localhost/chat
@views.route('/chat', methods=['GET', 'POST'])
def chat():

    print(session)
    try:
        if 'username' not in session:
            return redirect('/login')
    except Exception:
        return redirect('/login')

    username = session.get('username')

    # checking if current user is in the valid sessions
    if username in session_start_times:
        session_start_time = session_start_times[username]
        # If the session has timed out, log in again
        if time.time() - session_start_time > SESSION_TIMEOUT:
            del session['username']
            del session_start_times[username]
            return 'Session expired. Please log in again.'
    else:
        # Reseting session timer
        session_start_times[username] = time.time()

    return render_template('index.html', username=session.get('username'), sessionid=session.get('session_id'), permission=session.get('permission'))

# Home page
@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

# Only accessable using Post request (via code)
@views.route('/query', methods=['POST'])
def query():
    if request.method == 'POST':
        print("POST Request")
        # Getting details
        query = request.form['query']
        permission = request.form['permission']
        # calling privateGPT.main and passing query and permission
        result = private.main(query, permission)
        # returning result and query to post it on to the /chat directory
        return {'query':result[0], 'answer':result[1]}#render_template('result.html', query=result[0], answer=result[1])
