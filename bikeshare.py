import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

days = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            global city
            city = input('Would you like to see data from Chicago, New York City or Washington?\n')
        except:
            print('That is not a valid entry.')
        if city.lower() in CITY_DATA:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input('Would you like to see data from January, February, March, Arpil, May, June or "all" data.\n')
        except:
            print('That is not a valid entry.')
        if month.lower() in months:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input('Choose which day of the week you would like to see data from or choose "all" if you want to see data from all days.\n')
        except:
            print('That is not a valid entry.')
        if day.lower() in days:
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
    df = pd.read_csv(CITY_DATA[city.lower()])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    if month.lower() != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1
        df = df[df['month'] == month]
   
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_number = df['month'].mode()[0]
    common_month = months[month_number].title()
    print('The most common month is ',common_month,'.\n')

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The most common day of the the week is ',common_day,'.\n')

    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('The most common start hour is ',common_hour,'.\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most common start station is ',common_start_station,'.\n')

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most common end station is ',common_end_station,'.\n')

    # display most frequent combination of start station and end station trip
    df['start to end'] = df['Start Station'] + ' to ' + df['End Station']
    common_start_end = df['start to end'].mode()[0]
    print('The most common start and end station combination is:\n',common_start_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total = df['Trip Duration'].sum()
    total_days = int(total/86400)
    total_hr = int((total%86400)/3600)
    total_min = int(((total%86400)%3600)/60)
    total_sec = ((total%86400)%3600)%60
    print('The total travel time is:\n {} days, {} hours, {} minutes and {} seconds\n'.format(total_days, total_hr, total_min, total_sec))

    # display mean travel time
    mean = df['Trip Duration'].mean()
    mean_min = int(mean/60)
    mean_sec = mean%60
    print('The mean travel time is {} minutes and {} seconds .\n'.format(mean_min, mean_sec))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User types and counts are as follows:\n',user_types,'\n')

    # Display counts of gender
    if city.lower() == 'washington':
        print('There is no gender data for Washington.\n')
    else:
        genders = df['Gender'].value_counts()
        print('Genders and counts are as follows:\n',genders,'\n')

    # Display earliest, most recent, and most common year of birth
    if city.lower() == 'washington':
        print('There is no birth year data for Washington.\n')
    else:
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        most_common = int(df['Birth Year'].mode()[0])
        print('The earliest, most recent, and most common year of birth are', earliest, ',', most_recent, ',', '&', most_common, 'respectively.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        n = 0

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        while True:
            try:
                raw_data = input('\nWould you like to see some of the raw data, yes or no?\n')
            except:
                print('That is not a valid entry.')
           
            df = pd.read_csv(CITY_DATA[city.lower()])
            df['Start Time'] = pd.to_datetime(df['Start Time'])
            df['month'] = df['Start Time'].dt.month
            df['day_of_week'] = df['Start Time'].dt.weekday_name
    
            if month.lower() != 'all' and type(month) == 'str':
                months = ['january', 'february', 'march', 'april', 'may', 'june']
                month = months.index(month.lower()) + 1
                df = df[df['month'] == month]
            else:
                month = month
   
            if day != 'all':
                df = df[df['day_of_week'] == day.title()]
    
            if raw_data.lower() == 'yes':
                n += 5
                print(df.head(n))
            else:
                break
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
