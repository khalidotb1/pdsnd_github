import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

CITIES = ['chicago', 'new york', 'washington']

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all' ]


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    print("\nChoose a City: New York City, Chicago or Washington?")
    while True:
       city = input('ENTER A CITY: ').lower()
       if city in CITIES:
           break


    # get user input for month (all, january, february, ... , june)
    print("\nChoose a Month: January, February, March, April, May, June or  all")
    while True:
        month = input('ENTER A MONTH: ').lower()
        if month in MONTHS:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print("\nChoose a day: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or all")
    while True:
        day = input('ENTER A DAY: ').lower()
        if day in DAYS:
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
    #load selected file from the user into data frame
    df = pd.read_csv('{}.csv'.format(city))

    #convert Start Time and End Time columns to date
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month, day and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month
    if month != 'all':
        month =  MONTHS.index(month) + 1
        df = df[ df['month'] == month ]

    # filter by day
    if day != 'all':
        df = df[ df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month is: ", df['month'].value_counts().idxmax())

    # display the most common day of week
    print("The most common day is: ", df['day_of_week'].value_counts().idxmax())

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("The most common hour is: ", df['hour'].value_counts().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most common start station is: ", df ['Start Station'].value_counts().idxmax())

    # display most commonly used end station
    print("The most common end station is: ", df['End Station'].value_counts().idxmax())

    # display most frequent combination of start station and end station trip
    most_common_start_end_station = df[['Start Station', 'End Station']].mode().loc[0]
    print("The most frequent combination of start station and end station trip are {}, {}".format(most_common_start_end_station[0],most_common_start_end_station[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time in hours
    total_duration = df['Trip Duration'].sum() / 3600
    print("total travel time {} Hours".format(int(total_duration)))

    # display mean travel time in minutes
    mean_duration = df['Trip Duration'].mean() / 60
    print("mean travel time {} Minutes".format(int(mean_duration)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of user types:")
    user_types = df['User Type'].value_counts()
    print(user_types.to_string())

    # Display counts of gender
    try:
        print("\nCounts of of gender:")
        user_gender = df['Gender'].value_counts()
        print(user_gender.to_string())
    except KeyError: print("US Bikeshare does not provide information on genders in Washington")

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_yob = int(df['Birth Year'].min())
        most_recent_yob = int(df['Birth Year'].max())
        most_common_yob = int(df['Birth Year'].value_counts().idxmax())

        print("\nThe earliest year of birth is: {} \n"
          "The most recent year of birth is: {} \n"
          "The most common year of birth is: {}".format(earliest_yob,most_recent_yob,most_common_yob))
    except KeyError: print("US Bikeshare does not provide information on years of birth in Washington")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data (df):
    """Displays the 5 rows will added in each time"""
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 5
    while (view_data != 'no'):
        print(df.head(start_loc))
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()