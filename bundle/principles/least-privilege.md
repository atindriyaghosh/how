---
type: principle
title: Least privilege
summary: A credential carries only the authority its actual usage requires, never the broader default it's handed.
---

A credential or token carries only the authority its actual usage requires,
never the broader default it's handed by whatever issues it. This is a
different axis from no egress: no egress asks whether a component can
reach the network at all; least privilege asks, given that it can act, how
much it's allowed to do once there. Both matter; neither substitutes for
the other. Each mechanism this applies to is its own section below.

#### GitHub Actions

Grant the workflow's token only the scopes its steps actually use —
`contents: read`, `pages: write`, `id-token: write` here, not the broader
default a workflow gets when it doesn't ask. A workflow holding more
permission than it uses is a bigger blast radius if any one action in it is
ever compromised, regardless of whether that action is pinned by SHA.
