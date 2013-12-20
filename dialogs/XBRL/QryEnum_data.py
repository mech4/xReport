import com.ihsan.lib.remotequery as rqlib
import sys

def runQuery(config, params, returns):
  RQ = rqlib.RQSQL(config)
  RQ.handleOperation(params, returns)

def FormOnSetDataEx(uideflist, params):
  # procedure(uideflist: TPClassUIDefList; params: TPClassUIDataPacket)
  config = uideflist.config
  dtsid = params.FirstRecord.dtsid
  try:
    fid = params.FirstRecord.fid
    s = '''
      select distinct metaenum from dtsmeta where dtsformid=%s and metaenum is not null
    ''' % str(fid)
    meList = config.CreateSQL(s).RawResult
    i = 0
    enumnamelist = '''
      and dtsenumname in (
    '''
    while not meList.Eof:
      if i>0:
        enumnamelist +=', '
      enumnamelist += "'{0}'".format(meList.metaenum)
      i+=1
      meList.Next()
    enumnamelist += ')'
  except:
    enumnamelist = ''
    fid = 0
    pass    
  s = '''
    select distinct dtsenumname from dtsenum where dtsid={0} {1}
  '''.format(str(dtsid),enumnamelist)
  res = config.CreateSQL(s).RawResult
  firstPickName = res.dtsenumname
  try:
    enumname = params.FirstRecord.enumname
    iindex = params.FirstRecord.iIndex
  except:
    enumname = firstPickName
    iindex = 0
    pass
  uideflist.PrepareReturnDataset()
  mlu = config.ModLibUtils
  rq = rqlib.RQSQL(config)
  rq.SELECTFROMClause = '''  
              SELECT DTSEnumValue, DTSEnumDesc
              FROM DTSEnum
  ''' 
  rq.WHEREClause = '''  
              DTSId = %s
              and DTSEnumName = '%s'
  ''' % (str(dtsid), enumname)
  rq.columnSetting = '''
object TColumnsWrapper
  Columns = <
    item
      Expanded = False
      FieldName = 'DTSENUMVALUE'
      Title.Caption = 'Sandi'
      Visible = True
    end
    item
      Expanded = False
      FieldName = 'DTSENUMDESC'
      Title.Caption = 'Keterangan'
      Width = 508
      Visible = True
    end>
end
  '''
  rq.keyFieldName = 'DTSEnumValue'
  rq.setAltOrderFieldNames('DTSEnumValue;DTSEnumDesc')
  rq.setBaseOrderFieldNames('DTSEnumValue')
  
  rq.initOperation(uideflist.DataPacket)
  uip = uideflist.uipart1
  if uip.Dataset.RecordCount == 0:
    rec = uideflist.uipart1.Dataset.AddRecord()
  else:
    rec = uideflist.uipart1.Dataset.GetRecord(0)
  rec.dtsid = dtsid
  rec.enumIndex = iindex
  rec.fid = fid
  pass

def GetEnumNames(config, params, returns):
  status = returns.CreateValues(['Err', ''])
  nameList = returns.AddNewDatasetEx('eList','item:string')
  dtsid = params.FirstRecord.dtsid
  fid = params.FirstRecord.fid
  config.BeginTransaction()
  try:
    enumnamelist = ''
    if fid>0:
      s = '''
        select distinct metaenum from dtsmeta where dtsformid=%s and metaenum is not null
      ''' % str(fid)
      meList = config.CreateSQL(s).RawResult
      i = 0
      enumnamelist = '''
        and dtsenumname in (
      '''
      while not meList.Eof:
        if i>0:
          enumnamelist +=', '
        enumnamelist += "'{0}'".format(meList.metaenum)
        i+=1
        meList.Next()
      enumnamelist += ')'
    s = '''
      select distinct dtsenumname from dtsenum where dtsid={0} {1}
    '''.format(str(dtsid),enumnamelist)
    res = config.CreateSQL(s).RawResult
    while not res.Eof:
      rec = nameList.AddRecord()
      rec.item = res.dtsenumname
      res.Next()
    config.Commit()
  except:
    config.Rollback()
    status.Err = str(sys.exc_info()[1])