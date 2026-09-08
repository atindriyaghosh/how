---
type: principle
title: Minimal dependencies
---

Default to vanilla HTML, CSS, and JavaScript. No framework, no bundler, no
package.json, unless the problem genuinely can't be solved without one.

Every dependency is a promise to keep updating it, and a supply-chain
surface someone else controls. When a library earns its place (a PDF
parser, a hashing routine nobody should hand-roll), vendor the exact file
into the repo — `vendor/<package>@<version>/` — rather than loading it from
a CDN at runtime. A vendored file can't change out from under you, can't be
swapped by whoever controls the CDN, and doesn't need an exception carved
into the page's own CSP just to load.
