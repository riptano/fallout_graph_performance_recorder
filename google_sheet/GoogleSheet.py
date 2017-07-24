import os
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class GoogleSheet():
	scope = None
	credentials = None
	google_sheet_name = None
	worksheet_name = None
	worksheet = None

        def __init__(cls, google_sheet_name, worksheet_name):
		"""
		@param google_sheet_name:	name of the Google sheet we write to
		@type google_sheet_name:	str
		@param worksheet_name:		name of the worksheet within the Google sheet we will write to
		@type worksheet_name:		str
		"""
		cls.scope = ['https://spreadsheets.google.com/feeds']
		# TO DO: Make this cleaner
		path_to_google_json = os.environ['GOOGLE_JSON_PATH']
		cls.credentials = ServiceAccountCredentials.from_json_keyfile_name(path_to_google_json, cls.scope)
		cls.google_sheet_name = google_sheet_name
		cls.worksheet_name = worksheet_name
		cls.worksheet = gspread.authorize(cls.credentials).open(cls.google_sheet_name).worksheet(cls.worksheet_name)

        def write_results(self, list_of_column_headers, list_of_data_dicts):
		"""
		@param list_of_column_headers:	list of ordered column headers for our Google sheet
		@type list_of_column_headers:	list of str
		@param list_of_data_dicts:	list of dicts (each of which maps a query to a corresponding result for the query);
						each dict in the list is to correspond to a column in the spreadsheet
		@type list_of_data_dicts:	list of dicts
		"""
		# this will reset the worksheet to empty
                self.worksheet.resize(rows=1)
		# we know the very first column will correspond to queries
		column_headers = ["QUERIES"] + list_of_column_headers
		# write out the appropriate column titles:
		print column_headers
                self.worksheet.append_row(column_headers)
		list_of_rows = []
		# the fallout test run URL will be written last
		fallout_url_row = []
		# iterate through our set of queries
		for query in list_of_data_dicts[0]:
			curr_row = [query]
			# iterate through data dicts, "add a cell" to curr_row
			for data_dict in list_of_data_dicts:
				curr_row.append(data_dict[query])
			if query == 'FALLOUT TEST RUN URL':
				fallout_url_row = curr_row
			else:
				list_of_rows.append(curr_row)
		# append the fallout url row last
		list_of_rows.append(fallout_url_row)
		# at this point, we have our list of rows. Write them to Google sheet
                for row in list_of_rows:
			print row
                        self.worksheet.append_row(row)
		self.worksheet.append_row([])
		# allow user to see last time the worksheet was updated
		now = time.strftime("%c")
		row = ["Last updated:  %s"  % now]
		self.worksheet.append_row(row)
