# -*- coding: utf-8 -*-
"""
Created on 18-11-2 下午3:26

@author: dmyan
"""
import sys
sys.path.append('./gen-py')
from process_query import Process
from process_query.ttypes import *
from process_query.constants import *

from myRetriever import Thrift
from myRetriever.transport import TSocket
from myRetriever.transport import TTransport
from myRetriever.protocol import TBinaryProtocol

try:
    transport = TSocket.TSocket('192.168.108.128', 9001)

    transport = TTransport.TBufferedTransport(transport)

    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    client = Process.Client(protocol)

    transport.open()
    msg = client.sayHello('dahskjdhaksjd')
    print(msg)


except Exception as inst:
    print(inst)
if __name__ == '__main__':
    pass
