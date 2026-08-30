# chs-downloader (deprecated)

**This prototype is deprecated as of 2026-08-30 and the repository is
archived.** Its purpose is fully absorbed into the dissertation monorepo:

- Working bulk downloader: `phd-scripts/chapter3-geoai/scripts/chs_bulk_download.py`
  (plan / smoke / go modes, throttled one-session client, resumable manifest).
- Endpoint documentation: `phd-scripts/chapter3-geoai/docs/chs-data-access.md`
  (the full verified chain: guest login, `GetMappingPoints`, download grid,
  Create/Get zip).

The lasting contribution of this prototype was discovering the
`GetMappingPoints` endpoint (save-point discovery by bounding box), which the
monorepo tool now uses. The Selenium browser-automation code here remains
only as a historical fallback reference.
