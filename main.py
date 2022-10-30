from flask import Flask, render_template, request
from forms import GasForm
from gas import *
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = "amongus"
def getLocation(address):
    locator = Nominatim(user_agent="GassedUp")
    location = locator.geocode(address)
    return location.latitude, location.longitude 

@app.route('/', methods=['GET', 'POST'])
def home():
    form = GasForm()
    radii = [25,15,10,5]
    stationList = pd.read_csv('stationList.csv')
    cars = pd.read_csv('vehicles.csv')
    if request.method == 'POST':
        if request.form['submit_button'] == 'Submit':
            result = request.form
            addrLatitude = getLocation(result.get('address'))[0]
            addrLongitude = getLocation(result.get('address'))[1]
            if (result.get('fueltype') == 'Regular' or result.get('fueltype') == 'regular'):
                fuelTypeId = '1'
            elif (result.get('fueltype') == 'Midgrade' or result.get('fueltype') == 'midgrade'):
                fuelTypeId = '2'
            elif (result.get('fueltype') == 'Premium' or result.get('fueltype') == 'premium'):
                fuelTypeId = '3'
            elif (result.get('fueltype') == 'Diesel' or result.get('fueltype') == 'diesel'):
                fuelTypeId = '4'
            else:
                fuelTypeId = '1'
            getStationList(float(result.get('radii')), float(addrLatitude), float(addrLongitude), fuelTypeId, float(result.get('mpg')))
            stationList = pd.read_csv('stationList.csv')
        elif request.form['submit_button'] == 'Get Data':
            result = request.form
            if result.get('model') != '':
                model = result.get('model')
                form.mpg.data = cars.loc[cars['carModel'] == model]['combMPG'].values[0]
                form.fueltype.data = cars.loc[cars['carModel'] == model]['fuelType'].values[0]
        else:
            pass
    return render_template("index.html", 
    form=form, radii=radii, carMakes = cars.carModel.values.tolist(),
    tables=[stationList.to_html(escape=False,index_names=False)],  stationList = stationList)



if __name__ == '__main__':
    app.run('0.0.0.0', port=5001)

