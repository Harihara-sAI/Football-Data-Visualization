import pandas as pd
from statsbombpy import sb
from mplsoccer import Pitch
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
st.write("ShreeRamaJayam")
data= pd.read_csv("C:\Users\hahas\Downloads\Statsbomb 2015-16 event data")
st.dataframe(data)