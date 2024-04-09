import streamlit as st
import preprocess
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whats app chat analyzer")

uploaded_file=st.sidebar.file_uploader("Choose a File")



if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode('utf-8')
    df=preprocess.preprocessing(data)
    st.dataframe(df)



    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')


    usr=st.sidebar.selectbox("Show Analysis of:",user_list)

    if st.sidebar.button("show analysis"):#,media,num_links
        num_msg,words,media,links=helper.fetch_stats(usr,df)

        st.title("Top Statistics")
        col1,col2,col3,col4=st.columns(4)

        with col1:
            st.header("Toatal messages")
            st.title(num_msg)
        with col2:
            st.header("total words")
            st.title(words)
        with col3:
            st.header("total media")
            st.title(media)
        with col4:
            st.header("total links")
            st.title(links)
        
        #monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(usr,df)

        fig,ax = plt.subplots()
        timePlot = timeline['time'].to_numpy()  # Convert to numpy array
        msgPlot = timeline['messages'].to_numpy() 

        ax.plot(timePlot,msgPlot,color = 'green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        #daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(usr,df)

        fig,ax = plt.subplots()
        onlyDate = daily_timeline['only_date'].to_numpy()
        msgPlot = daily_timeline['messages'].to_numpy()

        ax.plot(onlyDate , msgPlot,color = 'black')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        
        #activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("most busy day")
            busy_day = helper.weakActivityMap(usr,df)

            fig,ax = plt.subplots()

            ax.bar(busy_day.index,busy_day.values,color = 'purple')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy Day")
            busy_month = helper.monthActivityMap(usr,df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color = 'purple')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

        st.title("Weakly Activity Map")
        user_heatmap = helper.activityHeatMap(usr,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)


        if(usr == 'Overall'):
            st.title("Most Busy Users")
            x,new_df = helper.mostBusyUsers(df)
            fig,ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # st.title("Word Cloud")
        # df_word_cloud = helper.wordCloudDef(usr,df)
        # fig,ax = plt.subplots()
        # ax.imshow(df_word_cloud)
        # st.pyplot(fig)
            
        st.title("Most Common Wrods")
        most_commong_df = helper.mostCommonWords(usr,df)
        fig,ax = plt.subplots()
        ax.barh(most_commong_df[0],most_commong_df[1])
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)
        
        
        # st.title("Emoji Analysis")
        # emoji_df = helper.emojiHelper(usr,df)
        
        # col1,col2 = st.columns(2)

        # with col1:
        #     st.dataframe(emoji_df)
        # with col2:
        #     fig,ax = plt.subplots()
        #     ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(),autopct = "%0.2f")
        #     st.pyplot(fig)