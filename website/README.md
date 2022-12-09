# hoverbois PIE website

This folder is where we keep all files required to build the static site.

The webpage is generated with [Hugo](https://gohugo.io/), a static site
generator similar to Jekyll (the default for GitHub Pages). You will need to
install Hugo on your machine to build the website and test locally.

## Website Layout

The content on the website that you need to worry about is structured as
follows:

| Path                                | Description                             |
|-------------------------------------|-----------------------------------------|
| `config.toml`                       | Main configuration file for the website |
| `content/_index.md`                 | Front page                              |
| `content/docs/PAGE_TITLE/_index.md` | Website pages                           |
| `assets/images/`                    | Directory for storing images            |

## Testing Changes Locally

### Getting the theme

Before you can run locally or deploy, you need to get the theme.

The [monochrome](https://kaiiiz.github.io/hugo-theme-monochrome/) theme is
installed as a git submodule. You must tell git to track the submodule.

```
git submodule init
git submodule update
```

This only needs to be run once.

### Run locally

Run `hugo server`. It will build the static site and host it locally on your
machine. This lets you make changes to the site and see how it will look
without having to redeploy it. Hugo will rebuild the site if it detects changes
in the files.

## Deployment

Note: try to leave this to Devlin. I do not want too many PRs being put in and
such. I am putting a summary of the process in case something occurs that
prevents me from doing it.

Due to how the PIE github pages is setup, we need to build the static website,
(do not commit to this repo), copy it to a clone of [the PIE 2022 website
repo](https://github.com/olincollege/pie-2022-03/tree/main) on the `gh-pages`
branch, and lastly submit a PR.

You can build the static site by running

```
hugo server
```

It will populate all the static content, including the theme, in a directory
called `public`. DO NOT COMMIT THIS TO THE REPO PLEASE (it is `.gitignored`,
but please still be careful).
