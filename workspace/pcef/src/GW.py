#!/usr/bin/env python
                         
#Next two lines are to include parent directory for testing
import sys
import json
sys.path.append("..")
# Remove them normally

#from libDiameter import *
from libDiameter import LoadDictionary, Connect, logging
from libDiameter import  HDRItem, stripHdr
from libDiameter import dictCOMMANDcode2name, ERROR
from libDiameter import splitMsgAVPs, findAVP, decodeAVP
from pcef import PCEF
from http import HTTP

# COMMUNICATION
if __name__ == "__main__":
    # Construct PCEF object
    pcef= PCEF()

    #logging.basicConfig(level=logging.DEBUG)
    LoadDictionary("../diameter/dictDiameter.xml")
    ################
    # Connect to server
    Conn=Connect(pcef.PCRF,pcef.PCRF_PORT)
    ###########################################################
    # Let's build CER
    msg=pcef.create_CER()
    # msg now contains CER Request as hex string
    logging.debug("+"*30)
    # send data
    Conn.send(msg.decode("hex"))
    
    ###########################################################
    # RECEIVING CEA RESPONSE AND PARSING IT
    ###########################################################
    
    # Receive response
    received = Conn.recv(pcef.MSG_SIZE)
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
    # CREATE CCR-I AND SEND IT TO PCRF AND PARSE IT
    #############################################################
    msg=pcef.create_CCR_I(DEST_REALM)
    # msg now contains CCR as hex string
    logging.debug("+"*30)
    # send data
    Conn.send(msg.decode("hex"))
    # Receive response
    received = Conn.recv(pcef.MSG_SIZE)
    
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
        message=message+str(pcef.dumpAVP(decodeAVP(avp)))+", "
        
    message=message+"]"
    message=message.replace(", ]", " ]")
    
    #############################################################
    # SEND CCR-I ANSWER AS JSON
    #############################################################
    # Construct objects
    http = HTTP()
    print http.POST(pcef.OCS, message)


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
   
    msg=pcef.create_CCR_T(DEST_REALM)
    # msg now contains CCR as hex string
    logging.debug("+"*30)
    # send data
    Conn.send(msg.decode("hex"))
    # Receive response
    received = Conn.recv(pcef.MSG_SIZE)
    
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
    msg=pcef.create_DPR()
    # msg now contains CER Request as hex string
    logging.debug("+"*30)
    # send data
    Conn.send(msg.decode("hex"))
    
    ###########################################################
    # RECEIVING DPA RESPONSE AND PARSING IT
    ###########################################################
    
    # Receive response
    received = Conn.recv(pcef.MSG_SIZE)
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
