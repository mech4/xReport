# GLOBALS
DEBUG_MODE    = False
ATTR_ORACLE   = 0x01
ATTR_MONGODB  = 0x02 
ATTR_TYPE     = ATTR_ORACLE  

import com.ihsan.util.dbutil as dbutil
import com.ihsan.util.debug as debug
import com.ihsan.util.attrutil as attrutil
import com.ihsan.foundation.pobjecthelper as phelper
import sys, os
import pyFlexcel
if ATTR_TYPE == ATTR_MONGODB: 
  from pymongo import Connection

def SaveReport(config, params, returns):
  if DEBUG_MODE:
    app = config.AppObject
    app.ConCreate('out')
  #--
  
  helper = phelper.PObjectHelper(config)
  status = returns.CreateValues(["IsErr", 0], ["ErrMessage",""])

  uMain    = params.uipMain.GetRecord(0)
  uDeleted = params.uipDeleted
  uData    = params.uipData  
  
  reportAttr = {}
  attrutil.transferAttributes(helper, [
    'class_id=reportclass.class_id'
    , 'period_id=period.period_id'
    , 'branch_id=branch.branch_id'
  ], reportAttr, uMain)
  
  if ATTR_TYPE == ATTR_MONGODB:
    conn  = Connection()    
    db    = conn[uMain.group_code]
    table = db[uMain.GetFieldByName('reportclass.report_code')]
  else:
    itemName = "{0}_{1}".format(uMain.group_code
      , uMain.GetFieldByName('reportclass.report_code'))
  #--

  config.BeginTransaction()
  try:
    oReport  = helper.GetObjectByNames('Report', reportAttr)
    if oReport.isnull:
      oReport = helper.CreatePObject('Report', reportAttr) 
    else:
      #-- delete row
      if DEBUG_MODE:
        app.ConWriteln(str(uDeleted.RecordCount))
      #--
      for i in range(uDeleted.RecordCount):
        rec     = uDeleted.GetRecord(i)
        item_id = rec.item_id
        if DEBUG_MODE:
          app.ConWriteln(str(item_id))
        #--
        if ATTR_TYPE == ATTR_MONGODB:
          oItem = helper.GetObject('ReportItem', item_id)
          table.remove({"item_id": item_id}) 
        else:
          oItem = config.CreatePObjImplProxy(itemName)
          oItem.Key = item_id
        #--
        if not oItem.IsNull:
          oItem.Delete()
      #--
    #--
    
    report_id = oReport.report_id
    attrlist = eval(uMain.attrlist)
    
    for i in range(uData.RecordCount):
      rec = uData.GetRecord(i)
      item_id = rec.item_id or -1
      if ATTR_TYPE == ATTR_MONGODB:
        if item_id == -1:
          item = helper.CreatePObject('ReportItem')
          item_id = item.item_id        
          itemdata = {'report_id': report_id, 'item_id': item_id}
        else:
          itemdata = table.find_one({'item_id': item_id})
        #--
        if DEBUG_MODE:
          app.ConWriteln(str(itemdata))
        #--
        attrutil.transferAttributes(helper, attrlist, itemdata, rec)
        table.save(itemdata)
      elif ATTR_TYPE == ATTR_ORACLE:
        if item_id == -1:
          item = config.CreatePObject(itemName)
          item.report_id = report_id
        else:
          item = config.CreatePObjImplProxy(itemName)
          item.Key = item_id
        #--
        attrutil.transferAttributes(helper, attrlist, item, rec)
      #--
    #--
     
    config.Commit()
  except:
    config.Rollback()
    status.IsErr = 1
    if DEBUG_MODE:
      errMessage = debug.getExcMsg()
      #app.ConWriteln(errMessage)
    else:
      errMessage = str(sys.exc_info()[1])
    #--
    status.ErrMessage = errMessage 
  #-- try.except
  if DEBUG_MODE:
    app.ConRead('Press any key')
  #--
#--

