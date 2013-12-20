import com.ihsan.lib.remotequery as rqlib
import com.ihsan.util.xmlio as xutil
import sys, os, shutil
import zipfile
import pyFlexcel

def runQuery(config, params, returns):
  RQ = rqlib.RQSQL(config)
  RQ.handleOperation(params, returns)

def FormOnSetDataEx(uideflist, params):
  # procedure(uideflist: TPClassUIDefList; params: TPClassUIDataPacket)
  config = uideflist.config
  dtsid = params.FirstRecord.dtsid
  uideflist.PrepareReturnDataset()
  uipMain = uideflist.GetPClassUIByName('uipMain')
  if uipMain.Dataset.RecordCount > 0:
    rec = uipMain.Dataset.GetRecord(0)
  else:
    rec = uipMain.Dataset.AddRecord()
  rec.dtsid = int(dtsid)
  #uipTest = uideflist.GetPClassUIByName('uipMain')
  #tst = uipTest.Dataset.GetRecord(0)
  #raise Exception, tst.dtsid
  mlu = config.ModLibUtils
  rq = rqlib.RQSQL(config)
  rq.SELECTFROMClause = '''  
              SELECT 
              a.dtsformid,
              a.dtsformcode,
              a.dtsformdesc,
              a.tempready, 
              a.isempty,
              a.formtype,
              a.datasize
              FROM 
              DTSForm a, 
              DTSFile b, 
              DTSFolder c
  ''' 
  rq.WHEREClause = '''  
              a.dtsformid=b.dtsfileid 
              and b.dtsfolderid=c.dtsfolderid 
              and c.dtsid = %s
  ''' % str(dtsid)
  rq.keyFieldName = 'a.dtsformid'
  rq.setAltOrderFieldNames('a.dtsformid;a.dtsformcode;a.dtsformdesc;a.tempready;a.isempty;a.formtype;a.datasize')
  rq.setBaseOrderFieldNames('a.dtsformid')
  rq.columnSetting = '''
    object TColumnsWrapper
      Columns = <
        item
          Expanded = False
          FieldName = 'DTSFORMID'
          Title.Caption = 'ID'
          Visible = True
        end
        item
          Expanded = False
          FieldName = 'DTSFORMCODE'
          Title.Caption = 'Kode'
          Visible = True
        end
        item
          Expanded = False
          FieldName = 'DTSFORMDESC'
          Title.Caption = 'Deskripsi'
          Width = 400
          Visible = True
        end
        item
          Expanded = False
          FieldName = 'TEMPREADY'
          Title.Caption = 'Aktif'
          Visible = True
        end
        item
          Expanded = False
          FieldName = 'ISEMPTY'
          Title.Caption = 'Nihil'
          Visible = True
        end
        item
          Expanded = False
          FieldName = 'FORMTYPE'
          Title.Caption = 'Jenis'
          Visible = True
        end
        item
          Expanded = False
          FieldName = 'DATASIZE'
          Title.Caption = 'Ukuran Data'
          Visible = True
        end>
    end
      '''
  
  rq.initOperation(uideflist.DataPacket)
  pass

