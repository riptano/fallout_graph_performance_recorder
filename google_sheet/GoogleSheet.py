import gspread
import os
import time
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheet():
    scope = None
    credentials = None
    google_sheet_name = None
    worksheet_name = None
    worksheet = None
    cells = []

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

        #Get the cells and clear the sheet
        cls.worksheet.resize(rows=100, cols=10)
        cls.cells = cls.worksheet.range(1, 1, 100, 10)
        for cell in cls.cells:
            cell.value = ""

    def write_results(self, list_of_column_headers, list_of_data_dicts):
        """
        @param list_of_column_headers:	list of ordered column headers for our Google sheet
        @type list_of_column_headers:	list of str
        @param list_of_data_dicts:	list of dicts (each of which maps a query to a corresponding result for the query);
                        each dict in the list is to correspond to a column in the spreadsheet
        @type list_of_data_dicts:	list of dicts
        """
        current_row_number = 1
        column_headers = ["QUERIES"] + list_of_column_headers

        for idx, header in enumerate(column_headers):
            cell = self.get_cell(current_row_number, idx + 1)
            cell.value = header

        for query in list_of_data_dicts[0]:
            current_row_number += 1
            self.get_cell(current_row_number, 1).value = query

            # iterate through data dicts, "add a cell" to curr_row
            for idx, data_dict in enumerate(list_of_data_dicts):
                self.get_cell(current_row_number, idx + 2).value = data_dict[query]

        now = time.strftime("%c")
        current_row_number += 2
        self.get_cell(current_row_number, 1).value = ["Last updated:  %s" % now]
        self.worksheet.update_cells(self.cells)

    def get_cell(self, row, col):
        for cell in self.cells:
            if cell.row == row and cell.col == col:
                return cell

        raise Exception("Invalid cell {}, {}".format(row, col))