def DownloadReport(config, params, returns):
  def fixMap():
    for col in pos:
      sfield = datamap[col]
      
      if sfield.split("_")[0] in reflist:
        datamap[col] = "{0}.{1}".format(sfield.split("_")[0]
          , sfield[sfield.find("_")+1:])
      #--
    #-- for
  #-- def           
    
  if DEBUG_MODE:
    app = config.AppObject
    app.ConCreate('out')
  #--
  
  helper = phelper.PObjectHelper(config)
  status = returns.CreateValues(["IsErr", 0], ["ErrMessage",""])
  
  try :
    rec = params.FirstRecord
    tmplDir  = "c:/dafapp/ibank2/report/regulatory/templates/"
    tmplFile = tmplDir + rec.xlstemplate
    owb = pyFlexcel.Open(tmplFile)
    owb.ActivateWorksheet("report")
    
    rec = params.FirstRecord
    reportAttr = {}
    attrutil.transferAttributes(helper, 
      ['class_id', 'period_id', 'branch_id']
      , reportAttr, rec)
  
    oReport   = helper.GetObjectByNames('Report', reportAttr)
    if oReport.isnull: 
      raise Exception, "Report not found!"
    #--
    report_id = oReport.report_id or -1
    
    reportclass = helper.GetObject("ReportClass", rec.class_id)
    period      = helper.GetObject("Period", rec.period_id)
    branch      = helper.GetObject("Branch", rec.branch_id)
    
    owb.SetCellValue(2, 1, reportclass.report_name)
    owb.SetCellValue(3, 2, "{0} - {1}".format(branch.branch_code, branch.branch_name))
    owb.SetCellValue(4, 2, "{0} - {1}".format(period.period_code, period.description))

    if ATTR_TYPE == ATTR_MONGODB:
      conn  = Connection()
      db    = conn[rec.group_code]
      table = db[rec.report_code]
    else:
      itemName = "{0}_{1}".format(rec.group_code, rec.report_code)
    #--
     
    row = int(rec.xlstopline)
    datamap = eval(rec.xlsmap)
    pos = datamap.keys()
    reflist = eval(rec.reflist)     
    
    if ATTR_TYPE == ATTR_MONGODB:
      for data in table.find({"report_id": report_id}).sort("item_id"):
        for col in pos:
          fieldname = datamap[col]
          svalue = data[fieldname]
          if DEBUG_MODE:
            app.ConWriteln(str(row)+"."+str(col))
            app.ConWriteln(fieldname)
            app.ConWriteln(str(svalue))
          #-- 
          owb.SetCellValue(row, col, svalue)
        #-- for
        
        row += 1 
      #-- for
    else:
      fixMap()
      
      res = config.CreateSQL('''
        select item_id from {0} where report_id = {1} 
      '''.format(itemName, report_id)).rawresult
      
      while not res.Eof:
        oItem = config.CreatePObjImplProxy(itemName)
        oItem.Key = res.item_id
        for col in pos:
          fieldname = datamap[col]
          svalue = oItem.EvalMembers(fieldname)

          owb.SetCellValue(row, col, svalue)          
        #--
        row += 1
        res.Next()
      #--
    #--

    storeDir  = config.UserHomeDirectory
    storeFile = storeDir + rec.xlstemplate
    if os.access(storeFile, os.F_OK) == 1: os.remove(storeFile)
    spath = os.path.dirname(storeFile)
    if not os.path.exists(spath): os.makedirs(spath)
    owb.SaveAs(storeFile)

    app = config.AppObject
    sw = returns.AddStreamWrapper()
    sw.LoadFromFile(storeFile)
    sw.Name = "return"
    sw.FileName = rec.xlstemplate
    sw.MIMEType = app.GetMIMETypeFromExtension(storeFile)
  except:    
    config.Rollback()
    status.IsErr = 1
    if DEBUG_MODE:
      errMessage = debug.getExcMsg()
      #app.ConWriteln(errMessage)
    else:
      errMessage = str(sys.exc_info()[1])
    #--
    status.ErrMessage = errMessage 
  #-- try.except
  if DEBUG_MODE:
    app.ConRead('Press any key')
  #--
  return 1

