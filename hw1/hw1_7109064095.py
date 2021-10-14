import sys
import yaml
import optparse



def main(argv=None):
    if argv == None:
        argv = sys.argv

    try:
        parser = optparse.OptionParser()
        parser.add_option('-i', '--inputFile', action='store', dest='input', help='read file from the input path')
        parser.add_option('-o', '--outputFile', action='store', dest='output', help='output file to the output path')
        parser.add_option('-q', '--quiet', action='store_true', dest='quietMode', help='quiet mode', defualt=False)
    except Exception as e:
        pass



if __name__ == '__main__':
    main()
