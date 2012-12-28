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
      "20" : '''('212020000001', ',212020000002', '212020000003', '212020000004', '212020000005', )''',
      "25" : '''('212050000000',)''',
      "30" : '''('212060000001',)''',
      "41" : '''('212070110000',)''',
      "49" : '''('212070120000',)''',
      "51" : '''('212070210000',)''',
      "59" : '''('212070220001', '212070220002', '212070220003', '212070220039',)''',
      "80" : '''('212190510001',)''',
      "81" : '''('212190520001',)''',
      "85" : '''('211',)''',
      "99" : '''('212190100001', '212190100002', '212190100003', '212190100004', '212190300001', 
                 '212190300002', '212190300003', '212190300004', '212040000001',  
                 '212190300005', '212190300006', '212190300007', '212190300008', '212190300009',
                 '212190300039', '212190400001', '212190400002',  
                 '212190600001', '212190600002', '212190600003', '212190700001', '212190700002',
                 '212190700003', '212190700004', '212190700005', '212190700006', '212190700007',
                 '212190700008', '212190700009', '212190700010', '212190700011', '212190700012',
                 '212190700013', '212190700014', '212190700016', '212190700017',
                 '212190700018', '212190700019', '212190700020', '212190700021', '212190700022',
                 '212190700023', '212190700024', '212190700025', '212190700026', '212130000001', )''',
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
    s = "select a.refdata_id from %s a, %s b where a.reftype_id=b.reftype_id and b.reference_name='R_GOLONGAN_STATUS' and a.reference_code='49'" % (
                config.MapDBTableName('enterprise.referencedata'),    
                config.MapDBTableName('enterprise.referencetype')
        )
    opcode = config.CreateSQL(s).RawResult.refdata_id 
    s = "select a.refdata_id from %s a, %s b where a.reftype_id=b.reftype_id and b.reference_name='R_GOLONGAN_STATUS' and a.reference_code='10'" % (
                config.MapDBTableName('enterprise.referencedata'),    
                config.MapDBTableName('enterprise.referencetype')
        )
    op2code = config.CreateSQL(s).RawResult.refdata_id 

    s = "select * from %s a, %s b where a.reftype_id=b.reftype_id and b.reference_name='R_JENIS_RUPA_PASIVA' order by a.refdata_id" % (
                config.MapDBTableName('enterprise.referencedata'),    
                config.MapDBTableName('enterprise.referencetype')
        )
    res = config.CreateSQL(s).RawResult
    while not res.Eof:
      if res.reference_code in coaMap.keys(): 
        value = GetValue(coaMap[res.reference_code], period, listcabang, 1)
        if res.reference_code=='99':
          valueadd = GetValue('''('212190700027',)''', period, listcabang, 1)
          if valueadd>0:
            value+=valueadd  
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
        rec = ds.AddRecord()
        if res.reference_code in ('30','85'):
          rec.SetFieldByName('LGOLSTAT.reference_desc', 'Penduduk - Pemerintah pusat')    
          rec.SetFieldByName('LGOLSTAT.reference_code', '10')    
          rec.SetFieldByName('LGOLSTAT.refdata_id', op2code)
        else:
          rec.SetFieldByName('LGOLSTAT.reference_desc', 'Penduduk - Lainnya')    
          rec.SetFieldByName('LGOLSTAT.reference_code', '49')    
          rec.SetFieldByName('LGOLSTAT.refdata_id', opcode)
        rec.SetFieldByName('LJENIS.reference_desc', res.reference_desc)    
        rec.SetFieldByName('LJENIS.reference_code', res.reference_code)    
        rec.SetFieldByName('LJENIS.refdata_id', res.refdata_id)
        rec.SetFieldByName('LJENISVALUTA.reference_desc', 'IDR - Indonesia Rupiah')    
        rec.SetFieldByName('LJENISVALUTA.reference_code', '360')    
        rec.SetFieldByName('LJENISVALUTA.refdata_id', valcode)
        rec.SetFieldByName('Jumlah', str(rp))    
      else:
        rp = 0
      res.Next()
    #--
