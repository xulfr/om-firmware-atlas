# Implementation and population plan

This plan records the bootstrap scope and what remains. The bootstrap section below is historical; the catalogue has since grown well beyond it. The user created `xulfr/om-firmware-atlas` and authorised bootstrap pushes to main; branch protection follows setup.

## Initial delivery

- Entry contract, shared Claude pointer, three short roles and source/status/freshness workflows.
- Seven record types: the original six plus community venues, with schemas and scoped-reference checks. A technical `reference` type followed ([0006](decisions/0006-technical-reference.md), [0007](decisions/0007-build-facts.md), [0008](decisions/0008-hazard-symptoms.md)), making eight.
- A bounded initial corpus spanning the two OM-5 generations, OM-3, E-P7, PEN-F and an E-M10 IV discovery route.
- Small shared guides that route into existing technical homes rather than mirror their notebooks.
- Generated camera/project/evidence/source/community pages and agent route shards with reading costs.
- Fixed routing cases, semantic/generator regression tests, strict site build and read-only PR validation.
- GitHub Pages from main, with source revision/build time and a prominent community directory linking r/M43 and the confirmed published Discord invite.

The OM-5 evidence slice retains a named-package failure, restoration from that incident, an incomplete positive Mark II report and bounded emulator tracing. This validates distinctions before expanding the catalogue.

## Since bootstrap

The catalogue now spans bodies from the PEN E-PM2 to the OM-5 Mark II, with mod builders, research notes, emulators and analysis tools listed in the [project directory](../views/projects/index.md). Project showcase pages (features, releases, goals) and the per-build technical reference were added. Weekly freshness checks feed reviewed release and source updates.

## Remaining work

Done since bootstrap: main is protected (required PRs, passing **Atlas validation**, up-to-date branches, resolved conversations; maintainers may merge their own PRs), and agents have taken many source URLs through the PR workflow. Routing tests remain deterministic checks, not proof of external client compliance.

1. Deepen OM-3/E-P7 feature-level evidence and interface records, including minimum-release semantics and unsupported exports. Do not infer a shared-panel agreement.
2. Add exact input hashes for the firmware entries that currently record version/build only. Review individual db firmware camera reports before promoting its release-level claims.
3. Keep adding body projects from upstream discovery lists and community reports through bounded source PRs. Expand research/tool profiles when an actual task needs them.
4. Add community venues or more precise public channel links as the community supplies them. Record listing basis, access and link-check scope; preserve technical findings through specific posts/messages and their publication permission.
5. Let `freshness --fetch` fall back to `git ls-remote` when the GitHub API is unavailable; agents currently do this by hand ([freshness workflow](../agents/workflows/review-freshness.md)).

Weekly CI produces a source/freshness report and republishes the existing main content. It does not call an LLM, crawl private chats, change canonical claims or raise unsolicited upstream messages. A maintainer can hand a queue item to an agent. Automatically invoking a separate agent service is a later operational choice.

Success means a source can become scoped evidence, useful routes and human pages through a reviewable PR. An exhaustive camera database, symbol index or new shared firmware toolchain is outside this initial delivery.
