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
'''
if ATTR_TYPE == ATTR_MONGODB: 
  from pymongo import Connection
'''

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
    '''
    conn  = Connection()    
    db    = conn[uMain.group_code]
    table = db[uMain.GetFieldByName('reportclass.report_code')]
    '''
    pass
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
          '''
          oItem = helper.GetObject('ReportItem', item_id)
          table.remove({"item_id": item_id})
          '''
          pass 
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
        pass
        '''
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
        '''
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

def CheckRepExist(config, params, returns):
  helper = phelper.PObjectHelper(config)
  status = returns.CreateValues(["IsErr", 0], ["totalRow", 0])
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
    
    # count total record
    itemName = "{0}_{1}".format(rec.group_code
      , rec.report_code)
    
    res = config.CreateSQL('''
      select count(*) from {0}
      where report_id = {1}
    '''.format(itemName, oReport.report_id)).rawresult
    
    if not res.Eof:
      status.totalRow = res.GetFieldValueAt(0) or 0
    #--
  except:    
    status.IsErr = 1

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
    
  #if DEBUG_MODE:
  app = config.AppObject
  app.ConCreate('out')
  #--
  
  helper = phelper.PObjectHelper(config)
  mlu = config.ModLibUtils
  status = returns.CreateValues(["IsErr", 0], ["ErrMessage",""])
  dayname = ('', 'Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu')
  
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
    
    if reportclass.group_id==2 and reportclass.report_code in ('FORM405','FORM406'):
      pcode = str(period.period_code)
      #raise Exception, (pcode[4:8],pcode[2:4],pcode[0:2])
      tgllap = mlu.EncodeDate(int(pcode[4:8]),int(pcode[2:4]),int(pcode[0:2]))
      if reportclass.report_code=='FORM405':
        nrow = 30
      else:
        nrow = 14
      for i in range(nrow):
        tglplus = mlu.DecodeDate(tgllap+i+1)
        hariplus = mlu.DayOfWeek(tgllap+i+1)
        #raise Exception, (tglplus,hariplus)
        owb.SetCellValue(3, i+4, dayname[hariplus])
        owb.SetCellValue(4, i+4, '{0}-{1}-{2}'.format(tglplus[2],tglplus[1],tglplus[0]))
    
    owb.SetCellValue(2, 1, reportclass.report_name)
    owb.SetCellValue(3, 2, "{0} - {1}".format(branch.branch_code, branch.branch_name))
    owb.SetCellValue(4, 2, "{0} - {1}".format(period.period_code, period.description))

    if ATTR_TYPE == ATTR_MONGODB:
      pass
      '''
      conn  = Connection()
      db    = conn[rec.group_code]
      table = db[rec.report_code]
      '''
    else:
      itemName = "{0}_{1}".format(rec.group_code, rec.report_code)
    #--
     
    row = int(rec.xlstopline)
    datamap = eval(rec.xlsmap)
    pos = datamap.keys()
    reflist = eval(rec.reflist)     
    
    if ATTR_TYPE == ATTR_MONGODB:
      pass
      '''
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
      '''
    else:
      fixMap()
      
      res = config.CreateSQL('''
        select item_id from {0} where report_id = {1} order by item_id
      '''.format(itemName, report_id)).rawresult
      
      i = 1
      while not res.Eof:
        if i % 10 == 0: app.ConWriteln("Load data ke-{0}".format(i))
        oItem = config.CreatePObjImplProxy(itemName)
        oItem.Key = res.item_id
        colskip = 0
        for col in pos:
          fieldname = datamap[col]
          if fieldname[0]!='@':
            fieldname = fieldname.strip('!')
            svalue = oItem.EvalMembers(fieldname)
            
            owb.SetCellValue(row, col-colskip, svalue)
          else:
            colskip += 1          
        #--
        row += 1
        res.Next()
        i += 1
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
      if val in(None,''): val=0
      if str(type(val))=="<type 'str'>" and not val.isdigit(): val=0
      val = int(val)
    #--
    if tipe==2:
      if val in(None,''): val=0
      if str(type(val))=="<type 'str'>" and not val.isdigit(): val=0
      val = int(val*100000)
    #--
    if tipe==3:
      if val in(None,''): val=0
      if str(type(val))=="<type 'str'>" and not val.isdigit(): val=0
      val = int(val*100)
    if tipe==4:
      val = str(val)
      val = val[0:2]+'/'+val[2:4]+'/'+val[4:8]
    if val=='-':
      val = ''
    if val==None:
      val = ''
    #--
    s = str(val)
    if tipe in (0,4):
      s = s.ljust(size)[:size]
    else:
      s = s.zfill(size)[-size:]
    return s
  #-- def          
  def Eom(month, year):
    year = int(year)
    if month<12:
      month = int(month)+1
    else:
      month = 1
      year = year+1
    mlu = config.ModLibUtils
    d = mlu.EncodeDate(year, month, 1)
    d = d-1
    ret = mlu.DecodeDate(d)
    return ret[2] 
    
  #if DEBUG_MODE:
  app = config.AppObject
  app.ConCreate('out')
  #--
  FilterSandi = {
    "405" : (None, '', ' ', '1051', '1058', '1065', '1066', '1085', '1120', '1135', '1147', '1170', '1171', '1174',
             '1177', '1180', '1183', '1205', '1225', '1226', '1235', '1245', '1255', '1265', '1287', '1294', '1305',
             '1315', '1325', '1335', '1357', '1365', '1375', '1385', '1395', '1405', '1427', '1475', '1485', '1495',
             '1527', '1528', '1535', '1545', '1555', '1565', '1587', '1607', '1608', '1615', '1625', '1635', '1645',
             '1667', '1668', '1675', '1685', '1695', '1705', '1727', '1728', '1735', '1755', '1765', '1745'
             )
    ,
    "406" : (None, '', ' ', '3061', '3071', '3072', '3075', '3085', '3089', '3111', '3121', '3122', '3125', '3135',
             '3136', '3139', '3161', '3164', '3186', '3195', '3205', '3227', '3235', '3257', '3265', '4051', '4065', '4075', '4085',
             '4107', '4115', '4125', '4135', '4145', '4155'
             )
    ,
  }
  
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
    jenis_laporan = 'A'
    no_form = reportclass.report_code.split('FORM')[-1]
    useheader = rec.useheader
    jml_record = 0
      
    #1: true LKPBU, 0:false, 2:row header only (LBUS), 3:header LHBU, 4:row header (LBBU)
    #set header LKPBU
    if int(useheader)==1:
      periode_laporan='M'+periode_laporan[2:6]+periode_laporan[0:2]+'01'
    header=sandi_pelapor[:3]+'000000'+periode_laporan+jenis_laporan+no_form.zfill(4)
    if int(useheader)==3:
      # if LHBU use this header
      header=sandi_pelapor[:3]+'08'+periode_laporan+no_form
    
    itemName = "{0}_{1}".format(rec.group_code, rec.report_code)
     
    datamap = eval(rec.xlsmap)
    pos = datamap.keys()
    reflist = eval(rec.reflist)
    txtmap = eval(rec.txtmap)     
    contents = ''
    
    fixMap()
      
    res = config.CreateSQL('''
        select item_id from {0} where report_id = {1}
        order by item_id 
    '''.format(itemName, report_id)).rawresult
      
    jml = 0
    totalrp = 0
    totalva = 0
    skipped1strow = 0
    if res.Eof and itemName[0:4]=='LBBU' and itemName[-1:] in ('5','6','7','9'):
      res = config.CreateSQL('''
          select -1 "item_id" from dual 
      ''').rawresult
    lastoutnum = -1
    while not res.Eof:
      if (jml % 100 == 0) and (jml<>lastoutnum): 
        app.ConWriteln("Process data ke - {0}".format(jml))
        lastoutnum = jml
      if res.item_id > 0:
        oItem = config.CreatePObjImplProxy(itemName)
        oItem.Key = res.item_id
      if int(useheader)==2:
        #row header LBUS
        if no_form in ('01','02') and oItem.EvalMembers(datamap[1]) in (None,'', ' '):
          pass
        else:
          contents += 'LS'+no_form+sandi_pelapor+periode_laporan
      if int(useheader)==4:
        #row header LBBU
        if no_form.isdigit():
          no_form = no_form.zfill(2).ljust(4)[:4]
        else:
          if jml==0:
            no_form = '0'+str(no_form)
          no_form = no_form.ljust(4)[:4]
        if no_form[0:2]=='09':
          contents += 'LBBUS'+str(no_form)+sandi_pelapor[:3]+'990'+periode_laporan+'121005517990'+str(jml+5).zfill(4)+str(jml+1).zfill(6)
        else:
          contents += 'LBBUS'+str(no_form)+sandi_pelapor[:3]+'990'+periode_laporan+'121005517990'+str(jml+1).zfill(4)+str(jml+1).zfill(4)
      #raise Exception, pos
      for col in pos:
        fieldname = datamap[col]
        if fieldname[0] != '!':
          fieldname = fieldname.strip('@')
          if fieldname == 'Rownum':
            svalue = str(jml+1).zfill(2)
            if no_form[0:2]=='11':
              svalue = str(jml+1)
          elif fieldname == 'Endmonth':
            svalue = str(Eom(periode_laporan[4:6], periode_laporan[0:4])).zfill(2)+periode_laporan[4:6]+periode_laporan[0:4]
          else:
            if res.item_id > 0:
              svalue = oItem.EvalMembers(fieldname)
            else:
              if col==1:
                svalue = 'NIHIL'
              else:
                svalue = None
            #sum rp dan va FORM1 LBBU
            if (int(useheader)==4) and (no_form=='01  ') and (col==4):
              totalrp+=svalue
            if (int(useheader)==4) and (no_form=='01  ') and (col==5):
              totalva+=svalue
          #raise Exception, no_form
          if int(useheader)==2 and no_form in ('01','02') and oItem.EvalMembers(datamap[1]) in (None,'', ' '):
            pass
          elif int(useheader)==3 and no_form in ('405','406') and oItem.EvalMembers(datamap[1]) in (FilterSandi[no_form]):
            pass
          else:
            contents += formTxtValue(svalue, txtmap[col][0], txtmap[col][1])          
          #--
      #-- End for col in pos
      if int(useheader)==2:
        if no_form in ('01','02') and oItem.EvalMembers(datamap[1]) in (None,'', ' '):
          if jml==skipped1strow:
            skipped1strow+=1
        else:
          #row footer LBUS
          contents += str(jml+1).zfill(5)
          if jml==skipped1strow:
            extra = ''.zfill(187-len(contents))
          contents += extra
          #uknown data
          contents += '   020393    20000000000000000000000000000000000000000000000000'
      if int(useheader)==4:
        #row footer LBBU
        if jml==0:
          extra = ''.zfill(1300-len(contents))
        contents += extra
      if int(useheader)==2 and no_form in ('01','02') and oItem.EvalMembers(datamap[1]) in (None,'', ' '):
        pass
      elif int(useheader)==3 and no_form in ('405','406') and oItem.EvalMembers(datamap[1]) in (FilterSandi[no_form]):
        pass
      else:
        contents += '\n'
      if int(useheader)==3 and no_form in ('405','406') and oItem.EvalMembers(datamap[1]) in (FilterSandi[no_form]):
        pass
      else:
        jml+=1
      res.Next()
    #--
    if (int(useheader)==4) and (no_form=='01  '):
      #summary FORM1 LBBU
      totalrp = int(totalrp)
      totalva = int(totalva)
      contents += 'LBBUS'+str(no_form)+sandi_pelapor[:3]+'990'+periode_laporan
      contents += '121005517990'+str(jml+1).zfill(4)+str(jml+1).zfill(4)
      contents += 'JUMLAH'.ljust(50)+str(jml+1).zfill(2).ljust(5)+'31121901'
      contents += str(totalrp).zfill(30)+str(totalva).zfill(30)+''.zfill(1135)+'\n'
      jml+=1
      contents += 'LBBUS'+str(no_form)+sandi_pelapor[:3]+'990'+periode_laporan
      contents += '121005517990'+str(jml+1).zfill(4)+str(jml+1).zfill(4)
      contents += 'RATA-RATA'.ljust(50)+str(jml+1).zfill(2).ljust(5)+'31121901'
      contents += str(totalrp/(jml-1)).zfill(30)+str(totalva/(jml-1)).zfill(30)+''.zfill(1135)+'\n'
    if (int(useheader)==4) and (no_form=='09  '):
      #summary FORM9 LBBU
      contents += 'LBBUS'+str(no_form)+sandi_pelapor[:3]+'990'+periode_laporan
      contents += '121005517990'+str(1).zfill(4)+str(999996).zfill(6)
      for col in pos:
        if col==1:
          svalue = 'Total Saldo Pembiayaan Yang Direstrukturisasi Bulan ini'
        elif col==19:
          svalue = 0 #total
        elif col==30:
          svalue = str(Eom(periode_laporan[4:6], periode_laporan[0:4])).zfill(2)+periode_laporan[4:6]+periode_laporan[0:4]
        else:
          svalue = None
        contents += formTxtValue(svalue, txtmap[col][0], txtmap[col][1])
      contents += ''.zfill(602)+'\n'
      contents += 'LBBUS'+str(no_form)+sandi_pelapor[:3]+'990'+periode_laporan
      contents += '121005517990'+str(2).zfill(4)+str(999997).zfill(6)
      for col in pos:
        if col==1:
          svalue = ' '
        elif col==19:
          svalue = 0 #total
        elif col==30:
          svalue = str(Eom(periode_laporan[4:6], periode_laporan[0:4])).zfill(2)+periode_laporan[4:6]+periode_laporan[0:4]
        else:
          svalue = None
        contents += formTxtValue(svalue, txtmap[col][0], txtmap[col][1])
      contents += ''.zfill(602)+'\n'
      contents += 'LBBUS'+str(no_form)+sandi_pelapor[:3]+'990'+periode_laporan
      contents += '121005517990'+str(3).zfill(4)+str(999998).zfill(6)
      for col in pos:
        if col==1:
          svalue = 'Saldo Pembiayaan Yang Direstrukturisasi Bulan Lalu'
        elif col==19:
          svalue = 0 #total bln lalu?
        elif col==30:
          svalue = str(Eom(periode_laporan[4:6], periode_laporan[0:4])).zfill(2)+periode_laporan[4:6]+periode_laporan[0:4]
        else:
          svalue = None
        contents += formTxtValue(svalue, txtmap[col][0], txtmap[col][1])
      contents += ''.zfill(602)+'\n'
      contents += 'LBBUS'+str(no_form)+sandi_pelapor[:3]+'990'+periode_laporan
      contents += '121005517990'+str(4).zfill(4)+str(999999).zfill(6)
      for col in pos:
        if col==1:
          svalue = 'Saldo Kumulatif Pembiayaan yang Direstrukturisasi'
        elif col==19:
          svalue = 0 #total
        elif col==30:
          svalue = str(Eom(periode_laporan[4:6], periode_laporan[0:4])).zfill(2)+periode_laporan[4:6]+periode_laporan[0:4]
        else:
          svalue = None
        contents += formTxtValue(svalue, txtmap[col][0], txtmap[col][1])
      contents += ''.zfill(602)+'\n'
    if int(useheader)==1:
      header += str(jml).zfill(9)[-9:]+'\n'
    elif int(useheader)==3:
      header += str(jml).zfill(8)[-8:]+'\n'
    else:
      header += str(jml).zfill(6)[-6:]+'\n'
    
    storeDir  = config.UserHomeDirectory
    storeFile = storeDir + rec.txttemplate
    if os.access(storeFile, os.F_OK) == 1: os.remove(storeFile)
    spath = os.path.dirname(storeFile)
    if not os.path.exists(spath): os.makedirs(spath)
    fOut = open(storeFile, "w")
    if int(useheader) in (1,3):
      #if LKPBU or LHBU : use header
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