def GenerateTxt(config, params, returns):
  def fixMap():
    for col in pos:
      sfield = datamap[col]
      
      if sfield.split("_")[0] in reflist:
        datamap[col] = "{0}.{1}".format(sfield.split("_")[0]
          , sfield[sfield.find("_")+1:])
      #--
    #-- for
  #-- def   
  def formTxtValue(val, size, tipe):
    if tipe==1:
      val = int(val)
    #--
    if tipe==2:
      val = int(val*100000)
    #--
    if val=='-':
      val = ''
    #--
    s = str(val)
    if tipe==0:
      s = s.ljust(size)[:size]
    else:
      s = s.zfill(size)[-size:]
    return s
  #-- def          
    
  if DEBUG_MODE:
    app = config.AppObject
    app.ConCreate('out')
  #--
  
  helper = phelper.PObjectHelper(config)
  status = returns.CreateValues(["IsErr", 0], ["ErrMessage",""])
  
  try :
    rec = params.FirstRecord
    reportAttr = {}
    attrutil.transferAttributes(helper, 
      ['class_id', 'period_id', 'branch_id']
      , reportAttr, rec)
  
    oReport   = helper.GetObjectByNames('Report', reportAttr)
    if oReport.isnull: 
      raise Exception, "Report not found!"
    #--
    report_id = oReport.report_id or -1
    
    reportclass = helper.GetObject("ReportClass", rec.class_id)
    period      = helper.GetObject("Period", rec.period_id)
    branch      = helper.GetObject("Branch", rec.branch_id)
    
    sandi_pelapor = branch.branch_code
    periode_laporan = period.period_code
    jenis_laporan = '01'
    no_form = reportclass.report_code.split('FORM')[-1]
    useheader = rec.useheader
    jml_record = 0
      
    #set header
    header=sandi_pelapor+periode_laporan+jenis_laporan+no_form
    
    itemName = "{0}_{1}".format(rec.group_code, rec.report_code)
     
    datamap = eval(rec.xlsmap)
    pos = datamap.keys()
    reflist = eval(rec.reflist)
    txtmap = eval(rec.txtmap)     
    contents = ''
    
    fixMap()
      
    res = config.CreateSQL('''
        select item_id from {0} where report_id = {1} 
    '''.format(itemName, report_id)).rawresult
      
    jml = 0
    while not res.Eof:
      oItem = config.CreatePObjImplProxy(itemName)
      oItem.Key = res.item_id
      for col in pos:
        fieldname = datamap[col]
        svalue = oItem.EvalMembers(fieldname)
        
        contents += formTxtValue(svalue, txtmap[col][0], txtmap[col][1])          
        #--
      contents += '\n'
      jml+=1
      res.Next()
    #--
    header += str(jml).zfill(6)[-6:]+'\n'
    
    storeDir  = config.UserHomeDirectory
    storeFile = storeDir + rec.txttemplate
    if os.access(storeFile, os.F_OK) == 1: os.remove(storeFile)
    spath = os.path.dirname(storeFile)
    if not os.path.exists(spath): os.makedirs(spath)
    fOut = open(storeFile, "w")
    if useheader:
      fOut.write(header)
    fOut.write(contents)
    fOut.close()
    app = config.AppObject
    sw = returns.AddStreamWrapper()
    sw.LoadFromFile(storeFile)
    sw.Name = "return"
    sw.FileName = rec.txttemplate
    sw.MIMEType = app.GetMIMETypeFromExtension(storeFile)
  except:    
    config.Rollback()
    status.IsErr = 1
    if DEBUG_MODE:
      errMessage = debug.getExcMsg()
      #app.ConWriteln(errMessage)
    else:
      errMessage = str(sys.exc_info()[1])
    #--
    status.ErrMessage = errMessage 
  #-- try.except
  if DEBUG_MODE:
    app.ConRead('Press any key')
  #--
  return 1
