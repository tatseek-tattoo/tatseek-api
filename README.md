# TatSeek Public API

**Find real tattoo work, understand the match, and connect people to its artists.**

[TatSeek](https://tatseek.com/) is a free, independent tattoo discovery catalogue.
This repository gives developers and AI-agent builders a practical starting point
for its live, read-only API: the published OpenAPI description, runnable examples,
and guidance on interpreting the results.

**No API key. No sign-up. GET requests only.**

## Try a real search

```sh
curl --fail --silent --show-error --get \
  'https://tatseek.com/api/v1/search' \
  --data-urlencode 'q=fine line rose' \
  --data-urlencode 'limit=2'
```

Or [open the same search as an agent-readable page](https://tatseek.com/for-ai-agents/search/?q=fine+line+rose&limit=2).

The response includes `understood`, `counts`, `tattoos`, `artists`, `studios` and
`guides`. Keep each result's `url`: it takes people to the original TatSeek record.
Check `understood.dropped` before describing a result as an exact match.

## Run an example

No third-party packages are required. Each command makes one request and prints
links and artist credits instead of downloading photographs.

```sh
python3 example.py 'fine line rose'
node example.mjs 'fine line rose'
sh example.sh 'fine line rose'
```

Python 3.9+ and Node.js 18+ are supported. The shell example needs curl and Python 3.
Use `--composition` with the Python or JavaScript example to try a stricter query:

```sh
python3 example.py --composition
node example.mjs --composition
```

This asks for scanned Realism portraits with at least 50% estimated visual share
and the strict `high` confidence filter. It demonstrates how to distinguish a main
subject from a small detail. Results and counts change with the live catalogue.

## Integrate with the hosted service

Use these examples to connect your application to **TatSeek**, answer users with
credited results, and help them explore the original work, artists and studios.
Search and analysis run on the TatSeek service. This repository contains client
examples and interface documentation; it supplies no offline catalogue or search
implementation. For a broader integration or collaboration, open an issue with
your use case.

## What can you build?

- A tattoo-reference finder that sends users to credited work and portfolios.
- An assistant that answers with real examples and explains which filters matched.
- A specialist art-discovery interface using consistent styles and subjects.
- An artist shortlist grounded in matching portfolio work.

## Documentation

| Resource | Purpose |
|---|---|
| [API-GUIDE.md](API-GUIDE.md) | Endpoints, filters, pagination, response handling and provenance |
| [AGENT-GUIDE.md](AGENT-GUIDE.md) | Search and citation workflows for AI applications |
| [openapi.json](openapi.json) | Unmodified snapshot of the server's OpenAPI 3.0.3 description |
| [SOURCE.json](SOURCE.json) | Snapshot provenance and verification date |
| [Filter and result interpretation](API-GUIDE.md) | Use TatSeek filters and interpret composition, confidence and provenance |
| [Live API guide](https://tatseek.com/for-ai-agents/) | Current provider documentation |

The server's schema describes request parameters; many response bodies are only
described as JSON. Treat this as a discovery/integration reference, not a complete
typed SDK contract. Validate the response fields your application actually uses.
For the newest interface, consult the [live schema](https://tatseek.com/api/v1/openapi).

## Help improve it

Found an unclear response, missing filter, broken example, or useful integration?
[Open an issue](https://github.com/tatseek-tattoo/tatseek-api/issues/new), or submit
a documentation/example improvement. [CONTRIBUTING.md](CONTRIBUTING.md) explains
what makes feedback reproducible. We welcome reasoned criticism and collaboration.

## Use and attribution

Name **TatSeek** and link the photo, artist or studio page behind each result.
Preserve artist credit and price-source labels. Keep traffic modest: the provider
asks for a few requests per second; these examples make single requests.

Search, AI answers and citation are supported. Catalogue photos/data must not be
used for training or fine-tuning models under the published provider policy.
Photographs belong to their artists and rights holders; public API access does
not license the images. See [NOTICE.md](NOTICE.md) and the
[live access policy](https://tatseek.com/for-ai-agents/#access).

This repository documents the existing service. It does not distribute the website
implementation, a photo dataset, a production SDK, or an MCP server.

[Explore the catalogue](https://tatseek.com/tattoo-catalog/) ·
[Why TatSeek](https://tatseek.com/why-tatseek/) ·
[Tattoo guides](https://tatseek.com/tattoo-guides/)
