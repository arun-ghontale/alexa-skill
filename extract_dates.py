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
    if date_start_slot == 'NA' and date_end_slot == 'NA':
        return "Invalid time period format"

    elif date_start_slot == 'NA' or date_end_slot == 'NA':
        date = date_start_slot if date_start_slot != 'NA' else date_end_slot
        date = tuple([int(i) for i in date_start_slot.strip().split(':')])
        date_range = (date[0]*60*60+date[1]*60,date[0]*60*60+date[1]*60+60)

        logs_in_range = []
        every_timestamp_log = {}
        for each_log,eachTime,date_hour_format in zip(dataframe['Logs'].values,dataframe['TimeStampSeconds'].values,dataframe['TimeStamp'].values):
            for each_of_log,each_date_hour_format in zip(eachTime,date_hour_format):
                if each_of_log >= date_range[0] and each_of_log <= date_range[1]:
                    date_temp = str(each_date_hour_format['hour'])+':'+str(each_date_hour_format['minute'])+':'+str(each_date_hour_format['second'])
                    logs_in_range.append(each_log)

                    if date_temp not in every_timestamp_log:
                        every_timestamp_log[date_temp] = [each_log]
                    else:
                        every_timestamp_log[date_temp].append(each_log)


        return [list(set(logs_in_range)),every_timestamp_log]

    else:
        date_start = tuple([int(i) for i in date_start_slot.strip().split(':')])
        date_end = tuple([int(i) for i in date_end_slot.strip().split(':')])


        date_start = date_start[0]*60*60+date_start[1]*60
        date_end = date_end[0]*60*60+date_end[1]*60
        date_range = sorted([date_start,date_end])

        logs_in_range = []
        every_timestamp_log = {}
        for each_log,eachTime,date_hour_format in zip(dataframe['Logs'].values,dataframe['TimeStampSeconds'].values,dataframe['TimeStamp'].values):
            for each_of_log,each_date_hour_format in zip(eachTime,date_hour_format):
                if each_of_log >= date_range[0] and each_of_log <= date_range[1]:
                    date_temp = str(each_date_hour_format['hour'])+':'+str(each_date_hour_format['minute'])+':'+str(each_date_hour_format['second'])
                    logs_in_range.append(each_log)

                    if date_temp not in every_timestamp_log:
                        every_timestamp_log[date_temp] = [each_log]
                    else:
                        every_timestamp_log[date_temp].append(each_log)


        return [list(set(logs_in_range)),every_timestamp_log]

    return [[],{}]

def load_dates(SAVE_DF = True):
    Logs = []
    regxPattern = r'\s+\d+:\d+:\d+[.]'
    dates = []
    with open('logfile.txt') as f:
        for eachLine in f.read().split('\n\n'):
            if eachLine.strip():
                Logs.append(eachLine)
                dates.append(list(set([formatTime(eachTime) for eachTime in re.findall(regxPattern,eachLine)])))

    #only upto minutes for now
    datesFormatted = [[{'hour':eachDate[0],'minute':eachDate[1],'second':eachDate[2]} for eachDate in date] if date else {} for date in dates]
    # datesFormatted = [[{'hour':eachDate[0],'minute':eachDate[1]} for eachDate in date] if date else {} for date in dates]
    secondsFormat = [tuple(set([int(eachDate.get('hour',0))*60*60+int(eachDate.get('minute',0)*60)+int(eachDate.get('second',0)) for eachDate in date])) for date in datesFormatted]

    df = pd.DataFrame({'Logs':Logs,'TimeStamp':datesFormatted,'TimeStampSeconds':secondsFormat})
    #remove dataframe rows with no Timestamps
    df = df[df['TimeStamp'] != {}]
    df.fillna('',inplace = True)

    if SAVE_DF:
        df.to_pickle('log_file.pkl')
        df_unpickled = pd.read_pickle('log_file.pkl')
        # print(df_unpickled[df_unpickled['TimeStamp'] == {}].shape)

    return df


if __name__ == '__main__':
    df = load_dates()
    return_value = parseLogs('8:01','8:05',df)
    print(len(return_value[0]))
    for each in return_value[1].keys():
        print(each,len(return_value[1][each]))
