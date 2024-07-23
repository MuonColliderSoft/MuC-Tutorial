import argparse
import pyLCIO

X, Y, Z = 0, 1, 2

CAL_COLLECTIONS = [
    "ECALBarrelHits",
    "ECALEndcapHits",
    "HCALBarrelHits",
    "HCALEndcapHits",
]


def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", required=True, type=str, help="Input LCIO file")
    parser.add_argument(
        "-n", required=False, type=int, help="Number of events to process"
    )
    parser.add_argument(
        "--nhits",
        default=10,
        type=int,
        help="Max number of hits to dump for each collection",
    )
    return parser.parse_args()


def main():
    ops = options()
    print(f"Reading file {ops.i}")
    print(f"*** Printing at most {ops.nhits} hits for each collection ***")

    reader = pyLCIO.IOIMPL.LCFactory.getInstance().createLCReader()
    reader.open(ops.i)

    for i_event, event in enumerate(reader):

        if ops.n is not None and i_event >= ops.n:
            break

        cols = {}
        for col in CAL_COLLECTIONS:
            cols[col] = event.getCollection(col) or []

        print(f"Event {i_event} has")
        for col in cols:
            print(f"  {len(cols[col]):5} hits in {col}")

        for col_name in CAL_COLLECTIONS:
            for i_hit, hit in enumerate(cols[col_name]):
                if i_hit >= ops.nhits:
                    break
                position = hit.getPosition()
                line = f"CalorimeterHit {i_hit} in {col_name}: Energy {hit.getEnergy():.3f} Position ({position[X]:6.1f}, {position[Y]:6.1f}, {position[Z]:6.1f})"
                print(line)

        print("")


if __name__ == "__main__":
    main()
