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
      wClause+= "a.account_code like '%s" % (code[i])
      wClause+= "%'"
    wClause+= ') and a.branch_code in (%s)' % branches
    if isrp==1:
      wClause+= " and a.currency_code = 'IDR'"
    else:
      wClause+= " and a.currency_code <> 'IDR'"
    s = '''
       select b.account_name, sum(a.balancecumulative) "value" from table(%s(to_date('%s', 'dd-mm-yyyy'))) a
       join %s b on (a.account_code=b.account_code)
       where %s
       group by b.account_name
    ''' % (config.MapDBTableName('core.getdailybalanceat'), period, config.MapDBTableName('core.account'), wClause)
    res = config.CreateSQL(s).RawResult
    ds = uideflist.uipData.Dataset
    no=0
    while not res.Eof:
      value = res.value
      if value not in (None,'',0):
        no+=1
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
        rec.SetFieldByName('No', str(no))
        rec.SetFieldByName('Uraian', str(res.account_name))
        rec.SetFieldByName('Jumlah', str(rp))
      res.Next()    
    return 1
  if params.DatasetCount == 0 or params.GetDataset(0).Structure.StructureName != 'data':
    return
  
  form_loaditem.setData(uideflist, params)
  if uideflist.uipData.Dataset.RecordCount==0:
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
    coa = '''('407040000001', '407040000002', '407040000003', '407040000004', '407040000005', '407040000006', 
                  '407040000007', '407040000039', '407010000002', '407010000003',)'''

    value = GetValue(coa, period, listcabang, 1)
    #--
