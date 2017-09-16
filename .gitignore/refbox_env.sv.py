<%!
from ubTptEnvDb import dp, masterNum, slaveNum
from ubTptEnvDb import upperTopName, masterNum, slaveNum, CR_slv_num, IOC_slv_num, APB_slv_num, ATB_slv_num, AHB_slv_num, AXI_slv_num, OCP_slv_num, MEM_slv_num, SRAM_slv_num

from ubCommonUtils import topParamTDict, logPrint
%>
//===================modified start==================//
//int master_num = ${masterNum};
//int slave_num = ${slaveNum};
//------------------------------------------------
//------------------------------------------------
//int CR_slv_num = ${CR_slv_num};
//int IOC_slv_num = ${IOC_slv_num};
//int APB_slv_num = ${APB_slv_num};
//int ATB_slv_num = ${ATB_slv_num};
//int AHB_slv_num = ${AHB_slv_num};
//int AXI_slv_num = ${AXI_slv_num};
//int OCP_slv_num = ${OCP_slv_num};
//int MEM_slv_num = ${MEM_slv_num};
//int SRAM_slv_num = ${SRAM_slv_num};
//===================modified end====================//



`ifndef REFBOX_ENV_SV
`define REFBOX_ENV_SV

class refbox_env extends uvm_env;

  svt_ahb_system_env   ahb_net_env;
  net_svt_ahb_system_configuration ahb_net_cfg;
  refbox_virtual_sequencer virt_sqr;
  //utb_common_master utb_ahb_master;
  //utb_common_master utb_reg_master;\
%for inst_utb_mst_idx in list(range(masterNum)):
    <%
        if(inst_utb_mst_idx==0 or inst_utb_mst_idx==1):
            print 'create utb_master%d' % inst_utb_mst_idx
        else:
            continue
    %>
  utb_common_master utb_master${inst_utb_mst_idx};\
%endfor
##  // CR element
## //utb_cr_env slv_cr0;
## //utb_cr_env slv_cr1;
##//==============CR parameter==============#
  //CR element  \
%for cr_idx in list(range(CR_slv_num)):
    <%
        print 'This is CR end slave number:%d' % cr_idx
    %>
  utb_cr_env slv_cr${cr_idx};\
%endfor


  // AHB element
  end_svt_ahb_system_configuration ahb_end_cfg;\
%for ahb_idx in list(range(AHB_slv_num)):
    <%
        print 'This is AHB end slave number:%d' % ahb_idx
    %>
  utb_ahb_env slv_ahb${ahb_idx};\
%endfor\

<%doc>
  // APB element
  end_svt_apb_system_configuration apb_end_cfg;\
%for apb_idx in list(range(APB_slv_num)):
    <%
        print 'This is APB end slave number:%d' % apb_idx
    %>
  utb_apb_env slv_ahb${apb_idx};\
%endfor\
</%doc>
<%doc>
  // AXI element
  end_svt_axi_system_configuration axi_end_cfg;\
%for axi_idx in list(range(AXI_slv_num)):
    <%
        print 'This is AXI end slave number:%d' % axi_idx
    %>
  utb_axi_env slv_ahb${axi_idx};\
%endfor\
</%doc>
  // OCP element
  end_svt_ocp_system_configuration ocp_end_cfg;\
%for ocp_idx in list(range(OCP_slv_num)):
    <%
        print 'This is OCP end slave number:%d' % ocp_idx
    %>
  utb_ocp_env slv_ocp${ocp_idx};\
%endfor


  //IOC element
  vc_ioc_config ioc_cfg;\
%for ioc_idx in list(range(IOC_slv_num)):
    <%
        print 'This is IOC end slave number:%d' % ioc_idx
    %>
  utb_ioc_env slv_ioc${ioc_idx};\
%endfor


  //// SRAM element          //------just only one sram
  //vc_sram_if_config sram_cfg;
  //utb_sram_env slv_sram0;

  //SRAM element
  vc_sram_if_config sram_cfg;\
%for sram_idx in list(range(SRAM_slv_num)):
    <%
        print 'This is SRAM end slave number:%d' % sram_idx
    %>
  utb_sram_env slv_sram${sram_idx};
%endfor

  //MEM element \
%for mem_idx in list(range(MEM_slv_num)):
    <%
        print 'This is MEM end slave number:%d' % mem_idx
    %>
  utb_mem_env slv_mem${mem_idx};\
