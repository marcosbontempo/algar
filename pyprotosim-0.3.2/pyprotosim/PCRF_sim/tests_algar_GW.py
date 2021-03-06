#!/usr/bin/env python
###############################################################################
# Copyright (c) 2012, Sergej Srepfler <sergej.srepfler@gmail.com>
#               2014, PGW client tests are added by L.Belov <lavrbel@gmail.com>
# 		February 2012 - March 2014
# 		Version 0.1.0, Last change on Mar 13, 2014
# 		This software is distributed under the terms of BSD license.    
###############################################################################

## FLOWS AND DESCRIPTION:

## Capabilities Exchange:

#1) PGW ---> CER -----> PCRF
#2) PGW <--- CEA <----- PCRF

## CCR Initial to PCRF, PCRF checks if user is valid in SPR DB 
## and reply with PCC Charging-Install Rule and QoS profile settings 'basic'

#3) PGW ---> CCR-I ---> PCRF
#4)                     PCRF ---> SPR
#5) PGW <--- CCA-I <--  PCRF <--- SPR (PCC rule)

## RAR-U (Update) from PCRF to PGW (Push operation) will be sent using script test_push_RAR-U.py manually or (can be run from script)
## with PCC Charging Remove old 'basic ' QoS profile and setting new PCC Charging-Install Rule and QoS profile settings 'highspeed'
## PGW will reply with RAA 2001 reply


#6) PCRF ---> RAR-U ---> PGW 
                     
#7) PCRF <--- RAA <---   PGW

## User is logged off and now sending CCR-T (Terminate) to PCRF, PCRF terminates and reply with 2001 Success 

#8) PGW ---> CCR-T ---> PCRF

## Disconnect Pear Request to PCRF and 2001 Success Answer and close session

#9)  PGW ---> DPR ----> PCRF
#10) PGW <--- DPA <---- PCRF

#################################################################
                         
#Next two lines are to include parent directory for testing
import sys
import json
sys.path.append("..")
# Remove them normally

from libDiameter import *
import datetime
import time


def create_CER():
    # Let's build CER
    CER_avps=[]
    CER_avps.append(encodeAVP("Origin-Host", ORIGIN_HOST))
    CER_avps.append(encodeAVP("Origin-Realm", ORIGIN_REALM))
    CER_avps.append(encodeAVP('Host-IP-Address', PCEF))
    CER_avps.append(encodeAVP("Vendor-Id", 11111))
    CER_avps.append(encodeAVP("Origin-State-Id", 1))
    CER_avps.append(encodeAVP("Supported-Vendor-Id", 10415))
    CER_avps.append(encodeAVP('Supported-Vendor-Id', 0))
    CER_avps.append(encodeAVP('Supported-Vendor-Id', 10415))
    CER_avps.append(encodeAVP('Supported-Vendor-Id', 11111))
    CER_avps.append(encodeAVP('Auth-Application-Id', 16777238))
    CER_avps.append(encodeAVP('Product-Name', 'PCEF Algar'))

    # Create message header (empty)
    CER=HDRItem()
    # Set command code
    CER.cmd=dictCOMMANDname2code("Capabilities-Exchange")
    # Set Hop-by-Hop and End-to-End
    initializeHops(CER)
    # Add AVPs to header and calculate remaining fields
    msg=createReq(CER,CER_avps)
    # msg now contains CER Request as hex string
    return msg


def create_CCR_I():
    # Let's build Server-AssignmentRequest
    REQ_avps=[]
    REQ_avps.append(encodeAVP("Session-Id", SESSION_ID))
    REQ_avps.append(encodeAVP("Destination-Realm", DEST_REALM))
    REQ_avps.append(encodeAVP("Origin-Host", ORIGIN_HOST))
    REQ_avps.append(encodeAVP("Origin-Realm", ORIGIN_REALM))
    REQ_avps.append(encodeAVP('Auth-Application-Id', 16777238))
    REQ_avps.append(encodeAVP('CC-Request-Type', 1))
    REQ_avps.append(encodeAVP('CC-Request-Number', 0))
    REQ_avps.append(encodeAVP('Subscription-Id',[encodeAVP('Subscription-Id-Data', '1234567890'), encodeAVP('Subscription-Id-Type', 0)]))
    REQ_avps.append(encodeAVP('Subscription-Id',[encodeAVP('Subscription-Id-Data', '1'), encodeAVP('Subscription-Id-Type', 1)]))
    REQ_avps.append(encodeAVP('Framed-IP-Address', PCEF))
    # Create message header (empty)
    CCR=HDRItem()
    # Set command code
    CCR.cmd=dictCOMMANDname2code("Credit-Control")
    # Set Application-id
    CCR.appId=APPLICATION_ID
    # Set Hop-by-Hop and End-to-End
    initializeHops(CCR)
    # Set Proxyable flag
    setFlags(CCR,DIAMETER_HDR_PROXIABLE)    
    # Add AVPs to header and calculate remaining fields
    ret=createReq(CCR,REQ_avps)
    # ret now contains CCR Request as hex string
    return ret 

