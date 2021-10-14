import sys
import yaml
import optparse
from pprint import pprint

'''
助教您好，由於不確定老師在某些條件下的要求，和助教說明幾個程式碼的實作流程：
1.在EC_Engine key錯誤的情況下，選擇不比較內部的keys和values，並且不輸出YAML檔案；選擇略過quietMode（即使引數包含-q），直接將錯誤訊息顯示在命令列。
2.範例hw1_good_input2.cfg中，evaluatorType: rastrigrin，在網路上找到的拼法似乎是rastrigin；但程式碼中的拼音仍比照範例作為判斷依據。
'''

def main(argv=None):
    parabola_lookup = {'evaluatorType': str(), 'generationCount': int(), 'jobName': str(), 'populationSize': int(),
                       'randomSeed': int(), 'scalingParam': float()}
    rastrigrin_lookup = {'evaluatorType': str(), 'generationCount': int(), 'populationSize': int()}
    
    if argv == None:
        argv = sys.argv
    try:
        parser = optparse.OptionParser()
        parser.add_option('-i', '--inputFile', action='store', type='string', dest='input',
                          help='read file from the input path')
        parser.add_option('-o', '--outputFile', action='store', type='string', dest='output',
                          help='output file to the output path')
        parser.add_option('-q', '--quiet', action='store_true', dest='quietMode', help='quiet mode', default=False)

        (options, args) = parser.parse_args(argv)
        ec_engine = True
        bad_keys = []
        good_keys = []
        bad_values = []
        if options.input:
            try:
                with open(options.input, 'r') as file:
                    data = yaml.load(file, Loader=yaml.CLoader)
                keys = list(data.keys())

                if keys[0] != 'EC_Engine':
                    ec_engine = False
                else:
                    for k in keys:  # 這個迴圈是多餘的(只會執行一次)，留著是為了對齊YAML的巢狀結構，避免自己混淆
                        in_dict = data[k]
                        eval_type = in_dict.get('evaluatorType')
                        if eval_type:
                            lookup = None
                            if eval_type == 'parabola':
                                lookup = parabola_lookup
                            elif eval_type == 'rastrigrin':
                                lookup = rastrigrin_lookup
                            else:
                                bad_keys = ['evaluatorType']
                            if lookup:
                                # 把key list轉成set，利用set運算比較出兩者差異
                                # 並且只檢查其中正確key的value type
                                bad_keys = sorted(list(set(lookup.keys()) - set(in_dict.keys())))
                                good_keys = list(set(lookup.keys()) & set(in_dict.keys()))
                                for i in good_keys:
                                    if not isinstance(data['EC_Engine'][i], type(lookup[i])):
                                        bad_values.append(i)
                                bad_values = sorted(bad_values)

                                out_data = {'EC_Engine': {'missingParams': bad_keys, 'incorrectTypes': bad_values}}
                                if options.output:
                                    with open(options.output, 'w') as file:
                                        yaml.dump(out_data, file, Dumper=yaml.CDumper)
                        else:
                            bad_keys = ['evaluatorType']
            except Exception as e:
                print(e.with_traceback())
                return
        else:
            print('No input file!')
            return
        if not options.quietMode:
            if ec_engine:
                print('Missing Params: ', bad_keys)
                print('Incorrect Type: ', bad_values)
            else:
                print('Not EC_Engine!')
            print('Main Completed!')
    except Exception as e:
        print(e.with_traceback())


if __name__ == '__main__':
    # main()
    main(['-i', 'hw1_bad_input2.cfg', '-o', 'result.yml', '-qe'])
