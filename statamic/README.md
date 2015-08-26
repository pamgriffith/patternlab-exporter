This was set up with [Statamic](http://statamic.com/) version 1.10.5. To see it working:

- Get a copy of Statamic (which is not free, so it's not committed with this repository) and extract it somewhere, then remove the _themes and _content folders so the default site doesn't overwrite this one
- Remove everything in _config/fieldsets, too, so the default content types don't get confusing
- Copy everything else into this folder
- [Set up Statamic](http://statamic.com/learn/installing-and-updating/installing) according to official instructions. If you can, I'd recommend setting up a virtual host instead of running in a subdirectory because uploaded file urls don't seem to work right otherwise.
- Edit _theme in config/settings.yaml to say pattern instead of whatever their default is

You should be able to see the pre-imported patterns at the site root if it's set up correctly.

The homepage is in _content/page.md, which you can also edit in the control panel, but it has no content; the area at the top is the "hero" content type located in the hero folder, or you can edit it in the control panel by getting the list of hero items, then editing the one that's in there (probably best not to add more). Do make use of the control panel, the yaml on these content types is ok but easy to forget or break.

The features are the "features" content type, located in the features folder and also available in the control panel. You can add as many as you want and the page will show all of them.

There is also a blog page that shows a paged list of blog posts, 5 at a time. Those are the blog content type, located in the blog folder.

If you update the base patternlab patterns, run
```
python getpatterns.py
```
to import them into Statamic. You will need [python 2.7](https://www.python.org/downloads/) installed to run the script (if you're new to python, do not get version 3, it's pretty different and the script will not work).