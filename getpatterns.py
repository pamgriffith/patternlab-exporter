import sys, os, shutil, re, errno, json

statamic = os.path.abspath("./statamic/cms/_themes/pattern")
patternlab = os.path.abspath("./statamic/patternlab")

with open('statamic-conversions.json') as data_file:    
    conversions = json.load(data_file)

def outname(fname):
	return re.match(r"([0-9]+-)?(.*)\.mustache", fname).group(2) + '.html'

def makeOutputFolder(path):
	try:
		os.makedirs(path)
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			raise

def moveCss():
	shutil.copyfile(os.path.join(patternlab, "source/css/style.css"), os.path.join(statamic, "css/pattern.css"))

def copyTemplates():
	templateInDir = os.path.join(patternlab, "source/_patterns/03-templates")
	templateOutDir = os.path.join(statamic, "templates")
	templates = os.listdir(templateInDir)
	for fname in templates:
		if not fname.endswith('.mustache'):
			continue

		with open(os.path.join(templateInDir, fname)) as infile, open(os.path.join(templateOutDir, outname(fname)), 'w') as outfile:
			content = infile.readlines()
			for line in content:
				convert(line, outfile)

def copyPatterns():
	inPattern = "source/_patterns/{0}-{1}"
	outPattern = "partials/{0}"

	for num, name in enumerate(["atoms", "molecules", "organisms"]):
		inDir = os.path.join(patternlab, inPattern.format("{0:02d}".format(num), name))
		outDir = os.path.join(statamic, outPattern.format(name))
		makeOutputFolder(outDir)

		for (dirName, subdirList, fileList) in os.walk(inDir):
			# we're not going to copy the subdirectories, just the files, because the includes don't know subdirectories
			for fname in fileList:
				if fname.startswith('_') or not fname.endswith('.mustache'):
					continue

				with open(os.path.join(inDir, dirName, fname)) as infile, open(os.path.join(outDir, outname(fname)), 'w') as outfile:
					content = infile.readlines()
					for line in content:
						convert(line, outfile)


def convert(line, outfile):
	# text replacements to run before other conversions
	pager_next = re.compile("({{[#/]{0,1}\s*)next_page(\s*}})")             # {{# next_page }} {{/ next_page }} {{next_page}}
	pager_prev = re.compile("({{[#/]{0,1}\s*)previous_page(\s*}})")         # {{# previous_page }} {{/ previous_page }} {{previous_page}}
	blog_collection = re.compile("({{[#/]\s*)blog(\s*}})")                  # {{# blog }} {{/ blog }}

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
	line = re.sub(pager_next, conversions['pager_next'].format(), line)
	line = re.sub(pager_prev, conversions['pager_prev'].format(), line)
	line = re.sub(blog_collection, conversions['blog_collection'].format(), line)
	
	# Find places that include other patterns
	if re.search(include_with_params, line):
		# get parameters for the include
		params = getParams(re.search(include_with_params, line).group(3))
		paramstring = ""
		for key, value in params.iteritems():
			paramstring += conversions['param'].format(key=key, value=value.encode('string_escape'))
		# convert
		line = re.sub(include_with_params, conversions['include'].format(params=paramstring), line)
	elif re.search(include, line):
		line = re.sub(include, conversions['include'].format(params=""), line)
	
	# Find loops and if statements (mustache uses the same syntax for both, so if statements will have additional annotation)
	elif re.search(startsection, line):
		params = dict()
		annotation = re.search(comment, line)
		if annotation:
			params = getParams(annotation.group(1))
		if 'convert_to_if' in params:
			# it's not really a section, but mustache uses the same notation for ifs
			line = re.sub(startsection, conversions['if'].format(), line)
		else:
			if 'limit' in params:
				line = re.sub(startsection, conversions['paginated_loop'].format(limit=params['limit']), line)
			else:
				line = re.sub(startsection, conversions['loop'].format(), line)
	elif re.search(endsection, line):
		# line = re.sub(endsection, r'{{/\1}}', line)
		params = dict()
		annotation = re.search(comment, line)
		if annotation:
			params = getParams(annotation.group(1))
		if 'convert_to_if' in params:
			# it's not really a section, but mustache uses the same notation for ifs
			line = re.sub(endsection, conversions['endif'].format(), line)
		else:
			line = re.sub(endsection, conversions['endloop'].format(), line)
	
	# Find pagination (mustache doesn't do this, so it uses special annotations)
	elif re.search(startpager, line):
		params = getParams(re.search(startpager,line).group(1))
		paramstring = conversions['pager_pagination_params'].format(limit=params['limit'], group=params['group'])
		line = re.sub(startpager, conversions['pager'].format(params=paramstring), line)
	elif re.search(endpager, line):
		line = re.sub(endpager, conversions['endpager'].format(), line)

	# Find regular variables
	elif re.search(variable_to_format, line):
		line = re.sub(variable_to_format, conversions['variable'].format(), line)
	elif re.search(variable, line):
		line = re.sub(variable_to_format, conversions['variable'].format(), line)

	# get rid of annotations before output
	line = re.sub(comment, r' ', line)

	outfile.write(line)

def getParams(paramstring):
	params = dict()
	for matches in re.findall('([^\\s:]+)\\s*:\\s*([\'"]{0,1})(.+?)(?<!\\\\)\\2\\s*,{0,1}\\s*', paramstring):
		# a:"b", c:"d"; group 1 is key, 2 is quote backreference, 3 is value
		key = matches[0]
		value = matches[2]
		params[key] = value.decode('string_escape')
	return params

if __name__ == "__main__":
	moveCss()
	copyTemplates()
	copyPatterns()