# RHB Get Your Hack On Datathon 2022

Our goal was to build a dashboard that allows RHB to make data driven decisions on which areas to improve by using a machine learning powered sentiment analysis to study the language used in the feedback to understand customer grievances of various touch points

## Data Preprocessing (Brendan Lee)
The process we took to solve the problem is as follows:

We first streamlined and cleaned the data into processable segments python NLTK, lemmatizing and doing a binary classification on which customer accessed a particular touchpoint. The code would be able to process any csv file structured in the same format as the one provided. 

## Data Visualization and Analysis (Kong Yuki)

We then used PowerBI and Azure ML’s Sentiment Analysis API to obtain visualizations and the the sentiment score for each feedback.
