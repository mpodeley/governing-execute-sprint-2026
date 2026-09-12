"""Trusted test adapter. Administrative operations are harness-only, not worker APIs."""
from governing_execute.model import World


class AblatedWorld(World):
    mode = "reference"

    def reference_violations(self, tick, name, action, cost):
        errors = super().reference_violations(tick, name, action, cost)
        if name not in self.nodes:
            return errors
        own = self.nodes[name]
        if self.mode == "local_accounting":
            errors = [e for e in errors if e != "aggregate_budget"]
            if own.own_spent + cost > own.budget:
                errors.append("local_budget")
        elif self.mode == "stale_ancestry":
            errors = [e for e in errors if e not in ("revoked", "expired")]
            if own.revoked:
                errors.append("revoked")
            if tick >= own.expires:
                errors.append("expired")
        return errors


class Broker:
    def __init__(self, mode="reference"):
        if mode not in ("reference", "local_accounting", "stale_ancestry"):
            raise ValueError(mode)
        self.world = AblatedWorld("review", 3)
        self.world.mode = mode

    def grant(self, tick, parent, child, budget=100, expires=12,
              permissions=("work", "aux")):
        return self.world.delegate(tick, parent, child, budget, expires, permissions)["accepted"]

    def act(self, tick, name, action="work", cost=1):
        return self.world.act(tick, name, action=action, cost=cost)["accepted"]

    def queue(self, tick, request_id, name, cost=10):
        self.world.queue(tick, request_id, name=name, cost=cost)

    def commit(self, tick, request_id):
        return self.world.execute_pending(tick, request_id)["accepted"]

    def revoke(self, tick, name):
        self.world.revoke(tick, name)

    def shorten_expiry(self, tick, name, expires):
        if not tick <= expires <= self.world.nodes[name].expires:
            raise ValueError("administrative amendment must shorten expiry")
        self.world.nodes[name].expires = expires
        self.world.record(tick, "expiry_amendment", target=name, expires=expires)

    def set_input(self, available):
        self.world.input_available = available

    def report(self, tick, kind, delay, suppressed=False):
        self.world.report(tick, "r1", kind, delay, suppressed=suppressed)

    def resolve(self, tick):
        self.world.resolve_due(tick)

    def spent(self, name="root"):
        return self.world.nodes[name].subtree_spent

    def events(self):
        return self.world.events


def reference():
    return Broker()


def local_accounting():
    return Broker("local_accounting")


def stale_ancestry():
    return Broker("stale_ancestry")
