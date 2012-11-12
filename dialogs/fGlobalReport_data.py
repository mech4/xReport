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
      if val=='': val=0
      val = int(val)
    #--
    if tipe==2:
      if val=='': val=0
      val = int(eval(val)*100000)
    #--
    if tipe==3:
      if val=='': val=0
      val = int(eval(val)*100)
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
    
  if DEBUG_MODE:
    app = config.AppObject
    app.ConCreate('out')
  #--
  
  helper = phelper.PObjectHelper(config)
  par = params.FirstRecord
  g_code = params.FirstRecord.group_code
  #test override value
  #g_code = 'LBUS'
  status = returns.CreateValues(["IsErr", 0], ["ErrMessage",""],
        ["class_id", 0]
        , ["period_id", par.period_id]
        , ["branch_id", par.branch_id]
        , ["report_code", '']
        , ["txttemplate", '']
        , ["txtmap", '']
        , ["xlsmap", '']
        , ["reflist", '']
        , ["useheader", 0]
        , ["group_code", g_code]
      )
  
  try :
    s = '''
       select a.* from reportclass a, 
       reportclassgroup b 
       where a.group_id=b.group_id
       and b.group_code='%s'
       order by report_code
    ''' % g_code
    forms = config.CreateSQL(s).RawResult
    rec = status
    firstform = 0
    ids=''
    while not forms.Eof:
      ids+=str(forms.report_code)+', '
      sqlproperties = '''
        select * from reportclassproperties where class_id=%s
      ''' % str(forms.class_id)
      prop = config.CreateSQL(sqlproperties).RawResult
      rec.class_id = forms.class_id
      rec.report_code = forms.report_code
      rec.txttemplate = prop.txttemplate
      rec.useheader = prop.useheader
      sqlref = '''
        select * from refmap where class_id = %s
      ''' % str(forms.class_id)
      refs = config.CreateSQL(sqlref).RawResult
      reflist = '('
      while not refs.Eof:
        reflist += "'"+refs.refname+"', "
        refs.Next()
      reflist = reflist.rstrip(', ')
      reflist += ')'
      rec.reflist = reflist
      sqlx = '''
        select * from xlsmap where class_id = %s
      ''' % str(forms.class_id)
      xmap = config.CreateSQL(sqlx).RawResult
      xlsmap = '{'
      while not xmap.Eof:
        xlsmap += str(xmap.fieldnumber)+" : '"+str(xmap.fieldname)+"', "
        xmap.Next()
      xlsmap = xlsmap.rstrip(', ')
      xlsmap += '}'
      rec.xlsmap = xlsmap
      sqlt = '''
        select * from txtmap where class_id = %s
      ''' % str(forms.class_id)
      tmap = config.CreateSQL(sqlt).RawResult
      txtmap = '([0,0], '
      while not tmap.Eof:
        txtmap += "["+str(tmap.fieldlength)+","+str(tmap.fieldtypecode)+"], "
        tmap.Next()
      txtmap = txtmap.rstrip(', ')
      txtmap += ')'
      rec.txtmap = txtmap
      reportAttr = {}
      attrutil.transferAttributes(helper, 
        ['class_id', 'period_id', 'branch_id']
        , reportAttr, rec)
    
      oReport   = helper.GetObjectByNames('Report', reportAttr)
      itemName = "{0}_{1}".format(rec.group_code, rec.report_code)
      if not oReport.isnull: 
        #raise Exception, "Report %s not found!" % itemName
      #--
        #indent
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
        header=sandi_pelapor[:3]+'000'+periode_laporan+jenis_laporan+no_form.zfill(4)
        if int(useheader)==3:
          header=sandi_pelapor[:3]+'08'+periode_laporan+no_form
        
        datamap = eval(rec.xlsmap)
        pos = datamap.keys()
        reflist = eval(rec.reflist)
        txtmap = eval(rec.txtmap)
        if not firstform:
          contents = ''
        
        fixMap()
          
        res = config.CreateSQL('''
            select item_id from {0} where report_id = {1} 
        '''.format(itemName, report_id)).rawresult
          
        jml = 0
        totalrp = 0
        totalva = 0
        while not res.Eof:
          oItem = config.CreatePObjImplProxy(itemName)
          oItem.Key = res.item_id
          if int(useheader)==2:
            #row header LBUS
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
              contents += 'LBBUS'+str(no_form)+sandi_pelapor[:3]+'990'+periode_laporan+'121005517990'+str(jml+1).zfill(4)+str(jml+1).zfill(6)
            else:
              contents += 'LBBUS'+str(no_form)+sandi_pelapor[:3]+'990'+periode_laporan+'121005517990'+str(jml+1).zfill(4)+str(jml+1).zfill(4)
          #raise Exception, str(datamap)
          for col in pos:
            fieldname = datamap[col]
            fieldname = fieldname.strip('@')
            if fieldname == 'Rownum':
              svalue = str(jml+1).zfill(2)
              if no_form[0:2]=='11':
                svalue = str(jml+1)
            elif fieldname == 'Endmonth':
              svalue = str(Eom(periode_laporan[5:7], periode_laporan[1:5])).zfill(2)+periode_laporan[5:7]+periode_laporan[1:5]
            else:
              svalue = oItem.EvalMembers(fieldname)
              #sum rp dan va FORM1 LBBU
              if (int(useheader)==4) and (no_form=='01  ') and (col==4):
                totalrp+=svalue
              if (int(useheader)==4) and (no_form=='01  ') and (col==5):
                totalva+=svalue
            contents += formTxtValue(svalue, txtmap[col][0], txtmap[col][1])          
            #--
          if int(useheader)==2:
            #row footer LBUS
            contents += str(jml+1).zfill(5)
            if jml==0:
              extra = ''.zfill(187-len(contents))
            contents += extra
            #uknown data
            contents += '   020393    20000000000000000000000000000000000000000000000000'
          if int(useheader)==4:
            #row footer LBBU
            if jml==0:
              extra = ''.zfill(1300-len(contents))
            contents += extra
          contents += '\n'
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
        header += str(jml).zfill(6)[-6:]+'\n'
        #end indent
      firstform+=1
      forms.Next()
    #--
    storeDir  = config.UserHomeDirectory
    storeFile = storeDir + rec.txttemplate
    if os.access(storeFile, os.F_OK) == 1: os.remove(storeFile)
    spath = os.path.dirname(storeFile)
    if not os.path.exists(spath): os.makedirs(spath)
    fOut = open(storeFile, "w")
    if int(useheader) in (1,3):
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


