---
type: principle
title: No egress by default
---

Deny network access by default, and open only what's specifically needed —
enforced by whatever mechanism the component provides, not left to
convention. That mechanism is different per component; each is its own
section below.

#### JavaScript (in the browser)

Every tool ships a Content-Security-Policy that starts from
`default-src 'none'` — deny everything — then opens only what that tool
needs: `script-src`/`style-src` to `'self'`, `img-src` to `'self' data:
blob:'`, and `connect-src` left at `'none'`. The browser enforces this, not
just the code: even a compromised dependency or an injected script can't
phone anything home, because nothing is reachable to phone.

A tool that genuinely needs an external call (an AI feature hitting an LLM
API, say) states that as a scoped exception in its own CSP — one named
origin, on that one page — never by loosening the site-wide default. Every
other tool keeps `connect-src 'none'` and makes zero network requests after
load.

Caveat, honestly: `script-src` still carries `'unsafe-inline'`, because a
single-file tool ships its own JS inline. This policy blocks egress, not
injection — it's a guarantee about where data can go, not immunity from XSS.

#### Python (build tooling)

The build script is a pure, offline transformation: bundle and templates
in, `dist/` out, no network call anywhere in its own logic. A build that
reaches out to an API at build time is a build that can start failing, or
silently start producing different output, the day that API changes —
dependency resolution (`uv` syncing `pyproject.toml`) is a separate,
already-pinned step, not something the build script itself does.
