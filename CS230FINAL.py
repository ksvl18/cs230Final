import numpy as np
import streamlit as st
import pandas as pd
import geopy
import pgeocode as pgc
from geopy import distance
import matplotlib.pyplot as plt
FNAME = 'f500hq.csv'
st.set_page_config(page_title = 'Jack Blaettler', page_icon= ":Shark")

st.title("Jack Blaettler's CS 230 Final Project")
df2 = pd.read_csv(FNAME)
df2 = df2.rename(columns = {'LATITUDE':'lat', 'LONGITUDE':'lon'})
df2['ZIP'] = df2['ZIP'].apply('{0:0>5}'.format)
df2 = df2.drop('COUNTY', axis = 1)
df2 = df2.sort_values('OBJECTID')

st.write('CLick Here to Accept Cookies')
st.button('CLICK HERE')

#ZIP
st.header('Find the Distance Between an Entered Zip Code and a Fortune 500 Headquarters')
st.sidebar.subheader('Find the Distance Between an Entered Zip Code and a Fortune 500 Headquarters')
def distance2(zip, name):
    a = list(df2.index[df2['NAME'] == name])
    c = int(a[0])
    zip2 = df2['ZIP'][c]
    nomi = pgc.Nominatim('us')
    b = nomi.query_postal_code(zip)
    d = nomi.query_postal_code(zip2)
    lat1 = b['latitude']
    lon1 = b['longitude']
    lat2 = d['latitude']
    lon2 = d['longitude']
    q = geopy.distance.distance((lat1,lon1),(lat2,lon2))
    st.write(f'{zip} is {q.mi:.2f} mi from {name} headquarters')
    distdict = {'lat':[lat1,lat2],'lon':[lon1,lon2]}
    distdf = pd.DataFrame(distdict)
    st.map(distdf)

def distance3(zip, name = 'COSTCO'):
    a = list(df2.index[df2['NAME'] == name])
    c = int(a[0])
    zip2 = df2['ZIP'][c]
    nomi = pgc.Nominatim('us')
    b = nomi.query_postal_code(zip)
    d = nomi.query_postal_code(zip2)
    lat1 = b['latitude']
    lon1 = b['longitude']
    lat2 = d['latitude']
    lon2 = d['longitude']
    q = geopy.distance.distance((lat1,lon1),(lat2,lon2))
    st.write(f'{zip} is {q.mi:.2f} mi from {name} headquarters')
    distdict = {'lat':[lat1,lat2],'lon':[lon1,lon2]}
    distdf = pd.DataFrame(distdict)
    st.map(distdf)
def balloon():
    st.balloons()

st.write('Select an Option, then Follow the Directions to See Some Distances')
findPick = st.sidebar.radio('Select an option: ', ['Find distance by ZIP and Name',
                                    'Find distance to Costco HQ'],
             help = 'Click on one to select'
             )

if findPick == 'Find distance by ZIP and Name':
    b = st.text_input('Enter Starting Zip: ')
    c = st.text_input('Enter Name of Company: ').upper()
    # -------------------------------------------------------------------------------------
    if b or c == '':
        st.warning('Please Enter a Zip Code and the Name of a Fortune 500 Company')
    distance2(b,c)
if findPick == 'Find distance to Costco HQ':
    f = st.text_input('Enter Starting Zip: ')
    if f == '':
        st.warning('Please Enter a Zip Code')
    distance3(f)


#Bar Chart
st.header('Show the Average Profit by State of the Fortune 500 Headquarters')
st.sidebar.subheader('Show the Average Profit by State of the Fortune 500 Headquarters')
st.write('Select States to See the Average Profit Compared')
st.warning('The Lower the Bar, The Higher the Average')
statesPick = st.sidebar.multiselect('Pick States to Compare: ',['CA','NY','TX','IL','OH' ,'VA' ,'NJ' ,'PA' ,'CT'
    ,'GA' ,'MN' ,'FL' ,'MI' ,'MA' ,'TN' ,'NC' ,'WA' ,'CO' ,'MO' ,'WI' ,'IN' ,'AR'
    ,'OK' ,'NE' ,'AZ' ,'MD' ,'RI' ,'KY' ,'IA' ,'LA' ,'DE' ,'ID' ,'DC' ,'KS' ,'OR'
    ,'NV' ,'AL' ,'UT'],help = 'Select One or More States to See the Average Profits')
