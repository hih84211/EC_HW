import optparse

from optparse import OptionParser
# 一個幫助文檔解釋字符串
hstr = '%prog custom help string'
parser = OptionParser(hstr, description='custom description', version='%prog 1.0')
# 通過OptionParser類創建parser實例,初始參數usage中的%prog等同於os.path.basename(sys.argv[0]),即
# 你當前所運行的腳本的名字，version參數用來顯示當前腳本的版本。
'''
添加參數，-f、--file是長短options，有一即可。
dest='user' 將該用戶輸入的參數保存到變量user中，可以通過options.user方式來獲取該值
action用來表示將option後面的值如何處理，比如:
XXX.py -f test.txt
經過parser.parse_args()處理後,則將test.txt這個值存儲進-f所代表的一個對象，即定義-f中的dest
即option.filename = 'test.txt'
action的常用選項還有store_true,store_false等，這兩個通常在布爾值的選項中使用。

 metavar僅在顯示幫助中有用，如在顯示幫助時會有：
 -f FILE, --filename=FILE    write output to FILE
 -m MODE, --mode=MODE  interaction mode: novice, intermediate, or expert
                         [default: intermediate]
如果-f這一項沒有metavr參數，則在上面會顯示為-f FILENAME --filename=FILENAME,即會顯示dest的值

 defalut是某一選項的默認值，當調用腳本時，參數沒有指定值時，即採用default的默認值。
 '''
parser.add_option('-i', '--input', action='store', dest='input', help='read input data from input file')
parser.add_option('-o', '--output', action='store', dest='output', help='write data to output file')
parser.add_option('-q', '--quite', action='store_false', dest='version', help='don\'t print the version')
# parser.add_option('-v', '--version', action='store_true', dest='version', default=False, help='print the version')
# parser.add_option('-v', '--version', action='store_true', dest='version', help='print the version')

parser.add_option('-f', '--file', action='store', dest='file', help='file to handle')
parser.add_option('-a', '--add', action='append', dest='add', help='add to handle')
parser.add_option('-c', '--count', action='count', dest='count', help='count to handle')
parser.add_option('-d', '--count1', action='count', dest='count', help='count1 to handle')

# parser.add_option('-v', '--version', dest='version')

if parser.has_option('-f'):
    print('content -f')  # parser.set_default('-f', 'myFile')
    parser.remove_option('-f')
if not parser.has_option('-f'):
    print('do not content -f')
# 用一個數組模擬命令參數
# testArgs = ['-i', 'someForInput', '-f', 'someForFile', '-vq', '-a', 'test1 test2 test3', '-c', '-d']
testArgs = ['-i', 'someForInput', 'someForFile', 'someForFile1', '-q', '-a', 'test1 test2 test3', '-c', '-d', '-h']
options, args = parser.parse_args(testArgs)
print('options : %s' % options)
print('args : %s' % args)

if options.input:
    print('input in args : %s' % options.input)
if options.version:
    print('version 1.0.0')

# if options.file:
# print('file in args : %s' % options.file)
if options.add:
    print('add in args : %s' % options.add)

print('version in args', options.version)
