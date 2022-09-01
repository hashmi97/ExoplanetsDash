# ExoplanetsDash
A Project for my data visualisation course at Harbour Space University


### Usage

First, you will need to install the required libraries by issuing the command

`pip install -r requirements.txt`

After the libraries are installed, you can use the `report.ipynb` file to explore the data set and play with it.
or issue the command `python app.py` to launch the Dashboard. 

### Preliminary Data Analysis
You'll find the data [here](https://github.com/hashmi97/ExoplanetsDash/blob/main/data/data.csv). Inside the csv file, 
you'll find lots of columns, most of which are ignored within this project. However, if you would like to explore the 
data further,then make sure you checkout this [link](https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html)
to the data documentation.

The project mainly focused on the following columns (These are not the original column names).

`'starName', 'numStars', 'discoveryMethod', 'discoveryYear',
'discoveryLocale', 'discoveryFacility', 'tran_flag', 'ast_flag',
'obm_flag', 'orbitalPeriod', 'orbitSemiMaj', 'planetRadE', 'planetRadJ',
'planetDens', 'planetEcce', 'planetEqtT', 'starRadius', 'starMass',
'starDistance', 'planetMassJ', 'planetMassE'`


With the index representing the planet names.

### Data and acknowledgments
>This research has made use of the NASA Exoplanet Archive, which is operated by the California Institute of Technology,
> under contract with the National Aeronautics and Space Administration under the Exoplanet Exploration Program.

[Data Source](https://exoplanetarchive.ipac.caltech.edu/docs/data.html)