%endfor
  ##//utb_mem_env slv_mem0;

  svt_mem slave_mem;

  `uvm_component_utils_begin(refbox_env)
  `uvm_component_utils_end

  function new(string name, uvm_component parent=null);
    super.new(name, parent);
  endfunction: new

  function void build_phase(uvm_phase phase);
    `uvm_info(get_type_name(), "build phase entered", UVM_HIGH);
    super.build_phase(phase);
     // configure global memory to all of slave uIF
    slave_mem = new("slave_mem",
        "AMBA3",
        AHB_NET_DATA_WIDTH,
        0,
        0,
        ((1<<AHB_NET_ADDR_WIDTH)-1));
    uvm_config_db#(svt_mem)::set(this, "*", "slave_mem", slave_mem);

    // create AHB network
    if (!uvm_config_db#(net_svt_ahb_system_configuration)::get(this, "", "ahb_net_cfg", ahb_net_cfg)) begin
      `uvm_warning("GETCFG", "no test cfg set, and create a local net_svt_ahb_system_configuration")
      ahb_net_cfg = net_svt_ahb_system_configuration::type_id::create("ahb_net_cfg");
    end
    uvm_config_db#(svt_ahb_system_configuration)::set(this, "ahb_net_env", "cfg", ahb_net_cfg);
    ahb_net_env = svt_ahb_system_env::type_id::create("ahb_net_env", this);               //---create AHB network

    virt_sqr = refbox_virtual_sequencer::type_id::create("virt_sqr", this);

    // add AHB utb master0 and master1\
%for ahb_net_mst_idx in list(range(masterNum)):
    <%
        if(ahb_net_mst_idx==0 or ahb_net_mst_idx==1):
            print 'create utb_master%d' % ahb_net_mst_idx
        else:
            continue
    %>
    uvm_config_db#(svt_ahb_master_configuration)::set(this, "utb_master${ahb_net_mst_idx}", "master_cfg", ahb_net_cfg.master_cfg[${ahb_net_mst_idx+1}]);
    utb_master${ahb_net_mst_idx} = utb_common_master::type_id::create("utb_master${ahb_net_mst_idx}", this);\
%endfor
##    uvm_config_db#(svt_ahb_master_configuration)::set(this, "utb_reg_master", "master_cfg", ahb_net_cfg.master_cfg[1]);
##    utb_reg_master = utb_common_master::type_id::create("utb_reg_master", this);
##    // add AHB utb master1                                                                //---create utb_ahb master1
##    uvm_config_db#(svt_ahb_master_configuration)::set(this, "utb_ahb_master", "master_cfg", ahb_net_cfg.master_cfg[2]);
##    utb_ahb_master = utb_common_master::type_id::create("utb_ahb_master", this);


    // add CR0 utb slave and CR1 utb slave \
%for cr_idx in list(range(CR_slv_num)):
    <%
        print cr_idx
    %>
##    %for j in list(range(1,CR_slv_num+1)):
    uvm_config_db#(svt_ahb_slave_configuration)::set(this, "slv_cr${cr_idx}.slv", "slave_cfg", ahb_net_cfg.slave_cfg[${cr_idx+1}]);
    slv_cr${cr_idx} = utb_cr_env::type_id::create("slv_cr${cr_idx}", this);\
