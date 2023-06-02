import time
import pandas as pd
import numpy as np

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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Would you like to see data for Chicago, New York, or Washington? \n").lower()

    while city not in ['chicago', 'new york', 'washington']:
        city = input('input city name is not valid, please choose between Chicago, New York, or Washington\n').lower()

    #match city name to CITY_DATA
    if city == 'new york':
        city = 'new york city'

    global input_filter
    input_filter = input(
        'Would you like to filter the date by month, day, both, or not at all? Type \"none\" for no time filter\n').lower()
    while input_filter not in ['month', 'day', 'both', 'none']:
        city = input('input option is not valid, please choose between month, day, both, or none\n')

    month = 'all'
    day = 'all'

    # get user input for month (all, january, february, ... , june)
    if input_filter == 'month' or input_filter == 'both':
        month = input('which month? January, February, March, April, May, or June?\n').lower()
        while month not in ['january', 'february', 'march', 'april', 'may', 'june']:
            month = input('input not valid, please choose between January, February, March, April, May, or June?\n').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if input_filter == 'day' or input_filter == 'both':
        day = input('which day? Please type your response (e.g., Sunday)\n').lower()
        while day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            day = input('input not valid, please choose between Monday, Tuesday, Wednesday, Thursday, Friday, '
                        'Saturday, Sunday\n').lower()

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
    df = pd.read_csv(CITY_DATA[city])

    #convert start time to datetime object and extract month and day of week as new columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    #filter month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        #get the index of month in months which convert month from string to int
        month = months.index(month) + 1
        df = df[df.month == month]
    return df

    # filter by day of week
    if day != 'all':
        df = df[df.day_of_week == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if input_filter not in ['month', 'both']:
        popular_month = df['month'].mode()[0]
        count_month = df['month'].value_counts()[popular_month]

        print('Most popular month: ' + str(popular_month), end='')
        print(', Count: ' + str(count_month), end='')
        print(' Filter: ' + input_filter)

    # display the most common day of week
    if input_filter not in ['day', 'both']:
        popular_day_of_week = df['day_of_week'].mode()[0]
        count_day = df['day_of_week'].value_counts()[popular_day_of_week]

        print('Most popular day: ' + str(popular_day_of_week), end='')
        print(', Count: ' + str(count_day), end='')
        print(' Filter: ' + input_filter)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    count_hour = df['hour'].value_counts()[popular_hour]

    print('Most popular day: ' + str(popular_hour), end='')
    print(', Count: ' + str(count_hour), end='')
    print(' Filter: ' + input_filter)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    count_start_station = df['Start Station'].value_counts()[popular_start_station]
    
    print('Most popular Start Station: ' + str(popular_start_station), end='')
    print(', Count: ' + str(count_start_station), end='')
    print(' Filter: ' + input_filter)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    count_end_station = df['End Station'].value_counts()[popular_end_station]
    
    print('Most popular End Station: ' + str(popular_end_station), end='')
    print(', Count: ' + str(count_end_station), end='')
    print(' Filter: ' + input_filter)

    # display most frequent combination of start station and end station trip
    popular_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    count_trip = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False)[0]
    
    print('Most popular Trip: ' + str(popular_trip), end='')
    print(', Count: ' + str(count_trip), end='')
    print(' Filter: ' + input_filter)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('total travel time : ' + str(df["Trip Duration"].sum()), end='')
    print(', Count: ' + str(df.shape[0]), end='')

    # display mean travel time
    print(', mean travel time : ' + str(df["Trip Duration"].mean()), end='')
    print(' Filter: ' + input_filter)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    if city != 'washington':
        # Display counts of user types
        user_type = df['User Type'].value_counts()
        print(user_type)

        # Display counts of gender
        gender_type = df['Gender'].value_counts()
        print(gender_type)

        # Display earliest, most recent, and most common year of birth
        print('Earliest year of birth: ' + str(int(df["Birth Year"].min())),
              end='')
        print(
            ', Most recent year of birth: ' + str(int(df["Birth Year"].max())),
            end='')
        print(', Most common year of birth: ' + str(int(df['Birth Year'].mode()[0])), end='')
        print(', Count: ' + str(df['Birth Year'].value_counts()[df['Birth Year'].mode()[0]]), end='')
        print(' Filter: ' + input_filter)

    else:
        print('Washington has no user gender and birth year data')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Display data"""
    pd.set_option('display.max_columns', 200)

    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start = 0

    while True:
        if view_data == 'yes':
            print(df.iloc[start:start+5,:])
            start += 5
            view_data = input("Do you wish to continue?: ").lower()

        elif view_data == 'no':
            break   

        else: 
            view_data = input('Please enter yes or no.\n').lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()

        while restart not in ['yes', 'no']:
            restart = input('Please enter yes or no.\n').lower()
        
        if restart != 'yes':
            break

if __name__ == "__main__":
	main()
