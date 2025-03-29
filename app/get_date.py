from datetime import datetime, timedelta

def get_yesterday():
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    yesterday_str = yesterday.strftime('%d/%m/%Y')
    return yesterday_str
def format_date(date_str):
    date_object = datetime.strptime(date_str, "%Y-%m-%d")  # Parse the string
    formatted_date = date_object.strftime('%d/%m/%Y') 
    return formatted_date
def get_today():
    today = datetime.now()
    today_str = today.strftime('%d-%m-%Y')
    return today_str  
def get_3days_after(start_date: str):
    days = 2
    start_date_object = datetime.strptime(start_date, "%d/%m/%Y") 
    if start_date_object.weekday() in [2, 3, 4]:
        days = 5
    elif start_date_object.weekday() == 5:
        days = 4
    elif start_date_object.weekday() == 6:
        days = 3
    n_after = start_date_object + timedelta(days=days)
    n_after_str = n_after.strftime('%d/%m/%Y')
    return n_after_str