import com.ihsan.foundation.appserver as appserver
import com.ihsan.util.modman as modman
import traceback

# application-level modules, loaded via modman
modman.loadStdModules(globals(), 
  [
    "scripts#form_loaditem"
  ]
)


def FormOnSetDataEx(uideflist, params):
  config = uideflist.config 
  def GetValue(code, period, branches, isrp):
    if code=="()":
      return None
    code = eval(code)
    wClause = '('
    for i in range(len(code)):
      if i>0: 
        wClause+= " or "
      wClause+= "account_code like '%s" % (code[i])
      wClause+= "%'"
    wClause+= ') and branch_code in (%s)' % branches
    if isrp==1:
      wClause+= " and currency_code = 'IDR'"
    else:
      wClause+= " and currency_code <> 'IDR'"
    s = '''
       select sum(balancecumulative) "value" from table(%s(to_date('%s', 'dd-mm-yyyy')))
       where %s
    ''' % (config.MapDBTableName('core.getdailybalanceat'), period, wClause)
    value = config.CreateSQL(s).RawResult.value
    return value
  if params.DatasetCount == 0 or params.GetDataset(0).Structure.StructureName != 'data':
    return
  
  form_loaditem.setData(uideflist, params)
  if uideflist.uipData.Dataset.RecordCount==0:
    coaMapU = {
      "10" : '''('11202011',)''',
      "20" : '''('11202031',)''',
      "35" : '''('112020510001',)''',
      "37" : '''('112020520001',)''',
      "38" : '''('112020530001',)''',
      "36" : '''('112020540001',)''',
      "56" : '''('112020610001',)''',
      "57" : '''('112020620001',)''',
      "59" : '''('112020630001',)''',
      "40" : '''('11202071', '11201071',)''',
      "45" : '''('11202041',)''',
      "90" : '''('11202021',)''',
    }
    coaMapK = {
      "10" : '''('11202012',)''',
      "20" : '''('11202032',)''',
      "35" : '''('112020510002',)''',
      "37" : '''('112020520002',)''',
      "38" : '''('112020530002',)''',
      "36" : '''('112020540002',)''',
      "56" : '''('112020610002',)''',
      "57" : '''('112020620002',)''',
      "59" : '''('112020630002',)''',
      "40" : '''('11202072', '11201072',)''',
      "45" : '''('11202042',)''',
      "90" : '''('11202022',)''',
    }
    mlu = config.ModLibUtils
    s = '''
      select kode_cabang from branchmember where branch_id=%s
    ''' % (str(params.FirstRecord.branch_id))
    branchmembers = config.CreateSQL(s).RawResult
    listcabang = ''
    while not branchmembers.Eof:
      if listcabang != '':
        listcabang+=', '
      listcabang+=mlu.QuotedStr(branchmembers.kode_cabang)
      branchmembers.Next()
    pid = params.FirstRecord.period_id
    pCode = config.CreateSQL("select period_code from period where period_id=%s" % pid).RawResult.period_code
    tgl = 1
    bln = int(pCode[:2])
    thn = int(pCode[2:6])
    if bln<12:
      repdate = mlu.EncodeDate(thn, bln+1, tgl)
    else:
      repdate = mlu.EncodeDate(thn+1, 1, tgl)
    repdate = repdate-1
    (thn, bln, tgl) = mlu.DecodeDate(repdate)  
    period = "%s-%s-%s" % (str(tgl),str(bln),str(thn))
    ds = uideflist.uipData.Dataset
    s = "select a.refdata_id from %s a, %s b where a.reftype_id=b.reftype_id and b.reference_name='R_VALUTA_IJARAH' and a.reference_code='1'" % (
                config.MapDBTableName('enterprise.referencedata'),    
                config.MapDBTableName('enterprise.referencetype')
        )
    valcode = config.CreateSQL(s).RawResult.refdata_id 

    s = "select * from %s a, %s b where a.reftype_id=b.reftype_id and b.reference_name='R_BENTUK_PENYISIHAN' order by a.refdata_id" % (
                config.MapDBTableName('enterprise.referencedata'),    
                config.MapDBTableName('enterprise.referencetype')
        )
    res = config.CreateSQL(s).RawResult
    while not res.Eof:
      if res.reference_code in coaMapU.keys(): 
        value = GetValue(coaMapU[res.reference_code], period, listcabang, 1)
      else:
        value = None
      if value not in (None,'',0):
        #if value<0: value=value*-1
        rp = int(value/100000)
        if int(str(rp)[-1])>4:
          if rp<0:
            rp = (rp/10)
          else:
            rp = (rp/10)+1
        else:
          if rp<0:
            rp = (rp/10)+1
          else:
            rp = rp/10
      else:
        rp = 0
      if res.reference_code in coaMapK.keys(): 
        value = GetValue(coaMapK[res.reference_code], period, listcabang, 1)
      else:
        value = None
      if value not in (None,'',0):
        #if value<0: value=value*-1
        valas = int(value/100000)
        if int(str(valas)[-1])>4:
          if valas<0:
            valas = valas/10
          else:
            valas = (valas/10)+1
        else:
          if valas<0:
            valas = (valas/10)+1
          else:
            valas = valas/10
      else:
        valas = 0
      if rp<0:
        rp = rp*-1
      if valas<0:
        valas = valas*-1
      rec = ds.AddRecord()
      rec.SetFieldByName('LBENTUKPENYISIHAN.reference_desc', res.reference_desc)    
      rec.SetFieldByName('LBENTUKPENYISIHAN.reference_code', res.reference_code)    
      rec.SetFieldByName('LBENTUKPENYISIHAN.refdata_id', res.refdata_id)
      rec.SetFieldByName('LJENISVALUTA.reference_desc', 'RUPIAH')    
      rec.SetFieldByName('LJENISVALUTA.reference_code', '1')    
      rec.SetFieldByName('LJENISVALUTA.refdata_id', valcode)
      rec.SetFieldByName('CadUmumPPAP', str(rp))    
      rec.SetFieldByName('CadKhususPPAP', str(valas))    
      res.Next()
    #--
