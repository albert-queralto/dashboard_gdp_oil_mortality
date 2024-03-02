Mortality Rate and Oil Consumption App
======================================

Introduction
------------

This Dash app visualizes mortality rates and oil consumption data for different countries. It allows users to select a year and see the mortality rates and oil consumption per capita for various continents. The app also includes a density contour map of the mortality rates for the selected year.

Features
--------

* Interactive bar charts for mortality rates and oil consumption per capita
* Density contour map of mortality rates for the selected year
* User can select a year using a slider
* Checkboxes allow users to filter the data by continent
* Animated transition between years

Usage
-----

1. Open the app by running `python app.py` in the terminal
2. Use the slider to select a year
3. Click on the checkboxes to filter the data by continent
4. Press the Play button to animate the transitions between years

Data
----

The app uses data from the World Bank (CC BY-4.0 license) to populate the mortality rates and oil consumption per capita. The data is stored in a Pandas dataframe and manipulated using various Pandas functions.

Visualization
------------

The app uses Plotly to create the interactive visualizations.

Credits
-------

Thanks to the World Bank for providing the data used in this app.

License
-------

This app is licensed under the MIT License.
