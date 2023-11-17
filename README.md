# Data management workflow for reporting

This project aims to create a data management workflow for reporting on the Ebola cases and deaths in North Kivu Ebola outbreak. The project uses an *excerpt* of data from [HDX](https://data.humdata.org/dataset/ebola-cases-and-deaths-drc-north-kivu?).

## Tools

- **Streamlit**: A Python framework for building interactive web applications.
- **SQLite**: A lightweight and self-contained database engine.
- **Pandas**: A Python library for data analysis and manipulation.

## Project overview

The project consists of the following steps:

- **Data ingestion**: The project allows the user to upload their data (Excel files) gradually
- **Data transformation**: The project cleans and transforms the data using Pandas renaming columns, and aggregating data by country and region.
- **Data loading**: The project creates a SQLite database and loads the data into a table using the `sqlite3` library.
- **Data visualization**: The project uses Streamlit to create an interactive web application that displays the data in various charts and tables, such as line charts, bar charts, and maps.
- **Custom querying**: The project allows the user to input their SQL queries which retrieve the needed data in a dataframe

## How to run the project

To run the project, you need to have Python 3.7 or higher installed on your system, as well as the following libraries:

- streamlit
- pandas
- sqlite3

You can install these libraries using the `pip` command:

```
pip install streamlit pandas sqlite3
```

Then, you can clone this repository or download the ZIP file and extract it to your preferred location. To run the web application, navigate to the project folder and run the following command:

```
streamlit run app.py
```

This will open a new tab in your browser where you can interact with the web application. You can also access the web application from another device by using the URL displayed in the terminal.

## Project structure

The project folder contains the following files and folders:

- `app.py`: The main Python script that runs the web application using Streamlit.
- `data`: A folder that contains the CSV file with the data.
- `schema`: A folder that contain SQLite database file.
- `README.md`: This file that provides a brief introduction and instructions for the project.

## License

This project is licensed under the MIT License - see the [LICENSE] file for details.

## Extra

I hope this helps you with your project. If you have any feedback or questions, please let me know. 😊

## Next steps

- [ ] Creating a docker image for the project

