## Tests

```sh
python -m pip install -r requirements-test.txt
python -m pytest
```

These initial regression tests cover selected existing behavior. External services are mocked or not invoked; this is not end-to-end coverage.

Coverage: existing user loading, credential comparison, and persisted session updates. New-user registration and the LLM/document pipeline are not covered.
