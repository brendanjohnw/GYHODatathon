"""This code cleans and processes the data in the google sheet. Translation is done on the Google Sheet using Macros
    The code should be scheduled to run every 24 hours using a scheduler to pull data for pre-processing from the google sheet
    Ensure that PowerBI points to the same Cleaned_dataset.csv file that the python script generates """

import re
import time

import schedule
from googletrans import Translator
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

import pandas as pd
import nltk
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('omw-1.4')

lemmatizer = WordNetLemmatizer()
translator = Translator()


import gspread
from oauth2client.service_account import ServiceAccountCredentials
def bridge_API():
    scope = ["https://spreadsheets.google.com/feeds",
             'https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive.file',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name("GYHODatathon/rhb-project-339208-947e7de8b753.json", scope)
    client= gspread.authorize(credentials)
    sheet = client.open("Feedback Sheet Translated").sheet1

    return sheet


def preprocessing(text):
    extract_except = '[^A-Za-z ]+'
    text = re.sub(extract_except," ",text)
    text = (text.lower()).replace('\t\n'," ")
    # tokenizing
    token_text = [lemmatizer.lemmatize(word, pos = 'n')
                  for word in word_tokenize(text)
                  if not word in stopwords.words()]

    return token_text

def classify(all_customer_touchpoints):
    all_touchpoint_binary_class = []
    # [Counts, Positive, Negative]
    type_of_service = {"Human-based services":0, "Digital services":0, "Infrastructure":0}
    for customer_touchpoint in all_customer_touchpoints:
        touchpoint_binary_class = ["No", "No", "No", "No", "No", "No", "No"]
        for touchpoint in customer_touchpoint:

            if touchpoint == 'Social media':
                touchpoint_binary_class[0] = "Yes"
                type_of_service["Digital services"] += 1
                continue
            elif touchpoint == 'Call centre':
                touchpoint_binary_class[1] = "Yes"
                type_of_service["Human-based services"] += 1
                continue
            elif touchpoint == 'Branch':
                touchpoint_binary_class[2] = "Yes"
                type_of_service["Infrastructure"]+= 1
                continue
            elif touchpoint == 'RHB Internet Banking':
                touchpoint_binary_class[3] = "Yes"
                type_of_service["Digital services"] += 1
                continue
            elif touchpoint == 'RHB Mobile Banking Application':
                touchpoint_binary_class[4] = "Yes"
                type_of_service["Digital services"] += 1
                continue
            elif touchpoint == 'Relationship managers / Personal Bankers':
                touchpoint_binary_class[5] = "Yes"
                type_of_service["Human-based services"] += 1
                continue
            elif touchpoint == 'ATM, Cash Deposit Machines':
                touchpoint_binary_class[6] = "Yes"
                type_of_service["Infrastructure"] += 1
                continue

        all_touchpoint_binary_class.append(touchpoint_binary_class)

    return all_touchpoint_binary_class, type_of_service


def process_script():

    data = bridge_API().get_all_records()
    feedback_data = pd.DataFrame(data)

    lemmatized_sentences = []
    for sentence in feedback_data['Feedback']:
        lemmatized_sentence = preprocessing(str(sentence))
        lemmatized_sentences.append(" ".join(lemmatized_sentence))
    id_touchpoint = feedback_data[['ID', 'Touchpoint']]


    feedback_words = pd.DataFrame(lemmatized_sentences, columns = ["Feedback Words"])
    all_customer_touchpoints = []
    for touchpoint in id_touchpoint['Touchpoint']:
        split_touchpoint = touchpoint.split(';')[2:]
        resulting_touchpoint = []
        for item in split_touchpoint:
            if item not in ['item&gt','/item&gt', '&lt', '', '']:
                item = item.replace('&lt','')
                resulting_touchpoint.append(item)
        all_customer_touchpoints.append(resulting_touchpoint)

    pd.DataFrame(all_customer_touchpoints)
    touchpoint_list = ["Social media",
                       "Call centre",
                       "Branch",
                       "RHB Internet Banking",
                       "RHB Mobile Banking Application",
                       "Relationship managers / Personal Bankers",
                       'ATM, Cash Deposit Machines']
    touchpoint_df = pd.DataFrame(columns = touchpoint_list)


    all_touchpoint_binary_class, type_of_service = classify(all_customer_touchpoints)
    Main_df = pd.DataFrame(all_touchpoint_binary_class, columns =touchpoint_list, dtype = str)
    Main_df["Feedback"] = feedback_words
    Main_df["Rating"] = feedback_data['Rating']

    from gensim.summarization import keywords
    keyword_list = []
    for feedback in Main_df["Feedback"]:
        keyword_list.append(" ".join(keywords(feedback).split('\n')))


    Main_df["Detected Keywords"] = pd.DataFrame(keyword_list, columns = ["Keywords"])
    Main_df.to_csv("Cleaned_dataset.csv")
    print("Updated dataset exported")


def scheduler():
    schedule.every(10).minutes.do(process_script)
    process_script()
    while True:
        schedule.run_pending()
        time.sleep(1)

scheduler()



