
import datetime

def date_to_weekday(sheet):
	return [date.weekday() for date in sheet['Date'].tolist()]

def date_to_yearday(sheet):
	return [(date-datetime.datetime(year=date.year,month=1,day=1)).days for date in sheet['Date'].tolist()]

def read_sheet(sheet):
	return sheet['Last Price'].tolist(), date_to_yearday(sheet), date_to_weekday(sheet)