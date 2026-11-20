# OM Firmware Atlas

An independent map of Olympus and OM SYSTEM firmware research, tools, modifications and test evidence.

**[Explore the Atlas](https://xulfr.github.io/om-firmware-atlas/)** · [Camera directory](views/cameras/index.md) · [Projects](views/projects/index.md) · [Community](views/community/index.md) · [Contribute](CONTRIBUTING.md) · [How it works](docs/how-it-works.md)

Find existing work for your exact camera, understand what has actually been tested, and contribute to the project that owns the implementation. This is a documentation repository: firmware, emulators, patch builders and look editors stay with their authors.

## Start here

- **Camera owners:** choose your [camera](views/cameras/index.md), then follow a project's own documentation. Listing a model does not mean a working modification exists.
- **Researchers:** read [the research starting guide](docs/research.md) and the relevant [topic](knowledge/README.md). Keep model, firmware and package identity explicit.
- **AI agents:** read [AGENTS.md](AGENTS.md), then [agents/start.md](agents/start.md). Routes show what to read and its estimated cost.
- **Community:** find [r/M43 and Caduceus Discord](views/community/index.md). Discussion links are discovery routes, not test evidence.

The initial catalogue is deliberately bounded. It records reviewed sources and visible gaps; it is not an exhaustive list of every Olympus project. A successful emulator run, published release and physical-camera report are different facts. Read [how to interpret evidence](docs/evidence.md).

## Maintain the library

Python 3.10+ is required. Create a virtual environment, activate it, then:

```sh
python -m pip install -r requirements.txt
python scripts/atlas.py generate
python scripts/atlas.py check
python -m unittest discover -s tests -v
python scripts/atlas.py build
```

`site/` is the local static site. For a preview, run `python -m http.server 8000 --directory site --bind 127.0.0.1`. See [maintenance](maintenance/README.md) for routing, freshness, CI and publication.

[How the Atlas works](docs/how-it-works.md) explains records, generated pages, checks, review and publication, and has copyable agent prompts. Agents may raise PRs; humans review and merge.

Original Atlas contributions use the existing [Apache-2.0 licence](LICENSE). External projects retain their own terms. No vendor firmware is stored here. The Atlas links to other projects but is not responsible for their contents or downloads; see the [disclaimer](docs/about.md#disclaimer). Not affiliated with Olympus or OM Digital Solutions.
