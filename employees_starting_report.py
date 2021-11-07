#!/usr/bin/env python3
import csv
import datetime
import requests

# csv data
FILE_URL = "https://storage.googleapis.com/gwg-content/gic215/employees-with-date.csv"

def get_start_date():
    """Interactively get the start date to query for."""
    print()
    print('Getting the first start date to query for.')
    print()
    print('The date must be greater than Jan 1st, 2018')
    year = int(input('Enter a value for the year: '))
    month = int(input('Enter a value for the month: '))
    day = int(input('Enter a value for the day: '))
    print()

    return datetime.datetime(year, month, day)

def get_file_lines(url):
    """Returns the lines contained in the file at the given URL"""
    # Download the file over the internet
    response = requests.get(url, stream=True)
    lines = []
    for line in response.iter_lines():
        lines.append(line.decode("UTF-8"))
    return lines


def get_same_or_newer(start_date):
    """Returns the employees that started on the given date, or the closest one."""
    data = get_file_lines(FILE_URL)
    reader = csv.DictReader(data)
    max_date = datetime.datetime.today()
    #print(max_date)
    myDict ={}
    for row in reader:
        #print(row)
        row_date = datetime.datetime.strptime(row['Start Date'], '%Y-%m-%d')
        #print(row_date)
        # skip if date is before user's stated date.
        if row_date < start_date:
            continue

        # join employee's first name and last name
        employee = '{} {}'.format(row['Name'],row['Surname'])
        # checks if date is within expected range.
        if row_date < max_date:
            myDict.setdefault(row_date,[])
            myDict[row_date].append(employee)

    # sort employees by employment started dates.
    for start_on,employees in sorted(myDict.items()):
       print('Started on {}: {}'.format(start_on.strftime('%b %d, %Y'),employees))
    
def main():
    start_date = get_start_date()
    get_same_or_newer(start_date)

if __name__ == "__main__":
    main()
