These are the source [Pattern Lab](http://patternlab.io/) templates that will get exported to Statamic. If you are using Jekyll or Django, you should use the [other version of the templates](../patternlab-scoped/README.md).

These files were set up using Pattern Lab version 0.7.12.

## Installing and Running Pattern Lab

1. [Install PHP](http://php.net/manual/en/install.php) if you don't already have it and make sure you can use it on the command line

2. Download and extract a copy of Pattern Lab

3. Copy everything from the extracted folder except the source directory, .gitignore, CHANGELOG, LICENSE, and README.md into the patternlab-unscoped directory

4. Open up a command prompt, navigate to the patternlab-unscoped folder, and type the following to generate pattern lab for the first time:
   ```
   php core/builder.php -g
   ```

Open public/index.html in a web browser to view the generated patterns. This will not update if you make changes to the source templates, so you will need to run the command in step 4 again or you could run a different command to watch for changes as you work:

```
php core/builder.php -wr
```

See more in the [Pattern Lab documentation](http://patternlab.io/docs/command-line.html).

## Making Changes to CSS

The source CSS is written in Compass and compiled to style.css. You do not need to use compass for your own CSS, but the only file that the conversion script copies to the target CMS is style.css, so if you have other CSS files (with or without Compass) you will need to modify the conversion script to copy an additional CSS directory.

The Pattern Lab documentation includes notes on [installing and working with Compass](http://patternlab.io/docs/advanced-integration-with-compass.html).

## Additional Pattern Setup Notes

[Template Setup](../README.md#setting-up-your-templates-in-pattern-lab)

[Syntax](../README.md#template-syntax)