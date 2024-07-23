import argparse
import pyLCIO

X, Y, Z = 0, 1, 2

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

    for i_event, event in enumerate(reader):

        if ops.n is not None and i_event >= ops.n:
            break

        cols = {}
        cols["MCParticle"] = event.getCollection("MCParticle") or []
        for col in CAL_COLLECTIONS:
            cols[col] = event.getCollection(col) or []

        print(f"Event {i_event} has")
        for col in cols:
            print(f"  {len(cols[col]):5} hits in {col}")

        for i_mcparticle, mcparticle in enumerate(cols["MCParticle"]):
            if i_mcparticle >= ops.nhits:
                break
            momentum = mcparticle.getMomentum()
            vertex = mcparticle.getVertex()
            line = ""
            line += f"MCParticle {i_mcparticle}"
            line += f" PDG: {mcparticle.getPDG():4}"
            line += f" Energy: {mcparticle.getEnergy():7.3f}"
            line += f" Momentum (X, Y, Z): {momentum[X]:8.3f}, {momentum[Y]:8.3f}, {momentum[Z]:8.3f}"
            line += f" Vertex (X, Y, Z): {vertex[X]:4.1f}, {vertex[Y]:4.1f}, {vertex[Z]:4.1f}"
            line += f" Charge: {mcparticle.getCharge()}"
            line += f" Mass: {mcparticle.getMass():.5f}"
            line += f" Time: {mcparticle.getTime():.5f}"
            line += f" Generator Status: {mcparticle.getGeneratorStatus()}"
            print(line)

        for col_name in CAL_COLLECTIONS:
            for i_hit, hit in enumerate(cols[col_name]):
                if i_hit >= ops.nhits:
                    break
                position = hit.getPosition()
                line = f"SimCalorimeterHit {i_hit} in {col_name}: Energy {hit.getEnergy():.3f} Position ({position[X]:6.1f}, {position[Y]:6.1f}, {position[Z]:6.1f})"
                print(line)

        print("")


if __name__ == "__main__":
    main()
