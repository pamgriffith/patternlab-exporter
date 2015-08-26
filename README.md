This project is an experiment in exporting patterns from a pattern library (in this case [Pattern Lab](http://patternlab.io)) into various content managment systems to see how well I can make a pattern library be a living part of a website. The idea is that changes to the design of a site *must* be made to the pattern library and then get ported into the site so that the pattern library is always up to date.

The sample website is very simple and by no means a comprehensive example of everything one might want to put into a website template. It includes:
- a homepage with a [common design](http://www.novolume.co.uk/blog/all-websites-look-the-same/): a tagline and call to action and an area for a varying number of features with images
- a blog page with excerpts of posts
- a blog post page with a complete blog entry

The content management systems included are [Django](https://www.djangoproject.com/), [Jekyll](http://jekyllrb.com/), and [Statamic](http://statamic.com/). More may be added later. I did attempt to integrate [Perch](https://grabaperch.com/) and [Drupal](https://www.drupal.org/), as well, but the way they handle their templates is too unique to easily handle in the same script that's used for the others and would require substatial custom annotation in the templates to work correctly.

There are two versions of the pattern lab templates included here, patternlab-scoped and patternlab-unscoped, which handle variables in loops differently. The differences are described further below in the [Syntax section](#scoped-and-unscoped-loops). patternlab-unscoped is used by Statamic and patternlab-scoped is used by Django and Drupal; you only need to install and work with the one appropriate to the CMS you are using.

## Setting Up

### Install Pattern Lab

You only need to install the one you'll be using. The installation process is the same for both.

[Patternlab for Django and Jekyll](patternlab-scoped/README.md)

[Patternlab for Statamic](patternlab-unscoped/README.md)

### Install a CMS

You only need to install the one you'll be using.

[Django](django/README.md)

[Jekyll](jekyll/README.md)

[Statamic](statamic/README.md)

### Setting Up Your Templates in Pattern Lab

The export scripts make some assumptions about how your patterns are set up:

- All patterns are in patternlab/source/_patterns
- Templates are in 03-templates and everything else is in 00-atoms, 01-molecules, and 02-organisms. Pages are not exported, each CMS has different ways of dealing with that so read the instructions for the CMS you're interested in.
- File names are of the format "00-colors.mustache"--that's 2 digits, a dash, the pattern name, and the extension. Only files ending in ".mustache" will be exported, and files starting with an underscore will be ignored.
- Includes should be the [shorthand syntax](http://patternlab.io/docs/pattern-including.html) ({{> type-name }}, e.g. {{> molecules-block-hero }}), not the longer mustache syntax.
- Passing parameters to includes is supported, but the pattern matching for that isn't super robust. Most things should work, but don't try to end a string with a backslash right before the end quotation mark (\")
- You may have subdirectories inside your atoms, molecules, and organisms folders, but they along with the numbers will be stripped because the include syntax doesn't have them, so make sure your patterns all have unique names.
- Subdirectories are not allowed inside the templates folder. I'm not sure if pattern lab even supports them there?
- The css should be in patternlab/source/css/style.css, or be precompiled from Sass or Compass or whatever to that file. The scripts will not copy css preprocessor source files.

### Install Python

The conversion script uses [Python 2.7](https://www.python.org/downloads/). If you're new to python, do not install Python 3, it's pretty different and the script will not work.

## Converting the Pattern Lab patterns to your CMS

First get the appropriate version of Pattern Lab and your CMS running (see readme files linked above) and make changes to the templates in Pattern Lab until you are happy with them, then run the conversion script.

The conversion script is getpatters.py. It requires [Python 2.7](https://www.python.org/downloads/). You run it with the name of the CMS you'll be converting to.

For Django:
```
python getpatterns.py django
```

For Jekyll:
```
python getpatterns.py jekyll
```

For Statamic:
```
python getpatterns.py statamic
```

Generally each CMS will automatically pick up any template changes and you'll see them when you reload the page, but Django may need to be restarted if you add new files.

If your changes in Pattern Lab included changes to the JSON data, that will not be ported automatically. You will need to change the CMS data model yourself. There are notes on that in the CMS readme files ([Django](django/README.md), [Jekyll](jekyll/README.md), [Statamic](statamic/README.md)).

## Template Syntax

Generally, the Pattern Lab templates use [Mustache](https://mustache.github.io/) template syntax. However, there were some annotations I had to add for the converter in the form of Mustache comments to make if statements, loops, and pagination work correctly.

### If statements

Mustache templates are "logicless" and don't really have if statements. The syntax for showing something if it's defined and not if it isn't is exactly the same as looping through something:
  
```
{{# item_name }}
(do stuff here)
{{/ item_name }}
```

But the CMS probably has a different syntax for each and there's no way for the conversion script to tell them apart. To make it possible to have if statements rather than just loops for everything, I've added a comment annotation to distinguish them:

```
{{# next_page }}                         {{! convert_to_if:true }}
  <a href="{{next_page}}" class="prev">Older</a>
{{/ next_page}}                          {{! convert_to_if:true }}
```

You need the annotation on both the open and close lines.

### Looping

Pattern Lab loops through a list of items with the following syntax:
  
```
{{# item_name }}
(do stuff here)
{{/ item_name }}
```

There are no parameters involved. But many CMSs have additional parameters to add, like how many items to show. You can limit the number of items displayed by adding a mustache comment after the loop, like this example from organisms/sections/article-list.mustache:

```
{{# blog }} {{! limit:5 }}
{{> molecules-article-excerpt }}
{{/ blog }}
```

The conversion script will look for comments, then look for parameters in the comment with the same syntax as parameters passed into included templates.

**NOTE:** Limiting pagination this way only works in Statamic. In Jekyll, the number of items is set in _config.yml and apparently only works for blog posts, not other collections (see [Pagination](http://jekyllrb.com/docs/pagination/)). In Django, the number of items is set in the [view](https://docs.djangoproject.com/en/1.8/intro/tutorial03/#a-shortcut-render).

### Scoped and Unscoped Loops

Loops in Statamic work differently from those in Jekyll and Django, and I ended up setting up two versions of the Pattern Lab templates, one for Statamic and one for the other two.

Statamic uses patternlab-unscoped. When looping over a list, the properties of each item in the list are available as top-level variables within the loop:

```
{{# features }}
<li>
	<div class="feature">
		<img src="{{img_src}}" alt="{{img_alt}}" /><!--
		--><div class="feature-text">
			<h2>{{title}}</h2>
			<p>{{summary}}</p>
			<a class="more-link" href="{{url}}">Learn More</a>
		</div>
	</div>
</li>
{{/ features }}
```

In the JSON data, img_src, img_alt, title, summary, and url are all properties of each item in the feature list, but they are directly available as variables without having to say where they come from.

Jekyll and Django need the name of a variable to pass into the loop, which will hold all of that item's properties:

```
{{# features }} {{! var:"feature" }}
<li>
	<div class="feature">
		<img src="{{feature.img_src}}" alt="{{feature.img_alt}}" /><!--
		--><div class="feature-text">
			<h2>{{feature.title}}</h2>
			<p>{{feature.summary}}</p>
			<a class="more-link" href="{{feature.url}}">Learn More</a>
		</div>
	</div>
</li>
{{/ features }}
```

The annotation next to the loop tells the converter what to call the variable that's passed into the loop, and each property is accessed through that variable.

## Limitations

The sample site is somewhat limited by what the pattern library's template language ([Mustache](https://mustache.github.io/)) can express. For example Mustache is logicless, and "if" statements are expressed the same way as loops (if the variable does not exist the loop executes 0 times), but most content management system templates work differently, so I've had to add annotations using Mustache comments to indicate which loops are actually if statements. I haven't attempted numbered pagination at all because it just isn't possible with the statements Mustache allows.

The code is also limited by what can be done in a common way across all of the content management systems, and the converter code is slightly more complicated then it needs to be to normalize between different CMSs. I may at some point at a way to load customizations for a particular site so I can keep the same simple conversion script across multiple projects with customizations kept within each project.

The script currently only copies one CSS file (style.css) and does not copy any javascript or image directories at all. It easily could, I just haven't gotten to that.

## Usage

Feel free to use this and modify it for your own projects. Credit is always nice, but not required.
Sample text is from Ulysses by James Joyce.