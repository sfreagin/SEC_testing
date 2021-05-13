# Analyzing Publicly-Traded Businesses (stocks)

Hello! This repo contains financial data for publicly-traded companies, often referred to as *stocks*. The materials here are meant to help guide investment decisions and a better understanding of business financials generally.

We are NOT trying to "predict stocks" nor "beat the market" nor anything to do with stock buying / trading strategies. We are rather going to investigate the *financial characteristics* of publicly-traded companies, e.g. their Revenues, Earnings, Assets, Libailities, Cash Flows, etc. We will use those characteristics to predict / project future values, and hopefully gain a better understanding for how to value a business.

All financial data is ultimately sourced from [stockrow.com](https://stockrow.com/)

This repository is organized as follows:
### Financial sheet workbooks
These folders contain the raw data as pulled from stockrow.com:
- /BalanceSheet/
- /CashFlow/
- /Income/


### Jupyter notebooks
- **DCF_walkthrough**
    - I created this as an in-class exercise but it's quite available for anyone to use. Much of the code is reproduced in the *growth_calcs* notebook
- **pulling_stockrow**
    - This is the primary working file for pulling and cleaning stockrow.com data, turning the information into manageable DataFrames
- **graphic_test**
    - Generate quick images of select Income Statement, Balance Sheet, and Cash Flow Statement data. This pulls directly from stockrow. not a local repo
- **growth_calcs**
    - This is the basis for our Discounted Cash Flow (DCF) model, and much of its code is reproduced in the streamlit_bokeh.py app

### Streamlit App
See the streamlit share app located here: https://share.streamlit.io/sfreagin/sec_testing/main/streamlit_bokeh.py

It comes in two parts:
- **streamlit_bokeh.py**
    - This is the actual python code itself that takes user input and generates three financial charts plus a DCF projection model (maybe)
    - **requirements.txt**
    - This is a required document for any app to run on streamlit share, listing the required libraries and versions
    - You can autogenerate using pipreqs : https://stackoverflow.com/questions/57907655/how-to-use-pipreqs-to-create-requirements-txt-file
    
### Classification Models
These notebooks are in the */classification_models/* folder:
- **KMeans**
- **RandomForest**
- **LogReg** (not robust)

### images
Just a few images I pulled from the KMeans model -- do they look like Jackson Pollock paintings to you? Or just me?

### Miscellaneous .csv files
- **combo_df.csv**
    - This is the final output of the *pulling_stockrow.ipynb* file, and it contains financial data for all companies which did not throw errors
    - 2,889 companies / 104,000 rows of data / 15 features plus Date index and Ticker (17 total pseudo-features)
- **list_of_stocks.csv**
    - This is my source of public company tickers and industry sector. Forgive me but I've misplaced the original source :(
    
### Notes from other sources
This /*Notes_from_other_sources*/ folder contains some of the first explorations, in which I tried to parse data directly from SEC.gov. I followed along with several videos from SigmaCoding, who figured out how to extract Balance Sheet (et cetera) data directly from the EDGAR search tool on the SEC.gov website. I highly recommend his channel: https://www.youtube.com/channel/UCBsTB02yO0QGwtlfiv5m25Q