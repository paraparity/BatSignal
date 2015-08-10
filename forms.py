from flask import Flask, render_template, flash, request
from werkzeug.datastructures import MultiDict
from wtforms import Form, TextField, TextAreaField, validators
from wtforms import validators
from wtforms.fields.html5 import EmailField

class  updateConfig(Form):
    admins = EmailField('admins', filters = [lambda x: x or None])
    phrases = TextField('phrases', filters = [lambda x: x or None])
