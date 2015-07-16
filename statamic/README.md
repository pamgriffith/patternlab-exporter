This was set up with [Statamic](http://statamic.com/) version 1.10.5. To see it working:

- Get a copy of Statamic (which is not free, so it's not committed with this repository) and extract it somewhere, then remove the _themes, _content, and _config/fieldsets folders so the default site doesn't overwrite this one
- Copy everything else into this folder
- [Set up Statamic](http://statamic.com/learn/installing-and-updating/installing) according to official instructions. If you can, I'd recommend setting up a virtual host instead of running in a subdirectory because uploaded file urls don't seem to work right otherwise.
- Edit _theme in config/settings.yaml to say pattern instead of whatever their default is

You should be able to see the pre-imported patterns at the site root if it's set up correctly. The homepage is in _content/page.md, which you can also edit in the control panel. (Do use the control panel, the yaml is ok but fragile)

If you update the base patternlab patterns, run
```
python getpatterns.py
```
to import them into Statamic. You will need [python 2.7](https://www.python.org/downloads/) installed to run the script (if you're new to python, do not get version 3, it's pretty different and the script will not work).