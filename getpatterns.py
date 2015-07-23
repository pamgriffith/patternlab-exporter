import sys, os, shutil, re, errno

statamic = os.path.abspath("./_themes/pattern")
patternlab = os.path.abspath("../patternlab")

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
	include = re.compile("\{\{\>\s*([^-\s]+)-([^\s]+)\s*\}\}")              # {{> include-name }}
	include_with_params = ("\{\{\>\s*([^-\s]+)-([^\s]+)\s*\((.*)\)\s*\}\}") # {{> include-name(...) }}
	startsection = re.compile("{{#\s*([^\s]+)\s*}}")                        # {{# section-name }}
	endsection = re.compile("{{/\s*([^\s]+)\s*}}")                          # {{/ section-name }}
	variable = re.compile("{{\s*([^\s]+)\s*}}")                             # {{ variable-name }}
	variable_to_format = re.compile("{{{\s*([^\s]+)\s*}}}")                 # {{{ variable-name }}}
	comment = re.compile("{{!\s*(.*)\s*}}")                                 # {{! key:value, key2:"value2" }} (used to annotate other tags)
	startpager = re.compile("{{!\s*pagination\s*\((.*)\)\s*}}")             # {{! pagination(...) }}
	endpager = re.compile("{{!/\s*pagination\s*}}")                         # {{!/ pagination }}
	
	if re.search(include_with_params, line):
		# get parameters for the include
		params = getParams(re.search(include_with_params, line).group(3))
		paramstring = ""
		for key, value in params.iteritems():
			paramstring += " {0}=\"{1}\" ".format(key, value.encode('string_escape'))
		# convert
		line = re.sub(include_with_params, r'{{ theme:partial src="\1/\2" use_context="true" '+paramstring+' }}', line)
	elif re.search(include, line):
		line = re.sub(include, r'{{ theme:partial src="\1/\2" use_context="true" }}', line)
	
	elif re.search(startsection, line):
		# line = re.sub(startsection, r'{{\1}}', line)
		params = dict()
		annotation = re.search(comment, line)
		if annotation:
			params = getParams(annotation.group(1))
		if 'convert_to_if' in params:
			# it's not really a section, but mustache uses the same notation for ifs
			line = re.sub(startsection, r'{{ if \1 }}', line)
		else:
			paramstring = ""
			if 'limit' in params:
				paramstring += ' limit="{0}" paginate="true" '.format(params['limit'])
			line = re.sub(startsection, r'{{ entries:listing folder="\1" '+paramstring+' }}', line)
	elif re.search(endsection, line):
		# line = re.sub(endsection, r'{{/\1}}', line)
		params = dict()
		annotation = re.search(comment, line)
		if annotation:
			params = getParams(annotation.group(1))
		if 'convert_to_if' in params:
			# it's not really a section, but mustache uses the same notation for ifs
			line = re.sub(endsection, r'{{ endif }}', line)
		else:
			line = re.sub(endsection, r'{{ /entries:listing }}', line)
	
	elif re.search(startpager, line):
		params = getParams(re.search(startpager,line).group(1))
		paramstring = ""
		if 'limit' in params:
			paramstring += ' limit="{0}" '.format(params['limit'])
		if 'group' in params:
			paramstring += ' folder="{0}" '.format(params['group'])
		line = re.sub(startpager, r'{{ entries:pagination '+paramstring+' }}', line)
	elif re.search(endpager, line):
		line = re.sub(endpager, r'{{ /entries:pagination }}', line)

	elif re.search(variable_to_format, line):
		# remove one set of parentheses from variables that don't need escaping in patternlab
		line = re.sub(variable_to_format, r'{{\1}}', line)
	elif re.search(variable, line):
		# do nothing, works as-is
		line = re.sub(variable_to_format, r'{{\1}}', line)

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