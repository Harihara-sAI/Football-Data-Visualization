import pandas as pd
from statsbombpy import sb
from mplsoccer import Pitch
from mplsoccer import VerticalPitch
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
st.title("Top 5 Leagues Data Visualizations from 2015/16 season - Hariharasai Mohan")
st.text("This app uses Statsbomb's Open Data to make visualizations for particular teams")

sb.competitions()


@st.cache
def get_league_data(i):
    league_matches=sb.matches(competition_id=str(i),season_id='27')
    return league_matches

#Premier_League=get_league_data(2)
#Ligue_1=get_league_data(7)
#Bundesliga=get_league_data(9)
#La_Liga=get_league_data(11)
#Serie_A=get_league_data(12)

leagues=["Premier League", "La Liga", "Bundesliga", "Serie A", "Ligue 1"]

opt1=st.selectbox("Choose the League", options=leagues)



def get_league(a):
    if a=="Premier League":
        league=get_league_data(2)
    if a=="La Liga":
        league=get_league_data(11)
    if a=="Bundesliga":
        league=get_league_data(9)
    if a=="Ligue 1":
        league=get_league_data(7)
    if a=="Serie A":
        league=get_league_data(12)
    return(league)



def get_teams(opt1):
    
    league=get_league(opt1)
    teams=league["home_team"].unique()
    return(teams)

team=get_teams(opt1)

opt2=st.selectbox("Choose the Team", options=team)


def get_team_matches(league,team):
    away_matches=league[league["away_team"]==str(team)]
    away_matches[['Opponent Name']]=pd.DataFrame(away_matches.home_team.to_list(), index=away_matches.index)
    home_matches=league[league["home_team"]==str(team)]
    home_matches[['Opponent Name']]=pd.DataFrame(home_matches.away_team.to_list(), index=home_matches.index)
    matches=pd.concat([home_matches,away_matches],ignore_index=True)
    return(matches)

matches=get_team_matches(get_league(opt1), opt2)

matches_list=matches[['match_id']]
match_ids=matches_list['match_id'].to_list()

match_list=[]
for i in range(len(matches)):
    a=f"{matches['home_team'][i]} versus {matches['away_team'][i]}"
    match_list.append(a)

opt3=st.selectbox("Choose the Match", options=match_list)

m=match_ids[match_list.index(opt3)]

match=sb.events(match_id=m)

match=match[['team','type','pass_type','location','pass_end_location','player','under_pressure','pass_outcome']].reset_index()
match=match[(match['team']==opt2) & (match['type']=='Pass') &(match['under_pressure']==True) ]

match[['x_start', 'y_start']]=pd.DataFrame(match.location.to_list(), index=match.index)
match[['x_end', 'y_end']]=pd.DataFrame(match.pass_end_location.to_list(), index=match.index)



def make_pass_plot(pass_data):
    pitch=Pitch(pitch_type='statsbomb')
    fig, ax = pitch.draw(figsize=(15,8))
    success=pd.isnull(pass_data['pass_outcome'])
    s_passes=match[success]
    us_passes=match[~success]
    s_x_start=s_passes['x_start'].to_list()
    s_x_end=s_passes['x_end'].to_list()
    s_y_start=s_passes['y_start'].to_list()
    s_y_end=s_passes['y_end'].to_list()
    us_x_start=us_passes['x_start'].to_list()
    us_x_end=us_passes['x_end'].to_list()
    us_y_start=us_passes['y_start'].to_list()
    us_y_end=us_passes['y_end'].to_list()

    pitch.scatter(s_x_start,s_y_start,c='green',ax=ax,label='Origin of successful pass')
    pitch.scatter(us_x_start,us_y_start,c='red',ax=ax,label='Origin of unsuccessful pass')
    lc1=pitch.lines(s_x_start, s_y_start, s_x_end, s_y_end, lw=3, comet=True, color='green', ax=ax, label='Successful Passes',transparent=True)
    lc2=pitch.lines(us_x_start, us_y_start, us_x_end, us_y_end, lw=3, comet=True, color='red', ax=ax, label='Unsuccessful Passes',transparent=True)
    lgn=ax.legend(facecolor='white', edgecolor='black', fontsize=10, loc='upper left', handlelength=7)
    ax.set_title(f"{opt2}: Passes made under Pressure in {opt3}, 2015/16", fontsize=18)
    
    return(fig)

bor_dor_match=sb.events(match_id=m)
bor_dor_match_shot_data=bor_dor_match[['team','type','shot_type','shot_technique','location','player','shot_outcome','shot_statsbomb_xg']].reset_index()

shots=bor_dor_match_shot_data[(bor_dor_match_shot_data['team']==opt2) & (bor_dor_match_shot_data['type']=='Shot') ]
shots[['x_start', 'y_start']]=pd.DataFrame(shots.location.to_list(), index=shots.index)



def make_shot_plot(shot_data):
    pitch = VerticalPitch(pad_bottom=0.5,  half=True,  goal_type='box')
    fig , ax =pitch.draw(figsize=(15,8))
    penalty=shot_data['shot_outcome']=='Penalty'
    open_play_shots=shot_data[~penalty]
    penalty_shots=shot_data[penalty]
    #['Wayward', 'Blocked', 'Off T', 'Goal', 'Saved']
    
    Wayward_shots=shot_data[shot_data['shot_outcome']=='Wayward']
    Blocked_shots=shot_data[shot_data['shot_outcome']=='Blocked']
    Off_T_shots=shot_data[shot_data['shot_outcome']=='Off T']
    Saved_shots=shot_data[shot_data['shot_outcome']=='Saved']
    Goals=shot_data[shot_data['shot_outcome']=='Goal']

    wayward=pitch.scatter(Wayward_shots['x_start'], Wayward_shots['y_start'],s=((Wayward_shots['shot_statsbomb_xg']*500)+100), marker='^',edgecolors='#000000',c='#c70000',ax=ax, label='Wayward shots')

    off_t=pitch.scatter(Off_T_shots['x_start'], Off_T_shots['y_start'],s=((Off_T_shots['shot_statsbomb_xg']*500)+100), marker='X',edgecolors='#000000',c='#006f3c',ax=ax, label='Off Target')

    blocked=pitch.scatter(Blocked_shots['x_start'], Blocked_shots['y_start'],s=((Blocked_shots['shot_statsbomb_xg']*500)+100), marker='h',edgecolors='#000000',c='#f9a73e',ax=ax, label='Blocked')

    saved=pitch.scatter(Saved_shots['x_start'], Saved_shots['y_start'],s=((Saved_shots['shot_statsbomb_xg']*500)+100), marker='o',edgecolors='#000000',c='#264b96',ax=ax, label='Saved')

    goals=pitch.scatter(Goals['x_start'], Goals['y_start'],s=((Goals['shot_statsbomb_xg']*500)+100), marker='football',edgecolors='#000000',ax=ax, label='Goals')

    lgn=ax.legend(facecolor='#4a4e69', edgecolor='white',labelcolor='white', fontsize=20, loc='lower left')
    for handle in lgn.legend_handles:
        handle.set_sizes([100.0])
    ax.set_title('(Greater size refers to greater xG)', fontsize=10)
    fig.suptitle(f"{opt2}: Shots attempted in {opt3}, 2015/16", fontsize=18)
    
    return(fig)


a=st.button("Plot", type="secondary")

if a:
    st.pyplot(make_shot_plot(shots))
    st.pyplot(make_pass_plot(match))
