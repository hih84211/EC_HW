#
# Main.py -- Solution to HW1 w/o using OO or classes
#

import optparse
import sys
import yaml
       
#
# Main entry point
#
def main(argv=None):
    if argv is None:
        argv = sys.argv
        
    try:
        #
        # get command-line options
        #
        parser = optparse.OptionParser()
        parser.add_option("-i", "--inputFile", action="store", dest="inputFileName", help="input filename", default=None)
        parser.add_option("-o", "--outputFile", action="store", dest="outputFileName", help="output filename", default=None)
        parser.add_option("-q", "--quiet", action="store_true", dest="quietMode", help="quiet mode", default=False)
        (options, args) = parser.parse_args(argv)
        
        #validate command-line options
        #
        if options.inputFileName is None:
            raise Exception("Must specify input file name using -i or --inputFile option.")
        if options.outputFileName is None:
            raise Exception("Must specify output file name using -o or --outputFile option.")

        
        #read the YAML input config file
        #
        infile=open(options.inputFileName,'r')
        yml_cfg=yaml.safe_load(infile)
        infile.close()
        
        #get EC configuration dict
        #
        if 'EC_Engine' in yml_cfg:
            ec_cfg=yml_cfg['EC_Engine']
        else:
            raise Exception('Config file is missing EC_Engine section!')
                
        #verify the ec cfg data
        # 1. mandatory params must exist
        # 2. all data must have correct types

        #first let's make a lookup table (dict) with param names,
        #     expected types, mandatory/optional flag (True/False)
        ec_options={'populationSize': (int,True),
                    'generationCount': (int,True),
                    'randomSeed': (int,False),
                    'evaluatorType': (str,True),
                    'jobName': (str,False),
                    'scalingParam': (float,False)}
        
        #next let's iterate (loop) over the ec_cfg data and verify.
        # (Accumulate info about type and parameter errors in errorDict)
        errorDict={'missingParams':[], 'incorrectTypes':[]}
        for opt in ec_options:
            if opt in ec_cfg:
                optval=ec_cfg[opt]
 
                #verify parameter type
                if type(optval) != ec_options[opt][0]:
                    errorDict['incorrectTypes'].append(opt)
            else:
                if ec_options[opt][1]:
                    errorDict['missingParams'].append(opt)
                    
        #write errorDict to outputFile
        # (first sort lists alphabetically)
        for val in errorDict.values():
            val.sort()
        yaml.dump(errorDict,open(options.outputFileName,'w'))

        if not options.quietMode:   
            print(ec_cfg)    
            print('Main Completed!')    
    
    except Exception as info:
        if 'options' in vars() and not options.quietMode:
            raise   #re-raise Exception, interpreter shows stack trace
        else:
            print(info)   

if __name__ == '__main__':
    main()
    #main(['-i','hw1_good_input1.cfg','-o','error_log.txt'])
    