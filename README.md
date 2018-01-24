# [CarbonSteps](http://13.71.121.212)
[CarbonSteps](http://13.71.121.212) is a website, hosted on Azure, to check the carbon footprint made by people like you and us over a month. It calculates the total amount of carbon emission by using [Google Timeline](https://www.google.com/maps/timeline?pb) data and the average carbon emissions emitted by the car specified.
**Site hosted on:** [http://13.71.121.212](http://13.71.121.212)

## Explanation
### Google Timeline Data
Google provides its user to view his/her data like [timeline](https://takeout.google.com/settings/takeout/custom/location_history) to check what all it tracks. This data is then parsed and computed upon to calculate the distance one spent on road. The file is uploaded by the user manually.

### How does it identify the car?
To calculate total emissions produced, knowing the specific model of the car is necessary. For that, the image uploaded by the user is sent to [Orpix Inc.](http://www.orpix-inc.com/vehicle-recognition/) which uses its cognitive service to recognize the make, model and the year of the car.

### Calculation
The data received is then searched through our database to find its average emission in g/km. The emission rate is then multiplied by the total distance on road to obtain the approximate emission in grams.

#### The parsing and calculation of the data is performed for the whole month before showing the results on the page.
