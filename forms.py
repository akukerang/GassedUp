from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import geocoder

g = geocoder.ip('me')
coords = str(g.lat) + ", " + str(g.lng)
locator = Nominatim(user_agent="GassedUp")
location = locator.reverse(coords)
class CarForm(FlaskForm):
    mpg = StringField("MPG")
    fueltype = StringField("FuelType")
    address = StringField('Address',default=str(location))
    radius = StringField('Radius')

