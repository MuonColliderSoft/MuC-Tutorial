import argparse
import pyLCIO
from pyLCIO import EVENT, UTIL

CAL_COLLECTIONS = [
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

    # these are defined in the geometry file ($MUCOLL_GEO)
    system2name = {
        20: "ecal barrel system",
        29: "ecal endcap system",
        10: "hcal barrel system",
        11: "hcal endcap system",
    }

    for i_event, event in enumerate(reader):

        for col_name in CAL_COLLECTIONS:

            collection = get_collection(event, col_name)

            # get encoding, and create decoder
            if collection:
                encoding = collection.getParameters().getStringVal(
                    EVENT.LCIO.CellIDEncoding
                )
                decoder = UTIL.BitField64(encoding)
                print(f"Collection {col_name} has encoding {encoding}")

            for i_hit, hit in enumerate(collection):
                decoder.setValue(
                    (hit.getCellID0() & 0xFFFFFFFF) | (hit.getCellID1() << 32)
                )
                layer = decoder["layer"].value()
                system = decoder["system"].value()
                systemname = system2name[system]
                print(
                    f"Event {i_event} hit {i_hit} is on layer {layer} of {systemname}"
                )
                if i_hit > ops.nhits:
                    break

        print("")


def get_collection(event, name):
    names = event.getCollectionNames()
    if name in names:
        return event.getCollection(name)
    return []


if __name__ == "__main__":
    main()
