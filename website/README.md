# hoverbois PIE website

This folder is where we keep all files required to build the static site.

The webpage is generated with [Hugo](https://gohugo.io/), a static
site generator similar to Jekyll (the default for GitHub Pages).

## Website Layout

## Testing Changes Locally

Run `hugo server`. It will build the static site and host it locally on your
machine so you can see how it looks. Hugo will rebuild the site if it detects
changes.

## Deployment

Due to how the PIE github pages is setup, we need to build the static website,
(do not commit to this repo), copy it to a clone of [the PIE 2022 website
repo](https://github.com/olincollege/pie-2022-03/tree/main) on the `gh-pages`
branch, and lastly submit a PR.

```
Commands to run
```
