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
      '100':'''('201',
              '202',
              '204',
              '205',
              '206',
              '207',
              '208',
              '209',
              '211',
              '212')'''
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
    week = int(pCode[6:7])
    #tgl = mlu.DecodeDate(config.Now())
    bln = int(pCode[4:6])
    thn = int(pCode[0:4])
    ds = uideflist.uipData.Dataset
    if week==1:
      rg = (1,8)
    elif week==2:
      rg = (8,16)
    elif week==3:
      rg = (16,24)
    else:
      if bln<12:
        bln_berikutnya = bln+1
        thn_berikutnya = thn
      else:
        bln_berikutnya = 1
        thn_berikutnya = thn+1
      tglakhir = mlu.DecodeDate(mlu.EncodeDate(thn_berikutnya,bln_berikutnya,1)-1)[2]
      rg = (24, tglakhir)
    for i in range(rg[0],rg[1]):  
      rec = ds.AddRecord()
      rec.Tanggal = str(i).zfill(2)+str(bln).zfill(2)+str(thn)
      period = "%s-%s-%s" % (str(i).zfill(2),bln,thn)
      value = GetValue(coaMap['100'], period, listcabang, 1)
      if value not in (None,'',0):
        rp = int(value/1000000)
      else:
        rp = 0
      valas = 0
      rec.Rupiah = rp
      rec.Valas = valas
    #comment for auto on output
    #rec = ds.AddRecord()
    #rec.Tanggal = 'Jml'
    #rec = ds.AddRecord()
    #rec.Tanggal = 'Rata2'
    
