"""Fixed input/output contracts. Never scores the controller's violation labels."""
from importlib import import_module


def factory_from_path(path):
    module, name = path.split(":", 1)
    return getattr(import_module(module), name)


def siblings(b):
    assert b.grant(0, "root", "parent")
    assert b.grant(0, "parent", "a")
    assert b.grant(0, "parent", "b")


def attenuation(b):
    valid = b.grant(0, "root", "a", budget=60, expires=8, permissions=("work",))
    observations = [valid,
        b.grant(1, "a", "scope", budget=60, expires=8, permissions=("aux",)),
        b.grant(1, "a", "budget", budget=61, expires=8, permissions=("work",)),
        b.grant(1, "a", "expiry", budget=60, expires=9, permissions=("work",))]
    observations.append(b.grant(1, "a", "b", budget=60, expires=8, permissions=("work",)))
    observations.append(b.grant(1, "b", "c", budget=60, expires=8, permissions=("work",)))
    observations.append(b.grant(1, "c", "deep", budget=60, expires=8, permissions=("work",)))
    return observations, [True, False, False, False, True, True, False]


def shared_pool(b):
    siblings(b)
    return [b.act(1, "a", cost=60), b.act(2, "b", cost=60), b.spent()], [True, False, 60]


def current_expiry(b):
    siblings(b)
    first = b.act(1, "a", cost=10)
    b.shorten_expiry(2, "parent", 4)
    return [first, b.act(3, "a", cost=10), b.act(4, "a", cost=10), b.spent()], [True, True, False, 20]


def revoked_queue(b):
    siblings(b)
    first = b.act(0, "a", cost=10)
    b.queue(1, "q1", "a")
    b.revoke(2, "parent")
    return [first, b.commit(3, "q1"), b.act(4, "b", cost=10), b.spent()], [True, False, False, 10]


def historical_spend(b):
    siblings(b)
    first = b.act(0, "a", cost=10)
    before = [b.spent(), b.spent("parent"), b.spent("a")]
    b.revoke(2, "parent")
    return [first, before, [b.spent(), b.spent("parent"), b.spent("a")]], [True, [10, 10, 10], [10, 10, 10]]


def direct_intake(b):
    siblings(b)
    b.report(1, "false_alarm", 2, suppressed=True)
    observations = [b.act(1, "a"), b.act(1, "b", action="aux")]
    b.resolve(3)
    observations += [b.act(3, "a"), b.spent()]
    return observations, [False, True, True, 2]


def silence(b):
    siblings(b)
    b.set_input(False)
    b.report(1, "missing_input", 20)
    b.resolve(10)
    return [b.act(10, "a"), b.act(10, "b", action="aux"), b.spent()], [False, True, 1]


def request_binding(b):
    assert b.grant(0, "root", "a", permissions=("work",))
    return [b.act(1, "root", action="aux"), b.act(2, "a", action="aux"), b.act(3, "a"), b.spent()], [True, False, True, 2]


PROBES = (
    ("C1", "Grant attenuation", attenuation),
    ("C2", "Shared sibling pool", shared_pool),
    ("C3", "Current ancestor expiry", current_expiry),
    ("C4", "Revoked queue and sibling", revoked_queue),
    ("C5", "Historical expenditure", historical_spend),
    ("C6", "Direct intake and scoped hold", direct_intake),
    ("C7", "Silence supplies no input", silence),
    ("C8", "Request authority binding", request_binding),
)


def evaluate(factory, adapter):
    rows = []
    for code, title, probe in PROBES:
        broker = factory()
        try:
            observed, expected = probe(broker)
            row = dict(probe=code, title=title, adapter=adapter,
                       observed=observed, expected=expected, passed=observed == expected)
        except Exception as exc:
            row = dict(probe=code, title=title, adapter=adapter, passed=False,
                       error=f"{type(exc).__name__}: {exc}")
        row["events"] = broker.events()
        rows.append(row)
    return rows