%endfor


    // add AHB0 utb slave AHB1 utb slave
    if (!uvm_config_db#(end_svt_ahb_system_configuration)::get(this, "", "ahb_end_cfg", ahb_end_cfg)) begin
      `uvm_warning("GETCFG", "no test cfg set, and create a local end_svt_ahb_system_configuration")
      ahb_end_cfg = end_svt_ahb_system_configuration::type_id::create("ahb_end_cfg");    //---create ahb_end_cfg
    end\
%for ahb_idx in list(range(AHB_slv_num)):
    <%
        print ahb_idx
    %>
    uvm_config_db#(svt_ahb_master_configuration)::set(this, "slv_ahb${ahb_idx}.ahb_mst", "cfg", ahb_end_cfg.master_cfg[${ahb_idx+1}]);
    slv_ahb${ahb_idx} = utb_ahb_env::type_id::create("slv_ahb${ahb_idx}", this);\
%endfor


    //add MEM utb slave ----> utb_mem_env \
    ##//slv_mem0 = utb_mem_env::type_id::create("slv_mem0", this);
%for mem_idx in list(range(MEM_slv_num)):
    <%
        print mem_idx
    %>
    slv_mem${mem_idx} = utb_mem_env::type_id::create("slv_mem${mem_idx}", this);\
%endfor

##    //add AXI utb slave
##    //if (!uvm_config_db#(end_svt_axi_system_configuration)::get(this, "", "axi_end_cfg", axi_end_cfg)) begin
##    //  `uvm_warning("GETCFG", "no test cfg set, and create a local end_svt_axi_system_configuration")
##    //  axi_end_cfg = end_svt_axi_system_configuration::type_id::create("axi_end_cfg");
##    //end
##    //uvm_config_db#(svt_axi_port_configuration)::set(this, "slv_axi0.axi_mst", "cfg", axi_end_cfg.master_cfg[1]);
##    //slv_axi0 = utb_axi_env::type_id::create("slv_axi0", this);

    // add OCP0 utb slave
    if (!uvm_config_db#(end_svt_ocp_system_configuration)::get(this, "", "ocp_end_cfg", ocp_end_cfg)) begin
      `uvm_warning("GETCFG", "no test cfg set, and create a local end_svt_ocp_system_configuration")
      ocp_end_cfg = end_svt_ocp_system_configuration::type_id::create("ocp_end_cfg");    //---create ocp_end_cfg
    end\
%for ocp_idx in list(range(OCP_slv_num)):
    <%
        print ocp_idx
    %>
    uvm_config_db#(svt_ocp_core_configuration)::set(this, "slv_ocp${ocp_idx}", "cfg", ocp_end_cfg.m_o_mstr_cfg);
    slv_ocp${ocp_idx} = utb_ocp_env::type_id::create("slv_ocp${ocp_idx}", this);\
    //uvm_config_db#(svt_ocp_core_configuration)::set(this, "slv_ocp${ocp_idx}.ocp_mst", "cfg", ocp_end_cfg.master_cfg[${ocp_idx+1}]);
    ////uvm_config_db#(svt_ocp_master_configuration)::set(this, "slv_ocp${ocp_idx}.ocp_mst", "cfg", ocp_end_cfg.master_cfg[${ocp_idx+1}]);
    //slv_ocp${ocp_idx} = utb_ocp_env::type_id::create("slv_ocp${ocp_idx}", this);\
%endfor
##    //if (!uvm_config_db#(end_svt_ocp_system_configuration)::get(this, "", "ocp_end_cfg", ocp_end_cfg)) begin
##    //  `uvm_warning("GETCFG", "no test cfg set, and create a local end_svt_ocp_system_configuration")
##    //  ocp_end_cfg = end_svt_ocp_system_configuration::type_id::create("ocp_end_cfg");
##    //end
##    //uvm_config_db#(svt_ocp_core_configuration)::set(this, "slv_ocp0", "cfg", ocp_end_cfg.m_o_mstr_cfg);
##    //slv_ocp0 = utb_ocp_env::type_id::create("slv_ocp0", this);


    // add IOC0 utb slave IOC1 utb slave
    if (!uvm_config_db#(vc_ioc_config)::get(this, "", "ioc_cfg", ioc_cfg)) begin
      `uvm_warning("GETCFG", "no test cfg set, and create a local vc_ioc_config")
      ioc_cfg = vc_ioc_config::type_id::create("ioc_cfg");
    end\
%for ioc_idx in list(range(IOC_slv_num)):
    <%
        print ioc_idx
    %>
    uvm_config_db#(vc_ioc_config)::set(this, "slv_ioc${ioc_idx}.ioc_env", "cfg", ioc_cfg);
    slv_ioc${ioc_idx} = utb_ioc_env::type_id::create("slv_ioc${ioc_idx}", this);\
%endfor


##    // add SRAM0 utb slave
##    if (!uvm_config_db#(vc_sram_if_config)::get(this, "", "sram_cfg", sram_cfg)) begin
##      `uvm_warning("GETCFG", "no test cfg set, and create a local vc_sram_if_config")
##      sram_cfg = vc_sram_if_config::type_id::create("sram_cfg");
##    end
##    uvm_config_db#(vc_sram_if_config)::set(this, "slv_sram0.sram_env", "cfg", sram_cfg);
##    slv_sram0 = utb_sram_env::type_id::create("slv_sram0", this);

    // add SRAM utb slave
    if (!uvm_config_db#(vc_sram_if_config)::get(this, "", "sram_cfg", sram_cfg)) begin
      `uvm_warning("GETCFG", "no test cfg set, and create a local vc_sram_if_config")
      sram_cfg = vc_sram_if_config::type_id::create("sram_cfg");
    end\
%for sram_idx in list(range(SRAM_slv_num)):
    <%
        print sram_idx
    %>
    uvm_config_db#(vc_sram_if_config)::set(this, "slv_sram${sram_idx}.sram_env", "cfg", sram_cfg);
    slv_sram${sram_idx} = utb_sram_env::type_id::create("slv_sram${sram_idx}", this);\
%endfor

    `uvm_info(get_type_name(), "build phase exited", UVM_HIGH);

  endfunction: build_phase

  function void connect_phase(uvm_phase phase);
    virt_sqr.ahb_net_sequencer = ahb_net_env.sequencer;

    //utb_reg_master.b_fwd.connect(ahb_net_env.master[1].b_fwd);
    //utb_ahb_master.b_fwd.connect(ahb_net_env.master[2].b_fwd);
    //=========ahb net master number is ${masterNum}=========//\
%for ahb_net_mst_idx in range(masterNum):
    <%
        if(ahb_net_mst_idx==0 or ahb_net_mst_idx==1):
            print 'connect utb_master%d to ahb_net_env' % ahb_net_mst_idx
        else:
            continue
    %>
    utb_master${ahb_net_mst_idx}.b_fwd.connect(ahb_net_env.master[${ahb_net_mst_idx+1}].b_fwd);         //connect utb_master${ahb_net_mst_idx}\
%endfor\
##    //======modifie---comment 160---166 lines======//
##    //ahb_net_env.slave[1].resp_socket.connect(slv_cr0.slv.b_resp);
##    //ahb_net_env.slave[2].resp_socket.connect(slv_ahb0.slv.b_resp);
##    //ahb_net_env.slave[3].resp_socket.connect(slv_mem0.slv.b_resp);
##    ////ahb_net_env.slave[4].resp_socket.connect(slv_axi0.slv.b_resp);
##    //ahb_net_env.slave[5].resp_socket.connect(slv_ioc0.slv.b_resp);
##    //ahb_net_env.slave[6].resp_socket.connect(slv_ocp0.slv.b_resp);
##    //ahb_net_env.slave[7].resp_socket.connect(slv_sram0.slv.b_resp);

##%for slv_idx in list(range(1,slaveNum)):
##    <%
##        print 'N:%d' %slv_idx
##        %if(slv_idx < 3):
##            return 1
##        %else:
##            return 0
##        %endif
##    %>
##    %for cr_idx in list(range(CR_slv_num)):
##        <%
##            print cr_idx
##        %>\
####        ahb_net_env.slave[${slv_idx}].resp_socket.connect(slv_cr${cr_idx}.slv.b_resp);    // connect slv_cr0 and slv_cr1
####        ahb_net_env.slave[2].resp_socket.connect(slv_cr1.slv.b_resp);
##    %endfor
####    %for ahb_idx in list(range(AHB_slv_num)):
####        <%
####            print ahb_idx
####        %>
####    %endfor
####    %for ioc_idx in list(range(IOC_slv_num)):
####        <%
####            print ioc_idx
####        %>
####    %endfor
##    ahb_net_env.slave[${slv_idx}].resp_socket.connect(slv_cr${cr_idx}.slv.b_resp);    // connect slv_cr0 and slv_cr1
##%endfor

    //=========ahb net slave number is ${slaveNum}=========//\
<%
ahb_net_slv_lst = list(range(1,slaveNum))
cr_slv_lst = list(range(CR_slv_num))
ioc_slv_lst = list(range(IOC_slv_num))
apb_slv_lst = list(range(APB_slv_num))
atb_slv_lst = list(range(ATB_slv_num))
ahb_slv_lst = list(range(AHB_slv_num))
axi_slv_lst = list(range(AXI_slv_num))
ocp_slv_lst = list(range(OCP_slv_num))
mem_slv_lst = list(range(MEM_slv_num))
sram_slv_lst = list(range(SRAM_slv_num))
slv_lst = cr_slv_lst + ahb_slv_lst + ocp_slv_lst + ioc_slv_lst + mem_slv_lst + sram_slv_lst + apb_slv_lst + atb_slv_lst + axi_slv_lst
#slv_lst = cr_slv_lst + ioc_slv_lst + apb_slv_lst + atb_slv_lst + ahb_slv_lst + axi_slv_lst + ocp_slv_lst + mem_slv_lst
l = range(1,7)
l1 = range(0,2)
l2 = l1 + l1 + l1
#print l
#print l2
%>\

%for (ahb_net_slv_idx, slv_X_idx) in zip(ahb_net_slv_lst, slv_lst):
    <%
#        print i,j
        if(ahb_net_slv_idx==1 or ahb_net_slv_idx==2):
            print 'connect cr%d to ahb_net_env' % slv_X_idx
        else:
            continue
    %>
    ahb_net_env.slave[${ahb_net_slv_idx}].resp_socket.connect(slv_cr${slv_X_idx}.slv.b_resp);     // connect slv_cr${slv_X_idx}\
%endfor\

%for (ahb_net_slv_idx, slv_X_idx) in zip(ahb_net_slv_lst, slv_lst):
    <%
#        print i,j
        if(ahb_net_slv_idx==3 or ahb_net_slv_idx==4 or ahb_net_slv_idx==5 or ahb_net_slv_idx==6):
            print 'connect ahb%d to ahb_net_env' % slv_X_idx
        else:
            continue
    %>
    ahb_net_env.slave[${ahb_net_slv_idx}].resp_socket.connect(slv_ahb${slv_X_idx}.slv.b_resp);    // connect slv_ahb${slv_X_idx}\
%endfor\

%for (ahb_net_slv_idx, slv_X_idx) in zip(ahb_net_slv_lst, slv_lst):
    <%
#        print i,j
        if(ahb_net_slv_idx==7 or ahb_net_slv_idx==8 or ahb_net_slv_idx==9 or ahb_net_slv_idx==10):
            print 'connect ocp%d to ahb_net_env' % slv_X_idx
        else:
            continue
    %>
    ahb_net_env.slave[${ahb_net_slv_idx}].resp_socket.connect(slv_ocp${slv_X_idx}.slv.b_resp);    // connect slv_ocp${slv_X_idx}\
##    ahb_net_env.slave[6].resp_socket.connect(slv_ocp0.slv.b_resp);
%endfor\

%for (ahb_net_slv_idx, slv_X_idx) in zip(ahb_net_slv_lst, slv_lst):
    <%
#        print i,j
        if(ahb_net_slv_idx==11 or ahb_net_slv_idx==12):
            print 'connect ioc%d to ahb_net_env' % slv_X_idx
        else:
            continue
    %>
    ahb_net_env.slave[${ahb_net_slv_idx}].resp_socket.connect(slv_ioc${slv_X_idx}.slv.b_resp);    // connect slv_ioc${slv_X_idx}\
%endfor

%for (ahb_net_slv_idx, slv_X_idx) in zip(ahb_net_slv_lst, slv_lst):
    <%
#        print i,j
        if(ahb_net_slv_idx==13 or ahb_net_slv_idx==14):
            print 'connect mem%d to ahb_net_env' % slv_X_idx
        else:
            continue
    %>
    ahb_net_env.slave[${ahb_net_slv_idx}].resp_socket.connect(slv_mem${slv_X_idx}.slv.b_resp);    // connect slv_mem${slv_X_idx}\
##    ahb_net_env.slave[3].resp_socket.connect(slv_mem0.slv.b_resp);
%endfor

%for (ahb_net_slv_idx, slv_X_idx) in zip(ahb_net_slv_lst, slv_lst):
    <%
#        print i,j
        if(ahb_net_slv_idx==15):
            print 'connect sram%d to ahb_net_env' % slv_X_idx
        else:
            continue
    %>
    ahb_net_env.slave[${ahb_net_slv_idx}].resp_socket.connect(slv_sram${slv_X_idx}.slv.b_resp);    // connect slv_sram${slv_X_idx}\
##    ahb_net_env.slave[3].resp_socket.connect(slv_mem0.slv.b_resp);
%endfor
    //ahb_net_env.slave[15].resp_socket.connect(slv_sram0.slv.b_resp);   //manual add it for ahb_net_env--->slv_sram

##    //ahb_net_env.slave[1].resp_socket.connect(slv_cr0.slv.b_resp);    // connect slv_cr0 and slv_cr1
##    //ahb_net_env.slave[2].resp_socket.connect(slv_cr1.slv.b_resp);
##    //ahb_net_env.slave[3].resp_socket.connect(slv_ahb0.slv.b_resp);   // connect slv_ahb0 and slv_ahb1
##    //ahb_net_env.slave[4].resp_socket.connect(slv_ahb1.slv.b_resp);
##    //ahb_net_env.slave[4].resp_socket.connect(slv_axi0.slv.b_resp);
##    //ahb_net_env.slave[5].resp_socket.connect(slv_ioc0.slv.b_resp);   // connect slv_ahb0 and slv_ahb1
##    //ahb_net_env.slave[6].resp_socket.connect(slv_ioc1.slv.b_resp);
##    ////ahb_net_env.slave[6].resp_socket.connect(slv_ocp0.slv.b_resp);
##    //ahb_net_env.slave[7].resp_socket.connect(slv_sram0.slv.b_resp);
  endfunction: connect_phase

  task run_phase(uvm_phase phase);
  endtask: run_phase

endclass


`endif // REFBOX_ENV_SV
