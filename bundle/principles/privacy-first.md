---
type: principle
title: Privacy-first, local-first
---

If a tool works on user data, that data stays in the browser. No upload, no
analytics beacon carrying content, no server in the request path that
doesn't need to be there.

This isn't a compliance stance, it's an architecture default: client-side
execution is simpler to build, cheaper to run, and impossible to breach on
our end because there's nothing of the user's to breach. Reach for a
backend only when the task genuinely requires one (fetching from an API the
browser can't reach directly, work too heavy for a client), not because
it's the familiar shape.
