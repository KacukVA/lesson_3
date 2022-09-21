from flask import Flask, render_template, request
from faker import Faker
import requests
import random
import os


app = Flask(__name__)


@app.route('/requirements/', methods=['get'])
def requirements():
    context = {}
    file_name = 'requirements.txt'
    if not os.path.exists(file_name):
        os.system(f'pip freeze > {file_name}')
    with open(file_name, 'r') as f:
        context['content'] = f.read().split()
    return render_template('requirements.html', **context)


@app.route('/generate-users/', methods=['get', 'post'])
def generate_users():
    context = {}
    if request.method == 'POST':
        emails_amount = int(request.form['emails_amount'])
        domains = ['@gmail.com', '@yahoo.com', '@ukr.net', '@outlook.com']
        fake = Faker()
        emails = [fake.name().replace(' ', '.').lower() + random.choice(domains) for _ in range(emails_amount)]
        context['emails'] = emails
    return render_template('generate-users.html', **context)


@app.route('/space/', methods=['get'])
def space():
    context = {}
    try:
        r = requests.get('http://api.open-notify.org/astros.json')
        context['astro_number'] = len(r.json()["people"])
    except OSError:
        ...
    return render_template('space.html', **context)


if __name__ == '__main__':
    app.run()
