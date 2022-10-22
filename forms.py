from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class CarForm(FlaskForm):
    mpg = StringField("MPG")
    fueltype = StringField("FuelType")
    address = StringField('Address')
    radius = StringField('Radius')
    submit = SubmitField('Submit')