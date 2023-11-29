import pandas as pd
import mysql.connector
import streamlit as st
import plotly.express as px
import os
import json
from streamlit_option_menu import option_menu
from PIL import Image
con= mysql.connector.connect(host="localhost",
                            user= "root",
                            password="sujitha@1988",
                            db="phonepe")
cursor=con.cursor()

st.set_page_config(
    page_title="Phonepe",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
    
)
#st.title('Phonepe Pulse')
st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTUDH7CuP1cORrbg0wubQQoFIrRl9t23abzcrwqszznjg&s.png")
st.title(':violet[Phonepe Pulse]')
#st.markdown("*Streamlit* is **really** ***cool***.")


# Creating option menu in the side bar
with st.sidebar:
    selected = option_menu("Menu", ["Home","Top Charts","Explore Data","About"], 
                icons=["house","graph-up-arrow","bar-chart-line", "exclamation-circle"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})
# MENU 1 - HOME
if selected == "Home":
    st.markdown("# :violet[Data Visualization and Exploration]")
    st.markdown("## :violet[A User-Friendly Tool Using Streamlit and Plotly]")
    column1,column2,column3= st.columns([1,1.5,2],gap="medium")
    with column1:
        st.markdown("### :violet[Domain :] Fintech")
    with column2:   
        st.markdown("### :violet[Technologies used :] Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.")
    with column3:
        st.markdown("### :violet[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.")
    
