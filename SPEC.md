# App Studio decisions

The durable agreement between learner and AI. Update only agreed decisions and
actual evidence; pending is a valid state. Keep explanations/help in
[LEARNING.md](LEARNING.md), not a second copy here.

## Current stage

- **Current feature:** APP-003.
- **Status:** APP-001 merged with both main CI jobs passing; APP-002 merged with both main CI jobs passing; APP-003 merged in PR #6; issue #5 closed. APP-001 prediction remains pending.
- **Next step:** Verify latest main CI before submitting the repository URL.
- **Implementation marker:** `studio.json`: `implemented_through: 3` after passing cumulative checks.

This repository owns application code. Server/proxy changes and production
deployment are outside these three local-development lessons. Prepared helpers
are reusable foundations, not evidence that unfinished routes are implemented.

## APP-001 · Branded homepage

**Scope:** make the neutral FastAPI homepage express one chosen identity with
a simple original SVG mark, coherent copy, navigation and shared style tokens.
Keep account actions honest about their unfinished state.

| Decision | Agreement |
|---|---|
| Visitor and concrete use situation | Everyone, including school and college students, browsing books for school or leisure. |
| Reused IS117 brand, or name / promise / primary archetype | Shiv’s Book Store; Find your next book for school or leisure; AI-suggested Everyperson personality adopted with simple defaults. |
| One visible choice and visitor benefit | Learner requested books with names, prices, and short descriptions. Expected visitor effect remains pending. |
| Own issue / branch / PR | [Issue #1](https://github.com/ssp344/my-app-studio/issues/1); `feature/app-001-bookstore`; [PR #2](https://github.com/ssp344/my-app-studio/pull/2). |

**Keep when:** the agreed identity is visible and usable at desktop/narrow widths;
full foundation + APP-001 checks pass; AI review and the learner's actual check
interpretation/browser observation/keep reason are recorded; reviewed evidence
and verified GitHub state are linked below.

## APP-002 · Signup, login and logout

**Scope:** add browser forms and REST behavior for member signup, login, a private
dashboard and logout backed by SQLite. Reuse the prepared password/JWT/CSRF/session
helpers; keep data local. New accounts cannot choose their role.

| Decision | Agreement |
|---|---|
| Expected public/private behavior and account flow | Signup → login → private reader dashboard → logout. Anonymous dashboard visitors redirect to login. New accounts are members. |
| Valid and rejected cases to demonstrate | Valid signup/login; duplicate and invalid signup, role input, wrong passwords, missing CSRF, and revoked sessions rejected. |
| Own issue / branch / PR | [Issue #3](https://github.com/ssp344/my-app-studio/issues/3); `feature/app-002-accounts`; [PR #4](https://github.com/ssp344/my-app-studio/pull/4). |

**Keep when:** the agreed forms/API work; duplicate/invalid signup and wrong
credentials are rejected; passwords are hashed; authentication uses validated,
expiring JWTs with protected cookies and CSRF; private requests require a live
session and logout revokes it. Full cumulative checks, AI review, actual learner
contributions and GitHub state are recorded. This is not a production-security certification.

## APP-003 · Server-enforced roles

**Scope:** enforce a small member/admin boundary in the API and browser. Assign
roles only through the trusted local terminal command; use current server-side
permissions, including for an existing session after a role change.

| Visitor | Homepage | Member area | Admin area/API |
|---|---|---|---|
| Anonymous | Allowed | Login required | Login required |
| Member | Allowed | Allowed | Forbidden |
| Admin | Allowed | Allowed | Allowed |

| Decision | Agreement |
|---|---|
| Intended admin-only result | Read-only bookstore overview with store name, sample-book count and demo catalog status. Separate `/admin/login` entry point requested by learner; username `shivadmin` chosen for a local admin account. `/login` links to admin sign-in, preserving the prepared anonymous `/admin` redirect contract. No shared passkey or automatic admin signup. Anonymous visitors redirect to login; members get 403; admins get 200. Roles change only through the trusted local CLI and apply on the next request, including existing sessions. |
| Actual allowed/denied request evidence | Full APP-003 and normal checks passed: 99 foundation, 18 cumulative contracts, 2 Chromium tests. Anonymous API 401 / page login redirect; member API/page 403; admin API/page 200; promotion/downgrade applies to existing sessions. |
| Own issue / branch / PR | [Issue #5](https://github.com/ssp344/my-app-studio/issues/5); `feature/app-003-roles`; [PR #6](https://github.com/ssp344/my-app-studio/pull/6). |

**Keep when:** a direct request cannot bypass the role boundary, role changes
take effect as specified, new signup remains member-only, and full cumulative
checks plus AI review pass. Link the learner's actual interpretation/observation,
reviewed record and verified GitHub result. Hidden navigation alone is insufficient.

## Evidence

Link actual files/checks and the student's own issues/PRs. No fabricated URLs,
customer research or claims that a timestamp proves learning.

| Feature | Files / own issue / PR | Actual checks and learner observations | Kept / GitHub state |
|---|---|---|---|
| APP-001 | [Issue #1](https://github.com/ssp344/my-app-studio/issues/1); `app/brand.json`, `app/templates/home.html`, `app/templates/base.html`, `app/static/logo.svg`, `app/static/site.css` | Full `check --lesson APP-001` and normal `check` passed: 98 foundation + 2 contracts + 2 Chromium tests. Desktop 1280px and mobile 390px visually reviewed; no mobile horizontal overflow. Learner selected broken-link scenario with AI help and observed Browse books scrolling to the listings. | Learner chose to keep: simple and easy to look through. Record reviewed and pushed; [PR #2](https://github.com/ssp344/my-app-studio/pull/2) merged; issue closed; both main CI jobs passed. |
| APP-002 | [Issue #3](https://github.com/ssp344/my-app-studio/issues/3); `app/features/accounts.py`, `app/templates/account.html`, `app/templates/dashboard.html`, `app/templates/base.html` | Full APP-002 checks passed: 98 foundation, 14 cumulative contracts, 2 Chromium tests. Anonymous dashboard redirected to login; signup desktop/mobile reviewed. | Learner observed login page after logout/reopening dashboard; kept the flow to prevent access after logout; summary reviewed. Copied-cookie interpretation remains pending; [PR #4](https://github.com/ssp344/my-app-studio/pull/4) merged; issue #3 closed; both main CI jobs passed. |
| APP-003 | [Issue #5](https://github.com/ssp344/my-app-studio/issues/5); `app/features/roles.py`, `app/templates/admin.html`, `app/templates/forbidden.html` | Full cumulative checks passed; isolated real-browser CLI promotion and member denial reviewed; admin desktop/mobile layouts reviewed without horizontal overflow. | Learner observed admin overview as shivadmin and denial as test; kept the simple flow; summary reviewed. Independent check interpretation pending. [PR #6](https://github.com/ssp344/my-app-studio/pull/6) merged; issue #5 closed. Latest main CI must be verified before submission. |

The instructor's reference branches show possible implementations. They do not
establish this repository's completion or the learner's own reasoning.

## Submission record

- Submit this repository: https://github.com/ssp344/my-app-studio
- Completed merged lesson PRs: [APP-001 #2](https://github.com/ssp344/my-app-studio/pull/2), [APP-002 #4](https://github.com/ssp344/my-app-studio/pull/4), [APP-003 #6](https://github.com/ssp344/my-app-studio/pull/6). Corresponding issues #1, #3 and #5 are closed.
- [Actual GitHub CI runs](https://github.com/ssp344/my-app-studio/actions/workflows/check.yml): inspect the latest main run for both check and windows.
- Learning evidence gaps remain explicit: APP-001 prediction; APP-002 and APP-003 independent check interpretations. No missing student answers have been invented.
