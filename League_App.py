# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 03:38:52 2022

@author: Andriu
"""

import time 
import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt

st.set_page_config(page_title='League Comps API',page_icon=':ringed_planet:')

# st.image('https://i.imgur.com/WXbv7Bw.png')
st.image('https://i.imgur.com/G1m6Q1r.png')

st.title('LEAGUE COMP CREATION API')

#%% CLASS DEFINITION

class TEAM:
    
    def __init__(self, data):  
        
        self.AP = list(data.iloc[:,0].dropna().index)
        self.AD = list(data.iloc[:,1].dropna().index)
        self.TANK = list(data.iloc[:,2].dropna().index)
        self.seed = np.nan
        self.comp = []
        
    def create(self):
       
        now = dt.datetime.now()
        time = (now.year*now.month*now.day)+(now.hour*now.minute*now.second) + now.microsecond
        time = int(time)
        np.random.seed(time)
        
        self.seed = time
        
        ap = self.AP[np.random.randint(len(self.AP))]
        ad = self.AD[np.random.randint(len(self.AD))]
        tank = self.TANK[np.random.randint(len(self.TANK))]
        
        self.comp = (ap, ad, tank)
        
#%% FUNCION DEFINITION

@st.cache
def load_data():
    
    url = "https://github.com/AndriuFEN/League_Compos/blob/main/Champion_Pool.xlsx?raw=true"
    data = pd.read_excel(url)
    data.set_index('Campeon',drop=True,inplace=True)

    return data

def create_teams(n,pool):
    teams = []
    for i in range(n):
        t = TEAM(pool)
        t.create()
        teams.append(t)
        time.sleep(0.2)
    return teams

def creating_teams(n,pool):
    team_creation_state = st.text('Creating teams...')
    teams = create_teams(n, pool)
    team_creation_state.text('All teams created!')
    return teams

#%% LOAD DATA

# # Create a text element and let the reader know the data is loading.
# data_load_state = st.text('Loading data...')

# Apply function
data = load_data()

# # Notify the reader that the data was successfully loaded.
# data_load_state.text("Data Loading Done!")

#%% TEAM CONFIGURATION

st.header('Setup your teams')

n = st.number_input(label="Comps Number",min_value=1,value=2)
tz = st.radio(label="Team Size", options=['3v3','4v4','5v5], horizontal=True)

                                          
                                          
#%% TEAM CREATION

cr = st.button('CREATE')

if cr:
    if tz=='3v3':                                      
        teams = creating_teams(n, data)
    
        for i in range(len(teams)):
            st.write('Comp '+str(i+1))
            st.table(pd.DataFrame(teams[i].comp,index=['AP','AD','TANK'],columns=['Pick']))
            st.balloons()                                          
    else:
        st.write('WORK IN PROGRES...!')
    cr = False

#%% 

st.write('App made by Andriu.')

