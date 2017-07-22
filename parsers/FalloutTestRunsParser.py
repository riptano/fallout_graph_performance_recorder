import os
from GraphResultsFilesParser import GraphResultsFilesParser

class FalloutTestRunsParser():
	oauth_token = None
	fallout_user = None
	fallout_test = None
	list_of_results_file_paths = None
	
	def __init__(cls, fallout_test):
		# FUTURE: make this flexible for other users
		cls.oauth_token = '64cb75cf-e47a-4a5a-9617-c95bb01060b8'
		cls.fallout_user = 'jenkins-dse@datastax.com'
		cls.fallout_test = fallout_test
		# set these environment variables
		os.environ['OAUTH_TOKEN'] = cls.oauth_token
		os.environ['FALLOUT_USER'] = cls.fallout_user
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

	def parse_results_from_artifact(self, list_of_fallout_test_run_ids, artifact_path):
		for test_run_id in list_of_fallout_test_run_ids:
			os.environ['TEST_RUN_ID'] = test_run_id
			os.environ['ARTIFACT_PATH'] = artifact_path
			# download artifact
			self.download_artifact()
		parsed_results = GraphResultsFilesParser().parse_results_from_files(self.list_of_results_file_paths)
		# time to remove downloaded artifacts, post parsing
		for path in self.list_of_results_file_paths:
			self.delete_artifact(path)
		return parsed_results
