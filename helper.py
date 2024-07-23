import pandas as pd

def preprocess(df,region_df):
    
    df=df[df['Season']=='Summer']
    # We can Know the Country by thier NOC.
    df=df.merge(region_df,how='left',on='NOC')
    
    df.drop_duplicates(inplace=True)
    df=pd.concat([df,pd.get_dummies(df['Medal']).astype(int)],axis=1)
    return df

def medal_tally(df):
    # So,we are deleting rows with same 'Team','NOC','Games','Year','City','Sport','Event','Medal'
    medal_tally=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])

    medal_tally=medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_tally['Total']=medal_tally['Bronze']+medal_tally['Gold']+medal_tally['Silver']
    return medal_tally

def contry_year_list(df):
    years=df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')

    country=df['region'].dropna().unique().tolist()
    country.sort()
    country.insert(0,'Overall')

    return years,country

def fetch_medal_tally(df,year,country):
    medal_df=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag=0
    if year == 'Overall' and country=='Overall':
        temp_df=medal_df
    elif year=='Overall' and country!='Overall':
        flag=1
        temp_df=medal_df[medal_df['region']==country]
    elif year!='Overall' and country=='Overall':
        temp_df=medal_df[medal_df['Year']==year]
    else:
        temp_df=medal_df[(medal_df['Year']==year) & (medal_df['region']==country)]
        
    if flag==1:
        x=temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year',ascending=True).reset_index()
    else:   
        x=temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
        
    x['Total']=x['Bronze']+x['Gold']+x['Silver']
    return x

def data_overtime(df,col):
    year_wise_count=df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('Year')
    year_wise_count.rename(columns={'Year':'Edition','count':col},inplace=True)
    
    return year_wise_count

def heatmap_Events(df):
    x=df.drop_duplicates(['Year','Sport','Event'])
    return x

def most_successful(df,sport):
    # Droping rows with medal as nan
    temp_df=df.dropna(subset=['Medal'])

    if sport!='Overall':
        temp_df=temp_df[temp_df['Sport']==sport]
    #So,Now we have Athletes wrt to sport,who won Medals only.(reset_index is to convert into Dataframe)
    # taking Top 10 Only 
    x=temp_df['Name'].value_counts().reset_index().head(10).merge(df,how='left',on='Name')[['Name','count','Sport','region']].drop_duplicates('Name')
    #Reanaming Column
    x.rename(columns={'count':'Medals'},inplace=True)
    x.reset_index(inplace=True)
    x=x.drop(columns='index')
    return x

def country_wise_Medaltally(df,country):
    temp_df=df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    temp_df=temp_df[temp_df['region']==country]
    final_df=temp_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_sport_medal_overyears(df,selected_country):
    temp_df=df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    new_df=temp_df[temp_df['region']==selected_country]
    return new_df

def most_successful_in_country(df,country):
    # Droping rows with medal as nan
    temp_df=df.dropna(subset=['Medal'])

    temp_df=temp_df[temp_df['region']==country]
    #So,Now we have Athletes wrt to country,who won Medals only.(reset_index is to convert into Dataframe)
    # taking Top 10 Only 
    x=temp_df['Name'].value_counts().reset_index().head(10).merge(df,how='left',on='Name')[['Name','count','Sport']].drop_duplicates('Name')
    #Reanaming Column
    x.rename(columns={'count':'Medals'},inplace=True)
    x=x.reset_index()
    x=x.drop(columns='index')
    return x

def weight_vs_height(df,sport):
    athlete_df=df.drop_duplicates(subset=['Name','region'])
    athlete_df['Medal'].fillna('No Medal',inplace=True)
    temp_df=athlete_df[athlete_df['Sport']==sport]
    return temp_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final

