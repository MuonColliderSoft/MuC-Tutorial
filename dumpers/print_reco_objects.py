import argparse
import math
import pyLCIO

X, Y, Z = 0, 1, 2
TRACK_COL = "SiTracks"
CLUSTER_COL = "PandoraClusters"
PFO_COL = "PandoraPFOs"
BFIELD = 5.0

# https://bib-pubdb1.desy.de/record/81214/files/LC-DET-2006-004%5B1%5D.pdf
FACTOR = 3e-4


def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", required=True, type=str, help="Input LCIO file")
    parser.add_argument(
        "-n", required=False, type=int, help="Number of events to process"
    )
    return parser.parse_args()


def main():
    ops = options()
    print(f"Reading file {ops.i}")

    reader = pyLCIO.IOIMPL.LCFactory.getInstance().createLCReader()
    reader.open(ops.i)

    for i_event, event in enumerate(reader):

        if ops.n is not None and i_event >= ops.n:
            break

        tracks = get_collection(event, TRACK_COL)
        clusters = get_collection(event, CLUSTER_COL)
        pfos = get_collection(event, PFO_COL)

        for i_track, track in enumerate(tracks):
            name = "track"
            omega, tan_lambda, phi = (
                track.getOmega(),
                track.getTanLambda(),
                track.getPhi(),
            )
            theta = (math.pi / 2) - math.atan(tan_lambda)
            pt = BFIELD * FACTOR / abs(omega)
            pz = pt * tan_lambda
            p = math.sqrt(pt * pt + pz * pz)
            chi2, ndf = track.getChi2(), track.getNdf()
            descr = f"p = {p:5.1f} theta = {theta:5.2f} phi = {phi:5.2f} chi2/ndf = {chi2:5.2f}/{ndf:5.2f}"
            print(f"Event {i_event} {name:8} {i_track} {descr}")

        for i_clus, clus in enumerate(clusters):
            name = "cluster"
            energy, theta, phi = clus.getEnergy(), clus.getITheta(), clus.getIPhi()
            descr = f"e = {energy:5.1f} theta = {theta:5.2f} phi = {phi:5.2f}"
            print(f"Event {i_event} {name:8} {i_clus} {descr}")

        for i_pfo, pfo in enumerate(pfos):
            name = "PFO"
            momentum, energy = pfo.getMomentum(), pfo.getEnergy()
            pdg, charge = pfo.getType(), pfo.getCharge()
            px, py, pz = momentum[X], momentum[Y], momentum[Z]
            theta, phi = get_theta(px, py, pz), get_phi(px, py)
            descr = f"e = {energy:5.1f} theta = {theta:5.2f} phi = {phi:5.2f} pdg = {pdg:4} charge = {charge}"
            print(f"Event {i_event} {name:8} {i_pfo} {descr}")

        print("")


def get_theta(px, py, pz):
    pt = math.sqrt(px**2 + py**2)
    return math.atan2(pt, pz)


def get_phi(px, py):
    return math.atan2(py, px)


def get_collection(event, name):
    names = event.getCollectionNames()
    if name in names:
        return event.getCollection(name)
    return []

if __name__ == "__main__":
    main()
