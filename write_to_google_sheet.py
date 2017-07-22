from parsers.GraphResultsFilesParser import GraphResultsFilesParser
from parsers.FalloutTestRunsParser import FalloutTestRunsParser
from google_sheet.GoogleSheet import GoogleSheet
from optparse import OptionParser
from pprint import pprint

# These flags correspond to Google sheet details that we need
parser = OptionParser()
parser.add_option("--google_sheet", dest="google_sheet", help="Name of the Google sheet that we are writing our results into.")
parser.add_option("--worksheet", dest="worksheet", help="The worksheet within the Google spreadsheet that we are witing result into.")
parser.add_option("--column_headers", dest="column_headers", help="comma-delimited list of column headers for data. NOTE: The number and order of the column headers must correspond to the number and order of specified results file paths or Fallout test run IDs, respectively.")
# These flags correspond to source of result of a DSE Graph performance run
parser.add_option("--results_file_paths", dest="results_file_paths", default=None, help="comma-delimited list of paths to files that contains the performance results we want to write to Google sheet. NOTE: The number and order of results file paths must corespond to the number and order of the specified column headers, respectively.")
parser.add_option("--fallout_test", dest="fallout_test", default=None, help="Name of the Fallout test we are interested in.")
parser.add_option("--fallout_test_run_ids", dest="fallout_test_run_ids", default=None, help="comma-delimited list of IDs for corresponding test runs we are interested in recording performance results for. NOTE: The number and order of results file paths must corespond to the number and order of the specified column headers, respectively.")
parser.add_option("--fallout_artifact_path", dest="artifact_path", default=None, help="Directory path to Fallout aritfact where performance results are recorded.")

(options, args) = parser.parse_args()

google_sheet_name = options.google_sheet
worksheet_name = options.worksheet

if google_sheet_name is None:
	print "\nPlease provide a Google sheet name.\n"
	exit()
if worksheet_name is None:
	print "\nPlease provide a worksheet name within the Google sheet provided.\n"
	exit()

# TO DO: Error handling
google_sheet = GoogleSheet(google_sheet_name, worksheet_name)

results_file_paths = options.results_file_paths
fallout_test = options.fallout_test
fallout_test_run_ids = options.fallout_test_run_ids
artifact_path = options.artifact_path
column_headers = options.column_headers

list_of_column_headers = []
if column_headers is not None:
	list_of_column_headers = column_headers.split(",")
else:
	print "\nPlease provide a list of appropriate column headers for the results\n"
	exit()

results = None

# case that user provides local paths to results files
if results_file_paths is not None:
	list_of_file_paths = results_file_paths.split(",")
	# make sure the number of column headers matches the number of results file paths
	if len(list_of_column_headers) != len(list_of_file_paths):
		print "\nThe number of column headers does not match the number of results file paths provided.\n"
		exit()
	else:
		results = GraphResultsFilesParser().parse_results_from_files(list_of_file_paths)

# case that user provides Fallout test runs from which to grab results from
elif fallout_test is not None:
	if fallout_test_run_ids is not None:
		list_of_test_run_ids = fallout_test_run_ids.split(",")
		# make sure the number of column headers matches the number of Fallout test run ids
		if len(list_of_column_headers) != len(list_of_test_run_ids):
			print "\nThe number of column headers does not match the number of Fallout test run ids.\n"
			exit()
		else:
			results = FalloutTestRunsParser(fallout_test).parse_results_from_artifact(list_of_test_run_ids, artifact_path)
			# TO DO: Use the Fallout REST API in order to grab the results from the test runs
	# case that the user forgot to provide Fallout test run ids
	else:
		print "\nPlease provide test run ids for which you wish to write results for.\n"
		exit()
# case that the user has not provided any source of timing results
else:
	print "\nPlease provide local paths to test run results, or corresponding fallout test name.\n"
	exit()

print "\nTime to write to Google sheet...\n"
# at this point, we have grabbed all of our results from file or through Fallout REST API. Time to write to our Google sheet
google_sheet.write_results(list_of_column_headers, results["means"])
