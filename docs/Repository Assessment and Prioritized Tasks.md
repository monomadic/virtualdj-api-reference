# Repository Assessment — Review Record

Date: 2026-09-05  
Status: Inert dated assessment; revised after review  
Goal: Complete, evidence-backed documentation of VDJScript and the Skin SDK, including undocumented features.

The original eleven-task prescription is superseded. [TODO.md](../TODO.md) is the sole active planning state and contains the accepted sequence and execution criteria. This document preserves the diagnosis, review decisions, and reconciliation; it is not a startable queue.

## Assessment retained

The repository is on the right track. Its strongest assets are the compiled verb table, controlled runtime probes, reusable fixtures, structured evidence, and compact lookup commands. The gaps are contract completeness and systematic Skin SDK discovery, rather than missing infrastructure in general.

The initial review inspected repository code, artifacts, documentation, and recent commits. `just check` passed with four existing warnings in quarantined mappers. No new live VirtualDJ experiment was performed, and no new VirtualDJ feature was established. Binary opportunities below are leads, not behavioral findings. Billing and per-assignment token data were not inspected.

Concrete findings:

- `just next-task` matched exactly `Status: Ready`, whereas queue entries used bold text and suffixes; it returned nothing. Two headings were numbered 13, making references ambiguous.
- Task 14 retained `Status: **Ready.**` and an older 1,427-snippet narrative although commit `675addf` shipped the expanded corpus regression and the review's check covered 1,610 snippets. Task 15 also retained ready wording despite both loose ends being closed.
- The store's incomplete selector follows an assigned `needs_test` flag, not every missing contract. XML inventory “documented” means an element mention, not a full attribute/behavior contract. These are limitations of the metrics, not reasons to design a comprehensive schema first.
- The index still derives from prose; existing TODO task 11 owns reconciliation with stronger artifacts. It need not block independent discovery.
- Contract extraction stops at the first `RET`, follows direct `BL` calls one level with a ten-callee cap, and caps string references. Vocabulary extraction uses narrowly spaced address-construction instructions and code-proximity regions. These are concrete analysis boundaries; they do not prove that undiscovered forms exist.

Sources: [task selector](../justfile), [store](../tools/verbdb.py), [XML inventory](../tools/extract_xml_inventory.py), [contract extractor](../tools/extract_action_contracts.py), [vocabulary extractor](../tools/extract_binary_vocabularies.py), and [Evidence Standards](Evidence%20Standards.md).

## Priority decision

The original prescription put four infrastructure tasks before discovery. That was the wrong order for this goal. Storage and extractor changes should follow investigations and be sized by an actual missing representation or demonstrated extraction failure.

The accepted sequence, maintained only in TODO.md, is:

1. Repair queue selection and status ambiguity.
2. Investigate panel/group attribute readers using a real deck-skin fixture.
3. Build a known-position fixture for the unresolved `get_time` cue/loop forms, then run two independent experiments.
4. Make only the storage or extraction change demanded by those results.

A negative panel/group result is valid only with a code-level boundary: reader/dispatch functions inspected, call traversal depth and limits, unresolved targets/references, and branches or instructions not analyzed. “Analysis was limited” is insufficient. Deliver a bounded candidate comparison and a decisive experiment where a credible candidate exists; do not require the discovery of a new feature.

The `get_time` experiment must compare cue, loop-in, and loop-out forms at distinct independently established positions. Bare, `elapsed`, and nonsense arguments establish a floor: prior evidence already shows that an arbitrary argument can select elapsed-like behavior. They are not the primary discriminator. Drift was recorded in `deck2_playing` and `loop_active`; two independent runs are required, not merely `--repeat`. None of the existing ten fixtures establishes all these known positions, so fixture construction is an explicit prerequisite.

## Reconciliation with the existing queue

| Original report item | Existing owner / disposition |
| --- | --- |
| 1: queue repair | Accepted immediate repair; duplicate 13 and stale 14/15 are named defects. |
| 2 and 4: coverage/evidence schemas | Combined into demand-driven follow-up to the pilots, within TODO 0 and 10. No upfront multidimensional schema project. |
| 3: index inversion | Existing TODO 11; retained, not a pilot prerequisite. |
| 5: Skin SDK pilot | Extends TODO 10a's deck-skin fixture work; does not claim to close its separate waveform questions. |
| 6: extractor blind spots | New technical work only when a named pilot target demonstrates the need. |
| 7: argument candidates | Existing TODO 13 and the former duplicate 13, now 13b; narrowed next experiment is `get_time` with a new fixture. |
| 8: runtime parsing/helpers | Existing TODO 10/10b; follow a specific unresolved reader/helper, not a standalone programme around known symbols. |
| 9: economics bookkeeping | Removed. Use scripts for deterministic work and bounded delegation when worthwhile; add no per-assignment accounting requirement. |
| 10: build comparison | Deferred opportunity, not accepted prerequisite work. |
| 11: semantic regressions | Add focused regressions with accepted findings using existing harnesses. |

The report's original “Start here” link is removed. It remains discoverable as a dated review record. Queue corrections in this amendment are documentation changes; implementation of the selector and live investigations remains explicitly queued.
