from flask import Flask, request, Response, render_template
import requests
import itertools
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Regexp, ValidationError
import re


class WordForm(FlaskForm):
    avail_letters = StringField("Letters", validators= [
        Regexp(r'^$|^[a-z]+$', message="must contain letters only")
    ])
    pattern = StringField("Pattern", validators=[
        Regexp(r'^$|^[a-z.]+$', message="must be regex pattern")
    ])
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
        print("hello")
        letters = form.avail_letters.data 
        word_length = form.word_length.data
        pattern = form.pattern.data 
        if word_length == '':
            x = 0
        else:
            x = int(word_length)
        if len(pattern) > x and x != 0:
            return render_template("index.html", form=form, name="Michael Sadaghyani", error='Pattern length is greater than word length')
        if len(pattern) == 0:
            pattern = "^[a-z]+$"
        elif len(pattern) <= x and len(pattern) != 0:
            x = len(pattern) 
            pattern = "^" + pattern + "$"
    else:
        return render_template("index.html", form=form, name="Michael Sadaghyani")
    with open('sowpods.txt') as f:
        good_words = set(x.strip().lower() for x in f.readlines()) 
    word_set = set() 
    if letters == '':
        for word in good_words:
            if x == 0:
                wlist = re.findall(pattern, word)
                if len(wlist) != 0:
                    word_set.add(wlist[0])
                    wlist.clear 
            elif len(word) <= x: 
                wlist = re.findall(pattern, word)
                if len(wlist) != 0:
                    word_set.add(wlist[0])
                    wlist.clear 
    else: 
        for l in range(3, len(letters)+1):
            for word in itertools.permutations(letters,l):
                w = "".join(word) 
                if w in good_words and x == 0:
                    wlist = re.findall(pattern, w)
                    if len(wlist) != 0:
                        word_set.add(wlist[0])
                        wlist.clear
                elif w in good_words and len(w) <= x: 
                    wlist = re.findall(pattern, w)
                    if len(wlist) != 0:
                        word_set.add(wlist[0])
                        wlist.clear  
    word_set = sorted(word_set, key=lambda x: (len(x), x))
    return render_template('wordlist.html', wordlist=word_set, name="Michael Sadaghyani")

@app.route('/get-def')
def getDef():
    word = request.args.get('word')
    url = 'https://www.dictionaryapi.com/api/v3/references/collegiate/json/' + word + '?key=b4648064-9416-46e0-b3d9-a94733cc65d3'
    response = requests.get(url)
    resp = Response(response.text)
    resp.headers['Content-Type'] = 'application/json'
    return resp 



# https://www.dictionaryapi.com/api/v3/references/collegiate/json/test?key=b4648064-9416-46e0-b3d9-a94733cc65d3
