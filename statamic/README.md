This was set up with [Statamic](http://statamic.com/) version 1.10.5. To see it working:

1. You will need PHP and a web server. I like [WAMP](http://www.wampserver.com/en/) on Windows and [MAMP](https://www.mamp.info/en/) on Mac or [these instructions](https://help.ubuntu.com/community/ApacheMySQLPHP) on Ubuntu. You may also want to look at their [other requirements notes](http://statamic.com/learn/getting-ready).

2. Get a copy of Statamic (which is not free, so it's not committed with this repository) and extract it somewhere.

3. Copy everything from the extracted folder except the _themes, _content, and assets directories into the statamic directory.

4. Open _config/fieldsets and remove the contents; these are the content types for the default site, which we won't be using.

5. Edit _theme in config/settings.yaml to say "pattern" instead of the default site theme, that will be where the importer will place the templates.

6. Copy the statamic folder to your server and then [set up Statamic](http://statamic.com/learn/installing-and-updating/installing) according to official instructions. If you can, I'd recommend setting up a virtual host instead of running in a subdirectory, it seems to work better that way.

7. Open your site in a web browser. You should be able to see the pre-imported patterns if it's set up correctly.

## Editing Content

Statamic stores all of your content in markdown files, which you can edit directly, but it also provides a control panel that tells you what fields are needed for a given content type and makes it easy to edit without breaking anything. In addition to the above instructions, you'll need to set up a [new admin user](http://statamic.com/learn/control-panel/managing-members) then log into the control panel (if your site is http://localhost, the control panel would be http://localhost/admin). The home page and three content types (blog, features, and hero) should be there ready for you to edit. Features and hero are used by the homepage template, the blog templates use the blog content type.

All of the content files are stored in _content. The homepage content is in _content/page.md, the three content types have their own subfolders in _content.

## Editing Data Models

Each content type subfolder also has a fields.yaml that [lets you specify](http://statamic.com/learn/control-panel/fields-and-fieldsets) what data can be entered for that content type. If you make a change to your templates that requires a change in the data, you will need to edit the appropriate fields.yaml, too, it will not be updated for you automatically when you import the templates. You will also need to make sure existing content is updated accordingly.