#Alex Muralles
#May 25, 2018
#McManus Lab, Mellon College of Science
import sys

###############################################################################
                               #lysCheck.py#
###############################################################################


def lysCheck(filename, minimumSize):
    noFile = open("noLys.txt", "w")
    total = 0
    yes = 0
    no = 0
    geneFile = open(filename)
    gene = ""
    buffer = ""
    for geneLine in geneFile.readlines():
        if geneLine[0] == ">":
            if ("K" in buffer and len(buffer) > minimumSize):
                yes = yes + 1
                total = total + 1
            elif (len(buffer) > minimumSize):
                no = no + 1
                total = total + 1
                noFile.write(geneLine)
                noFile.write("\n")
            buffer = ""
            gene = geneLine
        else:
            buffer = buffer + geneLine
    no = no - 1
    total = total - 1
    percent = (float(yes)/float(total)) * 100
    return (total,percent)


inFile = sys.argv[1]
inLen = int(sys.argv[2])
total1, percent1 = lysCheck(inFile, inLen)
print("when considering peptides of lenth " + str(inLen) + " AA or greater....")
print("Of the " + str(total1) + " proteins provided, " + str(percent1) + "%  of them contain Lysine")
print("The proteins that don't have Lys (and their fasta headers) are stored in noLys.txt (in the same directory you are in)")
