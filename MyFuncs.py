
import datetime

def date_to_weekday(sheet):
	return [date.weekday() for date in sheet['Date'].tolist()]

def date_to_yearday(sheet):
	return [(date-datetime.datetime(year=date.year,month=1,day=1)).days for date in sheet['Date'].tolist()]

def read_sheet(sheet):
	return sheet['Last Price'].tolist(), date_to_yearday(sheet), date_to_weekday(sheet)

# bruno testing
import pandas as pd
import time
# clock
start = time.time()
xls = pd.ExcelFile('./SECRET ADMIRER.xlsx')
end = time.time()
elapsed = end - start
print(elapsed)

USDEUR = xls.parse(xls.sheet_names.index('EURUSD BGN'))

a = date_to_weekday(USDEUR)
b = date_to_yearday(USDEUR)
c = read_sheet(USDEUR)

print(a[0])
print(b[0])
print(c[1][0])
