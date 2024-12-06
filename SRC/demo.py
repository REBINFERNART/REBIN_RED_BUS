



















import streamlit as st
import pandas as pd
import pymysql
from datetime import time, datetime  # Ensure datetime is imported

st.set_page_config(page_title="RedBus Journey Planner", page_icon=":bus:")
st.title("START your JOURNEY with REDBUS :heart_eyes:")

st.markdown('<h1 class="title">WELCOME TO REDBUS</h1>', unsafe_allow_html=True)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amatic+SC:wght@700&display=swap');
    .title {
        font-family: 'Amatic SC', cursive;
        font-size: 72px;
        color: #FF5733;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .logo {
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
    }
    .stDataFrame {
        background-color: #f0f2f6;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .bus-card {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    .bus-card:hover {
        transform: scale(1.02);
    }
    .notice-card {

        background-color: #dc6a50;
        color: black;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        font-family: 'Amatic SC', cursive;
        text-align: center;
    }
    .notice-header {
        font-size: 36px;
        margin-bottom: 10px;
    }
    .notice-content {
        font-family: 'Amatic SC', cursive; 
        font-size: 18px;
        line-height: 1.6;
        font-weight: bold;
    }
    </style>
    <img src="https://s3.rdbuz.com/Images/rdc/rdc-redbus-logo.svg" class="logo">
    """,
    unsafe_allow_html=True
)

st.image(
    "https://s3.rdbuz.com/images/webplatform/india/HomeBannerNew.png",
    caption="RedBus Banner",
    use_container_width=True
)
st.write('Let\'s start your journey by selecting your source and destination :sunglasses:')

st.markdown(
    """
    <div class="notice-card">
        <div class="notice-header">🚨 Important Notice 🚨</div>
        <div class="notice-content">
            We are pleased to announce that bus routes for <strong>10 states</strong> are now available on our site!<br>
            These states include <strong>Kerala, Bihar, Uttar Pradesh, Jammu & Kashmir, Goa, Assam, Rajasthan, Punjab, Himachal Pradesh,</strong> and <strong>KAAC Transport</strong>.<br>
            You can conveniently book your tickets by clicking on the booking option located on the <strong>top left corner</strong> of the page. 🚍✨
        </div>
    </div>
    """,
    unsafe_allow_html=True
)





def get_data():
    try:
        mydb = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="redbus"
        )
        mycursor = mydb.cursor()
        query = "SHOW COLUMNS FROM bus_routes"
        mycursor.execute(query)
        columns_info = mycursor.fetchall()
        available_columns = [col[0] for col in columns_info]

        columns_to_select = [col for col in [
            'route_name', 'busname', 'bustype', 'departing_time',
            'star_rating', 'price', 'duration', 'reaching_time', 'seats_available', 'route_link'
        ] if col in available_columns]

        query = f"SELECT {', '.join(columns_to_select)} FROM bus_routes;"
        mycursor.execute(query)
        results = mycursor.fetchall()
        mydb.close()
        
        return results, columns_to_select
    except pymysql.Error as e:
        st.error(f"Error connecting to MySQL database: {e}")
        return [], []

def time_in_range(check_time, start_time, end_time):
    if check_time is None:
        return False
    if start_time < end_time:
        return start_time <= check_time <= end_time
    else:
        return check_time >= start_time or check_time <= end_time


def split_route_name(route_name):
    parts = route_name.split(' to ')
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    return route_name, route_name


data, columns = get_data()
df = pd.DataFrame(data, columns=columns)


df[['source', 'destination']] = df['route_name'].apply(split_route_name).apply(pd.Series)


df['star_rating'] = pd.to_numeric(df['star_rating'], errors='coerce').fillna(0)
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['price'] = df['price'] / 10

def convert_to_time(time_str):
    try:
        if 'days' in str(time_str):
            time_str = str(time_str).split('days ')[-1]
        return datetime.strptime(time_str, '%H:%M:%S').time()
    except:
        return time(0, 0)

df['departing_time'] = df['departing_time'].apply(convert_to_time)
df['reaching_time'] = df['reaching_time'].apply(convert_to_time)


st.sidebar.header('Filter Options')

unique_sources = df['source'].unique()
unique_destinations = df['destination'].unique()

selected_source = st.sidebar.selectbox('Select Source', unique_sources)
selected_destination = st.sidebar.selectbox('Select Destination', unique_destinations)


if 'bustype' in df.columns:
    filtered_bus_types = df['bustype'].unique()
    selected_bus_types = st.sidebar.multiselect('Select Bus Types', filtered_bus_types)

departing_time_range = st.sidebar.selectbox(
    'Select Departing Time Range', 
    [
        '00:00:00 to 05:59:00', 
        '06:00:00 to 11:59:00', 
        '12:00:00 to 17:59:00', 
        '18:00:00 to 23:59:00', 
        'All Time (00:00:00 to 23:59:00)'
    ]
)

star_rating_range = st.sidebar.selectbox(
    'Select Star Rating Range', 
    ['0 to 2.5', '2.5 to 5', 'Any Rating (0.0 to 4.9)']
)

time_ranges = {
    '00:00:00 to 05:59:00': (time(0, 0), time(5, 59)),
    '06:00:00 to 11:59:00': (time(6, 0), time(11, 59)),
    '12:00:00 to 17:59:00': (time(12, 0), time(17, 59)),
    '18:00:00 to 23:59:00': (time(18, 0), time(23, 59)),
    'All Time (00:00:00 to 23:59:00)': (time(0, 0), time(23, 59))
}

search = st.sidebar.button('Search')

if search:
    
    filtered_data = df[
        (df['source'] == selected_source) & 
        (df['destination'] == selected_destination) & 
        (df['bustype'].isin(selected_bus_types))
    ]
    
  
    if departing_time_range != 'All Time (00:00:00 to 23:59:00)':
        start_time, end_time = time_ranges[departing_time_range]
        filtered_data = filtered_data[
            filtered_data['departing_time'].apply(
                lambda x: time_in_range(x, start_time, end_time)
        )
    ]
    
   
    if star_rating_range == '0 to 2.5':
        filtered_data = filtered_data[(filtered_data['star_rating'] >= 0) & (filtered_data['star_rating'] <= 2.5)]
    elif star_rating_range == '2.5 to 5':
        filtered_data = filtered_data[(filtered_data['star_rating'] > 2.5) & (filtered_data['star_rating'] <= 5)]
    
    if filtered_data.empty:
        st.warning("We couldn't find any bus options matching your selected filters. Please try adjusting the filters and check again.")
    else:
        st.subheader("Available Buses")
        for _, bus in filtered_data.iterrows():
            st.markdown(f'''
            <div class="bus-card"> 
                    <h3 style="color: #FF5733;">{bus['busname']} 🚍</h3> 
                    <div style="display: flex; justify-content: space-between;"> 
                        <div> 
                            <p><strong style="color: red;">Route:</strong> <span style="color: black;">{bus['route_name']}</span></p>
                            <p><strong style="color: red;">Bus Type:</strong> <span style="color: black;">{bus['bustype']}</span></p>
                            <p><strong style="color: red;">Departing Time:</strong> <span style="color: black;">{bus['departing_time']}</span></p> 
                            <p><strong style="color: red;">Duration:</strong> <span style="color: black;">{bus['duration']}</span></p> 
                            <p><strong style="color: red;">Reaching Time:</strong> <span style="color: black;">{bus['reaching_time']}</span></p> 
                        </div> 
                        <div>
                            <h2 style="color: #4CAF50;">₹{bus['price']:.2f}</h2>
                            <p><strong style="color: #FF5733;">⭐ Rating:</strong> <span style="color: #0000FF; font-weight: bold;">{bus['star_rating']:.1f}/5</span></p>
                            <p><strong style="color: red;">Seats Available:</strong> <span style="color: black;">{bus['seats_available']}</span></p>
                        </div> 
                    </div> 
                </div>
                ''', unsafe_allow_html=True) 
            
            route_link = bus['route_link']
            st.markdown(f"[Explore {bus['route_name']} Route on RedBus]({route_link})", unsafe_allow_html=True)
            st.write("This link will open in a new tab and take you to the RedBus website, where you can easily book your bus ticket and enjoy great offers.")
