#
# Main.py
#

import optparse
import sys
import yaml


# class EC_Config:
#     """
#     EC_Engine configuration class
#     """
#     # class variables
#     sectionName='EC_Engine'
#      
#     #constructor
#     def __init__(self, inFileName):
#         #init error dict
#         mps='missingParams'
#         its='incorrectTypes'
#         self.errorDict={mps:[], its:[]}
# 
#         #read YAML config and get EC_Engine section
#         ymlcfg=yaml.safe_load(open(inFileName,'r'))
#         eccfg=ymlcfg.get(EC_Config.sectionName,None)
#         if eccfg is None: raise Exception('Missing EC_Engine section in cfg file')
#          
#         #mandatory params
#         self.populationSize=eccfg.get('populationSize',None)
#         if self.populationSize is None: self.errorDict[mps].append('populationSize')
#         elif type(self.populationSize) != int: self.errorDict[its].append('populationSize')
#  
#         self.generationCount=eccfg.get('generationCount',None)
#         if self.generationCount is None: self.errorDict[mps].append('generationCount')
#         elif type(self.generationCount) != int: self.errorDict[its].append('generationCount')
#  
#         self.evaluatorType=eccfg.get('evaluatorType',None)
#         if self.evaluatorType is None: self.errorDict[mps].append('evaluatorType')
#         elif type(self.evaluatorType) != str: self.errorDict[its].append('evaluatorType')
#          
#         #optional params
#         self.randomSeed=eccfg.get('randomSeed',None)
#         if (self.randomSeed != None) and (type(self.randomSeed) != int): self.errorDict[its].append('randomSeed')
#  
#         self.jobName=eccfg.get('jobName',None)
#         if (self.jobName != None) and (type(self.jobName) != str): self.errorDict[its].append('jobName')
#  
#         self.scalingParam=eccfg.get('scalingParam',None)
#         if (self.scalingParam != None) and (type(self.scalingParam) != float): self.errorDict[its].append('scalingParam')
#     
#     def writeLogfile(self,outFileName):
#         #write errorDict to outputFile
#         # (first sort lists alphabetically)
#         for val in self.errorDict.values():
#             val.sort()
#         yaml.dump(self.errorDict,open(outFileName,'w'))  
#         
#     def hasErrors(self):
#         #simple function to check
#         # whether there are any errors
#         for val in self.errorDict.values():
#             #check if any of the error lists have length > 0
#             if len(val) > 0:
#                 return True
#             
#         #if we made it here, no errors    
#         return False
#          
#     #string representation for class data    
#     def __str__(self):
#         return str(yaml.dump(self.__dict__,default_flow_style=False))


class EC_Config:
    """
    EC_Engine configuration class
    """
    # class variables
    sectionName='EC_Engine'
    options={'populationSize': (int,True),
             'generationCount': (int,True),
             'randomSeed': (int,False),
             'evaluatorType': (str,True),
             'jobName': (str,False),
             'scalingParam': (float,False)}
      
    #constructor
    def __init__(self, inFileName):
        #init error dict
        self.errorDict={'missingParams':[], 'incorrectTypes':[]}
         
        #read YAML config and get EC_Engine section
        infile=open(inFileName,'r')
        ymlcfg=yaml.safe_load(infile)
        infile.close()
        eccfg=ymlcfg.get(EC_Config.sectionName,None)
        if eccfg is None: raise Exception('Missing EC_Engine section in cfg file')
          
        #iterate over options
        for opt in EC_Config.options:
            if opt in eccfg:
                optval=eccfg[opt]
  
                #verify parameter type
                if type(optval) != EC_Config.options[opt][0]:
                    self.errorDict['incorrectTypes'].append(opt)
                  
                #create attributes on the fly
                setattr(self,opt,optval)
            else:
                if EC_Config.options[opt][1]:
                    self.errorDict['missingParams'].append(opt)
                else:
                    setattr(self,opt,None)
                     
    def writeLogfile(self,outFileName):
        #write errorDict to outputFile
        # (first sort lists alphabetically)
        for val in self.errorDict.values():
            val.sort()
        yaml.dump(self.errorDict,open(outFileName,'w'))  
         
    def hasErrors(self):
        #simple function to check
        # whether there are any errors
        for val in self.errorDict.values():
            #check if any of the error lists have length > 0
            if len(val) > 0:
                return True
             
        #if we made it here, no errors    
        return False
                   
    #string representation for class data    
    def __str__(self):
        return str(yaml.dump(self.__dict__,default_flow_style=False))
        
        
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
        parser.add_option("-i", "--input", action="store", dest="inputFileName", help="input filename", default=None)
        parser.add_option("-o", "--outputFile", action="store", dest="outputFileName", help="output filename", default=None)       
        parser.add_option("-q", "--quiet", action="store_true", dest="quietMode", help="quiet mode", default=False)
        (options, args) = parser.parse_args(argv)
        
        #validate options
        if options.inputFileName is None:
            raise Exception("Must specify input file name using -i or --input option.")
        if options.outputFileName is None:
            raise Exception("Must specify output file name using -o or --outputFile option.")
        
        #create EC_Config instance
        # constructor will read and validate all options
        cfg=EC_Config(options.inputFileName)
        
        #write output logfile
        cfg.writeLogfile(options.outputFileName)
                    
        if not options.quietMode:  
            print(cfg)                  

        #if config file had any errors, raise an exception
        if cfg.hasErrors():
            raise Exception('Input errors were detected: {}'.format(cfg.errorDict))

    
    except Exception as info:
        if 'options' in vars() and not options.quietMode:
            raise   #re-raise Exception, interpreter shows stack trace
        else:
            print(info)   

if __name__ == '__main__':
    main()
    #main(['-i','hw1_good_input1.cfg','-o','error_log.txt'])
    