import math

# return whether a certain year is a leap year or not
# e.g. 2020 -> True; 2019 -> False
def is_leap_year(year):
    if 0 == year % 4 and 0 != year % 100 or 0 == year % 400:
        return True
    else:
        return False

# parse the date str ('yyyymmdd' or 'yyyy-mm-dd') to yyyy, mm, dd, 3 ints
# if the bits of yyyy is less than 4, or the bits of mm or dd less than 2, prefix them with 0(s)
def parse(date):
    date = date.replace('-', '').replace('_', '')
    if len(date) != 8:
        print('Invalid date %s.' % date)
        return -1, -1, -1

    yyyy = int(date[:4])
    mm = int(date[4:6])
    dd = int(date[-2:])

    if is_leap_year(yyyy):
        month_days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    else:
        month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    if mm <= 12 and dd <= month_days[mm - 1]:
        return yyyy, mm, dd
    else:
        print('Invalid date %s.' % date)
        return -1, -1, -1

# return the index of a certain date in that year
# e.g. '20200401' -> 92, which means it is the 92nd date in that year
def date2index(date):
    yyyy, mm, dd = parse(date)
    if mm == -1:
        return -1

    if is_leap_year(yyyy):
        month_days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    else:
        month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    date_in_year = dd
    for i in range(mm - 1):
        date_in_year += month_days[i]

    return date_in_year

# return the date str and parsed ints of the nth date in year yyyy
# e.g. 2020, 1 -> '20200101', 2020, 1, 1; 2019, 365 -> '20191331', 2019, 12, 31
# 645, 192 -> '06450711', 645, 7, 11
def index2date(yyyy, idx):
    if is_leap_year(yyyy):
        month_days_cum = [0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366]
    else:
        month_days_cum = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365]

    if idx <= 0 or idx > month_days_cum[-1]:
        return 'invalid index %s.' % idx, -1, -1, -1

    for i in range(1, 13):
        if idx <= month_days_cum[i]:
            mm = i
            dd = idx - month_days_cum[i - 1]

            return '%0004d%02d%02d' % (yyyy, mm, dd), yyyy, mm, dd

# return the day of a certain date
# e.g. '20200401' -> 3 (Wed)
def date2day(date):
    yyyy, mm, dd = parse(date)
    if mm == -1:
        return -1

    if yyyy < 1582 or yyyy == 1582 and mm < 10 or yyyy == 1582 and mm == 10 and dd < 15:
        return 'Can NOT calculate dates before Oct 15th 1582.'

    day = 0

    rela_hundreds = [0, 5, 3, 1]
    rela_tens = [0, 3, 6, 2, 5, 1, 4, 0, 3, 6]
    rela_month = [6, 2, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]

    if is_leap_year(yyyy) and mm <= 2:
        day += 6

    yyyy %= 400
    day += rela_hundreds[int(yyyy / 100) % 10]
    day += int(yyyy % 100 / 4)

    day += rela_tens[int(yyyy / 10) % 10]
    day += yyyy % 10
    day += rela_month[mm - 1]
    day += dd

    return day % 7

# return the date index of the nth Sun-day in year yyyy
# target = {'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'}
# e.g. 2020, 1, 'Tue' -> 7; 2020, 2, 'Thu' -> 9;
# 2020, 5, 'Sun' -> 33 which means the 33rd date (Feb 2nd) in 2020
# 2020, 9, 'Sat' -> 60 which means the 60th date (Feb 29th) in 2020
def day2index(yyyy, n, target='Sun'):
    if n <= 0 or n > 53:
        return 'Invalid num %s.' % n

    new_year_day = date2day(str(yyyy) + '0101')  # the day of the New Year's Day
    day_dict = {'Sun': 0, 'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6}
    target_day = day_dict[target]

    return (target_day - new_year_day + 7) % 7 + (n - 1) * 7 + 1

# return the week index of a certain date in that year
# start = {'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'} denotes the start day of a week
# e.g. start = 'Sun': '20200101' -> 1; '20200104' -> 1; '20200105' -> 2; '20200106' -> 2;
# start = 'Mon': '20200101' -> 1; '20200104' -> 1; '20200105' -> 1; 20200106' -> 2
def date2week(date, start='Sun'):
    yyyy, mm, dd = parse(date)
    if mm == -1:
        return -1

    date_in_year = date2index(date)
    index_1st_day = day2index(yyyy, 1, start)       # the index of the 1st Start-day

    week_in_year = math.ceil((date_in_year - index_1st_day + 1) / 7)
    if index_1st_day != 1:
        week_in_year += 1

    return  week_in_year

# return the number of leap years between two different years (borders are NOT counted)
# e.g 2020, 2021 -> 0; 2020, 2030 -> 2; 2016, 2020 -> 0; 2021, 2019 -> 1
def n_leaps(yyyy1, yyyy2):
    if yyyy1 > yyyy2:
        yyyy1, yyyy2 = yyyy2, yyyy1

    n = 0
    for y in range(yyyy1 + 1, yyyy2):
        if is_leap_year(y):
            n += 1
            y += 4

    return n

# return the interval between 2 dates
# e.g. '20190227', 20200403' -> 401; 20200403', '20200101' -> -91
def dates_interval(date1, date2):
    yyyy1, mm1, dd1 = parse(date1)
    yyyy2, mm2, dd2 = parse(date2)
    if -1 in (yyyy1, mm1, dd1, yyyy2, mm2, dd2):
        return float('inf')

    date_in_year1 = date2index(date1)
    date_in_year2 = date2index(date2)

    if yyyy1 == yyyy2:
        return date_in_year2 - date_in_year1
    elif yyyy1 < yyyy2:
        if is_leap_year(yyyy1):
            interval1 = 366 - date_in_year1
        else:
            interval1 = 365 - date_in_year1
        interval12 = (yyyy2 - yyyy1 - 1) * 365 + n_leaps(yyyy1, yyyy2)
        interval2 = date_in_year2

        return interval1 + interval12 + interval2
    else:
        if is_leap_year(yyyy2):
            interval2 = 366 - date_in_year2
        else:
            interval2 = 365 - date_in_year2
        interval21 = (yyyy1 - yyyy2 - 1) * 365 + n_leaps(yyyy2, yyyy1)
        interval1 = date_in_year1

        return -interval2 - interval21 - interval1

print(date2index('20200402'))              # 93
print(index2date(2020, 94))                  # ('20200403', 2020, 4, 3)
print(date2day('20200402'))                 # 4
print(day2index(2020, 14, 'Fri'))           # 94
print(date2week('20200402', 'Mon'))  # 14
print(n_leaps(2011, 2020))                   # 2
print(dates_interval('20110902', '20160710'))   # 1773