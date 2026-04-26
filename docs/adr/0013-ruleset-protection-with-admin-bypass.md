# ADR-0013: Branch protection via ruleset with admin bypass, not classic protection

**Status:** Accepted
**Date:** 2026-04-26

## Context

The repository is a solo project with one maintainer (Chris) and a public, world-readable repo. The intent is that:

- The maintainer commits direct to `main` for routine work, gated by passing CI.
- Any external contributor (including future collaborators or drive-by PRs) must go through a pull request, with CI required to pass before merge.
- Force-pushes and branch deletion are blocked for everyone.
- Linear history is required.

Classic GitHub branch protection treats `required_pull_request_reviews` as binary: either everyone must PR or no one must. There is no first-class way to exempt the maintainer while requiring contributors to PR. The repo configuration therefore needs a different mechanism.

GitHub repository rulesets, introduced after classic branch protection, expose `bypass_actors` as a first-class field. A ruleset can require pull requests as a rule while listing specific actors who bypass that rule.

## Decision

Branch protection on `main` is implemented as a GitHub **ruleset** (not classic branch protection), with the following shape:

- **Target:** `~DEFAULT_BRANCH`
- **Enforcement:** `active`
- **Bypass actor:** `RepositoryRole` with `actor_id=5` (admin role), `bypass_mode: always`
- **Rules:**
  - `deletion` (block branch delete)
  - `non_fast_forward` (block force-push)
  - `required_linear_history`
  - `pull_request` with `required_approving_review_count: 0` and `dismiss_stale_reviews_on_push: true`
  - `required_status_checks` with `strict_required_status_checks_policy: true` and the single context `"ruff + mypy + import-linter + pytest"` (the CI workflow's job name, not the per-step labels)

The required status check references the **job name**, not individual step names. All quality gates (ruff format, ruff check, mypy, lint-imports, pytest) live inside one job; listing them as separate required contexts produces an unsatisfiable rule.

## Consequences

- The maintainer commits direct to `main` when local CI is green; CI on the remote is the safety net.
- External contributors must open a PR; CI must pass before merge.
- The configuration is managed via the GitHub REST API (`POST /repos/{owner}/{repo}/rulesets`), not the web UI's classic branch protection page. Future audits or recreations should use the API.
- The bypass actor is bound to the admin role (actor_id=5), not a specific user. This is durable across token rotations and personal account changes; anyone with admin on the repo bypasses, which is the intended scope.
- If the project later grows past solo maintenance, removing the bypass actor reverts the rule to "everyone PRs" without restructuring — a clean escape hatch.
- Classic branch protection is **not** in use and should not be added alongside the ruleset. Two overlapping protection mechanisms produce confusing precedence.

## Cross-references

- Session report 2026-04-26 §12.2 documents the ruleset creation, including the JSON payload submitted via `gh api`.
- `docs/design/DESIGN.md` §11.1 (Distribution Strategy) covers the public-repo posture.
- `CONTRIBUTING.md` "Branch and commit rules" section documents the contributor-facing PR workflow.
