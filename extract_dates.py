import pandas as pd
import re

def formatTime(eachTime):
    eachTime = eachTime.strip()
    if eachTime:
        eachTime = re.sub(' +',' ',re.sub('[^0-9]',' ',eachTime))
        return tuple([int(i) for i in eachTime.split()])

    return eachTime

def parseLogs(date_start_slot,date_end_slot,dataframe):
    """Yet to be completed"""
    return ''

Logs = []
regxPattern = r'\s+\d+:\d+:\d+[.]'
dates = []
with open('logfile.txt',encoding = 'utf-8') as f:
    for eachLine in f.read().split('\n\n'):
        if eachLine.strip():
            Logs.append(eachLine)
            dates.append(list(set([formatTime(eachTime) for eachTime in re.findall(regxPattern,eachLine)])))

datesFormatted = [[{'hour':eachDate[0],'minute':eachDate[1],'second':eachDate[2]} for eachDate in date] if date else {} for date in dates]

df = pd.DataFrame({'Logs':Logs,'TimeStamp':datesFormatted})
#remove dataframe rows with no Timestamps
df = df[df['TimeStamp'] != {}]
df.fillna('',inplace = True)
df.to_pickle('log_file.pkl')

df_unpickled = pd.read_pickle('log_file.pkl')
print(df_unpickled.head())
print(df_unpickled[df_unpickled['TimeStamp'] == {}].shape)