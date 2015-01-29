#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys
import logging

from flask import Flask, Response, g
from flask import render_template
from flask import abort, request, jsonify

from flask.ext.cors import CORS, cross_origin

import pandas as P
import sqlite3 as DBM
import re

import phonology

normalizer = phonology.get_normalisation_func("hokkien")
analyzer = phonology.get_analyseur_func("hokkien")

# create our little application :)
app = Flask(__name__)
app.debug = False
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
app.config['CORS_HEADERS'] = 'Content-Type'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = DBM.connect("data.sqlite3")
    return db

# API URLs
@app.route('/')
def home(name=None):
    return render_template('index.jade', name=name)

@app.route('/lookup/trs/<query>')
@cross_origin(send_wildcard=False)
def lookup_trs(query):
    try:
        norm = normalizer(query)
        # remove tones
        norm = re.sub("[14]","_",norm)
        dbh = get_db()
        df = P.read_sql("SELECT forme FROM ime WHERE normalisation LIKE ?", dbh, params=(norm,))
        strict_result = df.forme.values
        return "|".join(strict_result)
    except:
        return ""

@app.route('/api/lecture/<langue>/<query>')
def json_by_lecture(langue,query):
    return jsonify({'caracteres': 3, 'expressions': 1})

# RUN
def main():
    app.run("0.0.0.0", 8042)

if __name__ == '__main__':
    sys.exit(main())
