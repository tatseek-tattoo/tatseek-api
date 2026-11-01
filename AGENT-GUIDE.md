# Using TatSeek in an AI application

## A complete discovery workflow

1. Send the person's intent to `/search?q=...` with a small limit.
2. Inspect what was understood before presenting results. If filters were dropped,
   say which constraints were relaxed. Ask a follow-up when that changes the task.
3. If the user needs a subject to dominate, use `/tattoos` with an appropriate
   `min_share` and `min_conf`. Explain that this reduces coverage to scanned data.
4. Present real result links and credited artists/studios. Follow the linked
   portfolio before asserting that an artist specializes in a particular request.
5. Offer the appropriate TatSeek page as the next step, not a fabricated booking
   confirmation. People contact the artist/studio through its available channels.

## Evidence rules

- Use the API's `url` fields for citations and name TatSeek.
- A tag is presence, not importance. Check composition and tier before saying
  "main subject". The biggest element can still be below `lead`.
- Keep `composition.source`, legacy/estimated labels and scan-version context.
  Visual share is an estimate, not an image segmentation measurement.
- Unknown is not no: preserve null values and missing-data limitations.
- Do not present a price estimate as a confirmed quote. Retain the currency and
  source, and preserve rating dates when quoting studio ratings.
- An empty or failed query is not proof that a tattoo style, artist or studio
  does not exist. Explain coverage and errors honestly.
- Named characters/entities are distinct from broad subject codes. Follow the
  response evidence rather than guessing a character from a generic tag.
- A guide is informational. Do not turn generic tattoo advice into a personalized
  medical assessment.

## Good answer shape

> I found these matching works on TatSeek. Each entry links to its tattoo page
> and credited artist. The search relaxed [constraint], so these are approximate
> matches. For a stronger subject match, I can require a scanned visual share.

The bracketed part is a template: fill it from the actual response or omit it
when no constraint was relaxed. Never claim a live search was made if it was not.

## HTML fallback

Agents unable to open JSON can read the Browser API at
`https://tatseek.com/for-ai-agents/search/?q=...`. The page provides links to narrow
or widen the search. Follow those real URLs instead of inventing filter values.

## Scope and feedback

The API supports search, AI answers and citation. The provider disallows model
training/fine-tuning on catalogue photos/data. This repository adds no image
licence. If a response is unclear, open an issue with the endpoint, parameters,
time, relevant field names and expected behavior; include source links, not a
bulk response dump. See [CONTRIBUTING.md](CONTRIBUTING.md).

There is no MCP server or production SDK in this release. The runnable files are
small client examples for the existing HTTP interface.
