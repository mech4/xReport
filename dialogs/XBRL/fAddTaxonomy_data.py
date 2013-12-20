import sys, os, shutil
import zipfile
import com.ihsan.util.xmlio as xutil
import com.ihsan.foundation.pobjecthelper as phelper
import pyFlexcel

def FormOnSetDataEx(uideflist, params):
  #rf = xutil.XMLFolder('Test')
  #raise Exception, rf.folderName
  pass

def ProsesDTS(config, params, returns):        
  swfile = params.GetStreamWrapper(0)             
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
  startTime = config.ModLibUtils.Now()
  app = config.AppObject
  app.ConCreate('out')
  helper = phelper.PObjectHelper(config)
  res = params.FirstRecord
  periode = res.periode
  processFlag = res.processFlag
  masterxls = config.HomeDir + 'templates\\masterform.xls'
  config.BeginTransaction()
  try:
    formList = returns.AddNewDatasetEx(
       'fList',
       ';'.join([
       'kode:string',
       'nama:string',
       'proc:string'
       ])
    )
    storeDir  = config.HomeDir+'data\\DTS\\'
    xlsDir = config.HomeDir+'data\\templates\\' 
    # Prepare DTS Location
    fname = swfile.Name
    #fname = 'LBUSv21'  # for testing purpose
    fullfname = storeDir+fname+('.zip')
    # If same name exist, create alternative location
    if os.path.exists(fullfname):
      i = 1
      while os.path.exists(fullfname):
        nDir = storeDir + '%s\\' % str(i).zfill(4) 
        xnDir = xlsDir + '%s\\' % str(i).zfill(4) 
        fullfname = nDir+fname+'.zip'
        i+=1
      storeDir = nDir
      xlsDir = xnDir
      if not os.path.isdir(storeDir):
        os.mkdir(storeDir)
      if not os.path.isdir(xlsDir):
        os.mkdir(xlsDir)
    # save uploaded file
    swfile.SaveToFile(fullfname)
    #app.ConWriteln('File Saved : %s' % str(fullfname))
    app.ConWriteln('DTS successfully uploaded.')
    # Extract DTS zip file
    DTS = zipfile.ZipFile(fullfname)
    DTS.extractall(storeDir)
    #app.ConWriteln('File Extracted to : %s' % str(storeDir))
    app.ConWriteln('DTS successfully extracted.')
    zipRoot = DTS.namelist()[0].replace('/','')
    dtsRoot = storeDir+zipRoot
    xlsRoot = xlsDir+zipRoot
    if not os.path.isdir(xlsRoot):
      os.mkdir(xlsRoot)
    # Read DTS Structure
    #startTime = config.ModLibUtils.Now()
    rf = xutil.XMLFolder()
    rf.setRoot(dtsRoot)
    #endTime = config.ModLibUtils.Now()
    #ProcTime = endTime-startTime
    #status.ProcTime = ProcTime
    #app.ConWriteln(rf.getFullPath())
    # Save Structure to DB
    NewDTS = helper.CreatePObject('DTS')
    NewDTS.DTSName = fname
    NewDTS.PeriodType = periode
    NewDTS.DTSLocation = storeDir
    DTSTree = rf.walk()
    DTSTree.reverse()
    parentPool = {}
    xsdPool = {}
    for memberList in DTSTree:
      fRec = memberList[0]
      app.ConWriteln('Processing Folder : {0}'.format(fRec.folderName))
      NewFolder = helper.CreatePObject('DTSFolder')
      NewFolder.DTSId = NewDTS.DTSId
      NewFolder.DTSFolderName = fRec.folderName
      parentPool[fRec.folderId] = NewFolder.DTSFolderId
      if fRec.parent != None:
        NewFolder.ParentId = parentPool[fRec.parent.folderId]
      fileList = memberList[2]
      tempDir = fRec.getFullPath()
      createDir = tempDir.replace(storeDir, xlsDir, 1)
      if not os.path.isdir(createDir):
        os.mkdir(createDir)
      n = 0
      for files in fileList:
        n+=1
        if files.__class__.__name__ == 'xbrlSchema':
          # handle for form
          if files.schemaType == 'form':
            NewFile = helper.CreatePObject('DTSForm')
            NewFile.DTSFileName = files.fileName
            app.ConWriteln('Processing File : {0}'.format(files.fileName))
            NewFile.DTSFolderId = NewFolder.DTSFolderId
            xsdPool[files.fileId] = NewFile.DTSFileId
            NewFile.DTSFileType = files.schemaType
            NewFile.DTSFormCode = files.schemaCode
            fDesc = files.rootElement.seek('definition')
            if len(fDesc) > 0:
              fDesc = fDesc[0].text
            else:
              fDesc = ''
            NewFile.DTSFormDesc = fDesc 
            NewFile.TempReady = 'F' #set default to False for individual proc 
            NewFile.IsEmpty = 'T' #set default to True before mapping exists
            NewFile.FormType = 'N' #set default to Null before mapping exists 
            NewFile.DataSize = 'S' #set default to Small before mapping exists 
            rec = formList.AddRecord()
            rec.kode = files.schemaCode
            rec.nama = files.fileName
            #moved to individual process (global process takes too long)
            if 1==2:
              rec.proc = 'T'
              tempXLS = createDir + '\\%s.xls' % files.schemaCode 
              files.getMetaStructure()
              
              txls = pyFlexcel.Open(masterxls)
              txls.ActivateWorksheet("report")
              app.ConWriteln('Getting {0} meta structure'.format(files.schemaCode))
              metaProc = files.metaStructure
              dataStructure = recurseMeta(metaProc)
              dataStructure.reverse()
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
                txls.SetCellValue(1,cCol+1, dataStructure[idx][0])
                txls.SetCellValue(2,cCol+1, dataStructure[idx][1]) 
              app.ConWriteln('Creating template for : {0}'.format(files.schemaCode))
              txls.SaveAs(tempXLS)
            else:
              rec.proc = 'F'
          else:
            # handle for dict
            NewFile = helper.CreatePObject('DTSFile')
            app.ConWriteln('Processing File : {0}'.format(files.fileName))
            NewFile.DTSFileName = files.fileName
            NewFile.DTSFolderId = NewFolder.DTSFolderId
            NewFile.DTSFileType = files.schemaType
            xsdPool[files.fileId] = NewFile.DTSFileId
          ###read formula here!!!!!!!!!!
          #app.ConWriteln(str(files.linkbases))
          #app.ConRead('asd')
          pass
        else:
          # handle for non schema
          NewFile = helper.CreatePObject('DTSFile')
          app.ConWriteln('Processing File : {0}'.format(files.fileName))
          NewFile.DTSFileName = files.fileName
          NewFile.DTSFolderId = NewFolder.DTSFolderId
          NewFile.DTSFileType = files.fileType
          xsdPool[files.fileId] = NewFile.DTSFileId
    for alias in rf.aliases.keys():
      recAlias = rf.aliases[alias]
      NewAlias = helper.CreatePObject('DTSAlias')
      NewAlias.DTSAliasLink = alias
      NewAlias.DTSId = NewDTS.DTSId
      NewAlias.DTSAliasLoc = xsdPool[recAlias.fileId]
    for dictname in rf.dicts.keys():
      dLinks = rf.dicts[dictname]
      NewDict = helper.CreatePObject('DTSDict')
      NewDict.DTSId = NewDTS.DTSId
      NewDict.DictName = dictname
      NewDict.DictLoc = dLinks
    config.Commit()
  except:
    config.Rollback()
    app.ConWriteln(str(sys.exc_info()[1]))
    app.ConRead('Error detected')
    status.ErrMessage = str(sys.exc_info()[1])
    
def test(config, params, returns):
  status = returns.CreateValues(['tm', 0.0])
  mlu = config.ModLibUtils
  tm = mlu.Now()
  raise Exception, type(tm)