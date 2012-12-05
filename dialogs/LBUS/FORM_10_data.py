import com.ihsan.foundation.appserver as appserver
import com.ihsan.util.modman as modman

# application-level modules, loaded via modman
modman.loadStdModules(globals(), 
  [
    "scripts#form_loaditem"
  ]
)


def FormOnSetDataEx(uideflist, params):
  def toDate(val):
    if val not in (None,'',0):
      if type(val)==type(0.0):
        val = config.ModLibUtils.DecodeDate(val)
      return '%s%s' % (str(val[1]).zfill(2), str(val[0]))
    else:
      return "''"
  config = uideflist.config
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
    ds = uideflist.uipData.Dataset
    s = '''
        select a.nomor_rekening,
        a.jml,                                                   
        r1.reference_code c1, 
        r1.reference_desc d1,
        r1.refdata_id i1,
        r2.reference_code c2, 
        r2.reference_desc d2,
        r2.refdata_id i2,
        r3.reference_code c3, 
        r3.reference_desc d3,
        r3.refdata_id i3,
        fa.dropping_date tgl_mulai,
        fa.due_date tgl_tempo,
        r4.reference_code c4, 
        r4.reference_desc d4,
        r4.refdata_id i4,
        r5.reference_code c5, 
        r5.reference_desc d5,
        r5.refdata_id i5,
        r6.reference_code c6, 
        r6.reference_desc d6,
        r6.refdata_id i6
        from (select nomor_rekening, finmusyarakahaccount_type, count(nomor_rekening) jml from %s
        group by nomor_rekening,finmusyarakahaccount_type) a join %s fa on (a.nomor_rekening=fa.nomor_rekening) 
        left outer join %s b on (a.nomor_rekening=b.nomor_rekening)
        left outer join %s c on (a.nomor_rekening=c.nomor_rekening)
        left outer join %s d on (b.nomor_nasabah=d.nomor_nasabah)
        left outer join %s e on (fa.facility_no=e.facility_no)
        left outer join %s f on (b.nomor_nasabah=f.nomor_nasabah)
        left outer join %s r1 on (r1.reference_code=decode(c.status_piutang,'10','10','20') and r1.reftype_id=219)
        left outer join %s r2 on (r2.reference_code=decode(e.currency_code,'IDR','360','USD','840','SIN','702') and r2.reftype_id=232)
        left outer join %s r3 on (r3.reference_code=decode(f.is_pihak_terkait, 'T','1','2') and r3.reftype_id=124)
        left outer join %s r4 on (r4.reference_code=decode(fa.overall_col_level, 1,'1',2,'2',3,'3',4,'4',5,'5') and r4.reftype_id=230)
        left outer join %s r5 on (r5.reference_code=decode(a.finmusyarakahaccount_type, 'D', '10', '20') and r5.reftype_id=236)
        left outer join %s r6 on (r6.reference_code=decode(fa.financing_model, 'T', '9', '1') and r6.reftype_id=223)
        where e.kode_cabang in (%s,'400')
        and a.nomor_rekening = '40000122'
    ''' % ( 
           config.MapDBTableName('financing.finmusyarakahaccount'),
           config.MapDBTableName('financing.finaccount'),
           config.MapDBTableName('core.rekeningcustomer'),
           config.MapDBTableName('financing.finaccadditionaldata'),
           config.MapDBTableName('financing.fincustadditionaldata'),
           config.MapDBTableName('financing.finfacility'),
           config.MapDBTableName('core.nasabah'),
           config.MapDBTableName('enterprise.referencedata'),
           config.MapDBTableName('enterprise.referencedata'),
           config.MapDBTableName('enterprise.referencedata'),
           config.MapDBTableName('enterprise.referencedata'),
           config.MapDBTableName('enterprise.referencedata'),
           config.MapDBTableName('enterprise.referencedata'),
           listcabang
           )
    res = config.CreateSQL(s).RawResult
    i=0
    while i<10 and not res.Eof:
    #while not res.Eof:
      i+=1
      ins = ds.AddRecord()
      ins.NomorRekening = res.nomor_rekening
      ins.JumlahRekening = res.jml
      ins.SetFieldByName('LSTATUSPEMBIAYAAN.reference_code', res.c1)
      ins.SetFieldByName('LSTATUSPEMBIAYAAN.reference_desc', res.d1)
      ins.SetFieldByName('LSTATUSPEMBIAYAAN.refdata_id', res.i1)
      ins.SetFieldByName('LJENISVALUTA.reference_code', res.c2)
      ins.SetFieldByName('LJENISVALUTA.reference_desc', res.d2)
      ins.SetFieldByName('LJENISVALUTA.refdata_id', res.i2)
      ins.SetFieldByName('LHUBBANK.reference_code', res.c3)
      ins.SetFieldByName('LHUBBANK.reference_desc', res.d3)
      ins.SetFieldByName('LHUBBANK.refdata_id', res.i3)
      ins.BlnThnMulai = toDate(res.tgl_mulai)
      ins.BlnThnTempo = toDate(res.tgl_tempo)
      ins.SetFieldByName('LKOLEKTIBILITAS.reference_code', res.c4)
      ins.SetFieldByName('LKOLEKTIBILITAS.reference_desc', res.d4)
      ins.SetFieldByName('LKOLEKTIBILITAS.refdata_id', res.i4)
      ins.SetFieldByName('LJENIS.reference_code', res.c5)
      ins.SetFieldByName('LJENIS.reference_desc', res.d5)
      ins.SetFieldByName('LJENIS.refdata_id', res.i5)
      ins.SetFieldByName('LSIFAT.reference_code', res.c6)
      ins.SetFieldByName('LSIFAT.reference_desc', res.d6)
      ins.SetFieldByName('LSIFAT.refdata_id', res.i6)
      res.Next()
