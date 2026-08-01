# Evaluator visibility matrix

Traversal starts at `pages/current-verification/page.md` through the first navigation item. Every row below was checked without using OpenResearch logs or repository-only knowledge.

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `claim-1-current` | Complete | Complete | Complete | Complete | Complete | Complete | Complete |
| 2 | `claim-2-current` | Complete | Complete | Complete | Complete | Complete | Complete | Complete |
| 3 | `claim-3-current` | Complete | Complete | Complete | Complete | Complete | Complete | Complete |
| 4 | `claim-4-current` | Complete | Complete | Complete | Complete | Complete | Complete | Complete |
| 5 | `claim-5-current` | Complete | Complete | Complete | Complete | Complete | Complete | Complete |

`Complete` means the canonical traversal directly exposes the exact contract and assumptions, raw numerical result, current executable source, independent check, intended negative control, CPU/runtime/seed provenance, and limitations. The downloaded-candidate red-team record and checker output are stored under `artifacts/current/release/` before publication.
