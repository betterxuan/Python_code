import re,os
import xlrd
import xlwt
from xlwt import *
from xlutils.copy import copy


#source_file="/nfs/xa/proj/esp/eagle2.gls/xg756_b0_gls/COVERAGE/SAVE_LOG/XG756_C0_SPEC_3_2_COVER/log_for_merge_with_dft/log/vcs_cov_phys/reprot/with_12_exclude_report/TGL_report_with_exclude/urgReport_tgl_chip_soc/modinfo.txt"
source_file="/nfs/xa/proj/esp/eagle2.gls/xg756_b0_gls/COVERAGE/SAVE_LOG/XG756_C0_SPEC_3_2_COVER/log_for_merge_with_dft4.24/log/vcs_cov_phys/TGL_report/urgReport_tgl_chip_soc/modinfo.txt"
gen_excel_file="/nfs/xa/proj/esp/eagle2.gls/xg756_b0_gls/COVERAGE/SAVE_LOG/XG756_C0_SPEC_3_2_COVER/log_for_merge_with_dft3.11/log/vcs_cov_phys/Collected_Hier_TGL_XG756_C0.hier"
class gen_excel:
    
    def __init__(self):
        self._excel_list=[]
        self._search_status1=0
        self._search_status2=0
        self._cover_signal=0
        self._all_signal=0
