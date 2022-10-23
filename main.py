from flask import Flask, render_template, request
from forms import CarForm
from gas import *
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pandas as pd
app = Flask(__name__)
app.config["SECRET_KEY"] = "thesussys"

def getLocation(address):
    locator = Nominatim(user_agent="GassedUp")
    location = locator.geocode(address)
    return location.latitude, location.longitude 

@app.route('/', methods=['GET', 'POST'])
def home():
    form = CarForm()
    radii = [5, 10, 15, 25]
    if form.is_submitted():
        result = request.form
        addrLatitude = getLocation(result.get('address'))[0]
        addrLongitude = getLocation(result.get('address'))[1]
        if (result.get('fueltype') == 'Regular' or result.get('fueltype') == 'regular'):
            fuelTypeId = '1'
        elif (result.get('fueltype') == 'Premium' or result.get('fueltype') == 'premium'):
            fuelTypeId = '2'
        tableData = getStationList(float(result.get('radii')), float(addrLatitude), float(addrLongitude), fuelTypeId, float(result.get('mpg')))
    return render_template("index.html",form=form, radii=radii, tables=[tableData.to_html(classes='data')], titles=tableData.columns.values)



if __name__ == '__main__':
    app.run()

