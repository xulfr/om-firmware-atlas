# 0009 — A time-limited spotlight for new features

Status: accepted, 26 November 2026.

The home page shows what projects have built through agreed images, newest release first. A feature that arrives without screenshots, such as Caduceus for OM-3's Film Rolls in v0.41-beta2, cannot appear there, and its only home is one card among a dozen on the project page. Hand-written home-page prose would drift from the records and outlive the news.

A project feature may carry `spotlight_until`, a date. Until that date the home page shows the feature in a spotlight band above the showcase: project, cameras, the release named by `since`, the project's own status and summary, a link to the feature's card (feature cards now have stable `#feature-…` anchors), the linked capability, and the notes and warning of the newest release for the feature's camera, which is what a reader would install today. At most two features are shown, newest release first. When nothing is highlighted the band is empty, so the page needs no edit.

The date must fall within 31 days after the project's `last_reviewed`, which `check` enforces, so a highlight never outlives the review that set it, and the weekly rebuild removes it on time. The spotlight only re-presents record fields; it adds no claims, keeps the project's status words and the release warning, and links the Atlas evidence separately as everywhere else. Images still need maintainers' agreement and stay in the showcase.
