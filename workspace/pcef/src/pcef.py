#!/usr/bin/env python                      
#Next two lines are to include parent directory for testing
import sys
import datetime
sys.path.append("..")
from libDiameter import encodeAVP, HDRItem, dictCOMMANDname2code
from libDiameter import initializeHops, createReq, setFlags
from libDiameter import DIAMETER_HDR_PROXIABLE

class PCEF:
    PCEF="192.168.10.20"
    PCRF="192.168.10.10"
    OCS="http://127.0.0.1:10000"
    PCRF_PORT=3868
    ORIGIN_HOST="pgw.myrealm.example"
    ORIGIN_REALM="myrealm.example"
    IDENTITY="1234567890"                        
    APPLICATION_ID=16777238               
    MSG_SIZE=4096 # Let's assume that my Diameter messages will fit into 4k
    SESSION_ID='pgw.myrealm.example;1094791309121_1385989500_428022'    
    
    def create_CER(self):
        # Let's build CER
        CER_avps=[]
        CER_avps.append(encodeAVP("Origin-Host", self.ORIGIN_HOST))
        CER_avps.append(encodeAVP("Origin-Realm", self.ORIGIN_REALM))
        CER_avps.append(encodeAVP('Host-IP-Address', self.PCEF))
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
    
    
    def create_CCR_I(self, DEST_REALM):
        # Let's build Server-AssignmentRequest
        REQ_avps=[]
        REQ_avps.append(encodeAVP("Session-Id", self.SESSION_ID))
        REQ_avps.append(encodeAVP("Destination-Realm", DEST_REALM))
        REQ_avps.append(encodeAVP("Origin-Host", self.ORIGIN_HOST))
        REQ_avps.append(encodeAVP("Origin-Realm", self.ORIGIN_REALM))
        REQ_avps.append(encodeAVP('Auth-Application-Id', 16777238))
        REQ_avps.append(encodeAVP('CC-Request-Type', 1))
        REQ_avps.append(encodeAVP('CC-Request-Number', 0))
        REQ_avps.append(encodeAVP('Subscription-Id',[encodeAVP('Subscription-Id-Data', '1234567890'), encodeAVP('Subscription-Id-Type', 0)]))
        REQ_avps.append(encodeAVP('Subscription-Id',[encodeAVP('Subscription-Id-Data', '1'), encodeAVP('Subscription-Id-Type', 1)]))
        REQ_avps.append(encodeAVP('Framed-IP-Address', self.PCEF))
        # Create message header (empty)
        CCR=HDRItem()
        # Set command code
        CCR.cmd=dictCOMMANDname2code("Credit-Control")
        # Set Application-id
        CCR.appId=self.APPLICATION_ID
        # Set Hop-by-Hop and End-to-End
        initializeHops(CCR)
        # Set Proxyable flag
        setFlags(CCR,DIAMETER_HDR_PROXIABLE)    
        # Add AVPs to header and calculate remaining fields
        ret=createReq(CCR,REQ_avps)
        # ret now contains CCR Request as hex string
        return ret 
    
    def create_CCR_T(self, DEST_REALM):
        # Let's build Server-AssignmentRequest
        REQ_avps=[]
        REQ_avps.append(encodeAVP("Session-Id", self.SESSION_ID))
        REQ_avps.append(encodeAVP("Destination-Realm", DEST_REALM))
        REQ_avps.append(encodeAVP('Auth-Application-Id', 16777238))
        REQ_avps.append(encodeAVP("Origin-Host", self.ORIGIN_HOST))
        REQ_avps.append(encodeAVP("Origin-Realm", self.ORIGIN_REALM))
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
        CCR.appId=self.APPLICATION_ID
        # Set Hop-by-Hop and End-to-End
        initializeHops(CCR)
        # Set Proxyable flag
        setFlags(CCR,DIAMETER_HDR_PROXIABLE)    
        # Add AVPs to header and calculate remaining fields
        ret=createReq(CCR,REQ_avps)
        # ret now contains CCR Request as hex string
        return ret        
        
    def create_DPR(self):
        # Let's build DPR
        DPR_avps=[ ]
        DPR_avps.append(encodeAVP('Origin-Host', self.ORIGIN_HOST))
        DPR_avps.append(encodeAVP('Origin-Realm', self.ORIGIN_REALM))
        DPR_avps.append(encodeAVP('Disconnect-Cause', 'DO_NOT_WANT_TO_TALK_TO_YOU')) 
        DPR=HDRItem()
        DPR.cmd=dictCOMMANDname2code('Disconnect-Peer')
        initializeHops(DPR)
        # Add AVPs to header and calculate remaining fields
        msg=createReq(DPR,DPR_avps)
        # msg now contains DPR Request as hex string
        return msg
    
    def create_Session_Id(self):
        #The Session-Id MUST be globally and eternally unique
        #<DiameterIdentity>;<high 32 bits>;<low 32 bits>[;<optional value>]
        now=datetime.datetime.now()
        ret=self.ORIGIN_HOST+";"
        ret=ret+str(now.year)[2:4]+"%02d"%now.month+"%02d"%now.day
        ret=ret+"%02d"%now.hour+"%02d"%now.minute+";"
        ret=ret+"%02d"%now.second+str(now.microsecond)+";"
        ret=ret+self.IDENTITY[2:16]
        return ret 
       
    def dumpAVP(self, response):
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
