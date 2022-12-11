# Importing the libraries 

import streamlit as st
from streamlit_lottie import st_lottie
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import folium
from folium import plugins
import ipywidgets as widgets
from ipywidgets import Layout, interact, interactive, VBox, HBox


# Setting page configurations

st.set_page_config(layout = 'wide', page_icon = '📙')

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

file_url = 'https://assets4.lottiefiles.com/temp/lf20_aKAfIn.json'
lottie_book = load_lottieurl(file_url)
st_lottie(lottie_book, speed = 1, height = 100, key = 'initial')

st.markdown("<h1 style = 'text-align: center;'> Analysing Book Ratings Dataset </h1>", unsafe_allow_html = True)
st.markdown("<h3 style = 'text-align: center;'> A Web App by <b><a href = 'https://github.com/zilmabezerra'> Zilma Bezerra </a></b></h3>", unsafe_allow_html = True)

'''
Welcome to Zilma's Book Analysis App. This app analyses a dataset called "bookrec", in order to develop a recommendation system.
The dataset merges information of the three initial datasets provided:
* **BX-Books**, which contains data about books, such as ISBN, title, author, year of publication, publisher and image links;
* **BX-Users**, which has data about the users, such as ID, location and age;
* **BX-Book-Ratings**, which contains information on user ID, ISBN and rating.

The analysis of this raw data will guide further steps in data preparation and modelling.

*Please, scroll down and navigate through the tabs below to visualise the graphs.*
'''

# Reading the dataset

bookrec = pd.read_csv('bookrec.csv')

# Creating a custom template for plotly

custom_template = {'layout':
                   go.Layout(
                       font = {'family': 'Helvetica',
                               'size': 14,
                               'color': '#1f1f1f'},
                       
                       title = {'font': {'family': 'Helvetica',
                                         'size': 20,
                                          'color': '#1f1f1f'}},
                       
                       legend = {'font': {'family': 'Helvetica',
                                          'size': 14,
                                          'color': '#1f1f1f'}},
                       
                       plot_bgcolor = '#f2f2f2',
                       paper_bgcolor = '#ffffff'
                   )}

# Plotting the distribution of 'age'

fig_age = px.histogram(bookrec, x = 'age', title = "<b>Users' Age Distribution</b>", color_discrete_sequence = ['#FF7F50'])

fig_age.update_layout(height = 600, width = 1000, template = custom_template, xaxis_title = '<b>Age</b>',
                      yaxis_title = '<b>Count</b>')

# Plotting the top 10 locations with more ratings published

fig_lmr = px.bar(bookrec.value_counts('location', ascending = False).head(10),
                 x = bookrec.value_counts('location', ascending = False).head(10),
                 y = bookrec.value_counts('location', ascending = False).head(10).index,
                 title = "<b>Top 10 Locations with More Ratings Published</b>",
                 color_discrete_sequence = ['#FF7F50'])

fig_lmr.update_layout(height = 600, width = 1000, template = custom_template, xaxis_title = '<b>Rating Count</b>',
                      yaxis_title = '<b>Location</b>')

fig_lmr.update_yaxes(automargin = True, title_standoff = 10)

# Plotting the top 10 most rated books (by number of ratings)

fig_mrb = px.bar(bookrec.value_counts('book_title', ascending = False).head(10),
                 x = bookrec.value_counts('book_title', ascending = False).head(10),
                 y = bookrec.value_counts('book_title', ascending = False).head(10).index,
                 title = "<b>Top 10 Most Rated Books</b>",
                 color_discrete_sequence = ['#FF7F50'])

fig_mrb.update_layout(height = 600, width = 1000, template = custom_template, xaxis_title = '<b>Rating count</b>',
                      yaxis_title = '<b>Books</b>')

fig_mrb.update_yaxes(automargin = True, title_standoff = 10)

# Plotting the top 10 most rated authors (by number of ratings)

fig_mra = px.bar(bookrec.value_counts('book_author', ascending = False).head(10),
                 x = bookrec.value_counts('book_author', ascending = False).head(10),
                 y = bookrec.value_counts('book_author', ascending = False).head(10).index,
                 title = "<b>Top 10 Most Rated Authors</b>",
                 color_discrete_sequence = ['#FF7F50'])

fig_mra.update_layout(height = 600, width = 1000, template = custom_template, xaxis_title = '<b>Rating Count</b>',
                      yaxis_title = '<b>Authors</b>')

fig_mra.update_yaxes(automargin = True, title_standoff = 10)

# Plotting the distribution of 'book_rating'

fig_br = px.histogram(bookrec, x = 'book_rating', title = "<b>Rating Distribution</b>",
                       color_discrete_sequence = ['#FF7F50'])

fig_br.update_layout(height = 600, width = 1000, template = custom_template, xaxis_title = '<b>Rating</b>',
                      yaxis_title = '<b>Count</b>', xaxis = dict(tickmode = 'linear'), bargap = 0.1)

#
#
#

# Reading the subdataset: age range 55-75 and rating range 6-10

bookrec_65 = pd.read_csv('bookrec_65.csv')

