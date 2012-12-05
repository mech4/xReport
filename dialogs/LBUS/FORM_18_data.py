import com.ihsan.foundation.appserver as appserver
import com.ihsan.util.modman as modman

# application-level modules, loaded via modman
modman.loadStdModules(globals(), 
  [
    "scripts#form_loaditem"
  ]
)


def xFormOnSetDataEx(uideflist, params):
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
          select count(a.nomor_rekening) jml,
          a.nomor_rekening,
          sum(b.saldo_transaksi) total 
          from %s a, %s b, %s c
          where a.nomor_rekening=b.nomor_rekening 
          and b.kode_produk=c.kode_produk
          and c.kode_account in ('201020000001','201010000001','201010000002')
          group by a.nomor_rekening
;    ''' % ( 
           config.MapDBTableName('core.rekeningcustomer'),
           config.MapDBTableName('core.rekeningliabilitas'),
           config.MapDBTableName('core.glinterface'),
           )
    res = config.CreateSQL(s).RawResult
    while not res.Eof:
      ins = ds.AddRecord()
      ins.NomorRekening = res.nomor_rekening
      ins.JumlahRekening = res.jml
      ins.Jumlah = res.total
      res.Next()

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
          r5.refdata_id ri5,
          r5.reference_code rc5,
          r5.reference_desc rd5,
          case when (b.is_bagi_hasil_khusus='T') then b.nisbah_bagi_hasil else g.nisbah_bonus_dasar end nisbah,
          h.gdr*1.2*nisbah persen,
          j.saldo total 
          from %(RekeningCustomer)s a
          left outer join %(RekeningLiabilitas)s b on (a.nomor_rekening=b.nomor_rekening)
          left outer join %(GLInterface)s c on (b.kode_produk=c.kode_produk)
          left outer join %(RekeningTransaksi)s d on(a.nomor_rekening=d.nomor_rekening)
          left outer join %(Nasabah)s e on (a.nomor_nasabah=e.nomor_nasabah)
          left outer join %(Cabang)s f on (d.kode_cabang=f.kode_cabang)
          left outer join %(Produk)s g on (b.kode_produk=g.kode_produk)
          left outer join %(SaldoAkhirBulan)s j on (a.nomor_rekening=j.nomor_rekening) 
          left outer join bagihasil_tabgir h on (a.nomor_rekening=h.nomor_rekening and extract(month from h.tanggal) = '%(BulanProses)s')
          left outer join bagihasil_deposito i on (a.nomor_rekening=i.nomor_rekening and extract(month from i.tanggal) = '%(BulanProses)s')
          left outer join %(ReferenceData)s r1 on (decode(c.kode_account, '201020000001', '20', '201010000001', '10', '201010000002', '10','99')=r1.reference_code and r1.reftype_id=115)
          left outer join %(ReferenceData)s r2 on (decode(d.kode_valuta, 'IDR', '360', 'USD', '840', 'SGD', '702')=r2.reference_code and r2.reftype_id=232)
          left outer join %(ReferenceData)s r3 on (decode(e.is_pihak_terkait, 'T', '1', '2') = r3.reference_code and r3.reftype_id=124)
          left outer join %(ReferenceData)s r4 on (f.kode_lokasi=r4.reference_code and r4.reftype_id=251) 
          left outer join %(ReferenceData)s r5 on (decode(c.kode_account, '201010000002', '4', '1')=r5.reference_code and r5.reftype_id=221) 
          where c.kode_account in ('201020000001','201010000001','201010000002')
             and d.kode_cabang in (%(ParamCabang)s)
             and b.tanggal_buka <= to_date('%(TanggalLaporan)s','dd-mm-yyyy')
          order by rc1
     ''' % { 
           'RekeningCustomer'   : config.MapDBTableName('core.rekeningcustomer'),
           'RekeningLiabilitas' : config.MapDBTableName('core.rekeningliabilitas'),
           'GLInterface' : config.MapDBTableName('core.glinterface'),
           'RekeningTransaksi' : config.MapDBTableName('core.rekeningtransaksi'),
           'Nasabah' : config.MapDBTableName('core.nasabah'),
           'Cabang'  : config.MapDBTableName('enterprise.cabang'),
           'Produk'  : config.MapDBTableName('core.produk'),
           'SaldoAkhirBulan' : config.MapDBTableName('core.saldo_akhirbulan'),
           'BulanProses' : str(bln),
           'ReferenceData' : config.MapDBTableName('enterprise.referencedata'),
           'ParamCabang' : listcabang,
           'TanggalLaporan' : config.FormatDateTime('dd-mm-yyyy', repdate)
           }
    #raise Exception, s
    res = config.CreateSQL(s).RawResult
    while not res.Eof:
      ins = ds.AddRecord()
      ins.JumlahRekening = res.jml
      ins.SetFieldByName('LSIFAT.reference_code', res.rc5)
      ins.SetFieldByName('LSIFAT.reference_desc', res.rd5)
      ins.SetFieldByName('LSIFAT.refdata_id', res.ri5)
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
      ins.PersenBonus = round(res.nisbah, 2)
      t = int(res.total/100000)
      if int(str(t)[-1])>5:
        t = (t/10)+1
      else:
        t = t/10 
      ins.Jumlah = t
      res.Next()

    
