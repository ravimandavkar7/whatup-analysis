from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
import emoji
from collections import Counter

extractor=URLExtract()
def fetch_stats(selected_user,df):

    if selected_user != 'All':
        df= df[df['user'] == selected_user]
    num_message = df.shape[0]
    # number of world
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch no of media messages
    # num_media = df[df['message'].isin(['\u200evideo omitted\n', '\u200eimage omitted\n'])].shape[0]
    num_media_new = df[df.message=='\u200evideo omitted\n'].shape[0]
    # fetch no of link shared
    link = []
    for message in df['message']:
       link.extend(extractor.find_urls(message))


    return num_message, len(words), num_media_new,len(link)

def bussiest_user(df):
    x = df['user'].value_counts().head()
    df=round(df['user'].value_counts() / df.shape[0] * 100, 2).reset_index().rename(columns={'index': 'User', 'user': 'Percentage'})
    return x,df

def create_worldcloud(selected_user,df):
    if selected_user != 'All':
        df = df[df['user'] == selected_user]
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc=wc.generate(df['message'].str.cat(sep=" "))
    return df_wc
# most common word

def most_common_word(selected_user, df):
    if selected_user != 'All':
        df= df[df['user'] == selected_user]

    temp = df[df['user'] != 'Taval Toli 💥✨']
    temp = temp[temp['message'] != '\u200eimage omitted\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            words.append(word)
            from collections import Counter

    most_common_df=pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_collection(selected_user, df):
    if selected_user != 'All':
        df= df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_dataframe=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_dataframe

#monthly timeline
def monthly_timline(selected_user,df):
    if selected_user!= 'All':
        df=df[df['user']==selected_user]

    timeline = df.groupby(['year', 'month_num', 'Month_Name']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month_Name'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return  timeline

#weekly activity
def weekly_activity(selected_user,df):
    if selected_user!= 'All':
        df=df[df['user']==selected_user]

    return df['day_name'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user!= 'All':
        df=df[df['user']==selected_user]

    user_heatmap=df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap

def Monthly_activity(selected_user,df):
    if selected_user!= 'All':
        df=df[df['user']==selected_user]

    return df['Month_Name'].value_counts()
