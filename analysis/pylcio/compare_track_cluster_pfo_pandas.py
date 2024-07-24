import argparse
import glob
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pyLCIO

DATA_PATH = "/ospool/uc-shared/project/futurecolliders/data/fmeloni/DataMuC_MuColl10_v0A/v2/reco/pionGun_pT_50_250"
PDF = "plots.pdf"

MCPARTICLES = "MCParticle"
CLUSTERS = "PandoraClusters"
TRACKS = "SiTracks_Refitted"
PFOS = "PandoraPFOs"

COLS = [
    MCPARTICLES,
    CLUSTERS,
    TRACKS,
    PFOS,
]

X, Y, Z = 0, 1, 2
BFIELD = 5
FACTOR = 3e-4

def main():

    df = get_dataframe()
    plot_dataframe(df)

def get_dataframe():

    data = {
        "mcp_p": [],
        "trk_p": [],
        "clu_p": [],
        "pfo_p": [],
    }

    for event in get_events():
        mcp_p, mcp_theta, mcp_phi = get_leading_item(event, MCPARTICLES)
        trk_p, trk_theta, trk_phi = get_leading_item(event, TRACKS)
        clu_p, clu_theta, clu_phi = get_leading_item(event, CLUSTERS)
        pfo_p, pfo_theta, pfo_phi = get_leading_item(event, PFOS)
        data["mcp_p"].append(mcp_p)
        data["trk_p"].append(trk_p)
        data["clu_p"].append(clu_p)
        data["pfo_p"].append(pfo_p)

    return pd.DataFrame(data)

def get_events():

    print("Opening slcio files ...")

    for i_filename, filename in enumerate(get_files()):
        print(f"Analyzing {filename} ({i_filename})")
        reader = pyLCIO.IOIMPL.LCFactory.getInstance().createLCReader()
        reader.setReadCollectionNames(COLS)
        reader.open(filename)

        for event in reader:
            yield event

        reader.close()

def plot_dataframe(df):
    print(df)
    fig, ax = plt.subplots(figsize=(13, 4), ncols=3)
    objects = ["Cluster", "Track", "PFO"]
    measures = ["energy", "momentum", "energy"]
    prefixs = ["clu", "trk", "pfo"]
    bins = np.linspace(0, 1000, 100)
    for i, (obj, measure, prefix) in enumerate(zip(objects, measures, prefixs)):
        ax[i].set_xlabel("True momentum [GeV]")
        ax[i].set_ylabel(f"{obj} {measure} [GeV]")
        ax[i].hist2d(df["mcp_p"], df[f"{prefix}_p"], bins=bins, cmap="plasma", cmin=0.1)
    plt.savefig("plots.df.pdf")
        
def get_files(num=-1):
    files = sorted(glob.glob(DATA_PATH + "/*.slcio"))
    if num != -1:
        files = files[:num]
    print(f"Found {len(files)} files")
    return files

def get_leading_item(event, col_name):
    col = event.getCollection(col_name) or []
    if not col:
        return 0, 0, 0
    p, theta, phi = 0, 0, 0
    for obj in col:
        if isinstance(obj, pyLCIO.EVENT.MCParticle) and obj.getGeneratorStatus() != 1:
            continue
        this_p, this_theta, this_phi = get_properties(obj)
        if this_p > p:
            p, theta, phi = this_p, this_theta, this_phi
    return p, theta, phi

def get_properties(obj):
    if sum([isinstance(obj, pyLCIO.EVENT.MCParticle),
            isinstance(obj, pyLCIO.EVENT.Track),
            isinstance(obj, pyLCIO.EVENT.Cluster),
            isinstance(obj, pyLCIO.EVENT.ReconstructedParticle),
            ]) > 1:
        raise Exception("This object is too many things!!")

    if isinstance(obj, pyLCIO.EVENT.Track):
        omega, tan_lambda, phi = (
            obj.getOmega(),
            obj.getTanLambda(),
            obj.getPhi(),
        )
        theta = (math.pi / 2) - math.atan(tan_lambda)
        pt = BFIELD * FACTOR / abs(omega)
        pz = pt * tan_lambda
        p = math.sqrt(pt * pt + pz * pz)

    elif isinstance(obj, pyLCIO.EVENT.Cluster):
        p, theta, phi = obj.getEnergy(), obj.getITheta(), obj.getIPhi()

    elif any([isinstance(obj, pyLCIO.EVENT.ReconstructedParticle),
              isinstance(obj, pyLCIO.EVENT.MCParticle),
              ]):
        momentum, energy = obj.getMomentum(), obj.getEnergy()
        px, py, pz = momentum[X], momentum[Y], momentum[Z]
        theta, phi = get_theta(px, py, pz), get_phi(px, py)
        p = energy

    else:
        raise Exception(f"I dont recognize {obj}")

    return p, theta, phi

def get_theta(px, py, pz):
    pt = math.sqrt(px**2 + py**2)
    return math.atan2(pt, pz)

def get_phi(px, py):
    return math.atan2(py, px)

if __name__ == "__main__":
    main()
