import com.ihsan.foundation.appserver as appserver
import com.ihsan.util.modman as modman

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
    coaMap = {
      "10" : '''('21201', )''',
      "20" : '''()''',
      "30" : '''('21203',)''',
      "40" : '''('21208',)''',
      "45" : '''('21209',)''',
      "50" : '''('21210',)''',
      "60" : '''()''',
      "70" : '''('21211',)''',
      "80" : '''()''',
      "99" : '''('212190200000', '212190700028', '212190700029', '212190700030', '212190700031', 
                 '212190700032', '212190700033', '212190700034', '212190700035', '212190700036',
                 '212190700037', '212190700038', '212190700039', '212190700040', '212190700049', )''',
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
    s = "select a.refdata_id from %s a, %s b where a.reftype_id=b.reftype_id and b.reference_name='R_JENIS_VALUTA' and a.reference_code='360'" % (
                config.MapDBTableName('enterprise.referencedata'),    
                config.MapDBTableName('enterprise.referencetype')
        )
    valcode = config.CreateSQL(s).RawResult.refdata_id 
    s = "select a.refdata_id from %s a, %s b where a.reftype_id=b.reftype_id and b.reference_name='R_SANDI_PIHAK_KETIGA' and a.reference_code='886'" % (
                config.MapDBTableName('enterprise.referencedata'),    
                config.MapDBTableName('enterprise.referencetype')
        )
    opcode = config.CreateSQL(s).RawResult.refdata_id 
    s = "select a.refdata_id from %s a, %s b where a.reftype_id=b.reftype_id and b.reference_name='R_SANDI_PIHAK_KETIGA' and a.reference_code='801'" % (
                config.MapDBTableName('enterprise.referencedata'),    
                config.MapDBTableName('enterprise.referencetype')
        )
    op2code = config.CreateSQL(s).RawResult.refdata_id 
    s = "select a.refdata_id from %s a, %s b where a.reftype_id=b.reftype_id and b.reference_name='R_SANDI_PIHAK_KETIGA' and a.reference_code='862'" % (
                config.MapDBTableName('enterprise.referencedata'),    
                config.MapDBTableName('enterprise.referencetype')
        )
    op3code = config.CreateSQL(s).RawResult.refdata_id 
    s = "select a.refdata_id from %s a, %s b where a.reftype_id=b.reftype_id and b.reference_name='R_SANDI_PIHAK_KETIGA' and a.reference_code='889'" % (
                config.MapDBTableName('enterprise.referencedata'),    
                config.MapDBTableName('enterprise.referencetype')
        )
    op4code = config.CreateSQL(s).RawResult.refdata_id 
    s = "select a.refdata_id from %s a, %s b where a.reftype_id=b.reftype_id and b.reference_name='R_HUBUNGAN_DENGAN_BANK' and a.reference_code='2'" % (
                config.MapDBTableName('enterprise.referencedata'),    
                config.MapDBTableName('enterprise.referencetype')
        )
    hubcode = config.CreateSQL(s).RawResult.refdata_id 

    s = "select * from %s a, %s b where a.reftype_id=b.reftype_id and b.reference_name='R_KEWAJIBAN_LAINNYA' order by a.refdata_id" % (
                config.MapDBTableName('enterprise.referencedata'),    
                config.MapDBTableName('enterprise.referencetype')
        )
    res = config.CreateSQL(s).RawResult
    while not res.Eof:
      if res.reference_code in coaMap.keys(): 
        value = GetValue(coaMap[res.reference_code], period, listcabang, 1)
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
        if rp<0:
          rp = rp*-1
        if res.reference_code == '99':
          rec = ds.AddRecord()
          rec.SetFieldByName('LGOLPENAGIH.reference_desc', 'Baitul Maal Wa Tamwil (BMT)')    
          rec.SetFieldByName('LGOLPENAGIH.reference_code', '862')    
          rec.SetFieldByName('LGOLPENAGIH.refdata_id', op3code)
          rec.SetFieldByName('LJENIS.reference_desc', res.reference_desc)    
          rec.SetFieldByName('LJENIS.reference_code', res.reference_code)    
          rec.SetFieldByName('LJENIS.refdata_id', res.refdata_id)
          rec.SetFieldByName('LJENISVALUTA.reference_desc', 'IDR - Indonesia Rupiah')    
          rec.SetFieldByName('LJENISVALUTA.reference_code', '360')    
          rec.SetFieldByName('LJENISVALUTA.refdata_id', valcode)
          rec.SetFieldByName('LHUBBANK.reference_desc', 'IDR - Indonesia Rupiah')    
          rec.SetFieldByName('LHUBBANK.reference_code', '360')    
          rec.SetFieldByName('LHUBBANK.refdata_id', hubcode)
          rec.SetFieldByName('Jumlah', str(0))    
        rec = ds.AddRecord()
        if res.reference_code == '10':
          rec.SetFieldByName('LGOLPENAGIH.reference_desc', 'Kantor Perbendaharaan dan Kas Negara (KPKN)')    
          rec.SetFieldByName('LGOLPENAGIH.reference_code', '801')    
          rec.SetFieldByName('LGOLPENAGIH.refdata_id', op2code)
        elif res.reference_code == '99':
          rec.SetFieldByName('LGOLPENAGIH.reference_desc', 'Sektor swasta lainnya')    
          rec.SetFieldByName('LGOLPENAGIH.reference_code', '889')    
          rec.SetFieldByName('LGOLPENAGIH.refdata_id', op4code)
        else:
          rec.SetFieldByName('LGOLPENAGIH.reference_desc', 'Perseorangan')    
          rec.SetFieldByName('LGOLPENAGIH.reference_code', '886')    
          rec.SetFieldByName('LGOLPENAGIH.refdata_id', opcode)
        rec.SetFieldByName('LJENIS.reference_desc', res.reference_desc)    
        rec.SetFieldByName('LJENIS.reference_code', res.reference_code)    
        rec.SetFieldByName('LJENIS.refdata_id', res.refdata_id)
        rec.SetFieldByName('LJENISVALUTA.reference_desc', 'IDR - Indonesia Rupiah')    
        rec.SetFieldByName('LJENISVALUTA.reference_code', '360')    
        rec.SetFieldByName('LJENISVALUTA.refdata_id', valcode)
        rec.SetFieldByName('LHUBBANK.reference_desc', 'Tidak terkait dengan Bank')    
        rec.SetFieldByName('LHUBBANK.reference_code', '2')    
        rec.SetFieldByName('LHUBBANK.refdata_id', hubcode)
        rec.SetFieldByName('Jumlah', str(rp))    
      else:
        rp = 0
      res.Next()
    #--
