import streamlit as st
import streamlit.components.v1 as components
import requests as req
import re
from bs4 import BeautifulSoup as BS
import time
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

components.html(
    """
    <div style= "color: #0F52BA; font-weight: bold; text-align: left; font-size: 40px; font-family: Trebuchet MS; box-shadow: 5px 5px 5px #ADD8E6" >
    <img src = "https://img.icons8.com/external-avoca-kerismaker/512/external-Stock-business-avoca-kerismaker.png" style="width: 40px; height: 40px"/>
    Live Stocks 24/7
    <div style= "color: grey; text-align: left; font-size: 10px; font-family: Trebuchet MS;" >
    v.1.0.0      Crawled live from Naver and Google
    <br></br>
    </div>
    </div>
    """,
    height=120,
)

components.html(
    """
    <div style= "color: #000040; font-weight: bold; text-align: left; font-size: 20px; font-family: Trebuchet MS" >
    Historical Interest Rates of US
    </div>
    """,
    height=30,
)


st.sidebar.subheader("Customize Plot Size")
width = st.sidebar.slider("Plot width", 1, 25, 10)
height = st.sidebar.slider("Plot height", 1, 25, 2)

df = pd.read_csv("static/interest.csv")
fig = plt.figure(figsize=(width, height))
ax = sns.kdeplot(data=df, x="INTDSRUSM193N")
ax.set(xlabel='', ylabel='IR(%)', xticklabels=[], yticklabels=[])
st.pyplot(fig)

components.html(
    """
    <div style= "color: #000040; font-weight: bold; text-align: left; font-size: 20px; font-family: Trebuchet MS" >
    </div>
    """,
    height=30,
)

with st.spinner(text="Live Crawling..."):
    time.sleep(5)
    st.success("Loading complete.")

url = "https://www.timeanddate.com/worldclock/south-korea/seoul"
res = req.get(url)
soup = BS(res.text, "html.parser")

for stat in soup.select("div.bk-focus__qlook"):
    now_time = stat.select("span.h1")[0].get_text(strip=True)
    st.write("Live Crawled Time: " + now_time)

components.html(
    """
    <div style= "color: #000040; font-weight: bold; text-align: left; font-size: 20px; font-family: Trebuchet MS" >
    Most Active Stocks
    </div>
    """,
    height=30,
)


col1, col2, col3 = st.columns([1, 1, 2], gap="large")

with col1:
    st.subheader("Naver")
    url = "https://finance.naver.com/sise/lastsearch2.naver"
    res = req.get(url)
    soup = BS(res.text, "html.parser")

    list_one = []

    for tr in soup.select("table.type_5 tr")[2:]:
        if len(tr.select("a.tltle")) == 0:
            continue
        title = tr.select("a.tltle")[0].get_text(strip=True)
        list_one.append(title)
        price = tr.select("td.number:nth-child(4)")[0].get_text(strip=True)
        change = tr.select("td.number:nth-child(6)")[0].get_text(strip=True)
        if len(list_one) >= 11:
            break
        st.write(title, price, change)

with col2:
    list_two = []

    st.subheader("Google")
    url = "https://www.google.com/finance/markets/most-active?hl=en"
    res = req.get(url)
    soup = BS(res.text, "html.parser")

    for stat in soup.select("ul.sbnBtf li div.SxcTic"):
        title = stat.select("div.ZvmM7")[0].get_text(strip=True)
        list_two.append(title)
        price = stat.select("div.YMlKec")[0].get_text(strip=True)
        change = stat.select("div.JwB6zf")[0].get_text(strip=True)
        if len(list_two) >= 11:
            break
        st.write(title, price, change)

with col3:
    st.subheader("Exchange Rate (Live from Naver)")
    url = "https://finance.naver.com/marketindex/"
    res = req.get(url)
    body = res.text

    r = re.compile(
        r"h_lst.*?blind\">(.*?)</span>.*?value\">(.*?)</", re.DOTALL)
    captures = r.findall(body)

    for c in captures:
        st.write(c[0] + ": " + c[1])

    usd = captures[0][1].replace(",", "")
    won = st.text_input("Convert Won to Dollar: ")

    if len(won) > 0:
        try:
            with st.spinner(text="Converting..."):
                time.sleep(3)
            usd = float(usd)
            won = float(won)
            dollar = round(float(won/usd), 2)
            st.write(f"Currently {won} won is {dollar} dollar(s).")
        except KeyError:
            st.error("Enter a number.")
