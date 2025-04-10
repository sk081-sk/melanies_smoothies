# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session -- dont need this line if running directly with streamlit. its needed only for steamlit on snflk (sis)
from snowflake.snowpark.functions import col
import requests

# st.text(smoothiefroot_response.json())


helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")


# option = st.selectbox(
#     "What is your favorite fruit?",
#     ('Banana','Strawberries','Peaches'),
# )

# st.write("Your favorite fruit is:", option)


name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your Smoothie will be: ', name_on_order)

#session = get_active_session()  -- dont need this line if running directly with streamlit. its needed only for steamlit on snflk (sis)
cnx=st.connection("snowflake")   
session=cnx.session()            
# my_dataframe = session.table("smoothies.public.fruit_options")
# my_dataframe = session.table("smoothies.public.fruit_options").select (col('FRUIT_NAME'))
my_dataframe = session.table("smoothies.public.fruit_options").select (col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

ingredients_list = st.multiselect (
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '        
        # st.write(ingredients_string)
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" +  fruit_chosen)        
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """', '""" + name_on_order + """')"""
    
    #st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered', icon="✅")
