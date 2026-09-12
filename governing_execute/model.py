"""Deterministic, serialized authorization model; identity and time are trusted inputs."""
from dataclasses import dataclass, field

REGIMES = ("log", "local", "hierarchy", "review")


@dataclass
class Grant:
    name: str
    parent: str | None
    depth: int
    budget: int
    expires: int
    permissions: frozenset[str]
    valid_lineage: bool = True
    revoked: bool = False
    own_spent: int = 0
    subtree_spent: int = 0


@dataclass
class World:
    regime: str
    max_depth: int
    budget: int = 100
    nodes: dict = field(default_factory=dict)
    events: list = field(default_factory=list)
    frozen: set = field(default_factory=set)
    input_available: bool = True
    reports: dict = field(default_factory=dict)
    pending: dict = field(default_factory=dict)

    def __post_init__(self):
        if self.regime not in REGIMES or self.max_depth < 1 or self.budget < 0:
            raise ValueError("invalid world configuration")
        self.nodes["root"] = Grant("root", None, 0, self.budget, 12,
                                   frozenset({"work", "aux"}))

    @property
    def hierarchical(self):
        return self.regime in ("hierarchy", "review")

    def record(self, tick, kind, **fields):
        event = dict(seq=len(self.events), tick=tick, kind=kind, **fields)
        self.events.append(event)
        return event

    def lineage(self, name):
        result = []
        while name is not None:
            result.append(self.nodes[name])
            name = self.nodes[name].parent
        return result

    def delegate(self, tick, parent, child, budget, expires, permissions):
        if not isinstance(budget, int) or isinstance(budget, bool) or budget < 0:
            raise ValueError("budget must be a nonnegative integer")
        if child in self.nodes or parent not in self.nodes:
            return self.record(tick, "delegate", child=child, accepted=False,
                               violations=["identity"], reason="identity")
        p = self.nodes[parent]
        permissions = frozenset(permissions)
        violations = []
        if p.depth + 1 > self.max_depth:
            violations.append("depth")
        if not permissions <= p.permissions:
            violations.append("scope")
        if budget > p.budget:
            violations.append("budget_attenuation")
        if expires > p.expires or expires <= tick:
            violations.append("expiry_attenuation")
        if any(n.revoked or tick >= n.expires or not n.valid_lineage
               for n in self.lineage(parent)):
            violations.append("inactive_ancestor")
        frozen = self.regime == "review" and bool(permissions & self.frozen)
        accepted = not (self.hierarchical and (violations or frozen))
        if accepted:
            self.nodes[child] = Grant(child, parent, p.depth + 1, budget,
                                      expires, permissions, not violations)
        return self.record(tick, "delegate", parent=parent, child=child,
                           accepted=accepted, violations=violations,
                           reason="frozen" if frozen else ",".join(violations) or "ok")

    def revoke(self, tick, name):
        self.nodes[name].revoked = True
        self.record(tick, "revoke", target=name)

    def reference_violations(self, tick, name, action, cost):
        """Full-mandate scoring, recorded even when a weaker controller ignores it."""
        if name not in self.nodes:
            return ["unknown_grant"]
        chain = self.lineage(name)
        errors = []
        if any(not n.valid_lineage for n in chain):
            errors.append("invalid_lineage")
        if any(n.revoked for n in chain):
            errors.append("revoked")
        if any(tick >= n.expires for n in chain):
            errors.append("expired")
        if any(action not in n.permissions for n in chain):
            errors.append("scope")
        if any(n.subtree_spent + cost > n.budget for n in chain):
            errors.append("aggregate_budget")
        return errors

    def act(self, tick, name, action="work", cost=1, legitimate=True,
            unsafe=False, covered=True, request_id=None):
        if not isinstance(cost, int) or isinstance(cost, bool) or cost < 0:
            raise ValueError("cost must be a nonnegative integer")
        violations = self.reference_violations(tick, name, action, cost)
        reason = "ok"
        if name not in self.nodes:
            reason = "unknown_grant"
        elif action == "work" and not self.input_available:
            reason = "missing_input"  # physical task prerequisite in EVERY arm
        elif covered:
            n = self.nodes[name]
            if self.hierarchical and violations:
                reason = ",".join(violations)
            elif self.regime == "local":
                if n.revoked or tick >= n.expires or action not in n.permissions:
                    reason = "local_permission"
                elif n.own_spent + cost > n.budget:
                    reason = "local_budget"
            if reason == "ok" and self.regime == "review" and action in self.frozen:
                reason = "review_hold"
        accepted = reason == "ok"
        if accepted:
            self.nodes[name].own_spent += cost
            for n in self.lineage(name):
                n.subtree_spent += cost
        return self.record(tick, "action", actor=name, action=action, cost=cost,
                           accepted=accepted, reason=reason, violations=violations,
                           legitimate=legitimate, unsafe=unsafe, covered=covered,
                           request_id=request_id, root_spent=self.nodes["root"].subtree_spent)

    def queue(self, tick, request_id, **action):
        if request_id in self.pending:
            raise ValueError("duplicate pending request")
        self.pending[request_id] = action
        self.record(tick, "queued", request_id=request_id, request=action)

    def execute_pending(self, tick, request_id):
        request = self.pending.pop(request_id)
        return self.act(tick, request_id=request_id, **request)

    def report(self, tick, report_id, kind, delay, suppressed=False):
        if report_id in self.reports or kind not in ("missing_input", "false_alarm", "hazard"):
            raise ValueError("invalid report")
        # Labels are fixture inputs to a scripted reviewer, not worker truth claims.
        delivered = self.regime == "review"
        self.reports[report_id] = dict(kind=kind, submitted=tick,
                                      due=tick + delay if delivered else None,
                                      resolved=None)
        if delivered and kind in ("false_alarm", "hazard"):
            self.frozen.add("work")
        self.record(tick, "report", report_id=report_id, concern=kind,
                    relay_suppressed=suppressed, delivered=delivered,
                    direct_bypass=delivered and suppressed)

    def resolve_due(self, tick):
        for report_id, report in self.reports.items():
            if report["due"] != tick or report["resolved"] is not None:
                continue
            report["resolved"] = tick
            kind = report["kind"]
            if kind == "missing_input":
                self.input_available = True
            elif kind == "hazard":
                # Narrow amendment: work removed throughout the lineage; aux survives.
                for n in self.nodes.values():
                    n.permissions = n.permissions - {"work"}
            # An unresolved second report must retain the hold.
            if not any(r["resolved"] is None and r["due"] is not None and
                       r["kind"] in ("false_alarm", "hazard")
                       for r in self.reports.values()):
                self.frozen.discard("work")
            self.record(tick, "resolution", report_id=report_id, concern=kind,
                        latency=tick-report["submitted"], authority="scripted_human")
