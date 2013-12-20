import com.ihsan.lib.remotequery as rqlib

def runQuery(config, params, returns):
  RQ = rqlib.RQSQL(config)
  RQ.handleOperation(params, returns)

def FormOnSetDataEx(uideflist, params):
  # procedure(uideflist: TPClassUIDefList; params: TPClassUIDataPacket)
  config = uideflist.config
  uideflist.PrepareReturnDataset()
  mlu = config.ModLibUtils
  rq = rqlib.RQSQL(config)
  rq.SELECTFROMClause = '''  
              SELECT DTSId,DTSName,PeriodType from DTS
  ''' 
  rq.WHEREClause = '''  
              1 = 1
  '''
  rq.columnSetting = '''
object TColumnsWrapper
  Columns = <
    item
      Expanded = False
      FieldName = 'DTSID'
      Title.Caption = 'ID'
      Visible = True
    end
    item
      Expanded = False
      FieldName = 'DTSNAME'
      Title.Caption = 'Taxonomy'
      Visible = True
    end
    item
      Expanded = False
      FieldName = 'PERIODTYPE'
      Title.Caption = 'Jenis Periode'
      Visible = True
    end>
end
  '''
  rq.keyFieldName = 'DTSId'
  rq.setAltOrderFieldNames('DTSId;DTSName;PeriodType')
  rq.setBaseOrderFieldNames('DTSId')
  
  rq.initOperation(uideflist.DataPacket)
  pass

