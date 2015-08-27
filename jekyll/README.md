This was set up in [Jekyll](http://jekyllrb.com/) 2.5.3. To see it working:

1. [Install Jekyll](http://jekyllrb.com/docs/installation/). You will need to have [Ruby](http://www.ruby-lang.org/en/downloads/) installed, then use gem  to install Jekyll. It's not officially supported in Windows, but there are [instructions](http://jekyllrb.com/docs/windows/#installation) instructions to get it working with a slightly older version of Ruby (I have it with 2.0.0).

2. Open a command promp and run the development server with
   ```
   jekyll serve
   ```
   (There are also some [other ways](http://jekyllrb.com/docs/usage/) to build the site in the documentation, but this works for development purposes)

3. Open a web browser and go to [http://localhost:4000](http://localhost:4000). You should be able to see the pre-imported patterns if everything is working correctly.

## Editing Content

Jekyll is similar to Statamic in that all the content is stored in files, but there is no control panel interface so if you need to update the content you will need to update the files directly.

The sample site has two pages, a blog, and 2 [collections](http://jekyllrb.com/docs/collections/):

- The homepage content is jekyll/index.markdown, but there's basically nothing in it; everything comes from the template, which will be imported from Pattern Lab.

- The blog article list is jekyll/blog/index.html, and it is also basically empty except for the title; again, everything else comes from the template.

- Blog posts are in jekyll/_posts, and is just the [built-in](http://jekyllrb.com/docs/posts/) blog posts collection.

- There are 2 custom collections, _hero and _features, which are used on the home page. They use [custom frontmatter](http://jekyllrb.com/docs/frontmatter/) variables to store extra metadata like a title or image.

- Images are stored in jekyll/assets/img/.

## Editing Data Models

Unlike Django and Statmic, Jekyll does not have any data models outside of the content itself because there is no control panel that needs to know what to display. If you update the templates such that the content metadata needs to change, you will need to update all of the relevant content but you do not need to change anything else.