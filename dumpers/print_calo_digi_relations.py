import argparse
import pyLCIO

X, Y, Z = 0, 1, 2

RELATIONS = [
    "EcalBarrelRelationsSimDigi",
    "EcalEndcapRelationsSimDigi",
    "HcalBarrelRelationsSimDigi",
    "HcalEndcapRelationsSimDigi",
]

DIGI_COLLECTIONS = [
    "EcalBarrelCollectionDigi",
    "EcalEndcapCollectionDigi",
    "HcalBarrelCollectionDigi",
    "HcalEndcapCollectionDigi",
]

SIM_COLLECTIONS = [
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

        for rel_name, digi_name, sim_name in zip(
            RELATIONS,
            DIGI_COLLECTIONS,
            SIM_COLLECTIONS,
        ):

            rels = get_collection(event, rel_name)

            for i_rel, rel in enumerate(rels):

                if i_rel >= ops.nhits:
                    break

                digi_hit, sim_hit = rel.getFrom(), rel.getTo()

                digi_position = digi_hit.getPosition()
                digi_x, digi_y, digi_z = (
                    digi_position[X],
                    digi_position[Y],
                    digi_position[Z],
                )
                n_sim_contrib = sim_hit.getNMCContributions()

                digi_print = f"Hit with x, y, z = {digi_x:7.1f}, {digi_y:7.1f}, {digi_z:7.1f} ({digi_name})"
                sim_print = (
                    f"sim hit with {n_sim_contrib} MC contributions ({sim_name})"
                )

                print(
                    f"Event {i_event} relation {i_rel}: {digi_print} linked to {sim_print}"
                )

        print("")


def get_collection(event, name):
    names = event.getCollectionNames()
    if name in names:
        return event.getCollection(name)
    return []


if __name__ == "__main__":
    main()
