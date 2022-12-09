---
title: Front Page
type: docs
---

# A Remote Controlled Mini Hovercraft

TODO: Fill with project description, goals, and a few photos or a video (there
is the [gallery]({{< ref "docs/gallery/_index.md" >}}) for all your media
needs)

# A little cheatsheat for how to do certain things

Delete this section for final submission

## Shortcodes

Hugo has a system called shortcodes that allow you to define new syntax to
generate HTML snippets into your document with a nicer syntax. To call a
shortcode (either a custom or a builtin one), surround with the characters
\{\{\< shortcode arg1 arg2 arg... argN \>\}\}. You will see examples later that
don't have backslashes to escape the shortcode from running.

## Images

Place your images in the `/assets/images/` directory of the site. To insert the
image, call one of the short codes I've created, either `bio` for a bio image
(crops and scales to 200x200) or `img` (scales to 800xN) for a normal image.

{{< bio "images/test.png" "alt text for bio image" >}}

A bio image

{{< img "images/test.png" "alt text for img image" >}}

## Links

You can link to content that is internal to the site as follows

[link text]({{< ref "docs/about/_index.md" >}}). `ref` is a hugo shortcode that
will generate a url from the site, based off the baseurl. It ensures it works
in both `hugo server` as well as deployment.

You can link to content on external sites like so [link text](https://example.com). You
can also omit the link text: https://example.com

**DO NOT** link to pages on this site with this. It does not account for the
difference in base url that you will find in deployment vs local testing with
`hugo server`.

## Youtube Videos

If you want to embed a youtube video, you cannot just use a link:
https://youtu.be/dQw4w9WgXcQ

Use the hugo shortcode for generating a youtube embed:

{{< youtube dQw4w9WgXcQ >}}
