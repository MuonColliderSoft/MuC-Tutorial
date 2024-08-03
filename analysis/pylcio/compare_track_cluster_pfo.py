import argparse
import glob
import math
import os
import pyLCIO

import ROOT
ROOT.gROOT.SetBatch()

DATA_PATH = "/ospool/uc-shared/project/muoncollider/tutorial2024/electronGun_E_50_250"
PDF = "electrons.pdf"

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

    h2d = get_histograms()
    fill_histograms(h2d)
    plot_histograms(h2d)

def fill_histograms(h2d):

    print("Opening slcio files ...")
    reader = pyLCIO.IOIMPL.LCFactory.getInstance().createLCReader()
    reader.setReadCollectionNames(COLS)

    filenames = get_files()
    for i_filename, filename in enumerate(filenames):

        print(f"Analyzing {filename} ({i_filename} / {len(filenames)})")
        reader.open(filename)

        for event in reader:
            mcps = get_collection(event, MCPARTICLES)
            trks = get_collection(event, TRACKS)
            clus = get_collection(event, CLUSTERS)
            pfos = get_collection(event, PFOS)
            mcp_p, mcp_theta, mcp_phi = get_leading_item(mcps)
            trk_p, trk_theta, trk_phi = get_leading_item(trks)
            clu_p, clu_theta, clu_phi = get_leading_item(clus)
            pfo_p, pfo_theta, pfo_phi = get_leading_item(pfos)
            h2d["mcp_vs_clu_p"].Fill(mcp_p, clu_p)
            h2d["mcp_vs_trk_p"].Fill(mcp_p, trk_p)
            h2d["mcp_vs_pfo_p"].Fill(mcp_p, pfo_p)

        reader.close()


def plot_histograms(h2d):
    rootlogon()
    for i_hist, hist in enumerate(h2d.values()):
        canv = ROOT.TCanvas(f"canv_{i_hist}", "canv_{i_hist}", 800, 800)
        canv.Draw()
        stylize(hist)
        hist.Draw("colzsame")
        suff = suffix(i_hist, len(h2d))
        canv.Print(PDF + suff, "pdf")


def suffix(counter, total):
    if total == 1:
        return ""
    else:
        if counter == 0:
            return "("
        elif counter == total - 1:
            return ")"
        else:
            return ""
        

def get_histograms():
    h2d = {}
    h2d["mcp_vs_clu_p"] = ROOT.TH2D("mcp_vs_clu_p", ";True momentum [GeV];Cluster energy [GeV];Events", 100, 0, 300, 100, 0, 300)
    h2d["mcp_vs_trk_p"] = ROOT.TH2D("mcp_vs_trk_p", ";True momentum [GeV];Track momentum [GeV];Events", 100, 0, 300, 100, 0, 300)
    h2d["mcp_vs_pfo_p"] = ROOT.TH2D("mcp_vs_pfo_p", ";True momentum [GeV];PFO energy [GeV];Events", 100, 0, 300, 100, 0, 300)
    return h2d
        

def get_files(num=-1):
    files = sorted(glob.glob(DATA_PATH + "/*.slcio"))
    if num != -1:
        files = files[:num]
    print(f"Found {len(files)} files")
    return files


def get_leading_item(col):
    if not col:
        return 0, 0, 0
    p, theta, phi = 0, 0, 0
    for obj in col:
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


def rootlogon():
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetPadTickX(1)
    ROOT.gStyle.SetPadTickY(1)
    ROOT.gStyle.SetPaintTextFormat(".2f")
    ROOT.gStyle.SetTextFont(42)
    ROOT.gStyle.SetFillColor(10)
    # ROOT.gStyle.SetPalette(ROOT.kCherry)
    # ROOT.TColor.InvertPalette()
    ROOT.gStyle.SetPadTopMargin(0.06)
    ROOT.gStyle.SetPadRightMargin(0.19)
    ROOT.gStyle.SetPadBottomMargin(0.10)
    ROOT.gStyle.SetPadLeftMargin(0.15)


def stylize(hist):
    size = 0.04
    hist.SetLineWidth(2)
    hist.GetXaxis().SetTitleSize(size)
    hist.GetXaxis().SetLabelSize(size)
    hist.GetYaxis().SetTitleSize(size)
    hist.GetYaxis().SetLabelSize(size)
    hist.GetZaxis().SetTitleSize(size)
    hist.GetZaxis().SetLabelSize(size)
    hist.GetXaxis().SetTitleOffset(1.2)
    hist.GetYaxis().SetTitleOffset(1.6)
    hist.GetZaxis().SetTitleOffset(1.6)
    hist.GetZaxis().SetLabelOffset(0.003)
    hist.GetXaxis().SetNdivisions(505)


def get_collection(event, name):
    names = event.getCollectionNames()
    if name in names:
        return event.getCollection(name)
    return []

if __name__ == "__main__":
    main()
