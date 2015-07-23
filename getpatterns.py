import sys, os, shutil, re, errno, json

class converter(object):

	def __init__(self, cms):
		self.destination = ""
		self.source = os.path.abspath("./{cms}/patternlab".format(cms=cms))
		self.conversions = ""
		self.destination_css = ""
		self.destination_templates = ""
		self.destination_patterns = ""
		self.template_prepend = ""

		with open("{cms}-conversions.json".format(cms=cms)) as data_file:    
			self.conversions = json.load(data_file)
		if cms == "statamic":
			self.destination = os.path.abspath("./statamic/cms/_themes/pattern")
			self.destination_css = "css/pattern.css"
			self.destination_templates = "templates"
			self.destination_patterns = "partials/{0}"
		elif cms == "jekyll":
			self.destination = os.path.abspath("./jekyll/cms")
			self.destination_css = "css/style.css"
			self.destination_templates = "_layouts"
			self.destination_patterns = "_includes/{0}"
			self.template_prepend = "---\nlayout: default\n---\n"

	def outname(self, fname):
		return re.match(r"([0-9]+-)?(.*)\.mustache", fname).group(2) + '.html'

	def makeOutputFolder(self, path):
		try:
			os.makedirs(path)
		except OSError as exception:
			if exception.errno != errno.EEXIST:
				raise

	def moveCss(self):
		shutil.copyfile(os.path.join(self.source, "source/css/style.css"), os.path.join(self.destination, self.destination_css))

	def copyTemplates(self):
		templateInDir = os.path.join(self.source, "source/_patterns/03-templates")
		templateOutDir = os.path.join(self.destination, self.destination_templates)
		templates = os.listdir(templateInDir)
		for fname in templates:
			if not fname.endswith('.mustache'):
				continue

			with open(os.path.join(templateInDir, fname)) as infile, open(os.path.join(templateOutDir, self.outname(fname)), 'w') as outfile:
				outfile.write(self.template_prepend)
				content = infile.readlines()
				for line in content:
					self.convert(line, outfile)

	def copyPatterns(self):
		inPattern = "source/_patterns/{0}-{1}"
		outPattern = self.destination_patterns

		for num, name in enumerate(["atoms", "molecules", "organisms"]):
			inDir = os.path.join(self.source, inPattern.format("{0:02d}".format(num), name))
			outDir = os.path.join(self.destination, outPattern.format(name))
			self.makeOutputFolder(outDir)

			for (dirName, subdirList, fileList) in os.walk(inDir):
				# we're not going to copy the subdirectories, just the files, because the includes don't know subdirectories
				for fname in fileList:
					if fname.startswith('_') or not fname.endswith('.mustache'):
						continue

					with open(os.path.join(inDir, dirName, fname)) as infile, open(os.path.join(outDir, self.outname(fname)), 'w') as outfile:
						content = infile.readlines()
						for line in content:
							self.convert(line, outfile)


	def convert(self, line, outfile):
		# text replacements to run before other conversions
		pager_next = re.compile("({{[#/]{0,1}\s*)next_page(\s*}})")             # {{# next_page }} {{/ next_page }} {{next_page}}
		pager_prev = re.compile("({{[#/]{0,1}\s*)previous_page(\s*}})")         # {{# previous_page }} {{/ previous_page }} {{previous_page}}
		blog_collection = re.compile("({{[#/]\s*)blog(\s*}})")                  # {{# blog }} {{/ blog }}
		page_title = re.compile("({{\s*)title(\s*}})")                          # {{ title }} (this will catch too much if non-page-titles aren't scoped as in statamic, but statamic doesn't need to change anything, so...)

		# to convert from one template syntax to another
		include = re.compile("\{\{\>\s*([^-\s]+)-([^\s]+)\s*\}\}")              # {{> include-name }}
		include_with_params = ("\{\{\>\s*([^-\s]+)-([^\s]+)\s*\((.*)\)\s*\}\}") # {{> include-name(...) }}
		startsection = re.compile("{{#\s*([^\s]+)\s*}}")                        # {{# section-name }}
		endsection = re.compile("{{/\s*([^\s]+)\s*}}")                          # {{/ section-name }}
		variable = re.compile("{{\s*([^\s]+)\s*}}")                             # {{ variable-name }}
		variable_to_format = re.compile("{{{\s*([^\s]+)\s*}}}")                 # {{{ variable-name }}}
		comment = re.compile("{{!\s*(.*)\s*}}")                                 # {{! key:value, key2:"value2" }} (used to annotate other tags)
		startpager = re.compile("{{!\s*pagination\s*\((.*)\)\s*}}")             # {{! pagination(...) }}
		endpager = re.compile("{{!/\s*pagination\s*}}")                         # {{!/ pagination }}

		# Do text replacements first
		line = re.sub(pager_next, self.conversions['pager_next'].format(), line)
		line = re.sub(pager_prev, self.conversions['pager_prev'].format(), line)
		line = re.sub(blog_collection, self.conversions['blog_collection'].format(), line)
		line = re.sub(page_title, self.conversions['page_title'].format(), line)
		
		# Find places that include other patterns
		if re.search(include_with_params, line):
			# get parameters for the include
			params = self.getParams(re.search(include_with_params, line).group(3))
			paramstring = ""
			for key, value in params.iteritems():
				paramstring += self.conversions['param'].format(key=key, value=value.encode('string_escape'))
			# convert
			line = re.sub(include_with_params, self.conversions['include'].format(params=paramstring), line)
		elif re.search(include, line):
			line = re.sub(include, self.conversions['include'].format(params=""), line)
		
		# Find loops and if statements (mustache uses the same syntax for both, so if statements will have additional annotation)
		elif re.search(startsection, line):
			params = dict()
			annotation = re.search(comment, line)
			if annotation:
				params = self.getParams(annotation.group(1))
			if 'convert_to_if' in params:
				# it's not really a section, but mustache uses the same notation for ifs
				line = re.sub(startsection, self.conversions['if'].format(), line)
			else:
				if 'var' not in params:
					params['var'] = ""
				if 'limit' in params:
					line = re.sub(startsection, self.conversions['paginated_loop'].format(limit=params['limit'], var=params['var']), line)
				else:
					line = re.sub(startsection, self.conversions['loop'].format(var=params['var']), line)
		elif re.search(endsection, line):
			# line = re.sub(endsection, r'{{/\1}}', line)
			params = dict()
			annotation = re.search(comment, line)
			if annotation:
				params = self.getParams(annotation.group(1))
			if 'convert_to_if' in params:
				# it's not really a section, but mustache uses the same notation for ifs
				line = re.sub(endsection, self.conversions['endif'].format(), line)
			else:
				line = re.sub(endsection, self.conversions['endloop'].format(), line)
		
		# Find pagination (mustache doesn't do this, so it uses special annotations)
		elif re.search(startpager, line):
			params = self.getParams(re.search(startpager,line).group(1))
			paramstring = self.conversions['pagination_params'].format(limit=params['limit'], group=params['group'])
			line = re.sub(startpager, self.conversions['pager'].format(params=paramstring), line)
		elif re.search(endpager, line):
			line = re.sub(endpager, self.conversions['endpager'].format(), line)

		# Find regular variables
		elif re.search(variable_to_format, line):
			# these are formatted strings with html tags, can't be dates
			line = re.sub(variable_to_format, self.conversions['variable'].format(), line)
		elif re.search(variable, line):
			params = dict()
			annotation = re.search(comment, line)
			if annotation:
				params = self.getParams(annotation.group(1))
			if 'date' in params:
				line = re.sub(variable, self.conversions['date_format'].format(format=params['date']), line)
			else:
				line = re.sub(variable, self.conversions['variable'].format(), line)

		# get rid of annotations before output
		line = re.sub(comment, r' ', line)

		outfile.write(line)

	def getParams(self, paramstring):
		params = dict()
		for matches in re.findall('([^\\s:]+)\\s*:\\s*([\'"]{0,1})(.+?)(?<!\\\\)\\2\\s*,{0,1}\\s*', paramstring):
			# a:"b", c:"d"; group 1 is key, 2 is quote backreference, 3 is value
			key = matches[0]
			value = matches[2]
			params[key] = value.decode('string_escape')
		return params

if __name__ == "__main__":
	if sys.argv[1] and sys.argv[1] in ["statamic", "jekyll"]:
		c = converter(sys.argv[1])
		c.moveCss()
		c.copyTemplates()
		c.copyPatterns()
	else:
		print "Please provide a format to convert to"