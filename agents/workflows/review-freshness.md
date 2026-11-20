# Review freshness

Start from the open `atlas-update-queue` issue, or run `python scripts/atlas.py freshness --fetch` then `queue` for `.build/update-queue.md`; network access is required. It compares pinned GitHub revisions/releases, each project's newest release and other URLs without running source code.

For a new release, read its notes and add it to the project's `releases` (newest first) and `features` where it adds or changes one, citing a release source. Keep the project's own status words and warnings; test claims stay attributed.

If a listed project now publishes firmware on a branch, tag or release asset, propose removing its listing (decision 0008) instead of updating it. Read only changed/overdue source shards. A changed upstream revision queues review; it does not alter a capability. A failed fetch retains the source record and is reported as a failed check. Follow the ingestion workflow for a substantive update.

Update `last_reviewed` only after reviewing facts; link checking alone does not renew it. Historical observations retain their event/report dates. Never convert a scheduled job into automatic claim promotion or merging.
