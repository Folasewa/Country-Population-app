import streamlit
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import joblib
import altair as alt
raw_data = pd.read_csv('countries.csv')

menu = ['Home','Predict', 'Maps']
Menu = streamlit.sidebar.selectbox('Menu', menu)
if Menu=='Home':

    streamlit.header('A Country Population App')
    streamlit.text('Sharbie prototype')
    streamlit.text('Predict a country population')
    country_name = streamlit.selectbox('Country Name', ['None selected'] + list(raw_data.countries.unique()))
    year = list(raw_data.year.unique())
    streamlit.write('Make a Chart of thè population of the countries against year')

    if country_name != 'None selected':
        df_bar = raw_data[raw_data.countries == country_name]
        df_bar.year = df_bar.year.astype('str')
        plotly_chart = px.bar(data_frame = df_bar,
        x='year',y='population', color='population', 
        width= 700, title = '{} population\'s chart'.format(country_name),)
        
        streamlit.plotly_chart(plotly_chart, use_container_width=True)
    if streamlit.checkbox('Graph by Year'):
        df1=raw_data
        df1.year = df1.year.astype('str')
        input_y = streamlit.multiselect('Year', list(raw_data.year.unique()))
        if len(input_y)>0:
            df1 = df1[df1.year.isin(input_y)]
        y_graph = alt.Chart(df1).transform_filter(alt.datum.population > 0).mark_line().encode(
            x = alt.X('country', title = 'Countries', type = 'nominal'),
            y = alt.Y('population', title = 'Population'),
            color= 'year',
            tooltip = ['population', 'figure', 'year', 'country']).properties(
                width = 1200, height = 600).configure_axis(
                    labelFontSize = 10, titleFontSize =11)
        streamlit.altair_chart(y_graph)
#country_name = streamlit.selectbox('Country Name', ['None selected'] + list(raw_data.countries.unique()))
#year = streamlit.selectbox('Selected Year', ['None selected'] + list(raw_data.year.unique()))


#loading the ML models
joblib.load('country_model/Nigeria.pkl')
joblib.load('country_model/New Zealand.pkl')
joblib.load('country_model/Niger.pkl')
joblib.load('country_model/Nicaragua.pkl')
joblib.load('country_model/Norway.pkl')


#Making predictions
if Menu == 'Predict':
    country_name = streamlit.selectbox('Country Name', ['None selected'] + list(raw_data.countries.unique()))
    year = streamlit.selectbox('Selected Year', ['None selected'] + list(raw_data.year.unique()))
    if streamlit.button('Predict Population'):
        if country_name !='None selected':
            if country_name and year:
                pred_data = pd.DataFrame([year],columns=['year'])
                model = joblib.load('country_model/' + country_name +  '.pkl')
                resp = int(model.predict(pred_data))
                streamlit.write('Population of {} in year {} is {:,}'.format(country_name, year,resp))
        else:
            streamlit.error('Kindly select a country')
    
#if Menu == 'Maps':
        