def create_CCR_T():
    # Let's build Server-AssignmentRequest
    REQ_avps=[]
    REQ_avps.append(encodeAVP("Session-Id", SESSION_ID))
    REQ_avps.append(encodeAVP("Destination-Realm", DEST_REALM))
    REQ_avps.append(encodeAVP('Auth-Application-Id', 16777238))
    REQ_avps.append(encodeAVP("Origin-Host", ORIGIN_HOST))
    REQ_avps.append(encodeAVP("Origin-Realm", ORIGIN_REALM))
    REQ_avps.append(encodeAVP('CC-Request-Type', 3))
    REQ_avps.append(encodeAVP('CC-Request-Number', 1))
    REQ_avps.append(encodeAVP('Subscription-Id',[encodeAVP('Subscription-Id-Data', '1234567890'), encodeAVP('Subscription-Id-Type', 0)]))
    REQ_avps.append(encodeAVP('Subscription-Id',[encodeAVP('Subscription-Id-Data', '1'), encodeAVP('Subscription-Id-Type', 1)]))
    REQ_avps.append(encodeAVP('Framed-IP-Address', '192.168.0.1'))
    # Create message header (empty)
    CCR=HDRItem()
    # Set command code
    CCR.cmd=dictCOMMANDname2code("Credit-Control")
    # Set Application-id
    CCR.appId=APPLICATION_ID
    # Set Hop-by-Hop and End-to-End
    initializeHops(CCR)
    # Set Proxyable flag
    setFlags(CCR,DIAMETER_HDR_PROXIABLE)    
    # Add AVPs to header and calculate remaining fields
    ret=createReq(CCR,REQ_avps)
    # ret now contains CCR Request as hex string
    return ret        
    
def create_DPR():
    # Let's build DPR
    DPR_avps=[ ]
    DPR_avps.append(encodeAVP('Origin-Host', 'pgw.myrealm.example'))
    DPR_avps.append(encodeAVP('Origin-Realm', 'myrealm.example'))
    DPR_avps.append(encodeAVP('Disconnect-Cause', 'DO_NOT_WANT_TO_TALK_TO_YOU')) # tired :)
    DPR=HDRItem()
    DPR.cmd=dictCOMMANDname2code('Disconnect-Peer')
    initializeHops(DPR)
    # Add AVPs to header and calculate remaining fields
    msg=createReq(DPR,DPR_avps)
    # msg now contains DPR Request as hex string
    return msg

def create_Session_Id():
    #The Session-Id MUST be globally and eternally unique
    #<DiameterIdentity>;<high 32 bits>;<low 32 bits>[;<optional value>]
    now=datetime.datetime.now()
    ret=ORIGIN_HOST+";"
    ret=ret+str(now.year)[2:4]+"%02d"%now.month+"%02d"%now.day
    ret=ret+"%02d"%now.hour+"%02d"%now.minute+";"
    ret=ret+"%02d"%now.second+str(now.microsecond)+";"
    ret=ret+IDENTITY[2:16]
    return ret 
 
def dumpAVP(response):
    # adequart a string recebida para montar um json
    res=str(response)    
    res=res.replace("\',", "\':") # susbtituir o separador por :, apenas para os campos
    res=res.replace("(", "{") # trocar parentesis por chaves
    res=res.replace(")", "}") # trocar parentesis por chaves
    res=res.replace("u\'", "\'") # remover o u'
    res=res.replace("\'", "\"") # mudar aspas simples para duplas
    res=res.replace("\\", " ") # substituir as contrabarras que causam erros no loads
    # retorna dumped json. Para ler e necessario dar o loads.
    return res

