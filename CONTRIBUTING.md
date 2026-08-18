# Contributing

TriTrack Editing Assistant is in pre-release development. Contributions should
keep the local-first privacy boundary and editor ownership of story decisions
intact.

## Development setup

Use Python 3.12 and 3.13:

```bash
python3.13 -m venv venv
venv/bin/python -m pip install --constraint requirements/ci-constraints.txt pip setuptools
venv/bin/python -m pip install --constraint requirements/ci-constraints.txt -e '.[dev]'
venv/bin/python -m unittest discover -s tests -v
venv/bin/ruff check src tests examples scripts
```

## Change discipline

1. Open a focused issue once the public remote exists.
2. Add or update a test that fails for the intended reason.
3. Implement the smallest coherent change.
4. Run focused tests, the full suite, lint, package／CI contract tests, and the
   maintainer privacy and local-candidate gates available for that stage.
5. Explain compatibility and privacy effects in the pull request.

Do not include production media, transcripts, credentials, private paths,
camera serials, private title/font assets, or copied private-repository
history. Use invented or explicitly cleared fixtures only.

Generated outputs must be written to absent ignored directories and must not
overwrite source media. Provider features require an explicit opt-in and may
not become part of the default local path.

By contributing, you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md)
and license your contribution under Apache-2.0.
