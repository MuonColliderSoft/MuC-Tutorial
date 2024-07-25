import glob
import math
import pyLCIO

import ROOT
ROOT.gROOT.SetBatch()

DATA_PATH = "/ospool/uc-shared/project/muoncollider/tutorial2024/photonGun_E_250_1000"
PDF = "rt.pdf"

MC_PARTICLE = "MCParticle"
ECAL_BARREL_SIM = "ECalBarrelCollection"
ECAL_BARREL_DIG = "EcalBarrelCollectionDigi"
ECAL_BARREL_REL = "EcalBarrelRelationsSimDigi"

COLS = [
    ECAL_BARREL_SIM,
    ECAL_BARREL_DIG,
    ECAL_BARREL_REL,
    MC_PARTICLE,
]

PHOTON = 22
STABLE = 1

def main():
    nlayers = 50
    hist = ROOT.TH2F("rt", ";Sim. MC Contribution Time [ns];Digit Hit R [mm];Sim. MC Contribution Energy [GeV]", 100, 6.5, 8.2, 100, 1880, 2200)
    fill_histogram(hist)
    plot_histogram(hist)


def fill_histogram(hist):
    for event in get_events():
        photon_eta = get_photon_eta(event)
        if abs(photon_eta) > 1.0:
            continue
        print(f"Found photon with eta {photon_eta:.3f}")
        rels = get_collection(event, ECAL_BARREL_REL)
        for i_rel, rel in enumerate(rels):
            digi_hit, sim_hit = rel.getFrom(), rel.getTo()
            digi_r = get_r(digi_hit)
            sim_times, sim_energies = get_times_and_energies(sim_hit)
            for time, energy in zip(sim_times, sim_energies):
                hist.Fill(time, digi_r, energy)
        break


def get_photon_eta(event):
    particles = get_collection(event, MC_PARTICLE)
    for particle in particles:
        if abs(particle.getPDG()) == PHOTON and particle.getGeneratorStatus() == STABLE:
            momentum = particle.getMomentum()
            theta = get_theta(momentum[0], momentum[1], momentum[2])
            return -math.log(math.tan(theta / 2))
    raise Exception("No photon found")


def get_theta(px, py, pz):
    pt = math.sqrt(px**2 + py**2)
    return math.atan2(pt, pz)


def get_r(hit):
    position = hit.getPosition()
    x, y = position[0], position[1]
    return math.sqrt(x**2 + y**2)


def get_times_and_energies(sim_hit):
    nmc = sim_hit.getNMCContributions()
    times = [0] * nmc
    energies = [0] * nmc
    for i in range(nmc):
        times[i] = sim_hit.getTimeCont(i)
        energies[i] = sim_hit.getEnergyCont(i)
    return times, energies


def plot_histogram(hist):
    rootlogon()
    name = hist.GetName()
    canv = ROOT.TCanvas(f"canv_{name}", "canv_{name}", 800, 800)
    canv.Draw()
    stylize(hist)
    hist.SetMinimum(0)
    hist.Draw("colzsame")
    canv.Print(PDF + "(", "pdf")
    canv.SetLogz()
    canv.Print(PDF + ")", "pdf")



def get_collection(event, name):
    names = event.getCollectionNames()
    if name in names:
        return event.getCollection(name)
    return []


def get_events():

    print("Opening slcio files ...")
    filenames = get_files()
    i_event = 0

    for i_filename, filename in enumerate(filenames):
        print(f"Analyzing {filename} ({i_filename})")
        reader = pyLCIO.IOIMPL.LCFactory.getInstance().createLCReader()
        reader.setReadCollectionNames(COLS)
        reader.open(filename)

        for event in reader:
            print(f"Processing event {i_event}")
            i_event += 1
            yield event

        reader.close()


def get_files(num=-1):
    files = sorted(glob.glob(DATA_PATH + "/*.slcio"))
    if num != -1:
        files = files[:num]
    print(f"Found {len(files)} files")
    return files


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
    hist.GetYaxis().SetTitleOffset(1.8)
    hist.GetZaxis().SetTitleOffset(1.6)
    hist.GetZaxis().SetLabelOffset(0.003)
    hist.GetXaxis().SetNdivisions(505)

if __name__ == "__main__":
    main()