# Creating streamlit controls

def display_country_filter(df):
    country_list = list(df['country'].unique())
    country_list = [element.upper() for element in unique_countries]
    country_list.sort()
    country = st.selectbox('Country', country_list)
    st.header(f'{country}')
    return country

def display_rating_filter(df):
    rating_list = list(df['rating'].unique())
    rating_list.sort()
    rating = st.sidebar.selectbox('Rating', rating_list)
    st.header(f'{rating}')
    return rating

# Designing the popup for the map

def popup_html(row):
    
    i = row
    df = bookrec_65.copy()
    
    country_html = str(df['country'].iloc[i]).title() 
    book_html = df['book_title'].iloc[i]
    rating_html = df['book_rating'].iloc[i]
    cover_html = df['image_url_l'].iloc[i] 

    left_col_color = '#404040'
    right_col_color = '#D3D3D3'

    html = """
    <!DOCTYPE html>
    <html>
    <center><img src = \"""" + cover_html + """\" alt = "logo" width=100 ></center>
    <center> <table style = "height: 150px; width: 250px;">
    <tbody>
    <tr>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #ffffff;"> Country </span></td>
    <td style="width: 200px;background-color: """ + right_col_color + """;">{}</td>""".format(country_html) + """</td>
    </tr>
    <tr>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #ffffff;"> Book </span></td>
    <td style="width: 200px;background-color: """ + right_col_color + """;">{}</td>""".format(book_html) + """
    </tr>
    <tr>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #ffffff;"> Rating </span></td>
    <td style="width: 200px;background-color: """ + right_col_color + """;">{}</td>""".format(rating_html) + """
    </tr>
    </tbody>
    </table></center>
    </html>
    """
    return html

# Creating the function for the map

def updated_map(country, rating):
    
    df = bookrec_65.copy()
    df = df.sample(1000) # getting a random sample
    df_country = df.loc[df['country'] == country]
    df_rating = df_country.loc[df_country['book_rating'] == rating]
    
    # Designing the map

    # Creating the map base
    book_map = folium.Map(location = [39.3260685, -4.8379791], zoom_start = 1.5)

    # Clustering datapoints
    point = plugins.MarkerCluster().add_to(book_map)

    # Set up the colours based rating
    purpose_colour = {6:'gray', 7:'gray', 8:'gray', 9:'gray', 10:'orange'}

    # Looping through each row in the dataframe
    for i, row in df_rating.iterrows():
    
        try:
            icon_color = purpose_colour[row['book_rating']]
        except:
            icon_color = 'gray'
    
        # Add each row to the map
        folium.Marker(location = [row['lat'], row['long']],
                      popup = folium.Popup(folium.Html(popup_html(i), script = True)), 
                      icon = folium.Icon(icon = 'book', prefix = 'fa', icon_color = 'white', color = icon_color)).add_to(point)
    
    # Showing map
    st_map = st_folium(book_map, width = 700, height = 450)
        
#
#
#

# Creating the streamlit layout

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['**Age Distribution**', '**Top 10 Locations**', '**Top 10 Rated Books**', '**Top 10 Rated Authors**',
                                              '**Rating Distribution**', '**Interactive Map**'])

with tab1:
    st.header('Age Distribution')
    st.write(f'In this plot, it is possible to observe the presence of outliers. The ages **around and over 100** are most likely erroneous data inputs. These errors may have been made by accident or on purpose. For instance, some users may not want to disclose their personal information.')
    st.plotly_chart(fig_age)

with tab2:
    st.header('Top 10 Locations')
    st.write(f'Here, it can be seen that the locations with the highest number of individual ratings for books are either in the **USA** or **Canada**.')
    st.plotly_chart(fig_lmr)

with tab3:
    st.header('Top 10 Rated Books')
    st.write(f'This third graph shows the top 10 books with the highest number of individual ratings. It is possible to see that **Wild Animus**, the top rated, has more than double the number of ratings than the second position, **The Lovely Bones: A Novel**.')
    st.plotly_chart(fig_mrb)

with tab4:
    st.header('Top 10 Rated Authors')
    st.write(f'In this case, the plot shows the top 10 authors with the highest number of individual ratings, being **Stephen King**, the top rated.')
    st.plotly_chart(fig_mra)

with tab5:
    st.header('Rating Distribution')
    percentage = round(bookrec['book_rating'][bookrec['book_rating'] == 0].shape[0] / bookrec['book_rating'].shape[0], 2)*100
    st.write(f'The last histogram is about the rating distribution. Here, it is possible to observe that nearly **half a million** of the ratings are **zero**. This number represents {percentage}% of the dataset.')
    st.plotly_chart(fig_br)
    
with tab6:
    st.header('Interactive Map')
    st.write(f'The last histogram is about the rating distribution. Here, it is possible to observe that nearly **half a million** of the ratings are **zero**. This number represents {percentage} of the dataset.')
    col1, col2 = st.columns(2)
    with col1:
        country = display_country_filter(df)
        rating = display_rating_filter(df)
    with col2:
        st_map = updated_map(df, country, rating)
        
   