def PeriodCheck(config, params, returns):
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
        return '1'+str(thn)+str(bln).zfill(2), week[1]+' '+mon[bln]+' '+str(thn)
      elif tgl<16:
        return '2'+str(thn)+str(bln).zfill(2), week[2]+' '+mon[bln]+' '+str(thn)
      elif tgl<24:
        return '3'+str(thn)+str(bln).zfill(2), week[3]+' '+mon[bln]+' '+str(thn)
      else:
        return '4'+str(thn)+str(bln).zfill(2), week[4]+' '+mon[bln]+' '+str(thn)
    else:
      return str(tgl).zfill(2)+str(bln).zfill(2)+str(thn), dayname[hari]+' '+str(tgl).zfill(2)+' '+mon[bln]+' '+str(thn)     
  #--
  ptype = params.FirstRecord.period_type
  mlu = config.ModLibUtils
  tgl = mlu.DecodeDate(config.Now())
  hari = mlu.DayOfWeek(config.Now())
  bln = tgl[1]
  thn = tgl[0]
  tglnum = tgl[2]
  period = periodGenerate(ptype, tglnum, bln, thn, hari)
  s = "select * from period where period_code='%s' and period_type='%s'" % (period[0], ptype)
  res = config.CreateSQL(s).RawResult
  if not res.Eof:
    #raise Exception, 'Ada'
    pass
  else:
    #raise Exception, 'Belum Ada'
    s = "insert into period (period_id, period_code, description, period_type) values (seq_period, '%s', '%s', '%s')" % (period[0], period[1], ptype)
    config.ExecSQL(s)
  return 
  
def GetFormList(config, params, returns):
  helper = phelper.PObjectHelper(config)
  status = returns.CreateValues(["IsErr", 0], ["ErrMessage",""])
  g_code = params.FirstRecord.group_code
  formlist = returns.AddNewDatasetEx('forms',
          ';'.join([
             'class_id:integer'
             ,'report_code:string'
             ,'form_id:string'
          ])
  )
  try:
    s = '''
       select a.* from reportclass a, reportclassgroup b
       where a.group_id=b.group_id
       and b.group_code='%s'
    ''' % g_code
    res = config.CreateSQL(s).RawResult
    while not res.Eof:
      rec = formlist.AddRecord()
      rec.class_id = res.class_id
      rec.report_code = res.report_code
      rec.form_id = res.form_id
      res.Next()
    #--
  except:    
    status.IsErr = 1
    errMessage = str(sys.exc_info()[1])
    status.ErrMessage = errMessage 
