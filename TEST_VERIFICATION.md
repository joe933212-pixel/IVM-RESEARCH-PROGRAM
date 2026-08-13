# Repository Test Verification Record

## Purpose

This document distinguishes historical test artefacts from a clean verification rerun performed while assembling the repository.

The historical result files remain preserved in the version directories.

The rerun was performed from the correct runtime package root with the package path available to Python. This matters because the archived v0.1–v0.4 `TEST_RESULTS.txt` files include an import-path failure when invoked from outside the package root.

## Verification environment

Python: 3.13 runtime available in the research environment.

Command pattern:

`PYTHONPATH=. python -m unittest discover -s tests -p 'test*.py' -v`

## Results

| Runtime | Tests | Result |
|---|---:|---|
| v0.1 | 5 | PASS |
| v0.2 | 9 | PASS |
| v0.3 | 15 | PASS |
| v0.4 | 20 | PASS |

The separate process-death experiment remains recorded as **23 tests passed** in its own historical result file.

## Interpretation

These verification runs confirm that the packaged source suites execute successfully under the stated invocation.

They do not replace the original experimental records.

The process-death result is retained separately because it tests a distinct condition involving actual operating-system process termination and fresh-process recovery.

## Reproducibility note

The repository should eventually include an explicit environment specification and automated CI workflow so that these results can be reproduced independently of the research environment in which they were first generated.
