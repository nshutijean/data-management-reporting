import sqlite3
import pandas as pd
import streamlit as st
import sketch
import os

# First upload
def first_upload_to_db(conn, upload_file):

  if upload_file is not None:

    # Get the file name
    file_name = upload_file.name.replace('.xlsx', '')  

    # Check if table with same name already exists
    if file_name not in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall():

      df = pd.read_excel(upload_file)  

      # perform some data cleaning here, if needed 

      df.to_sql(file_name, conn, if_exists="fail")
      conn.commit()

      # Report here
      # important_reports(df)
    else:
      st.write("File already exists")



# Other uploads
def other_uploads(conn, upload_file):
  """
  Extra uploads with be appended to the first one after cleaning
  """

  if upload_file is not None:
 
    df = pd.read_excel(upload_file)

    # perform data cleaning on the dataframe (if needed) here
    
    # append the dataframe to table created before (update the table)
    file_name = upload_file.name.replace('.xlsx', '') 
    df.to_sql(file_name, conn, if_exists="fail")

    cursor = conn.cursor()
    insert_query = f"""INSERT INTO test_db SELECT * FROM {file_name}"""
    cursor.execute(insert_query)

    # drop the newly uploaded table after concantenation
    drop_query = f"""DROP TABLE {file_name}"""
    cursor.execute(drop_query)

    conn.commit()

    

def important_reports(df):

  # Read the database through a dataframe
  report_df = df

  st.header('2. Reports', divider='gray')

  # date formatting
  report_df['Date'] = pd.to_datetime(report_df['Date']).dt.strftime('%Y-%m-%d')

  # set data ranges

  # put the ranges in streamlit
  # date_range = st.date_input('Choose a data range', )

  # Report 1 
  st.write('**Sample data.** View a table of 10 randomly generated data points')
  sample_data = report_df.sample(10)
  sample_data = sample_data.drop(columns=['index'])
  st.table(sample_data)
  # st.button('Regenerate', on_click=sample_data)

  # Report 2
  number_of_cases = report_df['Cases'].count()
  st.text_input(label='**Number of cases**', placeholder=str(number_of_cases), disabled=True)

  # Report 3
  numnber_of_deaths = report_df['Death'].count()
  st.text_input(label='**Number of deaths**', placeholder=str(numnber_of_deaths), disabled=True)

  # Report 4
  case_fatility_rate = (numnber_of_deaths / number_of_cases) * 100
  st.text_input(label='**Case Fatility Rate for Ebola**', placeholder=str(case_fatility_rate), disabled=True)

  st.header('3. Charts', divider='gray')

  # scatterplot
  st.subheader('Scatterplots')

  # select columns to discard
  columns_to_discard = ['index', 'Date']

  # remove the specified columns from the list
  filtered_columns = [col for col in report_df.columns if col not in columns_to_discard]

  # x and y axes
  x_axis = st.selectbox('Select the x-axis', filtered_columns, key=32)
  y_axis = st.selectbox('Select the y-axis', filtered_columns, key=12)

  st.write(f'**Relationship between {x_axis} and {y_axis} of Ebola**')
  st.scatter_chart(data=report_df, x=x_axis, y=y_axis)

  # barplots
  st.subheader('Barplot')
  st.write(f'**{x_axis} vs {y_axis} barplot**')
  st.bar_chart(data=report_df, x=x_axis, y=y_axis)

  # lineplots
  st.subheader('Lineplot')
  st.write('How deaths increased/descreased over time')
  y_axis_line = st.selectbox('Select the y-axis', filtered_columns, key=23)

  st.line_chart(data=report_df, x='Date', y=y_axis_line)


def custom_querying(conn):

  # Input from Streamlit
  query = st.text_input(label="Write your query below and press Enter", placeholder="Query goes here")

  try:
      df = pd.read_sql_query(query, conn)
  
      # Print the dataframe
      st.dataframe(df)
  except TypeError:
      st.error("Check your query before executing")


if __name__ == '__main__':
    # Create a sqlite connection
    conn = sqlite3.connect('dbg_pfis.db')

    # present
    st.title("Ebola cases and deaths reporting")
    st.write("Use this web application to view reports of your data in an efficient and interactive way.")

    st.info('- Upload your __uniquely__ named Excel file. \n- Read sample reports. \n- Visualize relationships in charts. \n- Input your custom queries to explore the database')

    # Allow user to upload an Excel file
    st.header('1. Upload a file', divider='gray')
    upload_file = st.file_uploader("Choose an Excel file from your computer", type=["xlsx"])

    # check if the database is empty
    if len(conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()) == 0:
        first_upload_to_db(conn, upload_file)
    else:
        other_uploads(conn, upload_file)

    cursor = conn.cursor()

    table_name = "test_db"

    # # Visualize charts
    # if table_name not in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall():
    #   st.warning('No file uploaded yet or no table created')
    # else:
    retrieve_query = f"""SELECT * FROM {table_name}"""
    new_table_df = pd.read_sql_query(retrieve_query, conn)
    
    # report here
    important_reports(new_table_df)

    # Allow for custom queries
    st.header('4. Search with your custom queries', divider='gray')
    custom_querying(conn)

    conn.close()