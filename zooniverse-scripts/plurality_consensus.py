#!/usr/bin/python

import sys
import csv
import math
import random
import operator

def compare_by_classification(a,b):
    return cmp(a[0],b[0])

def get_species_counts(scals):
    spp = list()
    for cl in scals:
        if cl[0][10] != "": # ignore blanks
            spp.append(len(cl))
        else:
            spp.append(0)
    return spp

def tally_spp_votes(subject):
    vote_table = {}
    for entry in subject:
        spp = entry[10]
        if spp != "": # ignore blanks
            # already in table
            if spp in vote_table:
                vote_table[spp] = vote_table[spp] + 1
            # not in table yet
            else:
                vote_table[spp] = 1
    return vote_table

def calculate_pielou(nlist):
    if len(nlist)<2:
        return 0 
    # denominator
    lnS = math.log(len(nlist))
    # numerator
    sumlist = sum(nlist)
    plist = [float(n)/sumlist for n in nlist]
    plnplist = [n * math.log(n) for n in plist]
    sumplnp = -sum(plnplist)
    return sumplnp/lnS    

def choose_winners(numwin,sppvotes):
    # sort by votes
    sorted_sppvotes = sorted(sppvotes.iteritems(),
                             key=operator.itemgetter(1),
                             reverse=True)
    winners = sorted_sppvotes[0:numwin]

    # check for ties
    if len(sorted_sppvotes) > numwin:
        if sorted_sppvotes[numwin-1][1] == sorted_sppvotes[numwin][1]:
            votes = sorted_sppvotes[numwin-1][1]
            ties = []
            # get all the tied species
            for spp in sorted_sppvotes:
                if spp[1] == votes:
                    ties.append(spp)
            # choose one at random
            tiewinner = random.choice(ties)
            winners[numwin-1] = tiewinner

    return winners

def calculate_num_animals(noa):
    
    nums = []
    tens = []
    meds = []
    many = []
    for ea in noa:
        if len(ea)==1:
            nums.append(ea)
        elif ea=="10":
            tens.append(ea)
        elif ea=="11-50":
            meds.append(ea)
        else:
            many.append(ea)
    nums.sort()
    sorted_list = nums + tens + meds + many
    # round up (gotta choose one or the other)
    medind = int(math.ceil((len(sorted_list)+1)/2)-1)
    return [sorted_list[0],sorted_list[medind],sorted_list[-1]]

def calculate_TF_perc(items):
    ctr = 0
    for ea in items:
        if ea=="true":
           ctr = ctr + 1
    return float(ctr) / len(items)

def winner_info(sppwinners,numclass,numblanks,subject):
    info = []
    for spp in sppwinners:
        # fraction people who voted for this spp
        fracpeople = float(spp[1]) / (numclass-numblanks)
        # look through votes
        noa = []
        stand = []
        rest = []
        move = []
        eat = []
        interact = []
        baby = []

        for line in subject:
            if line[10]==spp[0]:
                noa.append(line[11])
                stand.append(line[12])
                rest.append(line[13])
                move.append(line[14])
                eat.append(line[15])
                interact.append(line[16])
                baby.append(line[17])
        
        # number of animals
        numanimals = calculate_num_animals(noa)
        
        # true-false questions
        stand_frac = calculate_TF_perc(stand)
        rest_frac = calculate_TF_perc(rest)
        move_frac = calculate_TF_perc(move)
        eat_frac = calculate_TF_perc(eat)
        interact_frac = calculate_TF_perc(interact)
        baby_frac = calculate_TF_perc(baby)
        
        # save it all
        info.append([spp[0],spp[1],fracpeople] + numanimals +
                    [stand_frac,rest_frac,move_frac,eat_frac,
                     interact_frac,baby_frac])
        
    return info
    
def process_subject(subject,filewriter):
    # sort by classification
    subject.sort(compare_by_classification)

    # then create 2D list to deal with them
    scals = list()
    lastclas = ""
    subcl = list()
    for entry in subject:
        if entry[0] == lastclas:
            subcl.append(entry)
        else:
            if len(subcl)>0:
                scals.append(subcl)
            subcl = [entry]
            lastclas = entry[0]
    scals.append(subcl)

    # count total number of classifications done
    numclass = len(scals)

    # count unique species per classification, ignoring blanks
    sppcount = get_species_counts(scals)

    # count and remove the blanks
    numblanks = sppcount.count(0)
    sppcount_noblanks = list(value for value in sppcount if value != 0)

    # take median (rounded up)
    sppcount_noblanks.sort()
    medianspp = sppcount_noblanks[int(math.ceil((len(sppcount_noblanks)+1)/2)-1)]

    # count up votes for each species
    sppvotes = tally_spp_votes(subject)

    # total number of (non-blank) votes
    totalvotes = sum(sppvotes.values())

    # Pielou evenness index
    pielou = calculate_pielou(sppvotes.values())

    # choose winners
    sppwinners = choose_winners(medianspp,sppvotes)

    # get winner info
    winnerstats = winner_info(sppwinners,numclass,numblanks,subject)

    # output
    # Fixed: grab last retirement reason instead of first (github issue #65)
    basic_info = (subject[0][2:4] + [subject[-1][5]] + subject[0][6:10] +
                  [numclass,totalvotes,numblanks,pielou,medianspp])
    ctr = 1
    for winner in winnerstats:
        spp_info = basic_info + [ctr] + winner
        filewriter.writerow(spp_info)
        ctr = ctr + 1



# --- MAIN ---

# get file names from command prompt
if len(sys.argv) < 3 :
    print ("format: plurality_consensus.py <infile> <outfile>")
    exit(1)

infilename = sys.argv[1]
outfilename = sys.argv[2]

infile = open(infilename, 'rb')
filereader = csv.reader(infile, delimiter=',', quotechar='"')

outfile = open(outfilename,'wb')
filewriter = csv.writer(outfile, delimiter=',', quotechar='"',
                        quoting=csv.QUOTE_NONE)

# header line
filereader.next()

filewriter.writerow(["subject_zooniverse_id","capture_event_id","retire_reason",
                     "season","site","roll","filenames",
                     "number_of_classifications","number_of_votes",
                     "number_of_blanks","pielou_evenness",
                     "number_of_species","species_index",
                     "species","species_votes","species_fraction_support",
                     "species_count_min","species_count_median","species_count_max",
                     "species_fraction_standing","species_fraction_resting",
                     "species_fraction_moving","species_fraction_eating",
                     "species_fraction_interacting","species_fraction_babies"])


# sort the classifications by subject
sortedclass = sorted(filereader, key=operator.itemgetter(2))

# go through the subjects one by one
lastsubject = sortedclass[0][2]
subjectlines = []
for entry in sortedclass:
    subject = entry[2]
    if subject == lastsubject:
        subjectlines.append(entry)
    else:
        process_subject(subjectlines,filewriter)
        subjectlines = [entry]
        lastsubject = subject
process_subject(subjectlines,filewriter)
        
        


infile.close()
outfile.close()
