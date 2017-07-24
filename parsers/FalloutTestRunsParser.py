import os
from GraphResultsFilesParser import GraphResultsFilesParser
from fallout.api import FalloutAPI

class FalloutTestRunsParser():
	fallout_test = None
	list_of_results_file_paths = None
	
	def __init__(cls, fallout_test):
		cls.fallout_test = fallout_test
		# set these environment variables
		# FUTURE: Make these flexible for other Fallout users
		os.environ['FALLOUT_USER'] = 'jenkins-dse@datastax.com'
		os.environ['FALLOUT_OAUTH_TOKEN'] = '64cb75cf-e47a-4a5a-9617-c95bb01060b8'
		os.environ['TEST'] = cls.fallout_test
		# will need to keep track of files that are downloaded locally
		cls.list_of_results_file_paths = []

	def download_artifact(self):
                bash_command = 'fallout testrun-artifact --user=$FALLOUT_USER $TEST $TEST_RUN_ID $ARTIFACT_PATH > $HOME/results_{id}'.format(id=os.environ['TEST_RUN_ID'])
		output = os.system(bash_command)
		if int(output) != 0:
			print "\nThere was an issue grabbing artifact for test run {id}\n".format(id=os.environ['TEST_RUN_ID'])
			exit()
		self.list_of_results_file_paths.append(os.environ['HOME'] + "/results_{id}".format(id=os.environ['TEST_RUN_ID']))

	def delete_artifact(self, path_to_downloaded_artifact):
		bash_command = 'rm {p}'.format(p=path_to_downloaded_artifact)
		output = os.system(bash_command)
		if int(output) != 0:
			print "\nThere was an issue deleting downloaded artifact for test run {id}\n".format(id=os.environ['TEST_RUN_ID'])
			exit()

	def add_fallout_test_run_urls(self, list_of_fallout_test_run_ids, parsed_results):
		"""
		@param list_of_fallout_test_run_ids:	list of ids for the Fallout test os.environ['TEST']
		@type list_of_fallout_test_run_ids:	list of str
		@param parsed_results:			dict of list of parsed out Fallout results
		@type parsed_results			dict of list of dicts 
		@return:				list of dicts
		"""
		from pprint import pprint
		#pprint(parsed_results)
		for key in parsed_results:
			for i in range(len(list_of_fallout_test_run_ids)):
				#import pdb; pdb.set_trace()
				parsed_results[key][i]['FALLOUT TEST RUN URL'] = 'http://fallout.datastax.lan/tests/ui/{u}/{t}/{idx}/artifacts'.format(u=os.environ['FALLOUT_USER'], t=os.environ['TEST'], idx=list_of_fallout_test_run_ids[i])

	def parse_results_from_artifact(self, list_of_fallout_test_run_ids, artifact_path):
		"""
                @param list_of_fallout_test_run_ids:    list of ids for the Fallout test os.environ['TEST']
                @type list_of_fallout_test_run_ids:     list of str
		@param artifact_path:	common path to Fallout artifact of interest
		@param atifact_path:	str
		@return:		list of dicts
		"""
		for test_run_id in list_of_fallout_test_run_ids:
			os.environ['TEST_RUN_ID'] = test_run_id
			os.environ['ARTIFACT_PATH'] = artifact_path
			# download artifact
			self.download_artifact()
		parsed_results = GraphResultsFilesParser().parse_results_from_files(self.list_of_results_file_paths)
		# tack on Falout URLs
		self.add_fallout_test_run_urls(list_of_fallout_test_run_ids, parsed_results)
		# time to remove downloaded artifacts, post parsing
		for path in self.list_of_results_file_paths:
			self.delete_artifact(path)
		from pprint import pprint
		pprint(parsed_results)
		return parsed_results
