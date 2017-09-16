#!/nfs/site/proj/inway/tools/opensource/python/3.3.5/bin/python
import re
import os
import sys
#sys.setdefaultencoding('utf-8')

file_root=sys.argv[1] if len(sys.argv)==2 else '/vobs/eagle2-xg746-prj/smulation/sim1/simfab.log'
  
text36=['iosf','rl_iosf_merged.tc_list.show'] 
text37=['pac','rl_pac_merged.tc_list.show'] 
text38=['dft','rl_dft_merged.tc_list.show']



texts=[text1,text2,text3,text4,text5,text6,text7,text8,text9,text10,text11,text12,text13,text14,text15,text16,text17,text18,
       text19,text20,text21,text22,text23,text24,text25,text26,text27,text28,text29,text30,text31,text32,text33,text34,text35,text36,text37,text38]
#text_result='source report_all_chip_regression.sf'
#text_result='source host.report_top_results.sf'
text_result='report_central_regression_module_result.sf'

def count(text):
    statur_list=[]
    passed=0
    failed=0
    unknown=0
    function_pass=0
    start_index=-1
    with open(file_root) as file_open:
        lines=file_open.readlines()
    for line in lines:
        if re.search(text,line):
            start_index=lines.index(line)
        else:
            pass
    if(start_index==-1):
        print("not found "+text+" skip ")
    for line in lines[start_index:]:
        if re.search('Total',line):
            break
        else:
            if re.search('PASSED',line):
                passed+=1
                function_pass+=1
            else:
                pass
            if re.search('FAILED',line):
                failed+=1
                if re.search('check_logs failed',line):
                    function_pass+=1
            else:
                pass
            if re.search('UNKNOWN',line):
                unknown+=1
            else:
                pass
    return(passed,function_pass,failed,unknown)
def detect(texts):
    testcase_num=0
    testcase_failed=0
    testcase_function_pass_num=0
    testcase_green_pass_num=0
    testcase_unknown=0
    for each_text in texts:
        passed=0
        failed=0
        unknown=0
        all=0
        function_pass=0
        for text in each_text[1:]:
            count(text)
            passed=passed+count(text)[0]
            failed=failed+count(text)[2]
            unknown=unknown+count(text)[3]
            function_pass=function_pass+count(text)[1]
            all=passed+failed+unknown
        print('%-15s all:%-10s  pass:%-10s failed:%-10s unknown:%-10s ' %(each_text[0],all,passed,failed,unknown))
        testcase_num=testcase_num+passed+failed+unknown
        testcase_function_pass_num=testcase_function_pass_num+function_pass
        testcase_green_pass_num=testcase_green_pass_num+passed
        testcase_failed=testcase_failed+failed
        testcase_unknown=testcase_unknown+unknown
    print("testcase all num : %s   green_pass_num: %s testcase failed : %s   testcae unknown: %s " %(testcase_num,testcase_green_pass_num,testcase_failed,testcase_unknown))
def clean_result(file_root,text_result):
    with open(file_root) as file_open:
        all_line=file_open.readlines()
    for line in all_line:
        if re.search(text_result,line):
            index=all_line.index(line)
            break
    all_line_clean=all_line[:index]
    file_open=open(file_root,'w')
    for line in all_line_clean:
        file_open.write(line)
    file_open.close()
    print('clean over')

if __name__=='__main__':
   detect(texts)
   clean_result(file_root,text_result)



