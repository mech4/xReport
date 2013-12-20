import com.ihsan.lib.remotequery as rqlib

def runQuery(config, params, returns):
  RQ = rqlib.RQSQL(config)
  RQ.handleOperation(params, returns)

def FormOnSetDataEx(uideflist, params):
  # procedure(uideflist: TPClassUIDefList; params: TPClassUIDataPacket)
  config = uideflist.config
  dtsid = params.FirstRecord.dtsid
  uideflist.PrepareReturnDataset()
  mlu = config.ModLibUtils
  rq = rqlib.RQSQL(config)
  rq.SELECTFROMClause = '''  
              SELECT a.dtsaliasid,a.dtsaliaslink,b.dtsfilename 
              from dtsalias a, dtsfile b
  ''' 
  rq.WHEREClause = '''  
              a.dtsaliasloc = b.dtsfileid
              and a.dtsid = %s
  ''' % str(dtsid)
  rq.columnSetting = '''
object TColumnsWrapper
  Columns = <
    item
      Expanded = False
      FieldName = 'DTSALIASID'
      Title.Caption = 'ID'
      Visible = True
    end
    item
      Expanded = False
      FieldName = 'DTSALIASLINK'
      Title.Caption = 'Alias Link'
      Width = 508
      Visible = True
    end
    item
      Expanded = False
      FieldName = 'DTSFILENAME'
      Title.Caption = 'Nama File'
      Width = 171
      Visible = True
    end>
end
  '''
  rq.keyFieldName = 'dtsaliasid'
  rq.setAltOrderFieldNames('dtsaliasid;dtsaliaslink;dtsfilename')
  rq.setBaseOrderFieldNames('dtsaliasid')
  
  rq.initOperation(uideflist.DataPacket)
  pass

