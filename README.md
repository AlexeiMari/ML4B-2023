# Journey-ML 
### (Created as a projetct for the course Machine Learning for Business (ML4B) at Friedrich-Alexander University in Germany)

JourneyML is a web application that leverages machine learning techniques to analyze and provide insights into user mobility patterns based on uploaded sensor data. 
By analyzing data from sensors such as accelerometer, location, and orientation, JourneyML generates a detailed timeline of the user's movements and offers various statistics related to their mobility.

## Features 
- Upload Sensor Data: Users can upload sensor data in either JSON format that contains all the sensor readings or a .zip file containing CSV files with sensor data.
  The data used for developement and testing was collected with the Sensor Logger app by Kelvin Tsz Hei Choi (https://play.google.com/store/apps/details?id=com.kelvin.sensorapp&hl=gsw&gl=US)
- Data Analysis: JourneyML applies machine learning algorithms to analyze the uploaded sensor data and generates a timeline of the user's movements.
- Mobility Statistics: The app provides a range of statistics, including the distribution of transportation modes, cumulative duration of each mode, and more, based on the uploaded data.
- GPS Data Visualization: JourneyML utilizes Google Maps to display the user's path as a visual representation, allowing users to visualize their journeys and trace the routes taken.

## Streamlit Site
This is the Link to our Streamlit site:
https://alexeimari-ml4b-2023-main-5a6h6b.streamlit.app/
The site is entirely on german. It contains a section explaining the developement process of this project.

## How to use
In order to use the App, it is required to upload sensor data containing accelerometer, orientation and location data. The ML model won't work if any of those sensors were not recorded.

## Trainingsdata for the Machine Learning Model
We collected the entire trainingsdataset by ourselves by recording different activities with the Sensor Logger App.

## Project Structure on GitHub
In the JupyterNotebooks folder is the Jupyter Notebook which implements the whole Data Preprocessing Pipeline and the Machine Learning parts. The main.py contains all the code for the Streamlit site to work.

Notebook: https://github.com/AlexeiMari/ML4B-2023/blob/main/JupyterNotebooks/Machine%20Learning%20and%20Dataprepro.ipynb

main.py: https://github.com/AlexeiMari/ML4B-2023/blob/main/main.py

Trainingsdata: https://github.com/AlexeiMari/ML4B-2023/blob/main/database_1min_split.csv

JSONs and CSVs for testing the JourneyML Website: https://github.com/AlexeiMari/ML4B-2023/tree/main/TestDataForWebsiteUse 

## Creators
Created by Rene Jokiel (@BelmontR) and Alexei Marinov (@AlexeiMari).
