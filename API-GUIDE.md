# API integration guide

Verified against the public service on **2 November 2026** (Asia/Almaty).
The hosted API is the current source of truth; this repository contains dated
documentation snapshots, not a promise of immutable catalogue contents or uptime.

## Access and formats

Base URL: `https://tatseek.com/api/v1`.
An alternative base published by the server is `https://tatseek.com/wp-json/tatseek/v1`.
No authentication is required. Requests are read-only GETs over HTTPS.

For tools that cannot read JSON, replace the base with
`https://tatseek.com/for-ai-agents/` and use the same endpoint and query parameters,
for example `/search/?q=fine+line+rose`. The Browser API returns readable HTML;
adding `format=json` requests JSON. Do not parse presentation HTML when your
application can use the JSON API directly.

## Endpoints

| GET path | What it returns | Useful parameters |
|---|---|---|
| `/search` | One combined answer: interpreted query, destination, tattoos, artists, studios, guides | `q`, exact filters, `limit`, `offset` |
| `/tattoos` | Tattoo results and pagination; one record with `id` | `q`, filters, `id`, `limit`, `offset` |
| `/artists` | Artists ranked by name and matching work; one artist with `artist` | `q`, filters, `artist`, `budget` |
| `/studios` | Studios and their context; one studio with `studio` | `q`, filters, `studio` |
| `/guides` | Relevant guide sections with destination links | `q` |
| `/vocabulary` | Valid filter codes and explanatory notes | none |
| `/stats` | Live catalogue counts | none |

See [openapi.json](openapi.json) for parameters per endpoint. Do not assume every
parameter works on every path: for example `/guides` documents `q`, not the entire
tattoo-filter set. The published source schema also documents one-record lookups.

## Choose words or exact filters

Use `q` for a person's description. The engine maps known terms and synonyms to
its vocabulary, reports corrections, and may drop a filter when it cannot match
everything. Read `understood.facets`, `corrected`, `free_words`, `exact_match` and
`dropped`; do not conceal fallback behavior from the user.

For a controlled UI, fetch `/vocabulary` and send its **codes/slugs**, not translated
display labels. The vocabulary has styles, subjects, placements, colours,
techniques, moods, size/detail codes and further scan axes. A subject group such
as `animals` includes its children; it is not a separate claim that all records
carry the parent as a direct tag. New codes can be valid before any records exist.

Common filters include:

| Parameter | Meaning / example |
|---|---|
| `style` | Visual style, e.g. `fine-line` or `realism` |
| `subject` | Depicted subject, e.g. `rose`, `portrait`, or a group such as `animals` |
| `placement` | Body placement, e.g. `forearm` |
| `color` | Broad colour category, e.g. `black-and-grey` |
| `technique` | Method such as `dotwork`, distinct from style |
| `city`, `country` | Geographic discovery filters; obtain current values from the live service |
| `size`, `detail` | Separate size and detail concepts; do not equate a large tattoo with a detailed one |
| `ink` | Specific ink colour such as `red`; follow the vocabulary's scan-coverage notes |
| `entity` | Named-character/entity filter; see the live parameter description |
| `min_share`, `min_conf` | Composition-based importance threshold and confidence filter |

The current schema also lists `mood`, `structure`, `coverage`, `look`, `density`,
`colourful`, `realism`, `effect`, `intent`, `one_sitting`, `lang`, `healed`,
`coverup` and `made_from`. Start with the documented examples; check current
values and coverage before exposing an advanced filter in a product.

## Require a subject to matter

```sh
curl --fail --silent --show-error --get \
  'https://tatseek.com/api/v1/tattoos' \
  --data-urlencode 'style=realism' \
  --data-urlencode 'subject=portrait' \
  --data-urlencode 'min_share=50' \
  --data-urlencode 'min_conf=high' \
  --data-urlencode 'limit=2'
```

`estimated_visual_share` estimates visual importance, in five-point steps. It is
not pixel area. Share and confidence answer different questions. `min_share` and
`min_conf` apply to scanned compositions; legacy estimates inferred from tags
are excluded. Missing composition is not evidence that a subject is absent.

Tier ranges in the provider documentation:

| Tier | Estimated visual share |
|---|---|
| `lead` | 50–100 |
| `major` | 25–49 |
| `supporting` | 10–24 |
| `accent` | 5–9 |

Only call a subject the **main** subject when its tier is `lead`. The largest
available element need not reach that threshold. `main_element`, `main_subject`
and `main_style` are related but distinct: an untagged element can be largest.
Legacy `estimated_from_tags` data can still show a high share or `sure`; retain
the provenance label instead of treating it as a scanned measurement.

## Pagination and single-record requests

For `/tattoos`, read `total`, `limit`, `offset` and `next_offset`. Request a small
page and follow a non-null `next_offset` if another page is needed. Do not assume
the search endpoint uses exactly the same pagination envelope. Counts describe
different result types; `artists_with_matching_work` is not tattoo count.

Get one tattoo with `/tattoos?id=...`, using an ID from a current result. Get one
artist with `/artists?artist=...` or studio with `/studios?studio=...`, following
the slug/identifier documented by the service. Avoid hard-coding record IDs as
permanent test fixtures: records can be corrected or removed.

## Render a useful result

1. Show a title and link to `url`.
2. Preserve available `artist` and `studio` names and their page URLs.
3. Explain the match and any relaxed filters.
4. If displaying a price, preserve the currency, range and source label. An
   estimate is not a studio quote. `/artists` budget is in the studio currency;
   do not compare different currencies as if they were all USD.
5. If displaying a studio rating, keep its source and recorded date. It is not
   a rating created by TatSeek.
6. Preserve relevant content warnings. Do not fetch or redistribute image files
   just to demonstrate an API client.

Nullable or omitted properties must be handled. `healed: null` does not mean
`false`; missing size does not mean zero size. An older scan may not have checked
an attribute now available in a newer scan. Use the returned scan version, basis
and explanatory notes rather than inventing a universal missing-value rule.

## Reliability and limits

Set a timeout and check HTTP status and JSON parsing. Network failures and empty
results are different conditions. Do not turn an error into a fabricated match.
On HTTP 429, honor `Retry-After` if supplied and back off; do not hammer the API.
The provider asks for only a few requests per second; no SLA or numeric quota is
promised here. Cache small reference vocabularies responsibly and refresh them
when validating new codes. Browser integrations should verify CORS behavior in
their own deployment. The examples do not require cookies, tokens or credentials.

## OpenAPI snapshot

`openapi.json` is copied unmodified from the live schema. Its declared API version
is `1.0`; OpenAPI format is `3.0.3`. This repository does not silently add invented
response schemas or advertise unsupported endpoints. The source schema uses
string types for many query parameters, including numeric-looking ones.
Generated clients still need runtime handling for nullable fields and changing
records. [SOURCE.json](SOURCE.json) records a digest so updates can be compared.

Sources: [provider guide](https://tatseek.com/for-ai-agents/),
[live schema](https://tatseek.com/api/v1/openapi),
[live vocabulary](https://tatseek.com/api/v1/vocabulary),
[taxonomy](https://tatseek.com/taxonomy/).
