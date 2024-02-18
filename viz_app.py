import pandas as pd
from statsbombpy import sb
from mplsoccer import Pitch
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
st.title("ShreeRamaJayam")

data=sb.competitions()

st.dataframe(data)

