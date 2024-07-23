import argparse
import pyLCIO

X, Y, Z = 0, 1, 2

RELATIONS = "CaloHitsRelations"
ALL_CAL_COLLECTIONS = [
    "ECALBarrelHits",
    "ECALEndcapHits",
    "HCALBarrelHits",
    "HCALEndcapHits",
    "ECalBarrelCollection",
    "ECalEndcapCollection",
    "HCalBarrelCollection",
    "HCalEndcapCollection",
]

def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", required=True, type=str, help="Input LCIO file")
    parser.add_argument(
        "-n", required=False, type=int, help="Number of events to process"
    )
    parser.add_argument("--nhits", default=10, type=int, help="Max number of hits to dump for each collection")
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
        for col in ALL_CAL_COLLECTIONS:
            cols[col] = event.getCollection(col) or []
        rels = event.getCollection(RELATIONS) or []

        for i_rel, rel in enumerate(rels):

            if i_rel >= ops.nhits:
                break

            digi_hit, sim_hit = rel.getFrom(), rel.getTo()

            def which_container_contains(hit):
                return ",".join([col for col in cols if hit in cols[col]])
            digi_col = which_container_contains(digi_hit)
            sim_col = which_container_contains(sim_hit)

            digi_position = digi_hit.getPosition()
            digi_x, digi_y, digi_z = digi_position[X], digi_position[Y], digi_position[Z]
            n_sim_contrib = sim_hit.getNMCContributions()

            digi_print = f"Hit with x, y, z = {digi_x:7.1f}, {digi_y:7.1f}, {digi_z:7.1f} ({digi_col})"
            sim_print = f"sim hit with {n_sim_contrib} MC contributions ({sim_col})"

            print(f"Event {i_event} relation {i_rel}: {digi_print} linked to {sim_print}")
            
        print("")


if __name__ == "__main__":
    main()
