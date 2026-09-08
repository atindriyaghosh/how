---
type: principle
title: Privacy-first, local-first
summary: A user's data never reaches a third party — either it never leaves their device, or it goes only to a backend I run myself.
---

Whatever a tool or app does with a user's data, it never reaches a third
party. Either it never leaves the user's own device at all — nothing of
theirs for me to even hold — or, when a backend is genuinely needed, it
goes only to a service I run myself, never someone else's. No upload to
someone else's service, no analytics beacon carrying content, no server in
the path that isn't mine.

This isn't a compliance stance, it's an architecture default. When nothing
needs to leave the device, don't build a backend for it: client-side
execution is simpler to build, cheaper to run, and impossible to breach on
my end because there's nothing of the user's to breach there. When a
backend is genuinely needed, it's still not a third party's — it's a
service I run and reach privately, not a public endpoint handed the data
on faith.

Where this shows up: the [HTML tool pattern](../patterns/html-tools.html)
is the "nothing needs to leave the device" case; the
[Private server-side app pattern](../patterns/private-server-side-app.html)
is the "a backend is genuinely needed" case.
