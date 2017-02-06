import datetime, sys
from flask import Flask, redirect, render_template, request, session, url_for, send_from_directory
import json
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = 'A0Zr98j/3yXR~XHH!jmN]LWX/,?RR'
server_path = 'http://127.0.0.1:5000'
exp_time = datetime.timedelta(seconds=2 * 3600)


@app.route('/client-api/home')
def home():
    if session.get('token') and not_expired():
        return render_template('home.html')
    return render_template('login.html')


@app.route('/client-api/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user, password = request.form['username'], request.form['password']
        if not user or not password:
            return render_template('login.html')
        data = {'username': user, 'password': password}
        url = server_path + "/api/login"
        headers = {'Content-Type': 'application/json'}
        req = requests.post(url, data=json.dumps(data), headers=headers)
        res = req.json()
        # print (req.json())
        if 'access_token' in res:
            session['token'] = res['access_token']
            session['exp'] = datetime.datetime.utcnow() + exp_time
        return redirect(url_for('home'))
    return render_template('login.html')


@app.route('/client-api/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username, password = request.form['username'], request.form['password']
        if not username or not password:
            return render_template('register.html')
        data = {'username': username, 'password': password}
        url = server_path + "/api/register"
        headers = {'Content-Type': 'application/json'}
        req = requests.post(url, data=json.dumps(data), headers=headers)
        # print (req.json())
        res = req.json()
        if res['message'] == 'Username is not unique':
            return render_template('register.html')
        return redirect(url_for('login'))
    return render_template('register.html')


def not_expired():
    return datetime.datetime.utcnow() < session['exp']


@app.route("/client-api/notes", methods=['GET'])
def get_notes():
    if request.method == 'GET' and session.get('token') and not_expired():
        token = session.get('token')
        url = server_path + '/api/notes'
        headers = {'Content-Type': 'application/json', 'Authorization': "JWT " + token}
        req = requests.get(url, headers=headers)
        # print(req.json())
        res = req.json()
        return render_template('notes.html', res=res)
    return redirect(url_for('home'))



@app.route("/client-api/notes/new", methods=['GET', 'POST'])
def new_note():
    if session.get('token') and not_expired():
        if request.method == 'POST':
            token = session.get('token')
            title, content, category, tag = request.form['title'], request.form['content'], \
                                            request.form['category'], request.form['tag']
            if title and content and category and tag:
                # tags should look like: "#tag1, #tag2"
                array = tag.split(', ')
                array = [i[1:] for i in array]
                data = {'title': title, 'content': content, 'category': category, 'tag': array.__str__()}
            else:
                return render_template('note-new.html')
            url = server_path + '/api/notes'
            headers = {'Content-Type': 'application/json', 'Authorization': "JWT " + token}
            req = requests.post(url, data=json.dumps(data), headers=headers)
            if req.status_code == 201:
                return redirect(url_for('get_notes'))
        return render_template('note-new.html')
    return redirect(url_for('home'))


@app.route("/client-api/notes/<int:note_id>", methods=['GET'])
def get_note(note_id):
    if session.get('token') and not_expired():
        if request.method == 'GET':
            token = session.get('token')
            url = server_path + '/api/notes/' + str(note_id)
            headers = {'Content-Type': 'application/json', 'Authorization': "JWT " + token}
            req = requests.get(url, headers=headers)
            print(req.json())
            res = req.json()
            if 'note_id' in res:
                return render_template('note.html', res=res, token=token)
            return redirect(url_for('get_notes'))
    return redirect(url_for('home'))


@app.route("/client-api/tags/<tag>", methods=['GET'])
def get_notes_by_tag(tag):
    if request.method == 'GET' and session.get('token') and not_expired():
        token = session.get('token')
        url = server_path + '/api/tags/' + tag
        headers = {'Content-Type': 'application/json', 'Authorization': "JWT " + token}
        req = requests.get(url, headers=headers)
        # print req.json()
        res = req.json()
        return render_template('note-by-tag.html', res=res)
    return redirect(url_for('home'))


@app.route("/client-api/categories/<category>", methods=['GET'])
def get_notes_by_category(category):
    if request.method == 'GET' and session.get('token') and not_expired():
        token = session.get('token')
        url = server_path + '/api/categories/' + category
        headers = {'Content-Type': 'application/json', 'Authorization': "JWT " + token}
        req = requests.get(url, headers=headers)
        # print (req.json())
        res = req.json()
        return render_template('note-by-category.html', res=res)
    return redirect(url_for('home'))


@app.route("/client-api/logout")
def logout():
    session.clear()
    return render_template('login.html')


@app.route('/client-api/static/style.css')
def css():
    return send_from_directory('static', 'style.css')


@app.route('/client-api/static/js.js')
def js():
    return send_from_directory('static', 'js.js')


if __name__ == '__main__':
    app.run(port=8888, debug=True)