#        self._module_dir={
#
#                          'INST_CORE':{'module':'INST_CORE','owner':'sunke','percent':''},
#                          'INST_PHY_PER_SHELL':{'module':'PHY_PER_SHELL','owner':'','percent':''},
#
#
#                                                   }

        self._module_dir={'INST_CPI_P4_CGU':{'module':'HOST_CGU','owner':'Zhao,qiang','percent':''},

                          'INST_MON_SBC_PER1_SHELL':{'module':'INST_MON_SBC_PER1_SHELL','owner':'','percent':''},
                          'INST_IPDB_CEU_SUPERISO':{'module':'INST_IPDB_CEU_SUPERISO','owner':'','percent':''},
                          'INST_P4_STM':{'module':'INST_P4_STM','owner':'','percent':''},
                          'INST_PHY_MON_SBC_PER4_SHELL':{'module':'INST_PHY_MON_SBC_PER4_SHELL','owner':'','percent':''},
                          'INST_P4_CAPCOM0_SHELL':{'module':'INST_P4_CAPCOM0_SHELL','owner':'','percent':''},
                          'INST_P4_GPTU1_SHELL':{'module':'INST_P4_GPTU1_SHELL','owner':'','percent':''},
                                                   }
    def option_parse(self):
        pass
    
    def extract_excel(self,file):
        
        for line in open(file):
            if (line.startswith('/') or len(line.strip())==0):
                pass
            else:
                excel_element=line.split()[1]
                self._excel_list.append(excel_element)

    def initial_excel(self):
        
        Title_report=['Instance','Owner','Toggle']
        Title_tgl=["Port","Toggle","Toggle 1->0","Toggle 0->1","Direction","comment"]

        pattern_title=xlwt.Pattern()
        pattern_title.pattern=xlwt.Pattern.SOLID_PATTERN
        pattern_title.pattern_fore_colour=5
        style_title=xlwt.XFStyle()
        style_title.pattern=pattern_title

        excel_table=Workbook()
        excel_sheet_report=excel_table.add_sheet("Coverage_Report")

        row=1
        column_report=0
        for element in Title_report:
            excel_sheet_report.write(0,column_report,element,style_title)
            column_report+=1

        for key in self._module_dir.keys():
            excel_sheet_report.write(row,0,self._module_dir[key]['module'])
            row+=1
            
        for element in self._excel_list:
            excel_name=element.split('.')[-1]
            excel_sheet=excel_table.add_sheet(excel_name)
            column=0
            for each_element in Title_tgl:
                excel_sheet.write(0,column,each_element,style_title)
                column+=1
        excel_table.save('chip_soc_tgl.xls')
    
    def update_report_percent(self):
        excel_report_open=xlrd.open_workbook('chip_soc_tgl.xls',formatting_info=True)
        table=excel_report_open.sheets()[0]
        table=excel_report_open.sheet_by_name(u'Coverage_Report')

        excel_copy=copy(excel_report_open)
        sheet=excel_copy.get_sheet(self.get_sheet_index("Coverage_Report"))
        for i in range(table.nrows):
            for key in self._module_dir.keys():
                if(table.cell(i,0).value==self._module_dir[key]['module']):
                    sheet.write(i,1,self._module_dir[key]['owner'])
                    sheet.write(i,2,self._module_dir[key]['percent'])
        os.remove('chip_soc_tgl.xls')
        excel_copy.save('chip_soc_tgl.xls')

    def get_sheet_index(self,search_name):
       excel_handle=xlrd.open_workbook('chip_soc_tgl.xls')
       i=0
       for sheet in excel_handle.sheets():
           if (sheet.name==search_name):
               print(i)
               return i
           else:
               pass 
           i+=1

    def search_write_excel(self,file):
        '''
        0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 
        17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 
        22 = Light Gray, 23 = Dark Gray
        '''
        pattern_yes=xlwt.Pattern()
        pattern_yes.pattern=xlwt.Pattern.SOLID_PATTERN
        pattern_yes.pattern_fore_colour=3
        style_yes=xlwt.XFStyle()
        style_yes.pattern=pattern_yes

        pattern_no=xlwt.Pattern()
        pattern_no.pattern=xlwt.Pattern.SOLID_PATTERN
        pattern_no.pattern_fore_colour=2
        style_no=xlwt.XFStyle()
        style_no.pattern=pattern_no

        pattern_exclude=xlwt.Pattern()
        pattern_exclude.pattern=xlwt.Pattern.SOLID_PATTERN
        pattern_exclude.pattern_fore_colour=22
        style_exclude=xlwt.XFStyle()
        style_exclude.pattern=pattern_exclude

        for element in self._excel_list:
            row=0
            element_num=0
            excel_open=xlrd.open_workbook('chip_soc_tgl.xls',formatting_info=True)
            excel_copy=copy(excel_open) 
            print(element.split('.')[-1])
            sheet=excel_copy.get_sheet(self.get_sheet_index(element.split('.')[-1]))
            #Used for check if the module in source file have  exclude signal infomation
            #if element number =2 ,no exclude ; if element number =3 ,with exclude
            for line in open(source_file,'r'):
                if((re.search(element,line) and not re.search(element+'\.',line))and not re.search(element+'_',line)):    
                    element_num+=1
            #for write to the excel
            for line in open(source_file,'r'):
                if((re.search(element,line) and not re.search(element+'\.',line)) and not re.search(element+'_',line)):    
                    print(line)
                    self._search_status1+=1
                if(element_num==2 and self._search_status1==1 and self._search_status2==1) or (element_num==3 and self._search_status1==3 and self._search_status2==1):
                    if(not line.startswith('=') and not line.startswith('-') and not line.startswith(' ')):
                        line_strip=line.rstrip().split()
                        row+=1
                        column=0
                        for entry in line_strip:
                            if(column==1 or column==2 or column==3):
                                if(entry=="Yes"):
                                    sheet.write(row,column,entry,style_yes)
                                elif(entry=="No"):
                                    sheet.write(row,column,entry,style_no)
                                elif(entry=="Excluded"):
                                    sheet.write(row,column,entry,style_exclude)
                                else:
                                    sheet.write(row,column,entry)

                                if(column==1 and entry=="Yes"):
                                    self._cover_signal+=1
                                    self._all_signal+=1
                                elif(column==1 and entry=="No"):
                                    self._all_signal+=1
                                elif(column==1 and entry=="Excluded"):
                                    self._cover_signal+=1
                                    self._all_signal+=1
                                else:
                                    pass

                            else:
                                sheet.write(row,column,entry)
                            column+=1
                if ((element_num==2 and self._search_status1==1)or (element_num==3 and self._search_status1==3)) and re.search("Port Details",line):
                    self._search_status2+=1
                if (self._search_status1==3 and line.startswith('=')) or (element_num==2 and self._search_status1==2):
                    break
            if (element.split('.')[-1] in self._module_dir):
                if (self._all_signal==0):
                    print("error for "+element)
                self._module_dir[element.split('.')[-1]]['percent']='%.2f%%'%(float(self._cover_signal)/float(self._all_signal)*100)
            else:
                pass
            self._cover_signal=0
            self._all_signal=0

            if (self._search_status1==0):
                print("Error : "+element+" Not Found")
            else:
                self._search_status1=0
            if (self._search_status2==0):
                print("Error :"+element+" Ports Not Found")
            else:
                self._search_status2=0
            os.remove('chip_soc_tgl.xls')
            excel_copy.save('chip_soc_tgl.xls')
            
     
if __name__=="__main__":
    excel_obj=gen_excel()
    excel_obj.extract_excel(gen_excel_file)
    excel_obj.initial_excel()
    excel_obj.search_write_excel(source_file)
    excel_obj.update_report_percent()
    