def PrepareForm(config, params, returns):        
  def recurseMeta(meta, valuableOnly=True, lv=0):
      output = []
      if len(meta.childrens) == 0:
          output.append((meta.name, meta.desc))
          return output
      else:
          lv+=1
          if (not valuableOnly) or (meta.hasValue):
              output.append((meta.name, meta.desc))
          for order, child in sorted(meta.childrens):
              output = recurseMeta(child, lv) + output
          lv-=1
          return output
  status = returns.CreateValues(["ErrMessage",""],["ProcTime",0.0])
  app = config.AppObject
  app.ConCreate('out')
  res = params.FirstRecord
  dtsid = res.dtsid
  dtsformid = res.dtsformid
  dtsformcode = res.dtsformcode
  if dtsformcode in ('BSMS1', 'BSMS45'):
    masterxls = config.HomeDir + 'templates\\mastervform.xls'
  else:
    masterxls = config.HomeDir + 'templates\\masterform.xls'
  storeDir  = config.HomeDir+'data\\DTS\\'
  xlsDir = config.HomeDir+'data\\templates\\'
  config.BeginTransaction()
  try:
    #read DTS from DB
    s = 'select * from dts where dtsid=%s' % str(dtsid)
    res = config.CreateSQL(s).RawResult
    dtsname = res.dtsname
    dtsloc = res.dtslocation
    xlsloc = res.templatelocation
    fullzipname = dtsloc + dtsname + '.zip'
    DTSzip = zipfile.ZipFile(fullzipname)
    zipRoot = DTSzip.namelist()[0].replace('/','')
    # if temp loc empty (create all)
    if xlsloc in (None, 'None', ''):
      #app.ConWriteln('template folders not exists, create a new one.')
      xlsloc = dtsloc.replace(storeDir, xlsDir)
      if not os.path.isdir(xlsloc):
        os.mkdir(xlsloc)
      DTSzip.extractall(xlsloc)
      xlsRoot = xlsloc + zipRoot
      for zp, zd, zf in os.walk(xlsRoot):
        for zzfile in zf:
          os.remove(zp+'\\'+zzfile)
      s = "update dts set templatelocation = '{0}' where dtsid={1}".format(xlsloc, str(dtsid))
      config.ExecSQL(s)
    else:
      #app.ConWriteln('template folders already exists, use existing folders.')
      pass
    config.Commit()
  except:
    config.Rollback()
    app.ConRead('hold')
    status.ErrMessage = str(sys.exc_info()[1])
    
  config.BeginTransaction()
  try:
    fname = dtsname
    #read Form from DB and Files
    rf = xutil.XMLFolder()
    rf.setRoot(dtsloc + zipRoot, False)
    s = "select a.dtsaliaslink, b.dtsfilename from dtsalias a,dtsfile b where a.dtsaliasloc=b.dtsfileid and a.dtsid=%s" % str(dtsid)
    res = config.CreateSQL(s).RawResult
    while not res.Eof:
      rf.addAlias(res.dtsaliaslink, res.dtsfilename)
      res.Next()
    procFile = rf.findFile('{0}.xsd'.format(dtsformcode))
    if len(procFile) < 1:
      raise Exception, 'file not found : {0}.xsd'.format(dtsformcode)
    procFile = procFile[0]
    readSchema = xutil.xbrlSchema(procFile.fileName, procFile.folder)
    schemaDir = procFile.folder.getFullPath()
    xlsDir = schemaDir.replace(storeDir, xlsDir)
    tempXLS = xlsDir + '\\%s.xls' % dtsformcode
    app.ConWriteln('Reading structure from file.')  
    readSchema.getMetaStructure(False)
    
    txls = pyFlexcel.Open(masterxls)
    txls.ActivateWorksheet("Report")
    app.ConWriteln('Getting {0} meta structure'.format(dtsformcode))
    metaProc = readSchema.metaStructure
    dataStructure = recurseMeta(metaProc)
    dataStructure.reverse()
    if dtsformcode in ('BSMS1', 'BSMS45'):
      xlsMaxCol = 650250
    else:
      xlsMaxCol = 250
    for idx in range(len(dataStructure)):
      app.ConWriteln('Setting field for {0}'.format(dataStructure[idx][0]))
      
      cCol = idx % xlsMaxCol 
      cPage  = idx / xlsMaxCol
      if cPage > 0:
        cSheet = "report{0}".format(str(cPage).zfill(2))
        if txls.IsWorksheetExist(cSheet)==0:
          txls.InsertSheet(cSheet)
        txls.ActivateWorksheet(cSheet)
      if dtsformcode in ('BSMS1', 'BSMS45'):
        txls.SetCellValue(cCol+2, 1, dataStructure[idx][0])
        txls.SetCellValue(cCol+2, 2, dataStructure[idx][1]) 
      else:
        txls.SetCellValue(1,cCol+1, dataStructure[idx][0])
        txls.SetCellValue(2,cCol+1, dataStructure[idx][1]) 
    app.ConWriteln('Creating template for : {0}'.format(dtsformcode))
    txls.SaveAs(tempXLS)
    config.Commit()
  except:
    config.Rollback()
    app.ConRead('Error')
    status.ErrMessage = str(sys.exc_info()[1])

def PrepareEmptyForm(config, params, returns):        
  status = returns.CreateValues(["ErrMessage",""],["ProcTime",0.0])
  app = config.AppObject
  app.ConCreate('out')
  res = params.FirstRecord
  dtsid = res.dtsid
  dtsformid = res.dtsformid
  dtsformcode = res.dtsformcode
  storeDir  = config.HomeDir+'data\\DTS\\'
  xlsDir = config.HomeDir+'data\\templates\\'
  config.BeginTransaction()
  try:
    s = '''
      update dtsform set formtype='N', isempty='T', tempready='T' where dtsformid = %s
    ''' % str(dtsformid)
    config.ExecSQL(s)
    config.Commit()
  except:
    config.Rollback()
    app.ConRead('Error')
    status.ErrMessage = str(sys.exc_info()[1])
