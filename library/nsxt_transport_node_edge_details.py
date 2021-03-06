#!/usr/bin/env python
# coding=utf-8
#
# Copyright © 2015 VMware, Inc. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
# to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions
# of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#__author__ = 'VJ49'

import yaml
import yamlordereddictloader
from collections import OrderedDict

import logging
logger = logging.getLogger('vswitch')
hdlr = logging.FileHandler('/var/log/chaperone/ChaperoneNSXtLog.log')
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(funcName)s: %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(10)





def main():
    module = AnsibleModule(
        argument_spec=dict(
        ),
        supports_check_mode=True
    )

    final_dict = {}
    sub_dict = {}
    main_dict = {}
    main_list= list()
    stream1 = open('/var/lib/chaperone/answerfile.yml', 'r')    
    dict1 = yaml.load(stream1, Loader=yamlordereddictloader.Loader)

    try:
        for data in dict1:
            if data.startswith('check_edge_node') == True:
                sub_dict[data] = dict1[data]
        for count in range(len(sub_dict)):
            hostname = str(count+1) + "_host_name"
            tnnode = "_tn_node"+ str(count+1)+ "_name"
            for content in dict1: 
                if content.startswith('nsx_edge') == True:
                    if hostname in content:
                        main_dict["host_name"]=dict1[content]
                        logger.info(main_dict)
                    if tnnode in content:
                        main_dict["node_name"]=dict1[content]
                        #logger.info('Node_name {}'.format(dict1[content]))
                        logger.info(main_dict)
                        main_list.append(main_dict)
                        main_dict={}
        #logger.info(main_list)
        #logger.info(main_dict)             
        final_dict['transport_edge_nodes']=main_list
	module.exit_json(changed=True, id=final_dict, msg= "Successfully got the information")

    except Exception as err:
        module.fail_json(changed=False, msg= "Failure: %s" %(err))

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
