import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

#@param	url, a string represents interested URL address
#output two tables
def craw_tables(url):
	## open destination url and parse into inso BeautifulSoup Object
	page = urllib.request.urlopen(url)
	soup = BeautifulSoup(page, 'html.parser')
	tables = soup.find_all('table')
	unplanned = tables[0].find_all('tr')
	planned = tables[1].find_all('tr')
	## get table header
	header = []
	for e in unplanned[0].find_all('th'):
		header.append(e.string)
	unplanned_table = get_table_elements(unplanned, header)
	planned_table = get_table_elements(planned, header)
	return (unplanned_table, planned_table)

#@param	soup, a BeautifulSoup object
#output: table as a list
def get_table_elements(soup, header):
	table = []
	table.append(header)
	for row in soup:
		lst = []
		for e in row.find_all('td'):
			lst.append(e.text)
		table.append(lst)
	table.remove([]) #remove the empty element caused by header
	return table 

def extract_remarks(string):
	if 'mcm/day' in string:
		if string.split('mcm/day')[1].strip() == '':
			return 'null'
		else:
			return string.split('mcm/day')[1].strip()
	else:
		return string

def extract_volume(string):
	if 'mcm/day' in string:
		return float(string.split('mcm/day')[0].strip())
	else:
		return 'null'

def convert_date(string):
	try:
		return pd.to_datetime(string)
	except Exception:
		return string

#@param df, a dataframe
#output another dataframe after manipulation
def data_manipulation(df):
	#replace na values
	df= df.replace(['', 'NA', 'Unknown', '-'], 'null')
	df['Time Published']=df['Time Published'].apply(convert_date)
	df['Time of Event']=df['Time of Event'].apply(convert_date)
	df['Expected End']=df['Expected End'].apply(convert_date)
	df['Actual End']=df['Actual End'].apply(convert_date)
	#create another variable
	df['Remarks']=df['Volume impact mcm/day'].apply(extract_remarks)
	df['Volume impact mcm/day']=df['Volume impact mcm/day'].apply(extract_volume)
	return df


url = 'https://www.shell.co.uk/business-customers/upstream-oil-and-gas-infrastructure/upstream-operational-information.html'
tables = craw_tables(url)

# convert into pandas dataframe & further data manipulation
unplanned = data_manipulation(pd.DataFrame(tables[0][1:len(tables[0])], columns = tables[0][0]))
planned = data_manipulation(pd.DataFrame(tables[1][1:len(tables[1])], columns = tables[1][0]))

#write as csv file
unplanned.to_csv("Unplanned Table.csv")
planned.to_csv("Planned.csv")
print("Tables saved as CSV files success.\n")















