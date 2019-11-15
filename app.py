from flask import Flask, request, Response, render_template
import requests
import itertools
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Regexp, ValidationError
import re 



class WordForm(FlaskForm):
    avail_letters = StringField("Letters")
    pattern = StringField("Pattern")
    word_length = SelectField(u'Word Length', choices=[('', ''), ('3', 3), ('4', 4), ('5', 5), ('6',6), ('7',7), ('8',8), ('9',9), ('10',10)])
    submit = SubmitField("Go")

    
csrf = CSRFProtect()
app = Flask(__name__)
app.config["SECRET_KEY"] = "row the boat"
csrf.init_app(app)

@app.route('/')
def index():
    form = WordForm() 
    return render_template("index.html", form=form, name="Michael Sadaghyani")


@app.route('/words', methods=['POST', 'GET'])
def letters_2_words():
    form = WordForm()
    if form.validate_on_submit():
        letters = form.avail_letters.data 
        word_length = form.word_length.data
        pattern = form.pattern.data 
    else:
        return render_template("index.html", form=form)
    with open('sowpods.txt') as f:
        good_words = set(x.strip().lower() for x in f.readlines()) 
    if word_length == '':  # if word length is blank we return all lengths 
        x = 0
    else:
        x = int(word_length)
    word_set = set() 
    if letters == '':
        for word in good_words:
            if x == 0:
                wlist = re.findall("^" + pattern + "$", word)
                if len(wlist) != 0:
                    word_set.add(wlist[0])
                    wlist.clear 
            elif len(word) <= x: 
                wlist = re.findall("^" + pattern + "$", word)
                if len(wlist) != 0:
                    word_set.add(wlist[0])
                    wlist.clear 
    else: 
        for l in range(3, len(letters)+1):
            for word in itertools.permutations(letters,l):
                w = "".join(word) 
                if w in good_words and x == 0:
                    wlist = re.findall("^" + pattern + "$", w)
                    if len(wlist) != 0:
                        word_set.add(wlist[0])
                        wlist.clear
                elif w in good_words and len(w) <= x: 
                    wlist = re.findall("^" + pattern + "$", w)
                    if len(wlist) != 0:
                        word_set.add(wlist[0])
                        wlist.clear  
    word_set = sorted(word_set, key=lambda x: (len(x), x))
    return render_template('wordlist.html', wordlist=word_set, name="Michael Sadaghyani")


@app.route('/get-def', methods=['GET'])
def getDef():
    word = request.args.get('word')
    url = 'https://www.dictionaryapi.com/api/v3/references/collegiate/json/' + word + '?key=b4648064-9416-46e0-b3d9-a94733cc65d3'
    response = requests.get(url)
    resp = Response(response.text)
    resp.headers['Content-Type'] = 'application/json'
    return resp 



# https://www.dictionaryapi.com/api/v3/references/collegiate/json/test?key=b4648064-9416-46e0-b3d9-a94733cc65d3


# @app.route('/post')
# def post():
#     return render_template("form.html")


# @app.route('/words', methods=['POST', 'GET'])
# def letters_2_words():
#     with open('sowpods.txt') as f:
#         good_words = set(x.strip().lower() for x in f.readlines()) 
#         x = [] 
#         for words in good_words:
#             if len(words) <= 3:
#                 x.append(words) 
#     return render_template('wordlist.html', wordlist=x)




# @app.route('/')
# def hello_world():
#     return f"<p> Hello, World </p>"

# @app.route('/user/<username>')
# def show_user_profile(username):
#     return f'User {username}'