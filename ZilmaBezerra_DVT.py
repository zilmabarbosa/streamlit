# Importing the libraries 

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout = 'wide')

st.title('Analysing Book Ratings Dataset')
st.subheader('A Web App by [Zilma Bezerra](https://github.com/zilmabezerra)')

'''
Welcome to Zilma's Book Analysis App. This app analyses the merged dataset called 'bookrec', in order to develop a recommendation system. The merged dataset contains information on the three original datasets:
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
                       color_discrete_sequence = ['#FFAC1C'])

fig_br.update_layout(height = 600, width = 1000, template = custom_template, xaxis_title = '<b>Rating</b>',
                      yaxis_title = '<b>Count</b>', xaxis = dict(tickmode = 'linear'), bargap = 0.1)

tab1, tab2, tab3, tab4, tab5 = st.tabs(['Age Distribution', 'Top 10 Locations', 'Most Rated Books', 'Most Rated Authors', 'Rating Distribution'])

with tab1:
    st.header('Age Distribution')
    st.write(f'In this plot, it is possible to observe the presence of outliers. The ages around and over 100 are most likely erroneous data inputs. These errors may have been made by accident or on purpose. For instance, some users may not want to disclose their personal information.')
    st.plotly_chart(fig_age)

with tab2:
    st.header('Top 10 Locations')
    st.write(f'Here, it can be seen that the locations with the highest number of individual ratings for books are either in the USA or Canada.')
    st.plotly_chart(fig_lmr)

with tab3:
    st.header('Most Rated Books')
    st.write(f'This third graph shows the top 10 books with the highest number of individual ratings. It is possible to see that <b>Wild Animus</b>, the top rated, has more than double the number of ratings than the second position, <b>The Lovely Bones: A Novel<b/>.')
    st.plotly_chart(fig_mrb)

with tab4:
    st.header('Most Rated Authors')
    st.write(f'In this case, the plot shows the top 10 authors with the highest number of individual ratings, being <b>Stephen King</b>, the top rated.')
    st.plotly_chart(fig_mra)

with tab5:
    st.header('Rating Distribution')
    percentage = round(bookrec['book_rating'][bookrec['book_rating'] == 0].shape[0] / bookrec['book_rating'].shape[0], 2)
    st.write(f'The last histogram is about the rating distribution. Here, it is possible to observe that nearly half a million of the ratings are zero. This number represents {percentage} of the dataset.')
    st.plotly_chart(fig_br)
