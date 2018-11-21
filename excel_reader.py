import pandas as pd
file_id = '1atn_R-iKdet3cxx5WCuNavwdHq82qgqG'
link = 'https://drive.google.com/uc?export=download&id={FILE_ID}'
csv_url=link.format(FILE_ID=file_id)
xls = pd.ExcelFile(csv_url)
df1 = pd.read_excel(xls, 0)
df2 = pd.read_excel(xls, 1)
#Note that the sheet_name argument to pd.read_excel() can be the name of the sheet
#(as above), an integer specifying the sheet number (eg 0, 1, etc), a list of
#sheet names or indices, or None. If a list is provided, it returns a dictionary
#where the keys are the sheet names/indices and the values are the data frames.
#The default is to simply return the first sheet (ie, sheet_name=0).
#If None is specified, all sheets are returned, as a {sheet_name:dataframe} dictionary.

print(df1)
