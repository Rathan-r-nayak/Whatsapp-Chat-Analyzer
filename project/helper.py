from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
from PIL import ImageFont


extract = URLExtract()



def fetch_stats(usr,df):
    if usr!='Overall':
        df=df[df['user']==usr]

    cont=df.shape[0]
    w=[]
    for i in df['messages']:
        w.extend(i.split())
    words=len(w)
    media=df[df['messages']=='<Media omitted>\n'].shape[0]

    links=[]
    for i in df['messages']:
        links.extend(extract.find_urls(i))

    return cont,words,media,len(links)


def monthly_timeline(usr,df):
    if (usr != 'Overall'):
        df = df[df['user'] == usr]
    timeline = df.groupby(['year','month_num','month_name']).count()['messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month_name'][i] + '-' + str(timeline['year'][i]))
    
    timeline['time'] = time
    return timeline

def daily_timeline(usr,df):
    if(usr != 'Overall'):
        df = df[df['user'] == usr]
    
    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()
    return daily_timeline


def weakActivityMap(usr,df):
    if(usr != 'Overall'):
        df = df[df['user'] == usr]
    
    return df['day_name'].value_counts()

def monthActivityMap(usr,df):
    if(usr != 'Overall'):
        df = df[df['user'] == usr]
    
    return df['month_name'].value_counts()

def activityHeatMap(usr,df):
    if(usr != 'Overall'):
        df = df[df['user'] == usr]
    
    user_heatmap = df.pivot_table(index = 'day_name', columns='period',values = 'messages',aggfunc='count').fillna(0)
    return user_heatmap


def mostBusyUsers(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(
        columns={'index':'name','user':'percent'})
    return x,df

def wordCloudDef(usr,df):
    # f = open('stop_hinglish.txt','r')
    # stop_words = f.read()

    if(usr != 'Overall'):
        df = df[df['user'] == usr]
    
    # temp = df[df['user'] != 'group_notification']
    # temp = temp[temp['msg'] != '<Media omitted>\n']

    # def removeStopWords(message):
    #     y = []
    #     for word in message.lower().split():
    #         if word not in stop_words:
    #             y.append(word)
    #     return " ".join(y)
    
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    # temp['msg'] = temp['msg'].apply(removeStopWords)
    df_wc = wc.generate(df['msg'].str.cat(sep=" "))
    return df_wc



def mostCommonWords(usr,df):
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    
    if(usr != 'Overall'):
        df = df[df['user'] == usr]
    
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']

    words = []

    for mseg in temp['messages']:
        for word in mseg.lower().split():   #my Name Is => ['my','name','is']
            if word not in stop_words:
                words.append(word)
    

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def emojiHelper(usr,df):
    if(usr != 'Overall'):
        df = df[df['user'] == usr]
    
    emojis = []

    for mesg in df['messages']:
        emojis.extend([c for c in mesg if c in emoji.UNICODE_EMOJI['en']])
    
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df