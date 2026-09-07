---
type: principle
title: Minimal dependencies
---

Default to vanilla HTML, CSS, and JavaScript. No framework, no bundler, no
package.json, unless the problem genuinely can't be solved without one.

Every dependency is a promise to keep updating it, a build step that can
break, and a supply-chain surface someone else controls. When a library
earns its place (a PDF parser, a hashing routine nobody should hand-roll),
pull it from a CDN pinned to an exact version — never `@latest` — so a
working tool doesn't change out from under you.
