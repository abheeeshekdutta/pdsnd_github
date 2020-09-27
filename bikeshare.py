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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('\nEnter the city name(chicago, washington or new york city): ').lower()
    while(city not in ['chicago','washington','new york city']):
        city = input('\nPlease enter a valid city name(chicago, washington or new york city): ').lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('\nEnter the month nameall, january, february, march, april, may , june): ').lower()
    while(month not in ['all','january','february','march','april','may','june']):
        month = input('\nPlease enter a valid month choice(all, january, february, march, april, may , june): ' ).lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('\nEnter the day of the week(all, monday, tuesday, wednesday, thursday, friday, saturday, sunday): ').lower()
    while(day not in['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']):
        day = input('\nPlease enter a valid day choice(all, monday, tuesday, wednesday, thursday, friday, saturday, sunday): ' ).lower()

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
    #Filter by city first
    df = pd.read_csv(CITY_DATA[city],index_col=0)

    while True:
        show_data = input('\nWould you like to see raw data for '+ city +'? Enter yes or no.\n')
        if show_data.lower() != 'yes':
            break
        else:
            print(df.sample(n = 5))
            print('-'*40)

    #Convert start and end time columns to datetime type
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    print('-'*40)
    print('\nExtracting month, day of week and hour from Start Time...')
    df['Month'] = df['Start Time'].apply(lambda x: x.strftime('%B').lower())
    df['Day Of Week'] = df['Start Time'].apply(lambda x: x.strftime('%A').lower())
    df['Start Hour'] = df['Start Time'].apply(lambda x: x.strftime('%-I %p'))


    #Filter by month IF month is not given as 'all'. If all was mentioned, skip this filtering code
    if(month != 'all'):
        df = df[df['Month'] == month]

    #Filter by day IF day is not given as 'all'. If all was mentioned, skip this filtering code
    if(day != 'all'):
        df = df[df['Day Of Week'] == day]


    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print('The most common month is: ' + df['Month'].mode()[0])

    # TO DO: display the most common day of week
    print('The most common day of the week : ' + df['Day Of Week'].mode()[0])

    # TO DO: display the most common start hour
    print('The most common start hour is: ' + df['Start Hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('The most common start station is: ' + df['Start Station'].mode()[0])

    # TO DO: display most commonly used end station
    print('The most common end station is: ' + df['End Station'].mode()[0])

    # TO DO: display most frequent combination of start station and end station trip
    print('The most common combination of start and end stations is: ' + str(df.groupby(['Start Station','End Station']).size().idxmax()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('Total travel time(in seconds) is : ' + str(df['Trip Duration'].astype('int').sum()))

    # TO DO: display mean travel time
    print('Mean travel time(in seconds) is : ' + str(df['Trip Duration'].astype('int').mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print(df['User Type'].value_counts())

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        print(df['Gender'].value_counts())
    else:
        print('\nGender information unavailable for Washington data')



    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:

        print('\nThe earliest year of birth is : ' + str(df[df['Birth Year'].notnull()]['Birth Year'].min()))
        print('The most recent year of birth is : ' + str(df[df['Birth Year'].notnull()]['Birth Year'].max()))
        print('The most common year of birth is : ' + str(df[df['Birth Year'].notnull()]['Birth Year'].mode()[0]))
    else:
        print('Birth year information unavailable for Washington data\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)

        #Remove temporary columns from dataframe
        df.drop(columns = ['Month', 'Day Of Week', 'Start Hour'], inplace=True)

        station_stats(df)

        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
