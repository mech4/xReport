import os
import sys
import com.ihsan.lib.remotequery as remotequery
import com.ihsan.util.modman as modman
import types
import rpdb2

LOOKUP_BASE_FOLDER = "lookups"

def runQuery(config, params, returns):
  #rpdb2.start_embedded_debugger("000")
  app = config.AppObject
  dsrequest = params.request
  recrequest = dsrequest.GetRecord(0)
  sessionName = recrequest.sessionname
  separator = '://'
  i = sessionName.find(separator)
  if i >= 0:
    system_id = sessionName[0:i]
    sessionName = sessionName[i + len(separator):]
    recrequest.sessionname = sessionName
    ph = app.CreatePacket()
    ph.Packet.AcquireAnotherPacket(params)
    phres = app.rexecscript(system_id, 'dialogs@lookups/fGenLookup_data.runQuery', ph)
    returns.AcquireAnotherPacket(phres.Packet)
  else:
    rqsql = remotequery.RQSQL(config)
    rqsql.handleOperation(params, returns)
#--

def initQuery(config, params, returns):
  #rpdb2.start_embedded_debugger("000")
  app = config.AppObject
  mlu = config.ModLibUtils
  fr = params.FirstRecord
  lookup_id = fr.lookup_id
  # lookup modules are stored under script_modules/lookups folder
  # lookup_id can be in format module_name@class_name
  # by default class_name is lookup
  les = lookup_id.split("@", 1)
  if len(les) == 1:
    lookup_module_id = lookup_id
    lookup_class_id = "lookup"
  else:
    lookup_module_id = les[0]
    lookup_class_id = les[1]
  #==  
  
  separator = '://' 
  i = lookup_module_id.find(separator)
  if i >= 0:
    system_id = lookup_module_id[0:i]
    lookup_module_id = lookup_module_id[i + len(separator):]
    if config.MapAppNameSpace(system_id) != '': # local RPC
      module_id = "%s.%s" % (LOOKUP_BASE_FOLDER, lookup_module_id)
      lookup_module = modman.getRefModule(config, system_id, module_id)
      isExternal = False
    else:
      isExternal = True
  else:
    system_id = ''
    module_id = "%s.%s" % (LOOKUP_BASE_FOLDER, lookup_module_id)
    lookup_module = modman.getModule(config, module_id)
    isExternal = False    

  if not isExternal: # local or local RPC
    lookup_class = lookup_module.__dict__.get(lookup_class_id)
    if type(lookup_class) is not types.ClassType:
      raise Exception, "%s is not a class in lookup module %s" % (lookup_class_id, lookup_module_id)
    try:
      lookupInst = lookup_class(config, fr)
    except:
      errMsg = str(sys.exc_info()[1])
      raise Exception, "Error instantiating class %s in lookup module %s\r\n.Details: %s" % (lookup_class_id, lookup_module_id, errMsg)
    #--
    rqsql = remotequery.RQSQL(config)
    lookupInst.initQueryObject(rqsql)
    try:
      rqsql.initOperation(returns)
      isErr = 0
      errMsg = ""
      rowCount = rqsql.rowCount
    except:
      isErr = 1
      errMsg = str(sys.exc_info()[1])
      rowCount = 0 
    #--
    dsStatus = returns.AddNewDatasetEx("status", "isErr: integer; errMsg: string; rowCount: integer")
    recStatus = dsStatus.AddRecord()
    recStatus.isErr = isErr
    recStatus.errMsg = errMsg
    recStatus.rowCount = rowCount
  else:
    ph = config.AppObject.CreatePacket()
    ph.Packet.AcquireAnotherPacket(params)
    fr = ph.FirstRecord
    fr.lookup_id = '%s@%s' % (lookup_module_id, lookup_class_id) 
    phres = app.rexecscript(system_id, 'dialogs@lookups/fGenLookup_data.initQuery', ph)
    packetres = phres.Packet
    dsstatus = packetres.status
    recstatus = dsstatus.GetRecord(0)
    if not recstatus.isErr: # modify the query session result
      dsInfo = packetres.__rtblresult
      recinfo = dsInfo.GetRecord(0)
      recinfo.resultid = '%s://%s' % (system_id, recinfo.resultid)  
      pass
    #--
    returns.AcquireAnotherPacket(packetres)
  #--  
#--
  