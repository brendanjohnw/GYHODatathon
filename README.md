# RHB Get Your Hack On Datathon 2022

Our goal was to build a dashboard that allows RHB to make data driven decisions on which areas to improve by using a machine learning powered sentiment analysis to study the language used in the feedback to understand customer grievances of various touch points

## Data Preprocessing 

We first streamlined and cleaned the data into processable segments python NLTK, lemmatizing and doing a binary classification on which customer accessed a particular touchpoint. The code would be able to process any csv file structured in the same format as the one provided. 

## Data Visualization and Analysis

We then used PowerBI and Azure ML’s Sentiment Analysis API to obtain visualizations and the the sentiment score for each feedback.

## Projected Improvements

Linking the Google Translate API to python to perform the translation on-site.
To link the cleaning and processing code in Python to PowerBI to seamlessly transform cleaned data into insightful visualizations

## Instructions
1. pip install the requirements for the software
```
  pip install -r requirements.txt

```
2. Open console.cloud.google.com and create a service account. Download the service account credentials as a .json file and place it in the same directory as your code.
3. In preprocessing.py under the bridge_API method, change the client credentials to the name of your JSON file
4. Run scheduler.py
5. If you wish to change the time interval, go to constants.py and change TIME_INTERVAL_MINUTES to any time interval in minutes you wish.
   Default value is set to 10 minutes.
7. Ensure that the csv file that is produced by the code is pointed to by powerBI
8. In powerBI change the source file to the file generated.