# MENU 2 - TOP CHARTS
if selected == "Top Charts":
    st.markdown("## :violet[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    colum1,colum2= st.columns([1,1.5],gap="large")
    with colum1:
        Year = st.slider("**Year**", min_value=2018, max_value=2023)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)
    
    with colum2:
        st.info(
                """
                #### From this menu we can get insights like :
                - Overall ranking on a particular Year and Quarter.
                - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.
                - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
                - Top 10 mobile brands and its percentage based on the how many people use phonepe.
                """,icon="🔍"
                )
    # Top Charts - TRANSACTIONS    
    if Type == "Transactions":
        col1,col2,col3 = st.columns([1,1,1],gap="small")
        
        with col1:
            st.markdown("### :violet[State]")
            cursor.execute(f"select state, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from aggtransactiondata where year = {Year} and quarter = {Quarter} group by state order by Total desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])

            fig = px.pie(df, values='Total_Amount',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True) 
        with col2:
            st.markdown("### :violet[District]")
            cursor.execute(f"select district , sum(Count) as Total_Count, sum(Amount) as Total from map_trans where year = {Year} and quarter = {Quarter} group by district order by Total desc limit 10")
            #print("500")
            df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])

            fig = px.pie(df, values='Total_Amount',
                             names='District',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
        with col3:
            st.markdown("### :violet[Pincode]")
            cursor.execute(f"select pincode, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from top_trans where year = {Year} and quarter = {Quarter} group by pincode order by Total desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['Pincode', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                             names='Pincode',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
    # Top Charts - Users    
    if Type == "Users":
        col1,col2,col3,col4 = st.columns([2,2,2,2],gap="small")
        with col1:
            st.markdown("### :violet[Brands]")
            cursor.execute(f"select brands, sum(count) as Total_Count, avg(percentage)*100 as Avg_Percentage from aggr_userdata where year = {Year} and quarter = {Quarter} group by brands order by Total_Count desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
            fig = px.bar(df,
                             title='Top 10',
                             x="Total_Users",
                             y="Brand",
                             orientation='h',
                             color='Avg_Percentage',
                             color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)   
        with col2:
            st.markdown("### :violet[District]")
            cursor.execute(f"select district, sum(RegisteredUser) as Total_Users, sum(Appopens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by district order by Total_Users desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                         title='Top 10',
                         x="Total_Users",
                         y="District",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)
        with col3:
            st.markdown("### :violet[Pincode]")
            cursor.execute(f"select Pincode, sum(RegisteredUsers) as Total_Users from top_user where year = {Year} and quarter = {Quarter} group by Pincode order by Total_Users desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['Pincode', 'Total_Users'])
            fig = px.pie(df,
                         values='Total_Users',
                         names='Pincode',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Users'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
        with col4:
            st.markdown("### :violet[State]")
            cursor.execute(f"select state, sum(RegisteredUser) as Total_Users, sum(Appopens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by Total_Users desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
            fig = px.pie(df, values='Total_Users',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Total_Appopens'],
                             labels={'Total_Appopens':'Total_Appopens'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
        
# MENU 3 - EXPLORE DATA
if selected == "Explore Data":
    Year = st.sidebar.slider("**Year**", min_value=2018, max_value=2023)
    Quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4)
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
   
    col1,col2 = st.columns(2)
    
# EXPLORE DATA - TRANSACTIONS
    if Type == "Transactions":
        
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
        with col1:
            st.markdown("## :violet[Overall State Data - Transactions Amount]")
            cursor.execute(f"select state as State, sum(count) as 'Total Transactions', sum(amount) as 'Total Amount', year as Year from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(cursor.fetchall(),columns= ['State', 'Total Transactions', 'Total Amount', 'Year'])
            df1.to_csv('statenames.csv')
            df2 = pd.read_csv('statenames.csv')
            india_states = json.load(open("india_states.geojson", "r"))
            fig = px.choropleth (
                df1,
                geojson=india_states,
                featureidkey='properties.ST_NM',
                locations='State',
                color='Total Transactions',
                color_continuous_scale='Reds',
                hover_data='Total Amount',
                width=900,
                height=900
            )
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig,use_container_width=False)
        with col2:
            st.markdown("## :violet[Top 10 State Data]")
            cursor.execute(f"select state as State, sum(count) as 'Total Transactions' from map_trans where year = {Year} and quarter = {Quarter} group by state order by count limit 10")
            #topTen_df = pd.DataFrame()
            st.dataframe(cursor.fetchall(),columns= ['State', 'Total Transactions'])
    if Type == "Users":
        
        # Overall State Data -Users - INDIA MAP 
        with col1:
            st.markdown("## :violet[Overall State Data - Users]")
            cursor.execute(f"select state as State, sum(RegisteredUser) as 'Registered Users', sum(AppOpens) as 'App Opens in Quarter', year as Year from map_user where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(cursor.fetchall(),columns= ['State', 'Registered Users', 'App Opens in Quarter', 'Year'])
            india_states = json.load(open("india_states.geojson", "r"))
            fig = px.choropleth (
                df1,
                geojson=india_states,
                featureidkey='properties.ST_NM',
                locations='State',
                color='Registered Users',
                color_continuous_scale='Reds',
                hover_data='App Opens in Quarter',
                width=900,
                height=900
            )
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig,use_container_width=False) 
        with col2:
            st.markdown("## :violet[Top 10 State Data]")
            cursor.execute(f"select state as State, sum(RegisteredUser) as 'Registered Users' from map_user where year = {Year} and quarter = {Quarter} group by state order by RegisteredUser limit 10")
            topTen_df1 = pd.DataFrame(cursor.fetchall(),columns= ['State', 'Total Users'])
            st.table(topTen_df1)
# MENU 4 - ABOUT
if selected == "About":
    col1,col2 = st.columns([3,3],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[About PhonePe Pulse:] ")
        st.write("##### BENGALURU, India, On Sept. 3, 2021 PhonePe, India's leading fintech platform, announced the launch of PhonePe Pulse, India's first interactive website with data, insights and trends on digital payments in the country. The PhonePe Pulse website showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With  over 45% market share, PhonePe's data is representative of the country's digital payment habits.")
        
        st.write("##### The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.")
        
        st.markdown("### :violet[About PhonePe:] ")
        st.write("##### PhonePe is India's leading fintech platform with over 300 million registered users. Using PhonePe, users can send and receive money, recharge mobile, DTH, pay at stores, make utility payments, buy gold and make investments. PhonePe forayed into financial services in 2017 with the launch of Gold providing users with a safe and convenient option to buy 24-karat gold securely on its platform. PhonePe has since launched several Mutual Funds and Insurance products like tax-saving funds, liquid funds, international travel insurance and Corona Care, a dedicated insurance product for the COVID-19 pandemic among others. PhonePe also launched its Switch platform in 2018, and today its customers can place orders on over 600 apps directly from within the PhonePe mobile app. PhonePe is accepted at 20+ million merchant outlets across Bharat")  
    with col2:
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        #st.image("Pulseimg.jpg")     