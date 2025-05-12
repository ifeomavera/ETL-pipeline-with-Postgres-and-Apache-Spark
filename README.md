ETL-pipeline-with-Postgres-and-Apache-Spark

Overview

This project involves the creation of a data pipeline that collects data from the Spotify API, processes and filters the data, and then loads it into a PostgreSQL database. The primary goal was to get familiar with the use of Apache Spark technology. Additionally, the project tackles the challenge of backlogging daily inputs to create a comprehensive dataset.


Features


Data Collection: Fetches data from the Spotify API using the Spotipy library.

Data Processing: Filters and processes the data to extract recent plays, top artists, and top songs. Normalizes the data to address inconsistencies in letter cases.

Data Loading: Loads the processed data into a PostgreSQL database.

Data Backlogging: Uses the OS library to manage backlog files, storing all generated data from the start of the project.


Technologies Used


API Source: Spotify API

Programming Language: Python

Tool: Jupyter Notebook

Libraries:

spotipy: For making API calls to Spotify

pandas: For data manipulation and processing

SQLAlchemy: For database interaction

psycopg2: For PostgreSQL connections

schedule: For scheduling tasks

os: For handling file operations

subprocess: For running external scripts

datetime: For managing dates and times


Project Structure


Data Collection: Python script to fetch data from the Spotify API.

Data Processing: Filtering and processing the data using Pandas.

Data Loading: Using SQLAlchemy and psycopg2 to load data into PostgreSQL.

Data Backlogging: Using the OS library to manage backlog files.


Challenges and Solutions


Running Scheduled Jobs: Overcame the challenge of running scheduled jobs using the schedule library.

Using PySpark: Familiarized with PySpark for the first time, which required a learning curve.

Using Spotipy Library: Managed to use the Spotipy library to make API calls to Spotify, despite initial unfamiliarity.

Backlogging Extracted Data: Tackled the challenge of backlogging data using the OS library to manage backlog files effectively.


Results and Insights


Successfully created a data pipeline to collect, process, and load data from Spotify into a PostgreSQL database.

Normalized and managed data to address inconsistencies.

Scheduled and automated tasks for continuous data collection and processing.

Efficiently handled backlogging of data to maintain a comprehensive dataset.

Future Enhancements


Data Segmentation: Consider segmenting the dataset into different views for more specialized analysis.

Enhanced Data Processing: Explore more advanced data processing techniques and optimizations.

Additional API Endpoints: Fetch data from additional Spotify API endpoints to enrich the dataset.

Improved Automation: Further automate the data pipeline using additional tools and libraries.

Conclusion


This project demonstrates the effective use of a data pipeline to collect, process, and load data into a PostgreSQL database. It showcases the ability to handle backlogging, normalize data, and run scheduled tasks. The insights gained from this project can be valuable for future data analysis and pipeline projects.
