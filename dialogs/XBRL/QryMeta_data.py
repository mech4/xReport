import com.ihsan.lib.remotequery as rqlib
import sys

def runQuery(config, params, returns):
  RQ = rqlib.RQSQL(config)
  RQ.handleOperation(params, returns)

def FormOnSetDataEx(uideflist, params):
  # procedure(uideflist: TPClassUIDefList; params: TPClassUIDataPacket)
  config = uideflist.config
  uideflist.PrepareReturnDataset()
  filtering = ''
  if params.FirstRecord:
    prm = params.FirstRecord
    filtering += 'and '
    fid = prm.fid
    fName = prm.fName
    filtering += 'dtsformid=%s' % str(fid)
    uip = uideflist.uipart1
    rec = uip.Dataset.AddRecord()
    rec.fid = fid
    rec.fName = fName
  mlu = config.ModLibUtils
  rq = rqlib.RQSQL(config)
  rq.columnSetting = '''
object TColumnsWrapper
  Columns = <
    item
      Expanded = False
      FieldName = 'dtsmetaid'
      Title.Caption = 'ID'
      Visible = True
    end
    item
      Expanded = False
      FieldName = 'metaname'
      Title.Caption = 'Kode'
      Visible = True
    end
    item
      Expanded = False
      FieldName = 'metatype'
      Title.Caption = 'Tipe Data'
      Visible = True
    end
    item
      Expanded = False
      FieldName = 'metadesc'
      Title.Caption = 'Deskripsi'
      Width = 400
      Visible = True
    end
    item
      Expanded = False
      FieldName = 'metaenum'
      Title.Caption = 'Nama Enum'
      Visible = True
    end>
end
  '''
  rq.SELECTFROMClause = '''  
              select 
              dtsmetaid,
              metaname, 
              metatype, 
              metadesc, 
              metaenum 
              from dtsmeta
  ''' 
  rq.WHEREClause = '''  
              metatype<>'Empty' {0}
  '''.format(filtering)
  rq.keyFieldName = 'dtsmetaid'
  rq.setAltOrderFieldNames('dtsmetaid;metaname;metatype;metadesc;metaenum')
  rq.setBaseOrderFieldNames('dtsmetaid')
  
  rq.initOperation(uideflist.DataPacket)
  pass

