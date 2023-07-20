import re
import pandas as pd


def preprocess(data):
    pattern = '\[\d{1,2}\/\d{1,2}\/\d{1,2},\s\d{1,2}:\d{1,2}:\d{1,2}\s(?:PM|AM|am|pm)\]\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'].str.strip(), format='[%d/%m/%y, %I:%M:%S %p]')
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # username
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group message')
            messages.append([entry[0]])
    df['user'] = users
    df['message'] = messages

    df.drop(columns=['user_message'], inplace=True)
    df['year'] = df['message_date'].dt.year
    df['month_num'] = df['message_date'].dt.month
    df['Month_Name'] = df['message_date'].dt.month_name()
    df['Day'] = df['message_date'].dt.day
    df['day_name'] = df['message_date'].dt.day_name()
    df['Hours'] = df['message_date'].dt.hour
    df['Minute'] = df['message_date'].dt.minute
    df['Second'] = df['message_date'].dt.second

    period = []
    for hour in df[['day_name', 'Hours']]['Hours']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str("00") + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
