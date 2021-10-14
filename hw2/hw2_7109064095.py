import sys
import yaml
import optparse


class YamlParser:
    def __init__(self, argv=None):
        self.in_yaml = None
        self.parabola_lookup = {'evaluatorType': str(), 'generationCount': int(), 'jobName': str(),
                                'populationSize': int(), 'randomSeed': int(), 'scalingParam': float()}
        self.rastrigrin_lookup = {'evaluatorType': str(), 'generationCount': int(), 'populationSize': int()}

        if argv == None:
            argv = sys.argv
        try:
            self.set_argv(argv)
            if not self.options.quietMode:
                print('Class YamlParser initiated!')
        except Exception as e:
            print(e.with_traceback())

    def parse(self):
        if self.in_yaml:
            ec_engine = True
            bad_keys = []
            good_keys = []
            bad_values = []

            keys = list(self.in_yaml.keys())

            if keys[0] != 'EC_Engine':
                ec_engine = False
            else:
                for k in keys:
                    in_dict = self.in_yaml[k]
                    eval_type = in_dict.get('evaluatorType')
                    if eval_type:
                        lookup = None
                        if eval_type == 'parabola':
                            lookup = self.parabola_lookup
                        elif eval_type == 'rastrigrin':
                            lookup = self.rastrigrin_lookup
                        else:
                            bad_keys = ['evaluatorType']
                        if lookup:
                            bad_keys = sorted(list(set(lookup.keys()) - set(in_dict.keys())))
                            good_keys = list(set(lookup.keys()) & set(in_dict.keys()))
                            for i in good_keys:
                                if not isinstance(self.in_yaml['EC_Engine'][i], type(lookup[i])):
                                    bad_values.append(i)
                            bad_values = sorted(bad_values)

                            out_data = {'EC_Engine': {'missingParams': bad_keys, 'incorrectTypes': bad_values}}
                            if self.options.output:
                                YamlParser.write_yaml(yml=out_data, path=self.options.output)
                    else:
                        bad_keys = ['evaluatorType']
            if not self.options.quietMode:
                if ec_engine:
                    print('Missing Params: ', bad_keys)
                    print('Incorrect Type: ', bad_values)
                else:
                    print('Not EC_Engine!')
        else:
            print('No valid input file.')

    @staticmethod
    def read_yaml(path):
        try:
            with open(path, 'r') as file:
                data = yaml.load(file, Loader=yaml.CLoader)
            return data
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def write_yaml(yml, path):
        try:
            with open(path, 'w') as file:
                yaml.dump(yml, file, Dumper=yaml.CDumper)
        except Exception as e:
            print(e)

    ''' Optional setter '''
    def set_argv(self, argv):
        parser = optparse.OptionParser()
        parser.add_option('-i', '--inputFile', action='store', type='string', dest='input',
                          help='read file from the input path')
        parser.add_option('-o', '--outputFile', action='store', type='string', dest='output',
                          help='output file to the output path')
        parser.add_option('-q', '--quiet', action='store_true', dest='quietMode', help='quiet mode', default=False)
        (self.options, self.args) = parser.parse_args(argv)
        if self.options.input:
            self.in_yaml = YamlParser.read_yaml(path=self.options.input)


if __name__ == '__main__':
    YamlParser().parse()
    '''my_parser = YamlParser(argv=['-i', 'hw1_bad_input3.cfg', '-o', 'result1.yml', '-q'])
    my_parser.parse()
    print()
    my_parser.set_argv(argv=['-i', 'hw1_bad_input2.cfg', '-o', 'result2.yml'])
    my_parser.parse()'''

