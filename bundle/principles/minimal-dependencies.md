---
type: principle
title: Minimal dependencies
---

Every dependency is a promise to keep updating it, and a supply-chain
surface someone else controls — so when one earns its place, pin it
exactly and hold it still. "Pin it" means something different per
component; each is its own section below.

#### JavaScript

Vendor the exact file into the repo — `vendor/<package>@<version>/` —
rather than loading it from a CDN at runtime. A vendored file can't change
out from under you, can't be swapped by whoever controls the CDN, and
doesn't need an exception carved into the page's own CSP just to load.

#### Python (build tooling)

Pin exact versions in `pyproject.toml` (`==`, not `>=`), and commit the
lockfile `uv` resolves from them. A range means the build installs
whatever the latest matching release happens to be on the day it runs —
the opposite of pinning. Exact pins plus a committed lockfile mean the
same build script installs the same interpreter-level dependencies whether
it runs today or in a year.

#### GitHub Actions

Reference every action by full commit SHA, never a version tag —
`uses: owner/action@<40-char-sha> # v4` at most, the tag as a comment for
a human, never as the ref itself. A tag like `@v4` is a pointer someone
else's repository controls and can repoint at will; a SHA is the one thing
in this list that's genuinely immutable. This applies equally to
first-party (`actions/*`) and third-party actions — first-party cuts
supply-chain risk, it doesn't remove the need to pin.
