# 0008 — No repositories that distribute firmware

Status: accepted, 20 November 2026.

The Atlas already stores no vendor firmware. Linking to a repository that publishes firmware would still point readers to that material and make the Atlas a route to it. A proposed entry for an E-M1 Mark III mod repository that commits a patched update file was closed without merging for this reason.

Rule: the Atlas does not list, cite or link a repository that publishes camera firmware on any branch or tag, or as a release asset. Firmware here means a stock or modified update file, a decoded or expanded firmware image, or a dump of part of one.

Not covered, and still allowed: card data files a mod reads (looks, settings), hashes and checksum lists, edit lists and patch descriptions, and builders that download the official file from the vendor on the user's own machine and patch it there.

Process: intake checks branches, tags and release assets by file name, size and location before any record is written, without running anything. A match stops intake and is reported to the requester. When a freshness review finds that a listed project has started publishing firmware, the reviewer proposes removing the listing.

Alternatives: listing with a warning (still a route to the files), or linking only clean subpaths (the repository remains one click away).
