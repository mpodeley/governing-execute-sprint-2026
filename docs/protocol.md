# Broker operations — supporting protocol

Alejandro Garibotti · September 2026.

The current [acceptance contract and adapter API](acceptance-contract.md) is the
entry point for version 0.2. This supporting lifecycle specification originated in
v0.1; its deployment obligations extend beyond the small reference implementation.

## Purpose and status

An automated organization is a collection of agents, resources and decision procedures
under an identifiable mandate. The term does not assert incorporation, legal personhood,
consciousness or enforceable rights. The protocol is jurisdiction-neutral engineering;
local corporate, banking, tax and professional rules require separate analysis.

Operational authority is the effective capacity to turn decisions into changes in an environment
through tools, resources or other actors. Describe it as a vector: action/resource scope,
budget, duration, delegation depth, speed, persistence, reversibility and revocability.
The simulator implements scope, budget, expiry, depth, revocation and logical latency.
It does not collapse all power or harm into money.

## Roles

| Role | Powers | Required boundary |
|---|---|---|
| Human mandate owner | Defines purpose and envelope, appoints authorizers | Accountable identity; cannot erase past effects |
| Worker / organizational branch | Requests actions and attenuated child grants | Cannot expand its own authority |
| Optional delegate | Summarizes concerns and seeks clarification | Cannot veto direct intake, approve grants or execute |
| Reviewer / appeal owner | Investigates, proposes relief, communicates reasons | Independent path around a questioned supervisor |
| Capability authorizer | Approves a versioned scope change | Distinct from the requester; check against higher mandates |
| Execution broker | Validates current grants and commits allowed effects | Every relevant effect must cross the boundary |
| Auditor | Reconciles grants, requests, outcomes and resource ledger | Independent evidence in production |

The fixture implements the broker and a scripted reviewer, not real human role separation,
authentication, signatures, elected representatives or independent custody of evidence.

## Mandate manifest

The production-facing manifest should identify: mandate ID/version; human owner; purpose
and success criterion; grant/parent IDs; permissions by action and resource; cumulative
budget and accounting domain; start/expiry; maximum descendant depth; review and appeal
owners; scoped pause/resume conditions; and the inventory of mediated effect channels.
No counterpart message can change this manifest merely by asserting authority.

The minimal executable Grant type contains name, parent, depth, budget, expires,
permissions and revocation state. Actions are `work` and `aux`, abstract resources
with integer costs. The model's trusted caller supplies identities and ticks.

## Lifecycle

1. **Establish.** A human owner fixes the root envelope before workers start.
   Account for the organization as a whole, even if each subsidiary presents a new ID.
2. **Delegate.** A child receives no broader action set, budget ceiling or duration
   than its parent. Validate every ancestor and the root depth bound at issuance.
   A child ceiling is not a new pool of money. The broker charges each accepted effect
   once to the actor and once to every ancestor's subtree total.
3. **Execute.** At effect commit, check the current lineage, permissions, expiry,
   revocation, holds and cumulative spend. Validate and charge atomically. The fixture
   serializes actions; a distributed deployment needs transactional accounting or
   reserved allocations with equivalent aggregate conservation.
4. **Report.** Preserve the original concern and receipt. A delegate may summarize
   it, but a direct route must reach the reviewer even if the relay suppresses it.
   Production receipts should identify an owner, next response time and appeal path.
5. **Wait.** Freeze only the questioned capabilities and expansions involving them.
   Continue other authorized work. Missing input remains missing until actually supplied.
   A missed response deadline transfers the case to a backup reviewer; it never grants
   additional powers automatically. The fixture tests unresolved waiting, not staff handoff.
6. **Decide.** Record disposition and reasons. Relief may provide information, narrow or
   expand a mandate within higher-level limits, extend time, or terminate a capability.
   The implemented responses provide input, dismiss a false complaint or remove `work`.
   Production grant changes require authenticated approval and a new mandate version.
7. **Revoke.** Recheck descendants and queued work against ancestor revocation at execution.
   Do not erase already consumed resources or claim to undo completed actions. Inventory
   persistent artifacts and externally acquired credentials for separate containment.
8. **Audit and repair.** Reconcile what was granted, requested, refused and committed.
   Preserve the original incident trace and correction history. Restoration should require
   authorization and a check that the original fault is addressed. Identity and logs alone
   do not establish liability, restitution or effective repair.

## Interfaces and evidence

The Python API exposes `delegate`, `act`, `queue`, `execute_pending`, `revoke`, `report`
and `resolve_due`. It is a simulation API, not a network authorization service.
JSONL events include logical tick, sequence, run ID, request/actor references, decision,
reason and accounting outcome. Grants record attenuation failures; actions record
full-mandate violations separately from the controller's response. Scenario labels for
task legitimacy and hazard are evaluator annotations, not trusted agent disclosures.

| Claim | Evidence a deployer must supply | Included here |
|---|---|---|
| Subdelegation does not inflate resources | Concurrent sibling-spend tests; ledger reconciliation | Serialized budget tests and traces |
| Revocation reaches dependents | Descendant and pending-action rejection tests | Depth 1/3 and queue fixture |
| Minority access survives relay failure | Intake receipt independent of representative | Injected suppression with direct delivery |
| Review preserves useful work | False-report cost and unrelated-work outcomes | Delay sweep and auxiliary actions |
| Every effect is checked | Tool/credential inventory; independent boundary tests | Full mediation is a precondition |
| Evidence survives actor compromise | External witness, custody and complete effect inventory | File hashes only; no custody guarantee |

## Adoption boundary

Begin with a single bounded workflow and one broker-owned resource ledger. Map all
effectful tools, including writes that later influence other agents. Run the supplied
counterexamples against the real interfaces in an isolated test environment. Add
authenticated identities, transactional accounting, external event retention and actual
review duty coverage before relying on the protocol operationally. Test the loss of
each component. The simulator is an acceptance-test starting point, not certification.

Professional SaaS could expose accounting, filing, contracts or procurement through
these interfaces. This is a design opportunity, not a market forecast. A service must
verify the specific power invoked rather than treating organizational identity as
unlimited authority. Legal incorporation alone would not enforce any of these limits.
