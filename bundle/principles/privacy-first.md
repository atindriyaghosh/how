---
type: principle
title: Privacy-first, local-first
summary: A user's data stays inside infrastructure I control — the browser, or a backend I host myself — never a third party's.
---

Whatever a tool or app does with a user's data, that data stays inside
infrastructure under my control — the browser, or a backend I host myself
— and never a third party's. No upload to someone else's service, no
analytics beacon carrying content, no server in the path that isn't mine.

This isn't a compliance stance, it's an architecture default. When nothing
needs to leave the device, don't build a backend for it: client-side
execution is simpler to build, cheaper to run, and impossible to breach on
my end because there's nothing of the user's to breach there. When a
backend is genuinely needed, it's still not a third party's — it's a
service I run and reach privately, not a public endpoint handed the data
on faith.
