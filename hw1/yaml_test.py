import yaml
from pprint import pprint

if __name__ == '__main__':
    lookup = {'evaluatorType': str(), 'generationCount': int(), 'jobName': str(), 'populationSize': int(),
              'randomSeed': int(), 'scalingParam': float()}
    if isinstance('this is a string', type(lookup['evaluatorType'])):
        print("YES")
    else:
        print("NO")
    with open('hw1_good_input1.cfg', 'r') as stream:
        data1 = yaml.load(stream, Loader=yaml.CLoader)

    with open('hw1_bad_input2.cfg', 'r') as stream:
        data2 = yaml.load(stream, Loader=yaml.CLoader)

    # pprint(data1)
    keys = data2.keys()
    for k in keys:
        in_dict = data2[k]
        # print(sorted(list(in_dict.keys())))

        print(sorted(list(set(lookup.keys()) - set(in_dict.keys()))))

