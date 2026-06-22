# kpatch-rewrite-benchmark

This repository contains Linux kernel CVE hotfix rewrite cases for testing
agents that rewrite upstream/downstream fix patches to bypass kpatch
limitations.

## Scope

- Target kernel: `6.6.102-5.2.alnx4.x86_64`
- Target tag: `6.6.102-5.2`
- Downstream source: `cloud-kernel/devel-6.6`
- CVE years: `2025`, `2026`
- Included cases: downstream fixes that are present in `devel-6.6`, absent from
  the target tag, trigger a kpatch limitation, and are considered
  rewrite-bypassable.

## Layout

```text
dataset.json
cases/
  CVE-YYYY-NNNNN/
    metadata.json
    original.patch
    rewritten.patch
    original_patches/
      0001-*.patch
      series
scripts/
  validate_dataset.py
```

Each case is self-contained:

- `original.patch` is the merged downstream fix diff used as the input patch.
- `original_patches/` preserves the per-commit downstream patch set.
- `rewritten.patch` is the final rewritten diff that bypasses the kpatch
  limitation.
- `metadata.json` records CVE metadata, upstream/downstream commit provenance,
  triggered kpatch limitations, and the rewrite rationale.

## Validation

Run:

```bash
python3 scripts/validate_dataset.py
```

The validator checks that every indexed case has the expected files and that
metadata is consistent with `dataset.json`.
