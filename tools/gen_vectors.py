# Writes tests/data/*.txt from Python's uuid module, the reference the
# tests compare against. Run from the repo root: python3 tools/gen_vectors.py
import random
import uuid

rng = random.Random(9562)

def name():
    n = rng.choice([0, 1, 5, 55, 56, 63, 64, 65, 119, 120, 200, 1000])
    return "".join(rng.choice("abcdefghijklmnopqrstuvwxyz0123456789.-_/:") for _ in range(n))

with open("tests/data/names.txt", "w") as f:
    f.write("# namespace\tname\tv3\tv5 (from Python's uuid module)\n")
    spaces = [uuid.NAMESPACE_DNS, uuid.NAMESPACE_URL, uuid.NAMESPACE_OID, uuid.NAMESPACE_X500]
    for i in range(400):
        ns = spaces[i % 4] if i < 200 else uuid.UUID(int=rng.getrandbits(128))
        s = name()
        f.write(f"{ns}\t{s}\t{uuid.uuid3(ns, s)}\t{uuid.uuid5(ns, s)}\n")

with open("tests/data/text.txt", "w") as f:
    f.write("# hyphenated\thi\tlo\tversion\tvariant (0 ncs, 1 rfc, 2 microsoft, 3 future)\n")
    for i in range(500):
        u = uuid.UUID(int=rng.getrandbits(128))
        var = {uuid.RESERVED_NCS: 0, uuid.RFC_4122: 1, uuid.RESERVED_MICROSOFT: 2, uuid.RESERVED_FUTURE: 3}[u.variant]
        ver = (u.int >> 76) & 15
        f.write(f"{u}\t{u.int >> 64}\t{u.int & (2**64 - 1)}\t{ver}\t{var}\n")

ALPHA = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
def ulid(n):
    return "".join(ALPHA[(n >> (5 * (25 - k))) & 31] for k in range(26))

with open("tests/data/ulid.txt", "w") as f:
    f.write("# ulid\thyphenated uuid with the same bits\n")
    for i in range(300):
        n = rng.getrandbits(128)
        if i == 0: n = 0
        if i == 1: n = 2**128 - 1
        f.write(f"{ulid(n)}\t{uuid.UUID(int=n)}\n")
