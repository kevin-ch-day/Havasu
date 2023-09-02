import sys, getopt

def main(argv):
    inputfile = ''
    outputfile = ''
    opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])

    for opt, arg in opts:
        
        if opt == '-h': # Help
           print ('test.py -i <inputfile> -o <outputfile>')
           sys.exit()

        elif opt in ("-i", "--ifile"): # Input
            inputfile = arg

        elif opt in ("-o", "--ofile"): # Output
            outputfile = arg
        # if
    # for
    
    print ('Input file is ', inputfile)
    print ('Output file is ', outputfile)
# main

if __name__ == "__main__":
   main(sys.argv[1:])
# if