if __name__ == "__main__":

    #logging.basicConfig(level=logging.DEBUG)
    LoadDictionary("../dictDiameter.xml")
    ################
    PCEF="192.168.10.20"
    HOST="192.168.10.10"
    PORT=3868
    ORIGIN_HOST="pgw.myrealm.example"
    ORIGIN_REALM="myrealm.example"
    IDENTITY="1234567890"                        
    APPLICATION_ID=16777238               
    # Let's assume that my Diameter messages will fit into 4k
    MSG_SIZE=65536
    # Connect to server
    Conn=Connect(HOST,PORT)
    ###########################################################
    # Let's build CER
    msg=create_CER()
    # msg now contains CER Request as hex string
    logging.debug("+"*30)
    # send data
    Conn.send(msg.decode("hex"))
    
    ###########################################################
    # RECEIVING CEA RESPONSE AND PARSING IT
    ###########################################################
    
    # Receive response
    received = Conn.recv(MSG_SIZE)
    # split header and AVPs
    CEA=HDRItem()
    stripHdr(CEA,received.encode("hex"))
    print "="*30
    print "THE CEA ANSWER IS:"
    msg=received.encode('hex')
    print "="*30
    H=HDRItem()
    stripHdr(H,msg)
    avps=splitMsgAVPs(H.msg)
    cmd=dictCOMMANDcode2name(H.flags,H.cmd)
    if cmd==ERROR:
     print 'Unknown command',H.cmd
    else:
     print cmd
     print "Hop-by-Hop=",H.HopByHop,"End-to-End=",H.EndToEnd,"ApplicationId=",H.appId
     print "="*30
     for avp in avps:
	# print "RAW AVP",avp
	print decodeAVP(avp)
    print "-"*30    
    # From CEA we needed Destination-Host and Destination-Realm
    Capabilities_avps=splitMsgAVPs(CEA.msg)
    #print Capabilities_avps
    DEST_HOST=findAVP("Origin-Host",Capabilities_avps)
    DEST_REALM=findAVP("Origin-Realm",Capabilities_avps)
    
    #############################################################
    # CREATE SESSION ID FOR NEW REQUESTS
    #############################################################
    
    #SESSION_ID=create_Session_Id()
    SESSION_ID='pgw.myrealm.example;1094791309121_1385989500_428022'
    
    #############################################################
    # CREATE CCR-I AND SEND IT TO PCRF AND PARSE IT
    #############################################################
    
    msg=create_CCR_I()
    # msg now contains CCR as hex string
    logging.debug("+"*30)
    # send data
    Conn.send(msg.decode("hex"))
    # Receive response
    received = Conn.recv(MSG_SIZE)
    
    # split header and AVPs
    CCA=HDRItem()
    stripHdr(CCA,received.encode("hex"))
    print "="*30
    print "THE CCA-I ANSWER IS:"
    msg=received.encode('hex')
    print "="*30
    H=HDRItem()
    stripHdr(H,msg)
    avps=splitMsgAVPs(H.msg)
    cmd=dictCOMMANDcode2name(H.flags,H.cmd)
    if cmd==ERROR:
     print 'Unknown command',H.cmd
    else:
     print cmd
     print "Hop-by-Hop=",H.HopByHop,"End-to-End=",H.EndToEnd,"ApplicationId=",H.appId
     print "="*30  
     message = "["
     for avp in avps:
	# print "RAW AVP",avp
      	message=message+str(dumpAVP(decodeAVP(avp)))+", "
    message=message+"]"
    message=message.replace(", ]", " ]")
    print message
	
    # Fazer na recepcao"
    loaded_message = json.loads(str(message))
    print str(loaded_message[0])

    print "-"*30    
    # From CCA we needed Destination-Host and Destination-Realm
    Capabilities_avps=splitMsgAVPs(CCA.msg)
    #print Capabilities_avps
    DEST_HOST=findAVP("Origin-Host",Capabilities_avps)
    DEST_REALM=findAVP("Origin-Realm",Capabilities_avps)
    
    ############################################################
    # Sending CCR-T message after user is logged off
    ############################################################
   
    msg=create_CCR_T()
    # msg now contains CCR as hex string
    logging.debug("+"*30)
    # send data
    Conn.send(msg.decode("hex"))
    # Receive response
    received = Conn.recv(MSG_SIZE)
    
    # split header and AVPs
    CCA=HDRItem()
    stripHdr(CCA,received.encode("hex"))
    print "="*30
    print "THE CCA-T ANSWER IS:"
    msg=received.encode('hex')
    print "="*30
    H=HDRItem()
    stripHdr(H,msg)
    avps=splitMsgAVPs(H.msg)
    cmd=dictCOMMANDcode2name(H.flags,H.cmd)
    if cmd==ERROR:
     print 'Unknown command',H.cmd
    else:
     print cmd
     print "Hop-by-Hop=",H.HopByHop,"End-to-End=",H.EndToEnd,"ApplicationId=",H.appId
     print "="*30
     for avp in avps:
    	# print "RAW AVP",avp
        print decodeAVP(avp)
    print "-"*30    
    # From CCA we needed Destination-Host and Destination-Realm
    Capabilities_avps=splitMsgAVPs(CCA.msg)
    #print Capabilities_avps
    DEST_HOST=findAVP("Origin-Host",Capabilities_avps)
    DEST_REALM=findAVP("Origin-Realm",Capabilities_avps)        
    
    ############################################################
    # Sending DPR message and closing connection
    ############################################################
    
  # Let's build DPR
    msg=create_DPR()
    # msg now contains CER Request as hex string
    logging.debug("+"*30)
    # send data
    Conn.send(msg.decode("hex"))
    
    ###########################################################
    # RECEIVING DPA RESPONSE AND PARSING IT
    ###########################################################
    
    # Receive response
    received = Conn.recv(MSG_SIZE)
    # split header and AVPs
    DPR=HDRItem()
    stripHdr(DPR,received.encode("hex"))
    print "="*30
    print "THE DPA ANSWER IS:"
    msg=received.encode('hex')
    print "="*30
    H=HDRItem()
    stripHdr(H,msg)
    avps=splitMsgAVPs(H.msg)
    cmd=dictCOMMANDcode2name(H.flags,H.cmd)
    if cmd==ERROR:
     print 'Unknown command',H.cmd
    else:
     print cmd
     print "Hop-by-Hop=",H.HopByHop,"End-to-End=",H.EndToEnd,"ApplicationId=",H.appId
     print "="*30
     for avp in avps:
	# print "RAW AVP",avp
        print decodeAVP(avp)
    print "-"*30    
    
    
    # And close the connection
    
    Conn.close()


