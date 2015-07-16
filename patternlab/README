These are the source [Pattern Lab](http://patternlab.io/) templates that will get exported to the other content management systems. You don't actually need to set up Pattern Lab for the exports to work, but if you want to see the patterns in context, extract a copy of Pattern Lab into this folder and [run it](http://patternlab.io/docs/command-line.html) (in case it matters, this was set up using version 0.7.12). If you want to modify the css, you'll also need to set up [Compass](http://patternlab.io/docs/advanced-integration-with-compass.html).

The export scripts make some assumptions about how your patterns are set up:

- All patterns are in patternlab/source/_patterns
- Templates are in 03-templates and everything else is in 00-atoms, 01-molecules, and 02-organisms. Pages are not exported, each CMS has different ways of dealing with that so read the instructions for the CMS you're interested in.
- File names are of the format "00-colors.mustache"--that's 2 digits, a dash, the pattern name, and the extension. Only files ending in ".mustache" will be exported, and files starting with an underscore will be ignored.
- Includes should be the [shorthand syntax](http://patternlab.io/docs/pattern-including.html) ({{> type-name }}, e.g. {{> molecules-block-hero }}), not the longer mustache syntax.
- Passing parameters to includes isn't currently supported.
- You may have subdirectories inside your atoms, molecules, and organisms folders, but they along with the numbers will be stripped because the include syntax doesn't have them, so make sure your patterns all have unique names.
- Subdirectories are not allowed inside the templates folder. I'm not sure if pattern lab even supports them there?
- The css should be in patternlab/source/css/style.css, or be precompiled from Sass or Compass or whatever to that file. The scripts will not copy css preprocessor source files.