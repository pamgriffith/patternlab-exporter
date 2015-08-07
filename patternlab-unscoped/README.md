These are the source [Pattern Lab](http://patternlab.io/) templates that will get exported to the other content management systems. You don't actually need to set up Pattern Lab for the exports to work, but if you want to see the patterns in context, extract a copy of Pattern Lab into this folder and [run it](http://patternlab.io/docs/command-line.html) (in case it matters, this was set up using version 0.7.12). If you want to modify the css, you'll also need to set up [Compass](http://patternlab.io/docs/advanced-integration-with-compass.html).

## How to set up your patterns

The export scripts make some assumptions about how your patterns are set up:

- All patterns are in patternlab/source/_patterns
- Templates are in 03-templates and everything else is in 00-atoms, 01-molecules, and 02-organisms. Pages are not exported, each CMS has different ways of dealing with that so read the instructions for the CMS you're interested in.
- File names are of the format "00-colors.mustache"--that's 2 digits, a dash, the pattern name, and the extension. Only files ending in ".mustache" will be exported, and files starting with an underscore will be ignored.
- Includes should be the [shorthand syntax](http://patternlab.io/docs/pattern-including.html) ({{> type-name }}, e.g. {{> molecules-block-hero }}), not the longer mustache syntax.
- Passing parameters to includes is supported, but the pattern matching for that isn't super robust. Most things should work, but don't try to end a string with a backslash right before the end quotation mark (\")
- You may have subdirectories inside your atoms, molecules, and organisms folders, but they along with the numbers will be stripped because the include syntax doesn't have them, so make sure your patterns all have unique names.
- Subdirectories are not allowed inside the templates folder. I'm not sure if pattern lab even supports them there?
- The css should be in patternlab/source/css/style.css, or be precompiled from Sass or Compass or whatever to that file. The scripts will not copy css preprocessor source files.

## Annotations

In addition, there are some annotations that I added to help with translation:

### Looping

Pattern Lab loops through a list of items with the following syntax:
  
```
{{# item_name }}
(do stuff here)
{{/ item_name }}
```

There are no parameters involved. But many CMSs have additional parameters to add, like how many items to show. You can limit the number if items displayed by adding a mustache comment after the loop, like this example from organisms/sections/article-list.mustache:

```
{{# blog }} {{! limit:5 }}
{{> molecules-article-excerpt }}
{{/ blog }}
```

The script will look for comments, then look for parameters in the comment with the same syntax as parameters passed into included templates. Pattern Lab will just ignore it.

### Pagination

Many CMSs have special syntax for pagination in order to set the next and previous pages, etc. I have added annotation, again using mustache comments, to mark the beginning and the end of pagination:

```
{{! pagination(group:"blog", limit:"5") }}
(do stuff here)
{{!/ pagination }}
```

You should provide a group parameter to match what item is being looped and a limit parameter that matches what you gave your loop.

### If statements

Mustache templates are "logicless" and don't really have if statements. The syntax for showing something if it's defined and not if it isn't is exactly the same as looping through something:
  
```
{{# item_name }}
(do stuff here)
{{/ item_name }}
```

But the CMS probably has a different syntax for each and there's no way for the script to tell them apart. To make it possible to have if statements rather than just loops for everything, I've added another comment annotation to distinguish them:

```
{{# next_page }}                         {{! convert_to_if:true }}
  <a href="{{next_page}}" class="prev">Older</a>
{{/ next_page}}                          {{! convert_to_if:true }}
```

You need the annotation on both the open and close lines.

## Some additional notes

I noted above that mustache templates are logicless. That limits what you can do with them, and in turn what you can translate directly into your target template system. One thing that I've noticed is not possible to do in mustache is a numbered pagination system, which requires loops and numerical comparisons. At least some of that would have to be moved over by hand, but I'm not sure what that workflow might look like.