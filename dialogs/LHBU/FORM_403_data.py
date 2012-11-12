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
    wClause = ''
    for i in range(len(code)):
      if i>0: 
        wClause+= " or "
      wClause+= "account_code like '%s" % (code[i])
      wClause+= "%'"
    wClause+= ' and branch_code in (%s)' % branches
    if isrp:
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
      '100':"('101',)",
      '131':"('103',)",
      '132':"()",
      '140':"('105','10305')",
      '170':"('108','109')",
      '223':"()",
      '224':"()",
      '300':"('20101','20201')",
      '320':"('20201','20202')",
      '330':"('20203',)",
      '351':"('204',)",
      '352':"()",
      '393':"()",
      '394':"()",
      '515':"()",
      '520':"()",
      '571':"()",
      '572':"()",
      '599':"()"
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
    tgl = pCode[2:4]
    bln = pCode[:2]
    thn = pCode[4:8]
    period = "%s-%s-%s" % (tgl,bln,thn)
    ds = uideflist.uipData.Dataset
    s = "select * from %s a, %s b where a.reftype_id=b.reftype_id and b.reference_name='R_JENIS_POSPOS' order by a.reference_code" % (
                config.MapDBTableName('enterprise.referencedata'),    
                config.MapDBTableName('enterprise.referencetype')
        )
    res = config.CreateSQL(s).RawResult
    while not res.Eof:
      rec = ds.AddRecord()
      rec.SetFieldByName('LPOS.reference_desc', res.reference_desc)    
      rec.SetFieldByName('LPOS.reference_code', res.reference_code)    
      rec.SetFieldByName('LPOS.refdata_id', res.refdata_id)
      value = GetValue(coaMap[res.reference_code], period, listcabang, 1)
      if value not in (None,'',0):
        rp = int(value/1000000)
      else:
        rp = 0
      value = GetValue(coaMap[res.reference_code], period, listcabang, 0)
      if value not in (None,'',0):
        valas = int(value/1000000)
      else:
        valas = 0
      total = rp+valas
      rec.SetFieldByName('Rupiah', str(rp))    
      rec.SetFieldByName('Valas', str(valas))    
      rec.SetFieldByName('Jumlah', str(total))    
      res.Next()
    #--
    
