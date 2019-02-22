import time
import pandas as pd
import numpy as np
from datetime import datetime
import os

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print() 
    
    while True:
        city = input('Please enter the name of the city you are interested in. You can choose between Washington, New York City and Chicago: ')
        city = city.lower()
        while city not in ('washington', 'chicago', 'new york city'):
            print('Please check your input! Only these values are valid (without space or comma and in lower case): washington, new york city, chicago.')
            city = input('Please enter the city you are interested in: ')
            print()
            city = city.lower()
        else:
            print('Thanks for choosing ' + city.strip().title() + '!\n')
            break
        
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input('Please enter the month you are interested in. You can choose between: "January", "February", "March", "April", "May" and "June". If you do not want to filter per month just type in "all"): ')
        month = month.lower()
        while month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            print('Please check your input! Only these values are valid (without space, quotation marks or comma): "January", "February", "March", "April", "May", "June" or "all"')
            month = input('Please enter the month you are interested in: ')
            month = month.lower()
        else:
            print('Thanks for choosing ' + month.strip().title() + '!\n')
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Please enter the day of the week you are interested in. If you do not want to filter per month just type in "all"): ')
        day = day.lower()
        while day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
            print('Please check your input! Only these values are valid (without space, quotation marks or comma): "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday" or "all"')
            day = input('Please enter the day you are interested in: ')
            day = day.lower()
        else:
     
            print('Thanks for choosing ' + day.strip().title() +'!\n')
            break
            
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    
    Returns:
        monthname - str - Name of most popular month for filtered DataFrame
        dayname - str - Name of most popular weekday for filtered DataFrame
        popular_hour - int - Hour (range(24)) of most popular starting hour for filtered DataFrame
    """
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # convert datatype of column Start Time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month from the Start Time column to create a month column
    df['month'] = df['Start Time'].dt.month
    # find the most popular month
    popular_month = df['month'].mode()[0]
    # switch month number into monthname
    monthnames = ['january', 'february', 'march', 'april', 'may', 'june']
    for monthname in monthnames:
        if monthnames.index(monthname) + 1 == popular_month:
            break    
    print('Most Popular Month in selected data:', monthname.title())

    # extract weekday from the Start Time column to create a weekday column
    df['day_of_week'] = df['Start Time'].dt.weekday
    # find the most popular month
    popular_day = df['day_of_week'].mode()[0]
    daynames = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    for dayname in daynames:
        if daynames.index(dayname) == popular_day:
            break
    print('Most Popular Day in selected data:', dayname.title())

    # extract month from the Start Time column to create a month column
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular month
    popular_hour = df['hour'].mode()[0]
    # check if popular hour (which ist in range(24) due to dt.hour-method) + 1 is bigger than 23:00
    # In Germany there is no am or pm declaration but hours from 00:00 to 23:59. 
    # There is no 24:00 but 00:00 which is ensured by the following loop.
    if popular_hour == 23:
        print('Most Popular starting hour in selected data: '+ str(popular_hour) + ':00 to 00:00')
    else:
        print('Most Popular Starting hour in selected data: '+ str(popular_hour) + ':00 to '+ str(popular_hour+1)+':00')
        print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    
    Returns:
        popular_start_station - str - Name of most popular Start Station for filtered DataFrame
        popular_end_station - str - Name of most popular End Station for filtered DataFrame
        popular_start_end - str - Most popular combination of start and end station
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    if 'Start Station' in df.columns and 'End Station' in df.columns:
        # select most commonly used start station
        popular_start_station = df['Start Station'].mode()[0]
        print('Most popular Start Station in selected data: '+ popular_start_station)
       
        # select most commonly used end station
        popular_end_station = df['End Station'].mode()[0]
        print('Most popular End Station in selected data: '+ popular_end_station)
    
        # select most frequent combination of start station and end station trip
        df['start_end'] = df['Start Station'] +' to '+ df['End Station']
        popular_start_end = df['start_end'].mode()[0]
        print('Most popular combination of Start and End Station in selected data: '+ popular_start_end)
    else:
        print('Sorry! No Start or End Station data available!\n')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    
    Returns:
        total_travel_time - str - String that shows total travel time splitted up in Years, Days, Hours, Minutes and seconds depending on value
        mean_travel_time - str - String that shows mean travel time splitted up in Days, Hours, Minutes and seconds depending on value
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    if 'Trip Duration' in df.columns:
        
        # display total travel time (all rents sumed up)
        ttt = (df['Trip Duration'].sum()) # ttt is total_travel_time
        ttt_years = str(ttt//31557600)
        ttt_days  = str((ttt%31557600)//86400)
        ttt_hours = str(((ttt%31557600)%86400)//3600)
        ttt_mins  = str((((ttt%31557600)%86400)%3600)//60)
        ttt_secs  = str((ttt%60).round(2))
        if ttt <=60:
            total_travel_time = ttt_secs +' sec(s)'
        elif ttt <=3600:
            total_travel_time = ttt_mins+' min(s) '+ttt_secs+' sec(s)'
        elif ttt <=86400:
            total_travel_time = ttt_hours+' hour(s) '+ttt_mins+' min(s) '+ttt_secs+' sec(s)'
        elif ttt <=34557600:
            total_travel_time = ttt_days+ 'day(s) '+ttt_hours+' hour(s) '+ttt_mins+' min(s) '+ttt_secs+' sec(s)'
        else:
            total_travel_time = ttt_years+' year(s) '+ttt_days+' day(s) '+ttt_hours+' hour(s) '+ttt_mins+' min(s) '+ttt_secs+' sec(s)'
        print('The total travel time for the selected data is: {}'.format(total_travel_time))
        # TO DO: display mean travel time
        mtt = (df['Trip Duration'].mean()) # mtt is mean_travel_time
        mtt_days  = str(int(mtt//86400))
        mtt_hours = str(int((mtt%86400)//3600))
        mtt_mins  = str(int(((mtt%86400)%3600)//60))
        mtt_secs  = str((mtt%60).round(2))
      
        if mtt <=60:
            mean_travel_time = mtt_secs +' sec(s)'
        elif mtt <=3600:
            mean_travel_time = mtt_mins+' min(s) '+mtt_secs+' sec(s)'
        elif mtt <=86400:
            mean_travel_time = mtt_hours+' hour(s) '+mtt_mins+' min(s) '+mtt_secs+' sec(s)'
        else:
            mean_travel_time = mtt_days+' day(s) '+mtt_hours+' hour(s) '+mtt_mins+' min(s) '+mtt_secs+' sec(s)'
        print('The mean travel time for the selected data is: {}'.format(mean_travel_time))
    else:
        print('Sorry! No trip duration data available!\n')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users.
    
    Returns:
        user types - pd.series - shows counts of user types
        nullcount_usertype - int - shows number of rows with NaN values in 'User Type'
        genders - pd.series - shows counts of genders
        nullcount_gender - int - shows number of rows with NaN values in 'Gender'
        nullcount_birthyear - int - shows number of rows with NaN values in 'Birth Year'
        yob_earliest - int - shows earliest year from 'Birth Year'
        yob_recent - int - shows most recent year from 'Birth Year'
        yob_common.idxmax() - method - shows most common year from 'Birth Year' if this is a unique value
        yob_common_max_df.index.tolist() - method - shows most common years from !Birth Year' in a list if there is more than one value
        
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    if 'User Type' in df.columns:
        user_types = df['User Type'].value_counts()
        
        print('The selected data contains following counts of user types:')
        print(user_types.to_string()) # found on https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_string.html
        nullcount_usertype = len(df['User Type']) - df['User Type'].count()
        if nullcount_usertype != 0:
            print('For {} users there is no user type defined.'.format(nullcount_usertype))
    else:
        print('Sorry! No user type data available!\n')
    
    # TO DO: Display counts of gender
    print()
    # as column Gender is not in every csv file first check availability of column
    if 'Gender' in df.columns:
        genders = df['Gender'].value_counts()
        print('The selected data contains following counts of Genders:')
        print(genders.to_string()) # found on https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_string.html
        # as there are NaN values in column Gender...
        nullcount_gender = len(df['Gender']) - df['Gender'].count()
        if nullcount_gender != 0:
            print('No gender information given in {} rows.'.format(nullcount_gender))
    else:
        print('Sorry! No gender data available!\n')

    # TO DO: Display earliest, most recent, and most common year of birth
    # as column Birth Year is not in every csv file first check availability of column
    if 'Birth Year' in df.columns:
        # creating new df1 from df without rows where NaNs in Birth Year and convert to int
        nullcount_birthyear = len(df['Birth Year']) - df['Birth Year'].count()
        #as there are nullvalues in the Birth Year column...
        if nullcount_birthyear != 0:
            print('\nThe selected data has {} rows without Birth Year. These rows have been filtered out for the following three stats.'.format(nullcount_birthyear))
        df = df[df['Birth Year'].notnull()]
        df1 = df.copy()
        df1['Birth Year'] = df['Birth Year'].astype(int) # found on https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.astype.html
        # earliest year of birth
        yob_earliest = df1['Birth Year'].min()
        veryold = ''
        if yob_earliest <= 1920:
            veryold = '      OMG... Pretty old for riding a bike with '+str(2017 - yob_earliest)+' years of age! ;)'
        print('The earliest year of birth is: '+str(yob_earliest)+' '+veryold)
        
        # most recent year of birth        
        yob_recent = df1['Birth Year'].max()
        veryyoung = ''
        if yob_recent >= 2015:
            veryyoung = '   OMG... Pretty young for hiring a bike with '+str(2017 - yob_recent)+' year of age! ;)'
        print('The most recent year of birth is: '+str(yob_recent)+' '+veryyoung)
        # most common year(s) of birth incl. check for multiple max common years
        yob_common = df1['Birth Year'].value_counts()
        max_value = yob_common.max()
        counter = yob_common[yob_common.values == max_value].count() 
        if counter == 1:
            print('The most common year of birth is: '+str(yob_common.idxmax())) # found on https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.idxmax.html
        else:
            yob_common_max = yob_common.head(counter)
            yob_common_max_df = yob_common_max.to_frame() # found on https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.to_frame.html
            print('The following years are the most common: ')
            print(yob_common_max_df.index.tolist()) # found on https://stackoverflow.com/questions/17241004/how-do-i-get-a-dataframe-index-series-column-as-an-array-or-list
        
    else:
        print('Sorry! No data for date of birth available!\n')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    """Displays statistics on bikeshare users. This is the main function that executes all the above described functions
    
    Returns:
        all above described return values if available
        seedata - str - if y is entered/reentered the df is printed (in sets of 5 rows). breaks for any other input
        restart - str - if y is entered the main function is restarting. breaks for any other input
        
    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        seedata = input('If you want to see the data you selected enter y! If not enter any other key.\n')
        i = 0
        while seedata.lower() == 'y':
            print(df[i:(i+5)])
            i +=5
            seedata = input('For more data enter y!\n')
        restart = input('\nFor restart enter y. For exit press any other key!\n')
        if restart.lower() != 'y':
             break
        else:
            clear = lambda: os.system('cls||clear') # found on https://stackoverflow.com/questions/2084508/clear-terminal-in-python
            clear()
            
if __name__ == "__main__":
	main()