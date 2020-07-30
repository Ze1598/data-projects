# Data Projects

A repository for all my data-related projects.

## 2019 Stack Overflow Developer Survey
Data analysis of the 2019 Stack Overflow Developer survey results in four different softwares:
* Microsoft Excel: data transformation and creation of two dashboards
* Microsoft Power BI: usage of the data transformed in Excel to recreate the same dashboards
* Jupyter Notebook (Python): complete analysis from scratch with NumPy, pandas and Plotly
* R Notebook: same analysis made in Python, but replicated with R code

The source dataset can be downloaded [here](https://drive.google.com/file/d/1QOmVDpd8hcVYqqUXDXf68UMDWQZP0wQV/view) (the file is too large to include in the repository).

You can view the Excel version of the analysis [here](https://ipppt-my.sharepoint.com/:x:/g/personal/2161161_iscap_ipp_pt/EZyjLWRSLGlLrl4mob110y4BwXPpXtswPM8WR3chfE-LWA?e=25Y4ia).

You can find the results of the Power BI version report as a PDF in [this folder](https://github.com/Ze1598/data-projects/tree/master/SO2019DevSurvey/results) of the repository or as a downloadable .pbix file in [this folder](https://github.com/Ze1598/data-projects/tree/master/SO2019DevSurvey/power%20bi).

You can view the Python version of the analysis in an HTML version of the resulting Jupyter Notebook [here](https://so2019devsurvey.ze1598.repl.co/).

The R notebook is available [here](https://github.com/Ze1598/data-projects/blob/master/SO2019DevSurvey/results/R_data_analysis.html) too.


## Anime analysis
Data analysis of a dataset about anime found on Kaggle. This dataset contains anime listings, the studios responsible for the animation, genres, warnings, etc. This project was divided in two parts:
* [Microsoft Power BI data analysis](https://github.com/Ze1598/data-projects/tree/master/anime%20analysis/anime%20analysis%20%5Bpower%20bi%5D): a straightforward data analysis in Microsoft Power BI
* [anime_db](https://github.com/Ze1598/data-projects/tree/master/anime%20analysis/anime_db%20%5Bpostgresql_python%5D): creation of a PostgreSql database and data analysis in Python, using the tables created in the Power BI analysis (exported from Power BI as CSV files). The [psycopg2](https://pypi.org/project/psycopg2/) library was used to perform database operations, and [pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/) and [Plotly](https://plotly.com/python/) were used for the data analysis.

The original dataset is available on Kaggle [here](https://www.kaggle.com/alancmathew/anime-dataset).

The results of the Power BI analysis are available [here](https://github.com/Ze1598/data-projects/blob/master/anime%20analysis/anime%20analysis%20%5Bpower%20bi%5D/anime_analysis.pdf) (a PDF of the report).

The results of the anime_db work is available [here](https://github.com/Ze1598/data-projects/tree/master/anime%20analysis/anime_db%20%5Bpostgresql_python%5D/results) (two Jupyter Notebooks and the database ERD). You can read the first notebook [here](https://animedb-part-1--ze1598.repl.co/) and the second [here](https://animedb-part-2--ze1598.repl.co/). The first is all about the data engineering part, that is, writing data to the database. The second notebook is the actual data analysis.


## 2020 Stack Overflow Developer Survey
Similar to the 2019 counterpart, but using the 2020 data. It is similar to last year's analysis but, in my opinion, it is better given the new knowledge and skills I've acquired since the first analysis.

So far, the data analysis of the 2020 Stack Overflow Developer survey was made in:
* Microsoft Power BI: data transformations in Power Query and creation of four dashboards (general data, technology-related, professional status, and other data)
* Microsoft Excel: similar analysis to Power BI, but has only two dashboards, including mostly the same information, but visually rearranged
* Python/PostgreSQL: a two-phase project. The first is data engineering oriented, where I pre-processed the dataset, created a PostgreSQL database using the psycopg2 driver and then inserted the data. The second phase is the proper data analysis, using Plotly for the visualization, similar to what I did in Excel and Power BI

The source dataset can be downloaded [here](https://drive.google.com/file/d/1dfGerWeWkcyQ9GX9x20rdSGj7WtEpzBB/view) (the file is too large to include in the repository).

You can find the results of the Power BI report as a PDF [here](https://github.com/Ze1598/data-projects/blob/master/SO2020DevSurvey/power%20bi/report.pdf) and as a downloadable .pbix file [here](https://github.com/Ze1598/data-projects/blob/master/SO2020DevSurvey/power%20bi/data_analysis.pbix).

You can find the Excel file version of the data analysis, as well as screenshots of the resulting dashboards, [here](https://github.com/Ze1598/data-projects/tree/master/SO2020DevSurvey/excel).

For the Python (and PostgreSQL) part, I divided the work in two Jupyter Notebooks. The first notebook covers the data engineering part, and the second covers the data analysis part. You can read the first notebook [here](https://so2020devsurvey-part1--ze1598.repl.co/
) and the second notebook [here](https://so2020devsurvey-part2--ze1598.repl.co/). Both notebooks are also available in this [repository](https://github.com/Ze1598/data-projects/tree/master/SO2020DevSurvey/python).


## Demos
Smaller demos created for specific purposes, such as how to perform a certain data transformation in Python, data analyses in Power BI, etc., including the resulting files of tutorials I've completed. The link to the original datasets can always be found in the respective "source.txt" file.
Some examples of the demos available so far:

* [Creation of an anime dataset by scraping LiveChart.me with Power BI](https://github.com/Ze1598/data-projects/tree/master/demos/livechart%20data%20scrape%20%5Bpower%20bi%5D)
* [Data Analysis of an Olympics dataset from Kaggle](https://github.com/Ze1598/data-projects/tree/master/demos/olympics%20%5Bpower%20bi%5D)
* [How to unpivot delimited data with Python and pandas](https://github.com/Ze1598/data-projects/tree/master/demos/unpivot%20delimited%20data%20%5Bpandas%5D)
