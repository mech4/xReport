import com.ihsan.foundation.pobjecthelper as phelper
import sys, os

def FormOnSetDataEx(uideflist, params):
  # procedure(uideflist: TPClassUIDefList; params: TPClassUIDataPacket)
  rec = params.FirstRecord
  config = uideflist.config
  fid = rec.fid
  fName = rec.fName
  tempLoc = rec.tempLoc
  fieldNum = rec.fieldNum
  #retreuve dtsid
  s = '''
    select a.dtsid from dtsfolder a,dtsfile b
    where a.dtsfolderid=b.dtsfolderid
    and b.dtsfileid=%s
  ''' % str(fid)
  dtsid = config.CreateSQL(s).RawResult.dtsid
  #raise Exception, "{0}:[{1}]{2} - {3}".format(fid,fLevel,fCode,fDesc)
  s = '''
    select * from dtsmap where dtsformid=%s
  ''' % str(fid)
  dtsmap = config.CreateSQL(s).RawResult
  if not dtsmap.Eof:
    s = '''
      select * from dtsmapquery where dtsmapid=%s
    ''' % dtsmap.dtsmapid
    mapquery = config.CreateSQL(s).RawResult
    if not mapquery.Eof:
      key = 'PObj:DTSMapQuery#DTSMapQueryId=%s' % str(mapquery.dtsmapqueryid)
      uideflist.SetData('uipQuery', key)
      formContent = uideflist.uipQuery.Dataset.GetRecord(0)
      formContent.IsNew = 'F'
      formContent.dtsformid = fid
      formContent.AssignCode = fName
      formContent.qid = mapquery.dtsmapqueryid
      formContent.fieldNum = fieldNum
      formContent.dtsid = dtsid
    else:
      uipData = uideflist.uipQuery
      newData = uipData.Dataset.AddRecord()
      newData.AssignCode = fName
      newData.QueryString = tempLoc
      newData.IsNew = 'T'
      newData.dtsformid = fid
      newData.DTSMapId = dtsmap.dtsmapid
      newData.qid = 0
      newData.fieldNum = fieldNum
      newData.dtsid = dtsid
  else:
    uipData = uideflist.uipQuery
    newData = uipData.Dataset.AddRecord()
    newData.AssignCode = fName
    newData.QueryString = tempLoc
    newData.IsNew = 'T'
    newData.dtsformid = fid
    newData.qid = 0
    newData.fieldNum = fieldNum
    newData.dtsid = dtsid
  
def saveQry(config, parameter, returns):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)
  rec = parameter.FirstRecord
  qryText = rec.qryText
  fid = rec.fid
  mid = rec.mid
  qid = rec.qid
  mlu = config.ModLibUtils
  tempLoc = rec.tempLoc
  fieldNum = rec.fieldNum
  status = returns.CreateValues(
      ['ErrMessage', ''],
      ['mid', 0],
      ['qid', 0]
  )
  helper = phelper.PObjectHelper(config)
  config.BeginTransaction()
  try:
    if fid in (None,'',0):
      raise Exception, 'no way we get thru here without dtsformid'
    if tempLoc in (None,'',0):
      raise Exception, 'we must be here by an accident'
    if qryText in (None,'',0):
      raise Exception, "isn't this handled in client side" 
    #check query validity
    todayDate = mlu.DecodeDate(mlu.Now())
    startDate = mlu.EncodeDate(todayDate[0], todayDate[1], 1)
    sdstr = mlu.DecodeDate(startDate)
    startDateStr = '{0}-{1}-{2}'.format(sdstr[0], sdstr[1], sdstr[2]) 
    if todayDate[1]<12:
      endDate = mlu.EncodeDate(todayDate[0], todayDate[1]+1, 1)-1
    else: 
      endDate = mlu.EncodeDate(todayDate[0]+1, 1, 1)-1
    edstr = mlu.DecodeDate(endDate)
    endDateStr = '{0}-{1}-{2}'.format(edstr[0], edstr[1], edstr[2])
    qryParam = {
      '_startdate' : mlu.QuotedStr(startDateStr),
      '_enddate' : mlu.QuotedStr(endDateStr),
      '_branchlist' : mlu.QuotedStr('000'), 
    }
    testText = qryText
    for varkey in qryParam.keys():
      testText = testText.replace(varkey, qryParam[varkey])
    tes = config.CreateSQL(testText).RawResult
    if tes.FieldCount!=fieldNum:
      raise Exception, 'Query returned {0} fields, while {1} fields expected'.format(tes.FieldCount,fieldNum)
    #query valid
    if mid in (None,'',0):
      #raise Exception, 'only formid, no map nor query'
      #create map here
      newMap = helper.CreatePObject('DTSMap')
      newMap.DTSFormId = fid
      newMap.DTSMapType = 'A'
      mid = newMap.DTSMapId
      status.mid = mid
    QueryFile = open(tempLoc, 'w')
    QueryFile.write(qryText)
    QueryFile.close()
    if qid in (None,'',0):
      #raise Exception, 'got formid and mapid, but no queryid'
      #create query here
      #set flag update or nevermind
      newQuery = helper.CreatePObject('DTSMapQuery')
      newQuery.DTSMapId = mid
      newQuery.QueryString = tempLoc
      qid = newQuery.DTSMapQueryId
      status.qid = qid
    else:
      updQuery = helper.GetObject('DTSMapQuery', qid)
      if updQuery.QueryString != tempLoc:
        updQuery.QueryString = tempLoc 
    #raise Exception, (fid,mid,qid,qryText,tempLoc)
    config.Commit()
  except:
    config.Rollback()
    status.ErrMessage = str(sys.exc_info()[1])

  return 1

def LoadQueryFromFile(config, parameter, returns):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)
  rec = parameter.FirstRecord
  tempLoc = rec.tempLoc
  status = returns.CreateValues(
      ['ErrMessage', ''],
      ['qryText', '']
  )
  try:
    QueryFile = open(tempLoc, 'r')
    status.qryText = QueryFile.read()
    QueryFile.close()
  except:
    status.ErrMessage = str(sys.exc_info()[1])

def deleteQry(config, parameter, returns):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)
  rec = parameter.FirstRecord
  fid = rec.fid
  mid = rec.mid
  qid = rec.qid
  tempLoc = rec.tempLoc
  status = returns.CreateValues(
      ['ErrMessage', '']
  )
  helper = phelper.PObjectHelper(config)
  config.BeginTransaction()
  try:
    if fid in (None,'',0):
      raise Exception, 'no way we get thru here without dtsformid'
    if tempLoc in (None,'',0):
      raise Exception, 'we must be here by an accident'
    if mid in (None,'',0):
      raise Exception, 'only formid, no map nor query'
    if qid in (None,'',0):
      raise Exception, 'got formid and mapid, but no queryid'
    else:
      delQuery = helper.GetObject('DTSMapQuery', qid)
      delQuery.Delete()
      delMap = helper.GetObject('DTSMap', mid)
      delMap.Delete()
    #raise Exception, (fid,mid,qid,qryText,tempLoc)
    os.remove(tempLoc)
    config.Commit()
  except:
    config.Rollback()
    status.ErrMessage = str(sys.exc_info()[1])

  return 1
