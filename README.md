# GassedUp
Gets a list of gas station within a range, and returns the best deal based off the distance and the fuel economy of the car.

Directions:
1. Run main.py to run the Flask server.
2. From the browser, go to http://127.0.0.1:5001
3. Enter your car model, and press "Get Data"
   - Or enter MPG and Fuel Type manually
4. Enter the location
   - By default, this should get an location somewhere around your actual area
   - To be more precise, use your actual location
5. Choose the radius
   - 5 miles takes the least time, while 25 takes the longest
6. Press submit
   - In cases, of internal server error. Reset the server.

Requirements:
- Pandas
- Requests
- Flask
- Flask_wtf
- wtforms
- Geocoder
- Geopy


![Form](/images/form.png)
![Best Deal](/images/best.png)
![Table](/images/table.png)
