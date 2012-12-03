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
          select 1 jml,
          a.nomor_rekening,
          r1.refdata_id ri1,
          r1.reference_code rc1,
          r1.reference_desc rd1,
          r2.refdata_id ri2,
          r2.reference_code rc2,
          r2.reference_desc rd2,
          r3.refdata_id ri3,
          r3.reference_code rc3,
          r3.reference_desc rd3,
          r4.refdata_id ri4,
          r4.reference_code rc4,
          r4.reference_desc rd4,
          decode(c.kode_account, '202010000001', 0, '202020000001', 0, '202030100001', 0, 
                                 '202030100002', 1, '202030100003', 3, '202030100004', 6,
                                 '202030100005', 12,'202030100006', 99,'202030200001', 0,
                                 '202030200002', 1, '202030200003', 3, '202030200004', 6,
                                 '202030200005', 12,'202030200006', 99) bln,
          decode(c.kode_account, '202030100001', 99, '202030200001', 99, 0) hari,
          case when (b.is_bagi_hasil_khusus='T') then b.nisbah_bagi_hasil else g.nisbah_bonus_dasar end nisbah,
          h.gdr*1.2*nisbah persen,
          d.saldo total 
          from %s a, %s b, %s c, %s d, %s e, %s f, %s g, 
          bagihasil_tabgir h, %s r1, %s r2, %s r3, %s r4
          where a.nomor_rekening=b.nomor_rekening 
          and b.kode_produk=c.kode_produk
          and a.nomor_rekening=d.nomor_rekening
          and a.nomor_nasabah=e.nomor_nasabah
          and d.kode_cabang=f.kode_cabang
          and b.kode_produk=g.kode_produk
          and a.nomor_rekening=h.nomor_rekening
          and decode(c.kode_account, '202010000001', '29', '202020000001', '21', '22')=r1.reference_code
          and r1.reftype_id=120 
          and decode(d.kode_valuta, 'IDR', '360', 'USD', '840', 'SGD', '702')=r2.reference_code
          and r2.reftype_id=232
          and decode(e.is_pihak_terkait, 'T', '1', '2') = r3.reference_code
          and r3.reftype_id=124
          and f.kode_lokasi=r4.reference_code
          and r4.reftype_id=251
          and c.kode_account in ('202010000001','202020000001','202030100001','202030100002','202030100003',
                                 '202030100004','202030100005','202030100006','202030200001','202030200002',
                                 '202030200003','202030200004','202030200005','202030200006')
          and extract(month from h.tanggal) = '%s'
          and d.kode_cabang in (%s)
     ''' % ( 
           config.MapDBTableName('core.rekeningcustomer'),
           config.MapDBTableName('core.rekeningliabilitas'),
           config.MapDBTableName('core.glinterface'),
           config.MapDBTableName('core.rekeningtransaksi'),
           config.MapDBTableName('core.nasabah'),
           config.MapDBTableName('enterprise.cabang'),
           config.MapDBTableName('core.produk'),
           config.MapDBTableName('enterprise.referencedata'),
           config.MapDBTableName('enterprise.referencedata'),
           config.MapDBTableName('enterprise.referencedata'),
           config.MapDBTableName('enterprise.referencedata'),
           str(bln), listcabang
           )
    #raise Exception, s
    res = config.CreateSQL(s).RawResult
    while not res.Eof:
      ins = ds.AddRecord()
      ins.JumlahRekening = res.jml
      ins.SetFieldByName('LJENIS.reference_code', res.rc1)
      ins.SetFieldByName('LJENIS.reference_desc', res.rd1)
      ins.SetFieldByName('LJENIS.refdata_id', res.ri1)
      ins.SetFieldByName('LJENISVALUTA.reference_code', res.rc2)
      ins.SetFieldByName('LJENISVALUTA.reference_desc', res.rd2)
      ins.SetFieldByName('LJENISVALUTA.refdata_id', res.ri2)
      ins.SetFieldByName('LHUBBANK.reference_code', res.rc3)
      ins.SetFieldByName('LHUBBANK.reference_desc', res.rd3)
      ins.SetFieldByName('LHUBBANK.refdata_id', res.ri3)
      ins.SetFieldByName('LLOKASI.reference_code', res.rc4)
      ins.SetFieldByName('LLOKASI.reference_desc', res.rd4)
      ins.SetFieldByName('LLOKASI.refdata_id', res.ri4)
      ins.Bulan = res.bln
      ins.Hari = res.hari
      ins.Nisbah = res.nisbah
      ins.Persen = res.persen
      ins.Jumlah = int(res.total/1000000)
      res.Next()

    
