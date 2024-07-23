import argparse
import pyLCIO

X, Y, Z = 0, 1, 2


def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", required=True, help="Input LCIO file")
    parser.add_argument(
        "-n", required=False, type=int, help="Number of events to process"
    )
    return parser.parse_args()


def main():
    ops = options()

    reader = pyLCIO.IOIMPL.LCFactory.getInstance().createLCReader()
    reader.open(ops.i)

    for i_event, event in enumerate(reader):

        if ops.n is not None and i_event >= ops.n:
            break

        names = event.getCollectionNames()
        if "MCParticle" not in names:
            raise Exception(f"No MCParticle collection found in event {i_event}")

        mcparticles = event.getCollection("MCParticle")
        for i_mcparticle, mcparticle in enumerate(mcparticles):
            momentum = mcparticle.getMomentum()
            vertex = mcparticle.getVertex()
            line = ""
            line += f"Event {i_event}"
            line += f" MCParticle {i_mcparticle}"
            line += f" PDG: {mcparticle.getPDG():4}"
            line += f" Energy: {mcparticle.getEnergy():.3f}"
            line += f" Momentum (X, Y, Z): {momentum[X]:8.3f}, {momentum[Y]:8.3f}, {momentum[Z]:8.3f}"
            line += f" Vertex (X, Y, Z): {vertex[X]:4.1f}, {vertex[Y]:4.1f}, {vertex[Z]:4.1f}"
            line += f" Charge: {mcparticle.getCharge()}"
            line += f" Mass: {mcparticle.getMass():.5f}"
            line += f" Time: {mcparticle.getTime()}"
            line += f" Generator Status: {mcparticle.getGeneratorStatus()}"
            print(line)


if __name__ == "__main__":
    main()
