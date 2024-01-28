from flask import Flask, Blueprint, request, render_template, url_for, redirect
import urllib.request
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

endpoint = 'https://mynginx9/pastebin/api'

app = Flask(__name__)
bp = Blueprint('mybp', __name__, 
               static_folder='static',
               static_url_path='/pastebin/static',
               template_folder='templates',
               url_prefix='/pastebin')

@bp.route(f'/', methods=['GET'])
@bp.route(f'/index.html', methods=['GET'])
def get_index():
    count_users = 0
    url = f'{endpoint}/users/'
    data = None
    headers = {'Accept': 'application/json'}
    method = 'GET'
    req = urllib.request.Request(url=url,
                                 data=data,
                                 headers=headers,
                                 method=method)
    try:
        with urllib.request.urlopen(req) as f:
            data = json.loads(f.read())
            count_users = len(data)
    except Exception as e:
        print(f"errors")
    count_pastes = 0
    url = f'{endpoint}/pastes/'
    data = None
    headers = {'Accept': 'application/json'}
    method = 'GET'
    req = urllib.request.Request(url=url,
                                 data=data,
                                 headers=headers,
                                 method=method)
    # try:
    with urllib.request.urlopen(req) as f:
        data = json.loads(f.read())
        count_pastes = len(data)
    # except Exception as e:
    #     print(f"errors")
    return render_template('index.html', 
                           count_users=count_users,
                           count_pastes=count_pastes)


@bp.route('/createuser', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        data = {'username': request.form['username'],
                'password': request.form['password']}
        headers = {'accept': 'application/json' ,
                   'Content-Type': 'application/json'}
        
        data = json.dumps(data).encode('utf-8')

        try:
            req = urllib.request.Request(f'{endpoint}/users/', data=data, headers=headers, method='POST')
            with urllib.request.urlopen(req) as response:
                if response.getcode() == 201:
                    return redirect(url_for('mybp.get_index'))
                else:
                    return "error"

        except Exception as e:
            print(f"Error: {e}")
            return "error"

    else:
        return render_template('createuser.html')
    
    
    
@bp.route('/createpaste', methods=['GET', 'POST'])
def create_paste():
    # try:
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        url_verify = f'{endpoint}/users/{username}/verify/?password={password}'
        data = None
        headers_verify = {'accept': 'application/json'}
        method_verify = 'GET'

        req_verify = urllib.request.Request(url=url_verify, data=data, headers=headers_verify, method=method_verify)
        with urllib.request.urlopen(req_verify) as f:
            user_data = json.loads(f.read())

        if 'id' not in user_data:
            return "Error: User authentication failed"

        url_create_paste = f'{endpoint}/users/{username}/pastes/?password={password}'
        data_create_paste = {'title': request.form['title'], 'content': request.form['content']}
        headers_create_paste = {'accept': 'application/json', 'Content-Type': 'application/json'}
        method_create_paste = 'POST'

        data_create_paste = json.dumps(data_create_paste).encode('utf-8')

        req_create_paste = urllib.request.Request(url=url_create_paste, data=data_create_paste, headers=headers_create_paste, method=method_create_paste)

        with urllib.request.urlopen(req_create_paste):
            pass
    # except Exception as e:
    #         print(f"Error: {e}")
    #         return "error"
    return render_template('createpaste.html')



@bp.route(f'/users/<username>/pastes', methods=['GET'])
def get_pastes(username):
    count_pastes = 0
    url = f'{endpoint}/pastes/'
    data = None
    headers = {'Accept': 'application/json'}
    method = 'GET'
    req = urllib.request.Request(url=url,
                                 data=data,
                                 headers=headers,
                                 method=method)
    try:
        with urllib.request.urlopen(req) as f:
            data = json.loads(f.read())
            count_pastes = len(data)
    except Exception as e:
        print(f"errors")
    try:
        response = urllib.request.urlopen(f'{endpoint}/users/{username}/pastes/')
        pastes = json.loads(response.read().decode('utf-8'))
        return render_template('getpastes.html', username=username, pastes=pastes, count_pastes = count_pastes)
    except Exception as e:
            print(f"errors")

app.register_blueprint(bp)


