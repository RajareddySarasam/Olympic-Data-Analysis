import streamlit as st
import pandas as pd
import helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff


df=pd.read_csv('athlete_events.csv')
region_df=pd.read_csv('noc_regions.csv')

df=helper.preprocess(df,region_df)
st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://cdn.pixabay.com/photo/2016/08/20/17/58/olympic-games-1608127_1280.png')
user_menu=st.sidebar.radio('Select an Option',
                 ('Medal Tally','Overall analysis','Country-wise Analysis','Athlete-wise Analysis')
                 )


if user_menu=='Medal Tally':

    st.sidebar.title('Medal Tally')
    years,country=helper.contry_year_list(df)

    selected_year=st.sidebar.selectbox('Select a Year',years)
    selected_country=st.sidebar.selectbox('Select a Country',country)

    medal_tally=helper.fetch_medal_tally(df,selected_year,selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    else :
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")

    st.table(medal_tally)

if user_menu == 'Overall analysis':

    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('Olympics Statistics')

    col1,col2,col3=st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    year_wise_count=helper.data_overtime(df,'region')
    fig=px.line(year_wise_count,x='Edition',y='region')
    st.title('No. of Participating Nations Overtime')
    st.plotly_chart(fig)

    year_wise_count=helper.data_overtime(df,'Event')
    fig=px.line(year_wise_count,x='Edition',y='Event')
    st.title('No. of Events Overtime')
    st.plotly_chart(fig)

    year_wise_count=helper.data_overtime(df,'Name')
    fig=px.line(year_wise_count,x='Edition',y='Name')
    st.title('No. of Althlete Overtime')
    st.plotly_chart(fig)

    x=helper.heatmap_Events(df)
    fig,ax=plt.subplots(figsize=(20,20))
    ax=sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot=True)
    st.title('No. of Events over time for Every Sport')
    st.pyplot(fig)

    sports=df['Sport'].unique().tolist()
    sports.sort()
    sports.insert(0,'Overall')
    selected_sport=st.selectbox('Select Sport',sports)
    st.title('Top 10 Athletes '+str(selected_sport))
    x=helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu=='Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')

    #line plot
    countries=df['region'].dropna().unique().tolist()
    countries.sort()
    countries.insert(0,'India')
    selected_country=st.sidebar.selectbox('Select Country',countries)
    st.title(str(selected_country)+"'s Medal Tally Over the Years")
    final_df=helper.country_wise_Medaltally(df,selected_country)
    fig=px.line(final_df,x='Year',y='Medal')
    st.plotly_chart(fig)

    #HeatMap
    new_df=helper.country_sport_medal_overyears(df,selected_country)
    st.title(str(selected_country)+"'s Medals for sport Over the Years")
    plt.figure(figsize=(15,15))
    sns.heatmap(new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(plt)

    # Top 10 Athletes in country
    st.title('Top 10 Athletes in '+str(selected_country))
    x=helper.most_successful_in_country(df,selected_country)
    st.table(x)

if user_menu=='Athlete-wise Analysis':
    # Age Distribution by medals
    athlete_df=df.drop_duplicates(subset=['Name','region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age by Medals")
    st.plotly_chart(fig)


    # Distribution of Age w.r.t Sports(Gold Medalist)
    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        # Onlly for Gold Medalists.
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age w.r.t Sports(Gold Medalist)")
    st.plotly_chart(fig)


    # Height vs weight - sport

    
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Archery')

    selected_sport = st.selectbox('Select a Sport', sport_list)
    st.title('Height vs Weight in '+str(selected_sport))

    temp_df = helper.weight_vs_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax=sns.scatterplot(temp_df,x='Weight',y='Height',hue='Medal',style='Sex',s=50)
    st.pyplot(fig)


    # Men vs Womenn Participation
    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)