def PeriodHandler(config, params, returns):
  gtype = params.FirstRecord.group_code
  config.BeginTransaction()
  s = "select distinct a.periode_type from reportclass a, reportclassgroup b where a.group_id=b.group_id and b.group_code='%s'" % gtype
  res = config.CreateSQL(s).RawResult
  while not res.Eof:
    PeriodCheck(config, res.periode_type)
    res.Next()
  #--
  config.Commit()
  return
   
def PeriodCheck(config, ptype):
  def periodGenerate(period_type, tgl, bln, thn, hari):
    mon = ('', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
    qtr = ('', '1st Quarter', '2nd Quarter', '3rd Quarter', '4th Quarter')
    week = ('', '1st Week of', '2nd Week of', '3rd Week of', '4th Week of')
    dayname = ('', 'Sunday,', 'Monday,', 'Tuesday,', 'Wednesday,', 'Thrusday,', 'Friday,', 'Saturday,')
    if period_type=='Y':
      return str(thn), str(thn)
    elif period_type=='M':
      return str(bln).zfill(2)+str(thn), mon[bln]+' '+str(thn)      
    elif period_type=='Q':
      return str((bln/3)+1).zfill(2)+str(thn), qtr[(bln/3)+1]+' '+str(thn)
    elif period_type=='W':
      if tgl<8:
        return str(thn)+str(bln).zfill(2)+'1', week[1]+' '+mon[bln]+' '+str(thn)
      elif tgl<16:
        return str(thn)+str(bln).zfill(2)+'2', week[2]+' '+mon[bln]+' '+str(thn)
      elif tgl<24:
        return str(thn)+str(bln).zfill(2)+'3', week[3]+' '+mon[bln]+' '+str(thn)
      else:
        return str(thn)+str(bln).zfill(2)+'4', week[4]+' '+mon[bln]+' '+str(thn)
    else:
      return str(tgl).zfill(2)+str(bln).zfill(2)+str(thn), dayname[hari]+' '+str(tgl).zfill(2)+' '+mon[bln]+' '+str(thn)     
  #--
  mlu = config.ModLibUtils
  tgl = mlu.DecodeDate(config.Now())
  hari = mlu.DayOfWeek(config.Now())
  bln = tgl[1]
  thn = tgl[0]
  tglnum = tgl[2]
  period = periodGenerate(ptype, tglnum, bln, thn, hari)
  #raise Exception, period[0]
  s = "select * from period where period_code='%s' and period_type='%s'" % (period[0], ptype)
  res = config.CreateSQL(s).RawResult
  if not res.Eof:
    #raise Exception, 'Ada'
    pass
  else:
    #raise Exception, 'Belum Ada'
    s = "insert into period (period_id, period_code, description, period_type) values (seq_period.nextval, '%s', '%s', '%s')" % (period[0], period[1], ptype)
    #raise Exception, s
    config.ExecSQL(s)
  
  if ptype=='D' and hari!=6:
    selisih_hari = 6-hari
    hari=6
    tglnum = tglnum+selisih_hari
    if bln<12:
      nmbln = bln+1
      nmthn = thn
    else:
      nmbln = 1
      nmthn = thn+1
    lastday = mlu.DecodeDate(mlu.EncodeDate(nmthn,nmbln,1)-1)
    lastday = lastday[2]
    if tglnum>lastday:
      tglnum=tglnum-lastday
      bln = nmbln
      thn = nmthn
    if tglnum<1:
      lastday = mlu.DecodeDate(mlu.EncodeDate(thn,bln,1)-1)
      thn = lastday[0]
      bln = lastday[1]
      tglnum = lastday[2]
    period = periodGenerate(ptype, tglnum, bln, thn, hari)
    #raise Exception, (period[0],ptype, tglnum, bln, thn, hari)
    s = "select * from period where period_code='%s' and period_type='%s'" % (period[0], ptype)
    res = config.CreateSQL(s).RawResult
    if not res.Eof:
      #raise Exception, 'Ada'
      pass
    else:
      #raise Exception, 'Belum Ada'
      s = "insert into period (period_id, period_code, description, period_type) values (seq_period.nextval, '%s', '%s', '%s')" % (period[0], period[1], ptype)
      #raise Exception, s
      config.ExecSQL(s)
  #return 
  
def ImportReport(config, params, returns):
  def fixMap():
    for col in pos:
      sfield = datamap[col]
      
      if sfield.split("_")[0] in reflist:
        datamap[col] = "{0}.{1}".format(sfield.split("_")[0]
          , sfield[sfield.find("_")+1:])
      #--
    #-- for
  #-- def           
  rec = params.FirstRecord
  row = int(rec.xlstopline)
  datamap = eval(rec.xlsmap)
  pos = datamap.keys()
  reflist = eval(rec.reflist)     
  f = open(config.GetHomeDir()+"dialogs\\"+rec.formid.replace("/","\\")+"_intr.py", "r")
  refmap = f.read()
  f.close()
  f = None
  refmap = eval(refmap.split("class")[0].replace("\n","").split("=")[-1])
  #raise Exception, refmap
  sw = params.GetStreamWrapper(0)
  helper = phelper.PObjectHelper(config)
  status = returns.CreateValues(["IsErr", 0], ["ErrMessage",""])
  sdef = ''
  rdef = ''
  fixMap()
  colcount = 0
  for col in pos:
    if datamap[col][0] != '@':
      sdef += datamap[col].strip('!')+':string'
      sdef += ';'
      if (datamap[col].split('.')[0] in reflist) and (datamap[col].split('.')[0] not in rdef) :
        rdef += datamap[col].split('.')[0]+'.refdata_id:integer;'
        rdef += datamap[col].split('.')[0]+'.reference_desc:string;'
        rdef += datamap[col].split('.')[0]+'.reference_code:string'
        rdef += ';' 
      colcount+=1
  sdef = sdef.rstrip(';')
  rdef = rdef.rstrip(';')
  res = returns.AddNewDatasetEx('iData', sdef)
  if rdef not in (None,''):
    rf = returns.AddNewDatasetEx('iReff', rdef) 
  try:
    tmplFile = config.UserHomeDirectory + sw.Name + '.xls'
    sw.SaveToFile(tmplFile)
    owb = pyFlexcel.Open(tmplFile)
    owb.ActivateWorksheet("report")
    check1 = owb.GetCellValue(2,1)
    check2 = owb.GetCellValue(3,2)
    check3 = owb.GetCellValue(4,2)
    if (check1!=rec.check1) or (check2!=rec.check2) or (check3!=rec.check3):
      raise Exception, 'File Not Match.'

    test = 'test'
    jml = 0
    #raise Exception, (sdef,rdef)
    while test not in (None,''):
      test = owb.GetCellValue(row,1)
      if test not in (None,''):
        iData = res.AddRecord()
        if rdef not in (None,''):
          iLink = rf.AddRecord()
          linkcounter = 0       
        colcount = 0     
        for col in pos:
          if datamap[col][0] == '@':
            pass
          elif datamap[col][0] == '!':
            colcount+=1
          else: 
            iData.SetFieldAt(colcount, owb.GetCellValue(row, colcount+1))
            if rdef not in (None,''):
              if ((datamap[col].split('.')[0] in reflist) and ('code' in datamap[col])):
                #raise Exception, str(type(unicode(owb.GetCellValue(row, colcount+1))))
                cellvalue = owb.GetCellValue(row, colcount+1)
                if str(type(cellvalue)) == "<type 'float'>":
                  cellvalue = str(int(cellvalue)) 
                s = '''
                   select * from %s a, %s b 
                   where a.reftype_id=b.reftype_id
                   and a.reference_code='%s' 
                   and b.reference_name='%s' 
                   ''' % (config.MapDBTableName('enterprise.ReferenceData'), 
                          config.MapDBTableName('enterprise.ReferenceType'),
                          cellvalue,
                          refmap[datamap[col].split('.')[0]]
                          )
                #if str(type(owb.GetCellValue(row, colcount+1))) != "<type 'unicode'>":
                #  raise Exception, s
                linkdata = config.CreateSQL(s).RawResult
                iLink.SetFieldByName(datamap[col].split('.')[0]+".refdata_id", linkdata.refdata_id)
                iLink.SetFieldByName(datamap[col].split('.')[0]+".reference_desc", linkdata.reference_desc)
                iLink.SetFieldByName(datamap[col].split('.')[0]+".reference_code", linkdata.reference_code)
            colcount+=1
        jml+=1
        row+=1
  except:    
    status.IsErr = 1
    errMessage = str(sys.exc_info()[1])
    status.ErrMessage = errMessage 
    
  
def CleanThisForm(config, params, returns):
  helper = phelper.PObjectHelper(config)
  status = returns.CreateValues(["IsErr", 0], ["totalRow", 0], ["ErrMessage", ''])
  config.BeginTransaction()
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
    
    # delete report
    itemName = "{0}_{1}".format(rec.group_code
      , rec.report_code)
    
    config.ExecSQL('''
      delete from {0}
      where report_id = {1}
    '''.format(itemName, oReport.report_id))
    config.ExecSQL('''
      delete from report
      where report_id = {0}
    '''.format(oReport.report_id))
    config.Commit()
    #--
  except:    
    config.Rollback()
    status.IsErr = 1
    status.ErrMessage = str(sys.exc_info()[1])

def DownloadF707(config, params, returns):
  def fixMap():
    for col in pos:
      sfield = datamap[col]
      
      if sfield.split("_")[0] in reflist:
        datamap[col] = "{0}.{1}".format(sfield.split("_")[0]
          , sfield[sfield.find("_")+1:])
      #--
    #-- for
  #-- def           
    
  #if DEBUG_MODE:
  app = config.AppObject
  app.ConCreate('out')
  #--
  
  mlu = config.ModLibUtils
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
    
    repdate = int(period.period_code[:2])
    repmon = int(period.period_code[2:4])
    repyear = int(period.period_code[4:8])
    period_desc = periodF707(mlu, repdate, repmon, repyear)
    
    owb.SetCellValue(5, 1, period_desc)
    
    row = int(rec.xlstopline)
    datamap = eval(rec.xlsmap)
    pos = datamap.keys()
    reflist = eval(rec.reflist)     
    itemName = "{0}_{1}".format(rec.group_code, rec.report_code)

    fixMap()
    
    res = config.CreateSQL('''
      select item_id from {0} where report_id = {1} 
    '''.format(itemName, report_id)).rawresult
    
    i = 1
    formulaField = ( '01', '02', '06', '11', '16', '21', '22', '23', '26', '31', '35', '40', '41')
    while not res.Eof:
      app.ConWriteln("Load data ke-{0}".format(i))
      oItem = config.CreatePObjImplProxy(itemName)
      oItem.Key = res.item_id
      colskip = 0
      if oItem.EvalMembers('LKOMPONEN.reference_code') not in formulaField:
        for col in pos:
          fieldname = datamap[col]
          if fieldname[0]!='@':
            svalue = oItem.EvalMembers(fieldname)
            if svalue in (None,''):
              svalue=0
            owb.SetCellValue(row, col+1, svalue)
          else:
            colskip += 1          
        #--
      row += 1
      res.Next()
      i += 1
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

def ImportF707(config, params, returns):
  def fixMap():
    for col in pos:
      sfield = datamap[col].lstrip('@')
      
      if sfield.split("_")[0] in reflist:
        datamap[col] = "{0}.{1}".format(sfield.split("_")[0]
          , sfield[sfield.find("_")+1:])
      #--
    #-- for
  #-- def           
  rec = params.FirstRecord
  row = int(rec.xlstopline)
  datamap = eval(rec.xlsmap)
  pos = datamap.keys()
  reflist = eval(rec.reflist)     
  f = open(config.GetHomeDir()+"dialogs\\"+rec.formid.replace("/","\\")+"_intr.py", "r")
  refmap = f.read()
  f.close()
  f = None
  refmap = eval(refmap.split("class")[0].replace("\n","").split("=")[-1])
  #raise Exception, refmap
  sw = params.GetStreamWrapper(0)
  helper = phelper.PObjectHelper(config)
  status = returns.CreateValues(["IsErr", 0], ["ErrMessage",""])
  sdef = ''
  rdef = ''
  fixMap()
  mlu = config.ModLibUtils
  colcount = 0
  for col in pos:
    currdata = datamap[col].lstrip('@')
    sdef += currdata+':string'
    sdef += ';'
    if (currdata.split('.')[0] in reflist) and (currdata.split('.')[0] not in rdef) :
      rdef += currdata.split('.')[0]+'.refdata_id:integer;'
      rdef += currdata.split('.')[0]+'.reference_desc:string;'
      rdef += currdata.split('.')[0]+'.reference_code:string'
      rdef += ';' 
    colcount+=1
  sdef = sdef.rstrip(';')
  rdef = rdef.rstrip(';')
  rd = returns.AddNewDatasetEx('iData', sdef)
  if rdef not in (None,''):
    rf = returns.AddNewDatasetEx('iReff', rdef) 
  try:
    tmplFile = config.UserHomeDirectory + sw.Name + '.xls'
    sw.SaveToFile(tmplFile)
    owb = pyFlexcel.Open(tmplFile)
    owb.ActivateWorksheet("report")
    c1 = 'Form 707 : Laporan Proyeksi Arus Kas'
    period      = helper.GetObject("Period", rec.period_id)
    repdate = int(period.period_code[:2])
    repmon = int(period.period_code[2:4])
    repyear = int(period.period_code[4:8])
    period_desc = periodF707(mlu, repdate, repmon, repyear)
    c2 = period_desc 
    check1 = owb.GetCellValue(1,1)
    check2 = owb.GetCellValue(5,1)
    formulaField = ( '01', '02', '06', '11', '16', '21', '22', '23', '26', '31', '35', '40', '41')
    if (check1!=c1) or (check2!=c2):
      raise Exception, 'File Not Match.'

    s = "select * from %s a, %s b where a.reftype_id=b.reftype_id and b.reference_name='R_ARUS_KAS' order by a.refdata_id" % (
                config.MapDBTableName('enterprise.referencedata'),    
                config.MapDBTableName('enterprise.referencetype')
        )
    res = config.CreateSQL(s).RawResult
    while not res.Eof:
      iData = rd.AddRecord()
      iLink = rf.AddRecord()
      iLink.SetFieldByName('LKOMPONEN.reference_desc', res.reference_desc)    
      iLink.SetFieldByName('LKOMPONEN.reference_code', res.reference_code)    
      iLink.SetFieldByName('LKOMPONEN.refdata_id', res.refdata_id)
      iData.SetFieldByName('LKOMPONEN.reference_desc', res.reference_desc)
      if res.reference_code not in formulaField:
        iData.Hari1 = str(int(owb.GetCellValue(int(res.reference_code)+8,3)))      
        iData.Hari2 = str(int(owb.GetCellValue(int(res.reference_code)+8,4)))      
        iData.Hari3 = str(int(owb.GetCellValue(int(res.reference_code)+8,5)))      
        iData.Hari4 = str(int(owb.GetCellValue(int(res.reference_code)+8,6)))      
        iData.Hari5 = str(int(owb.GetCellValue(int(res.reference_code)+8,7)))      
      res.Next()
  except:    
    status.IsErr = 1
    errMessage = str(sys.exc_info()[1])
    status.ErrMessage = errMessage 

def periodF707(mlu, repdate, repmon, repyear):
  namabln = ('', ' Januari', ' Februari', ' Maret', ' April', ' Mei', ' Juni', ' Juli', ' Agustus', ' September', ' Oktober', ' November', ' Desember')
  dfrom = repdate+3
  dto = repdate+7
  if repmon<12:
    cmon = repmon+1
    cyear = repyear
  else:
    cmon = 1
    cyear = repyear+1
  ldom = mlu.DecodeDate(mlu.EncodeDate(cyear,cmon,1)-1)[2]
  mfrom = namabln[repmon]
  mto = namabln[repmon]
  yfrom = ' '+str(repyear)
  yto = ' '+str(repyear)
  if dfrom>ldom:
    dfrom = dfrom-ldom
    mfrom = namabln[cmon]
    yfrom = ' '+str(cyear)
  if dto>ldom:
    dto = dto-ldom
    mto = namabln[cmon]
    yto = ' '+str(cyear)
  if mfrom==mto:
    mfrom=''
  if yfrom==yto:
    yfrom=''
  return "{0}{1}{2} - {3}{4}{5}".format(dfrom,mfrom,yfrom,dto,mto,yto)

def GenerateF707(config, params, returns):
  def fixMap():
    for col in pos:
      sfield = datamap[col]
      
      if sfield.split("_")[0] in reflist:
        datamap[col] = "{0}.{1}".format(sfield.split("_")[0]
          , sfield[sfield.find("_")+1:])
      #--
    #-- for
  #-- def           
    
  #if DEBUG_MODE:
  app = config.AppObject
  app.ConCreate('out')
  #--
  
  mlu = config.ModLibUtils
  helper = phelper.PObjectHelper(config)
  status = returns.CreateValues(["IsErr", 0], ["ErrMessage",""], ["storeFile", ""], ["fname", ""])
  
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
    
    repdate = int(period.period_code[:2])
    repmon = int(period.period_code[2:4])
    repyear = int(period.period_code[4:8])

    dayone = mlu.DayOfWeek(mlu.EncodeDate(repyear,repmon,1))
    sixweek = [0,0,0,0,0,0]
    j = 0
    for i in range(6):
      fday = 7-dayone+(7*i) 
      if fday>0:
        sixweek[j] = fday
        j+=1

    status.fname = '517000000F{0}{1}{2}A0707'.format(period.period_code[4:8],period.period_code[2:4],str(sixweek.index(repdate)).zfill(2))
    period_desc = periodF707(mlu, repdate, repmon, repyear)
    csv = "Form 707 : Laporan Proyeksi Arus Kas,,,,,,,\n"
    csv += ",,,,,,,\n"
    csv += "PT. BANK PANIN SYARIAH,,,,,,,\n"
    csv += "PROYEKSI ARUS KAS,,,,,,,\n"
    csv += "PERIODE %s,,,,,,,\n" % period_desc
    csv += "(dalam Rp. Juta),,,,,,,\n"
    csv += "Komponen,, Hari 1 , Hari 2 , Hari 3 , Hari 4 , Hari 5 ,\n"
    csv += ",,,,,,,\n"
    
    row = int(rec.xlstopline)
    datamap = eval(rec.xlsmap)
    pos = datamap.keys()
    reflist = eval(rec.reflist)     
    itemName = "{0}_{1}".format(rec.group_code, rec.report_code)

    fixMap()
    
    res = config.CreateSQL('''
      select item_id from {0} where report_id = {1} 
    '''.format(itemName, report_id)).rawresult
    
    i = 1
    formulaField = ( '02', '06', '11', '16', '01', '21', '26', '31', '35', '40', '23', '22', '41')
    CellFormula = { 
             "01" : "v['02'][j]+v['05'][j]+v['06'][j]+v['09'][j]+v['10'][j]+v['11'][j]+v['15'][j]+v['16'][j]+v['19'][j]+v['20'][j]",
             "02" : "v['03'][j]+v['04'][j]",
             "06" : "v['07'][j]+v['08'][j]",
             "11" : "v['12'][j]+v['13'][j]+v['14'][j]",
             "16" : "v['17'][j]+v['18'][j]",
             "21" : "",
             "22" : "v['23'][j]+v['24'][j]+v['25'][j]+v['26'][j]+v['30'][j]+v['31'][j]+v['34'][j]+v['35'][j]+v['38'][j]+v['39'][j]",
             "23" : "v['05'][j]+v['10'][j]+v['11'][j]+v['15'][j]-v['26'][j]-v['38'][j]-v['25'][j]",
             "26" : "v['27'][j]+v['28'][j]+v['29'][j]",
             "31" : "v['32'][j]+v['33'][j]",
             "35" : "v['36'][j]+v['37'][j]",
             "40" : "",
             "41" : "v['01'][j]-v['22'][j]"
    } 
    CellMaps = {}
    CellName = {}
    while not res.Eof:
      oItem = config.CreatePObjImplProxy(itemName)
      oItem.Key = res.item_id
      colskip = 0
      cid = oItem.EvalMembers('LKOMPONEN.reference_code') 
      CellMaps[cid] = [0,0,0,0,0]
      CellName[cid] = oItem.EvalMembers('LKOMPONEN.reference_desc') 
      if cid not in formulaField:
        for col in pos:
          fieldname = datamap[col]
          if fieldname[0]!='@':
            svalue = oItem.EvalMembers(fieldname)
            if svalue in (None,''):
              svalue=0
            CellMaps[cid][col-2]=int(svalue)
          else:
            colskip += 1          
        #--
      row += 1
      res.Next()
      i += 1
    #--
    for codes in formulaField:
      if codes not in ('21', '40'):
        for j in range(5):
          #raise Exception, eval(CellFormula[codes].replace('v','CellMaps')) 
          CellMaps[codes][j] = eval(CellFormula[codes].replace('v','CellMaps'))

    for codes in sorted(CellMaps.keys()):
      if codes in ('21', '40'):
        csv += ",,,,,,,\n"
      else:
        if CellName[codes][:5] == '     ':
          csv += ','+CellName[codes].lstrip(' ')+','
        else:
          csv += CellName[codes]+',,'
        for j in range(5):
          if CellMaps[codes][j]==0:
            csv += '-,'
          else:
            csv += str(CellMaps[codes][j])+','
        csv += '\n' 

    csv += ",,,,,,,\n"
    csv += ",,,,,,,\n"
    csv += ",,,,,,,\n"
    csv += "PT. BANK PANIN SYARIAH,,,,,,,\n"
    csv += "PROYEKSI ARUS KAS,,,,,,,\n"
    csv += "PERIODE %s,,,,,,,\n" % period_desc
    csv += "(dalam Ribuan USD) - NIHIL,,,,,,,\n"
    csv += "Komponen,, Hari 1 , Hari 2 , Hari 3 , Hari 4 , Hari 5 ,\n"
    csv += ",,,,,,,\n"

    for codes in sorted(CellMaps.keys()):
      if codes in ('21', '40'):
        csv += ",,,,,,,\n"
      else:
        if CellName[codes][:5] == '     ':
          csv += ','+CellName[codes].lstrip(' ')+','
        else:
          csv += CellName[codes]+',,'
        for j in range(5):
          csv += '-,'
        csv += '\n' 

    status.storeFile = csv
    app = config.AppObject
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
