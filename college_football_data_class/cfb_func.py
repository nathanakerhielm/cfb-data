
# College Football Functions
#
# Author(s):        BDT
# Developed:        09/02/2019
# Last Updated:     09/21/2019
# Version History:  [v01 09/02/2019] Prototype to get schedule and record info
#                   [v02 09/21/2019] Rewrite for increased efficiency
#                   [v03 09/25/2019] Rewrite completed
#
# Purpose:          This script is used by the college_football_data_class
#                   module for various functions
#
# Special Notes:    n/a
#
# Dev Backlog:      1) Rewrite code for added efficiency
#                   2) Add comments
#                   3) Fix handling for HTML conversion of dfs to be more modularized (header, style, table, footer)

import pandas as pd #to handle data in pandas dataframes
pd.set_option('display.max_rows', 500) #allow printing lots of rows to screen
pd.set_option('display.max_columns', 500) #allow printsin lots of cols to screen
pd.set_option('display.width', 1000) #don't wrap lots of columns

import requests #to pull JSON data
import numpy as np #to do conditional pandas operations
import datetime as dt #to track datetime stamps

from dateutil import tz #for timezone handling with datetime dtypes
api_mask = '%Y-%m-%dT%H:%M:%S.000Z' #this is the datetime string
                                    #format native to the API
                                    #output
readable_mask = "%a %m/%d/%Y %I:%M%p %Z" #this is a readable format
year_mask = "%Y" #just the year
from_zone = tz.tzutc() #API datetimes are in UTC time
to_zone = tz.tzlocal() #Used for converting to local timezone


def get_full_year_schedule_all_teams(year):
    r = requests.get(
        'https://api.collegefootballdata.com/games?year=' + str(year) + \
        '&seasonType=both'
    ).json()

    df = pd.DataFrame(r)
    
    df = df.sort_values(by=['season','season_type','week'], ascending=[True,False,True])
    
    df['start_time_dt'] = pd.to_datetime(df['start_date'].values, format=api_mask, utc=True).tz_convert(to_zone)
    df['start_time_str'] = pd.to_datetime(df['start_date'].values, format=api_mask, utc=True).tz_convert(to_zone).strftime(readable_mask)
    df['start_year_dtper'] = pd.to_datetime(df['start_date'].values, format=api_mask, utc=True).tz_convert(to_zone).tz_convert(None).to_period('Y')
    df['start_year_int'] = df['start_year_dtper'].astype(int) + 1970
    
    return df


def get_current_year():
    return int(dt.datetime.now().year)


def html_header(my_title=''):
    html_script = """
    <!DOCTYPE html>
    <HTML>
        <HEAD>
            <TITLE>"""
    
    html_title = my_title + '</TITLE>'
    
    html_script = html_script + '\n' + html_title    
    
    return html_script

def html_style_header():

    html_script = """
    <!-- CSS goes in the document HEAD or added to your external stylesheet -->
    <style type="text/css">
    table.gridtable {
        font-family: verdana,arial,sans-serif;
        font-size:11px;
        border-width: 1px;
        border-color: #666666;
        border-collapse: collapse;
    }
    table.gridtable th{
        border-width: 1px;
        padding: 18px;
        border-style: solid;
        border-color: #666666;
        background-color: #dedede;
    }
    table.gridtable td{
        border-width: 1px;
        padding: 6px;
        border-style: solid;
        border-color: #666666;
        background-color: #ffffff;
    }
    /* Define the default color for all the table rows */
    .gridtable tr{
        background: #b8d1f3;
    }
    /* Define the hover highlight color for the table row */
    .gridtable td:hover {
        background-color: #ffff99;
    }

    </style>
    </HEAD>
    """
    
    return html_script

def html_from_df(df):

    html_script = df.to_html(index=False).replace(
        '<table border="1" class="dataframe">',
        '<table class="gridtable">'
    )
    
    return html_script

def html_footer():

    html_script = """
    </BODY>
    </HTML>
    """
    
    return html_script

def df_to_html(my_title, df):

    html_script = ''
    html_script = html_script + html_header(my_title)
    html_script = html_script + html_style_header()
    html_script = html_script + html_from_df(df)
    html_script = html_script + html_footer()
    
    return html_script