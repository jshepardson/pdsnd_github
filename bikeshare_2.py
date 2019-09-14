import time
import pandas as pd
import numpy as np
import calendar as cal

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
    print('Hello! Let\'s explore some US bikeshare data!\n')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_list = ['Chicago','New York City','Washington']
    print('Valid City Names Are: {} \n'.format(city_list))
    
    valid_input = False
    while not valid_input:
        try:
            city = str(input('Please enter a city from the list of valid cities.\n'))
            print('\n')
            if city in city_list:
                valid_input = True
            else:
                raise ValueError
        except:
              print('"{}" is not a valid input. Please enter a city from the list of valid cities.\n'.format(city))

    # get user input for month (all, january, february, ... , june)
    #month = 'january'
    month_list = ['all','january', 'february', 'march', 'april', 'may', 'june']
    print('Months for which we have data are: {} \n'.format(month_list))
    
    valid_input = False
    while not valid_input:
        try:
            month = str(input('Please enter a month or all to select no filter. (all, january, february, ... , june)\n'))
            print('\n')
            if month in month_list:
                valid_input = True
            else:
                raise ValueError
        except:
              print('"{}" is not a valid mounth. Please enter a valid month or all.\n\n'.format(month))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    #day = 'Monday'
    day_list = ['all','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday']
    print('Valid days are: {} \n'.format(day_list))
    
    valid_input = False
    while not valid_input:
        try:
            day = str(input('Please enter a day of the week or all to select no filter. (all, monday, tuesday, ... sunday)\n'))
            print('\n')
            if day in day_list:
                valid_input = True
            else:
                raise ValueError
        except:
              print('"{}" is not valid. Please enter a valid weekday or all.\n'.format(day))

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
        df - pandas DataFrame containing city data filtered by month and day
    """
    #Make sure other city and Day are correct case
    city = city.lower()
    month = month.lower()
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['start_hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        month = months.index(month) + 1
        
        #Creat is month series to collect month indexes
        is_month = df['month'] == month
        
        # filter by month to create the new dataframe
        df = df[is_month]

    # filter by day of week if applicable
    if day != 'all':
        #Capitalize day parameter
        day = day.title()
        
        #Creat is day series to collect month indexes
        is_day = df['day_of_week'] == day
        
        # filter by day of week to create the new dataframe
        df = df[is_day]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].value_counts().idxmax()
    
    # display the most common day of week
    common_day_of_week = df['day_of_week'].value_counts().idxmax()

    # display the most common start hour
    common_hour = df['start_hour'].value_counts().idxmax()

    # consolidate print statements
    print('Month with the most use based on the selected filter: {} \n'.format(cal.month_name[common_month]))
    print('Day of the week with the most use based on selected filter: {} \n'.format(common_day_of_week))
    print('Hour of the day with the most use based on selected filter: {} \n'.format(common_hour))
 
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # find the most common hour (from 0 to 23)
    popular_hour = df['start_hour'].mode()[0]
    hour_count = (df['start_hour'] == popular_hour).sum()
 
    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    start_count = (df['Start Station'] == popular_start).sum()

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    end_count = (df['End Station'] == popular_end).sum()

    # display most frequent combination of start station and end station trip
    popular_trip = df[['Start Station','End Station']].mode()

    print('Most Frequent Start Hour:', popular_hour, '\nWith a count of: ', hour_count, '\n')
    print('Most Popular Start Station:', popular_start, '\nWith a count of: ', start_count, '\n')
    print('Most Popular End Station:', popular_end, '\nWith a count of: ', end_count, '\n')
    print('Most Popular Trip:\n{}'.format(popular_trip.to_string(index=False, justify='left')))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
   
    # display max travel time
    max_rental = df['Trip Duration'].max() / 60
    max_rental = round(max_rental, 0)

    # display min travel time
    min_rental = df['Trip Duration'].min() / 60
    min_rental = round(min_rental, 0)
    
    # display total travel time
    total_travel = df['Trip Duration'].sum() / 60
    total_travel = round(total_travel, 0)
    
    # display mean travel time
    mean_travel = df['Trip Duration'].mean() / 60
    mean_travel = round(mean_travel, 0)
 
    print('Longest rental time during selected filter: ', int(max_rental), 'minute(s)')
    print('Shortest rental time during selected filter: ', int(min_rental), 'minute(s)')
    print('Mean travel time during selected filter: ', int(mean_travel), 'minute(s)\n\n')
    print('Total travel time during selected filter: ', int(total_travel), 'minute(s)')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Count by user types:\n{}\n'.format(user_types))

    # Display counts of gender
    if city != 'Washington':
        gender_count = df['Gender'].value_counts()
        
        # Display earliest, most recent, and most common year of birth
        old_birth_year = int(df['Birth Year'].min())
        young_birth_year = int(df['Birth Year'].max())
        commmon_birth_year = int(df['Birth Year'].mode())

        print('Count by gender:\n{}\n'.format(gender_count))
        print('Rider Birth Year:\nOldest: {}\nYoungest: {}\nMost Common: {}\n'.format(old_birth_year,young_birth_year,commmon_birth_year))
    else:
        print('No rider statistics for gender or birth year are available for {}.\n'.format(city))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def continue_review():
    """Allow user to break the flow of data for review"""
    print('Press Enter to continue...\n')
    input()
    return

def raw_data_sample(df):
    """Asks user if they would like to see a sample of the raw data."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    five_rows = df.head()
    bottom_five = df.tail()

    # get user input (Yes or No)
    valid_choices = ['yes','no']
    valid_input = False
    while not valid_input:
        try:
            choice = str(input('Would you like to review a sample of the raw data? (yes or no)\n').lower())
            print('\n')
            if choice in valid_choices:
                if choice == 'yes':
                    print('Top five rows:\n', five_rows)
                    print('Bottom five rows:\n', bottom_five)
                else:
                    return
                valid_input = True
            else:
                raise ValueError
        except:
              print('"{}" is not a valid input. Please enter Yes or No.\n'.format(choice))

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        continue_review()
        station_stats(df)
        continue_review()
        trip_duration_stats(df)
        continue_review()
        user_stats(df,city)
        raw_data_sample(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
