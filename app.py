import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import praw
import pandas as pd
import datetime as dt
from wordcloud import WordCloud, STOPWORDS

reddit = praw.Reddit(client_id='w0cDom4nIf5druip4y9zSw', \
                     client_secret='mtCul8hEucwNky7hLwgkewlLPzH0sg', \
                     user_agent='Profile extractor', \
                     username='CarelessSwordfish541', \
                     password='Testing@2022')

st.title('Just Reddit as it is 👀')

st.write('This is a simple web app to extract data from Reddit and analyze it.')

DATA_URL = 'subreddit_data_v1.csv'



@st.cache
def load_data():
    data = pd.read_csv(DATA_URL)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("Done! (using st.cache)")


if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

subreddit = st.selectbox('Select a subreddit', data['subreddit'].unique())

st.subheader('Wordcloud of the most common words in the subreddit')


comment_words = ''
stopwords = set(STOPWORDS)

# iterate through the csv file
for val in data[data['subreddit'] == subreddit]['title']:
    # typecaste each val to string
    val = str(val)

    # split the value
    tokens = val.split()

    # Converts each token into lowercase
    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()

    comment_words += " ".join(tokens)+" "

wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = stopwords,
                min_font_size = 10).generate(comment_words)

# plot the WordCloud image
plt.figure(figsize = (8, 8), facecolor = None)

plt.imshow(wordcloud)

plt.axis("off")

plt.tight_layout(pad = 0)
st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot()


#Based on the subreddit selected , show the statistics of the subreddit
st.subheader('Statistics of the subreddit')
st.write(data[data['subreddit'] == subreddit].describe())

#Based on the subreddit selected display the number of posts per day
st.subheader('Number of posts per day')
st.write(data[data['subreddit'] == subreddit].groupby('created')['title'].count())

#Based on the subreddit selected display the number of comments per day
st.subheader('Number of comments per day')
st.write(data[data['subreddit'] == subreddit].groupby('created')['num_comments'].sum())

#display a bar chart of the score of the posts
st.subheader('Score of the posts')
st.bar_chart(data[data['subreddit'] == subreddit]['score'])





# st.subheader('Number of pickups by hour')
# hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
# st.bar_chart(hist_values)

# # Some number in the range 0-23
# hour_to_filter = st.slider('hour', 0, 23, 17)
# filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

# st.subheader('Map of all pickups at %s:00' % hour_to_filter)
# st.map(filtered_data)