b ={}
c = dict(df2.groupby('STATE')['PROFIT'].mean())
for i in range(len(statesPick)):
    a = statesPick[i]
    for key in c.keys():
        if key in statesPick:
            b[key] = c[key]
for i in b:
    b[i] = str(b[i])
f = pd.DataFrame(b.items(), columns= ['State','Average Profit'])
f.set_index('State', inplace = True)
st.bar_chart(f)

#Pie Chart
st.header('Show a Pie Chart of States that Fortune 500 Headquarters are in')
st.sidebar.subheader('Show a Pie Chart of States that Fortune 500 Headquarters are in')
west = ['CA','WA','AZ','ID','CO','MT','NV','NM','OR','UT','WY']
south = ['AL','AR','FL','GA','LA','MD','MS','NC','SC','TN','TX','VA','WV']
midwest = ['IL','IN','IA','KS','KY','MI','MN','MO','NE','ND','OH','OK','SD','WI']
northeast = ['CT','DE','ME','MA','NH','NJ','NY','PA','RI','VT']

regionList = ['West','South','Midwest','Northeast']
st.write('Select a Region to See the Proportion of '
         'Headquarters in the States of Those Regions')
regionPick = st.sidebar.selectbox('Pick a Region: ', regionList)

#st.write(df2['STATE'].value_counts())
valueList = [i for i in df2['STATE'].value_counts()]
stateList = list(df2['STATE'].value_counts().index.values)

pieList = []
pieListLabel = []
if regionPick == 'West':
    for i in range(len(stateList)):
        if stateList[i] in west:
            pieListLabel.append(stateList[i])
            pieList.append(valueList[i])
    fig1, ax1 = plt.subplots()
    ax1.pie(pieList, labels=pieListLabel,
            autopct='%1.2f%%', startangle=90,
            pctdistance = 1.5, labeldistance = 1.2,
            radius = 2,rotatelabels=True)
    ax1.axis('equal')
    st.pyplot(fig1)
if regionPick == 'South':
    for i in range(len(stateList)):
        if stateList[i] in south:
            pieListLabel.append(stateList[i])
            pieList.append(valueList[i])
    fig1, ax1 = plt.subplots()
    ax1.pie(pieList, labels=pieListLabel, autopct='%1.2f%%', startangle=90,
            pctdistance = 1.5, labeldistance = 1.2,
            radius = 2,rotatelabels=True)
    ax1.axis('equal')
    st.pyplot(fig1)
if regionPick == 'Midwest':
    for i in range(len(stateList)):
        if stateList[i] in midwest:
            pieListLabel.append(stateList[i])
            pieList.append(valueList[i])
    fig1, ax1 = plt.subplots()
    ax1.pie(pieList, labels=pieListLabel, autopct='%1.2f%%', startangle=90,
            pctdistance = 1.5, labeldistance = 1.2,
            radius = 2,rotatelabels=True)
    ax1.axis('equal')
    st.pyplot(fig1)
if regionPick == 'Northeast':
    for i in range(len(stateList)):
        if stateList[i] in northeast:
            pieListLabel.append(stateList[i])
            pieList.append(valueList[i])
    fig1, ax1 = plt.subplots()
    ax1.pie(pieList, labels=pieListLabel, autopct='%1.2f%%', startangle=90,
            pctdistance = 1.5, labeldistance = 1.2,
            radius = 2,rotatelabels=True)
    ax1.axis('equal')
    st.pyplot(fig1)

balloons = st.button('Click When Done')
if balloons:
    balloon()
    st.header('Congratulations!')
