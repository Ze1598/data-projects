Purpose
This project was created as a way for me to practice SQL, in this case PostgreSql.
Since I had analyzed this dataset previously in Microsoft Power BI, I simply exported the tables to CSV to insert on the database. The files were inserted in the database through Python and then queried against for data visualization with Plotly (also in Python).

-----------------------------
Methodology
The data was exported from Microsoft Power BI into five CSV files, with no further transformations required. Each file contained the data from a single table: anime, watch_status, genres, studios and warnings.

The database and the columns were created through the command line, with psql. The SQL code for this is avaible in the "database_tables_creation.sql" file.

The insertion of data was performed in Python, using the psycopg2 library. This allowed me to load the CSVs as pandas DataFrames and then insert them into the database using pure SQL queries, not ORM functions. The Python data insertion script is available in the "anime_db_inserts.ipynb" Jupyter Notebook.

After the insertions, I queried the database to perform data analysis and data visualization. The charts were created were the same I had created in the Power BI report. The plotting library chosen was Plotly for its interactivity and flexible API. This part is available in the "anime_db_analysis.ipynb" Jupyter Notebook.

The "database.ini" file contains information about the database to connect to it in Python.

The "results" folder contains extra information about this project, namely the HTML export of the Notebooks and the database's ER diagram.

The "data" folder contains the five CSV files exported from Microsoft Power BI. Unfortunately, due to the length of the rows available in the tables, a minority of the data was not exported (for files/tables that exceeded thirty thousand rows). Though in the ideal scenario no data would be left behind, I consider it an acceptable drawback as the focus in this project was to practice SQL operations, not the data analysis itself.

-----------------------------
Original data source
Kaggle: https://www.kaggle.com/alancmathew/anime-dataset