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
	include = re.compile("\{\{\>\s*([^-\s]+)-([^\s]+)\s*\}\}") # currently not handling parameters
	startsection = re.compile("{{#\s*([^\s]+)\s*}}")
	endsection = re.compile("{{/\s*([^\s]+)\s*}}")
	# print line
	if re.search(include, line):
		line = re.sub(include, r'{{ theme:partial src="\1/\2" use_context="true" }}', line)
	elif re.search(startsection, line):
		line = re.sub(startsection, r'{{\1}}', line)
	elif re.search(endsection, line):
		line = re.sub(endsection, r'{{/\1}}', line)
	
	outfile.write(line)

if __name__ == "__main__":
	moveCss()
	copyTemplates()
	copyPatterns()