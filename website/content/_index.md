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

## Images

![Image alt text](/pie-2022-03/hoverbois/test.png)

Images can be placed in the `static` folder of the website. Typically you could
reference with just `/image.png`, however, due to the baseurl, you specify
`/pie-2022-03/hoverbois/image.png`.

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
