# Dataset Schema

Schema version: `1.0`

## `dataset.json`

Top-level index for the benchmark.

Required fields:

- `schema_version`: schema version string.
- `name`: dataset name, currently `kpatch-rewrite-benchmark`.
- `target_kernel`: full target kernel version.
- `source_branch`: downstream branch used for source fixes.
- `target_tag`: downstream target kernel tag.
- `generated_at`: ISO 8601 generation timestamp.
- `case_count`: number of cases in `cases`.
- `selection`: inclusion criteria.
- `cases`: compact index of case records.

Case index fields:

- `cve_id`: CVE identifier.
- `path`: relative path to the case directory.
- `severity`: CVSS severity if available.
- `cvss_score`: CVSS score if available.
- `published_date`: CVE announcement/publication date.
- `limitations`: kpatch limitation categories triggered by the original patch.
- `downstream_commits`: downstream commit SHA list used to form the original
  patch set.

`build_status` is intentionally not part of the schema.

## `cases/<CVE>/metadata.json`

Per-case metadata.

Required fields:

- `schema_version`
- `cve_id`
- `description`
- `published_date`
- `cvss`
- `affected_stable_versions`
- `target`
- `upstream`
- `downstream`
- `kpatch`
- `files`
- `notes`

`target` fields:

- `kernel_version`
- `target_tag`
- `target_contains_fix`

`upstream` fields:

- `mainline_fix_sha`
- `fix_6_6_y`
- `all_6_6_y_fixes`

`downstream` fields:

- `status`
- `in_devel_6_6`
- `in_target_tag`
- `match_method`
- `commit_source`
- `commits`
- `completeness_confidence`
- `review_flags`

`kpatch` fields:

- `directly_buildable`
- `triggers_limit`
- `limitations`
- `bypassable_by_rewrite`
- `confidence`

`files` fields:

- `original_patch`
- `rewritten_patch`
- `original_patches_dir`

`notes` fields:

- `rewrite_idea`
- `agent_reasoning`
- `needs_review`

## Limitation Categories

The `limitations` list uses normalized strings from the source judgment data.
Common values include:

- `data-structure`
- `static-data`
- `exported-symbol`
- `dynamic-data-semantic`
- `header-wide`
- `traceability`
- `module-config`
- `static-local`
- `other`
