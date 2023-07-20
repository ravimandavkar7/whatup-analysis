import streamlit as st
import matplotlib.pyplot as plt

import helper
import preprocesser,helper
import ptvsd
import seaborn as sns

ptvsd.enable_attach(address=('0.0.0.0', 5678))

st.sidebar.title("wht up cht anlayiser")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
   bytes_data = uploaded_file.getvalue()
   data = bytes_data.decode("utf-8")
   df=preprocesser.preprocess(data)

   # fetch un
   # ique user

   user_list=df['user'].unique().tolist()
   user_list.remove('Taval Toli 💥✨')

   user_list.sort()
   user_list.insert(0,"All")
   selected_user=st.sidebar.selectbox("Analysis User",user_list)

   if st.sidebar.button("Show Analysis"):
      st.title("Total Analysis")

      num_messages,world,num_media_new,num_link=helper.fetch_stats(selected_user,df)

      col1, col2, col3, col4 = st.columns(4)

      with col1:
         st.header("Total Message")
         st.header(num_messages)

      with col2:
         st.header("Total world")
         st.header(world)

      with col3:
         st.header("Total Media")
         st.header(num_media_new)


      with col4:
         st.header("Total Links Shared")
         st.header(num_link)

      st.title("Monthly Time Line")
      df_timeline=helper.monthly_timline(selected_user, df)
      fig,ax=plt.subplots()
      ax.plot(df_timeline['time'], df_timeline['message'])
      plt.xticks(rotation='vertical')
      st.pyplot(fig)

      st.title("Weekly Activity")
      col1, col2 = st.columns(2)

      with col1:
         # Assuming selected_user and df are defined correctly before this point
         print("Selected user:", selected_user)
         df_weekly_activity = helper.weekly_activity(selected_user, df)
         print("Weekly activity DataFrame:", df_weekly_activity)

         if df_weekly_activity is not None:
            fig, ax = plt.subplots()
            ax.bar(df_weekly_activity.index, df_weekly_activity.values,color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
         else:
            st.write("No data available for the selected user.")

      with col2:
         # Assuming selected_user and df are defined correctly before this point
         print("Selected user:", selected_user)
         df_monthly_activity = helper.Monthly_activity(selected_user, df)
         print("Weekly activity DataFrame:", df_monthly_activity)

         if df_monthly_activity is not None:
            fig, ax = plt.subplots()
            ax.bar(df_monthly_activity.index, df_monthly_activity.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
         else:
            st.write("No data available for the selected user.")

      if selected_user=='All':

         st.title('Busy User')
         fig, ax =plt.subplots()
         x,df_new=helper.bussiest_user(df)

         col1, col2 = st.columns(2)
         with col1:
            ax.bar(x.index, x.values)
            st.pyplot(fig)
         with col2:
            st.dataframe(df_new)

      # Heatmap

      st.title("User Active Time")
      user_heatmap=helper.activity_heatmap(selected_user, df)
      fig,ax=plt.subplots()
      ax=sns.heatmap(user_heatmap)
      st.pyplot(fig)

      #wordcloud
      st.title("WordCloud")
      df_wc=helper.create_worldcloud(selected_user,df)
      fig,ax=plt.subplots()
      ax.imshow(df_wc)
      st.pyplot(fig)

      #most common word
      most_common_df=helper.most_common_word(selected_user,df)
      fig,ax=plt.subplots()
      ax.barh(most_common_df[0],most_common_df[1],color='red')
      plt.xticks(rotation='vertical')
      st.title('Most Common Word')
      st.pyplot(fig)

      #Emoji Collection
      emoji_dataframe=helper.emoji_collection(selected_user,df)
      st.title("Emoji Analysis")
      col1,col2=st.columns(2)
      with col1:
         st.dataframe(emoji_dataframe)
      with col2:
         fig, ax = plt.subplots()

         ax.pie(emoji_dataframe[1].head(), labels=emoji_dataframe[0].head(), autopct="%0.2f")
         st.pyplot(fig)




