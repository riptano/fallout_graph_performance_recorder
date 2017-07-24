class GraphResultsFilesParser():

	def verify_queries_agree(self, list_of_parsed_result_dicts):
		"""
		@param list_of_parsed_result_dicts:	list of dicts, whose keys correspond to queries
		@type list_of_parsed_result_dicts:	list of dicts
		"""
		list_of_query_lists = []
		for result_dict in list_of_parsed_result_dicts:
			list_of_query_lists.append(result_dict.keys())
		set_of_first_queries = set(list_of_query_lists[0])
		for query_list in list_of_query_lists:
			if set(query_list) != set_of_first_queries:
				print "\nThe queries for two or more sets of results do not agree.\n"
				exit()

	def parse_results_from_files(self, list_of_paths_to_results_files):
		"""
		@param list_of_paths_to_results_files:	list of local paths to results
		@type list_of_paths_to_results_files:	list of str
		"""
		list_of_mean_dicts = []
		list_of_stdev_dicts = []
		# iterate through each file containing results
		for path in list_of_paths_to_results_files:
			curr_results_file = open(path.strip(), "r")
			curr_mean_dict = {}
			curr_stdev_dict = {}
			for line in curr_results_file:
				# only want to deal with those lines that correspond to queries and results, no headers
				if line[0] is 'g':
					curr_result = line.split("|")
					#self.queries.append(curr_result[0])
					# the case that all queries failed
					if len(curr_result) == 2:
						curr_mean_dict[curr_result[0]] = curr_result[1].strip("\n")
					# the case that queries were successful
					if len(curr_result) >= 4:
						curr_mean_dict[curr_result[0]] = float(curr_result[3])
						if len(curr_result) == 5:
							curr_stdev_dict[curr_result[0]] = float(curr_result[4])
						else:
							curr_stdev_dict[curr_result[0]] = "Standard deviation not available"
			# append dicts to appropriate list of dicts
			list_of_mean_dicts.append(curr_mean_dict)
			list_of_stdev_dicts.append(curr_stdev_dict)
			curr_results_file.close()
		# verify that the set of queries are the same for all results files
		self.verify_queries_agree(list_of_mean_dicts)
		return {"means" : list_of_mean_dicts, "stdev" : list_of_stdev_dicts}
