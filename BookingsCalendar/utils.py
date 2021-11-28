from datetime import datetime, timedelta
from calendar import HTMLCalendar
import calendar
from schedular.models import UserBook,Schedule

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()
        calendar.setfirstweekday(calendar.SATURDAY)
        
    def formatday(self, day, bookings,user):
        bookings_per_day = bookings.filter(schedule__date__day=day)
        
        d = ''
        for booking in bookings_per_day:
            # print(booking)
            d += f'<li> {booking.get_html_url()} </li>'
        
        if day != 0:           
            return f"<span id='month' style='display: none;'>{self.month}</span><td title='{self.year}-{self.month}-{day} gregorian' id='{self.year}-{self.month}-{day}'><span class='{day} date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'
        
    def formatweek(self, theweek, bookings,user):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, bookings,user)
        return f'<tr> {week} </tr>'

    def formatmonth(self, user, withyear=True):
        bookings = UserBook.objects.filter(user=user).filter(schedule__date__year=self.year, schedule__date__month=self.month)
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, bookings,user)}\n'
        return cal