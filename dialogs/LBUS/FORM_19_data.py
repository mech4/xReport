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
          decode(decode(d.kode_jenis, 'DEP', i.ekuivalen_rate , h.gdr*nisbah/100), 
                 0, case when (b.is_bagi_hasil_khusus='T') then b.nisbah_bagi_hasil else g.nisbah_bonus_dasar end/10, 
                 null, case when (b.is_bagi_hasil_khusus='T') then b.nisbah_bagi_hasil else g.nisbah_bonus_dasar end/10,
                 decode(d.kode_jenis, 'DEP', i.ekuivalen_rate , h.gdr*nisbah/100)) persen,
          d.saldo total 
          from %s a
          left outer join %s b on (a.nomor_rekening=b.nomor_rekening)
          left outer join %s c on (b.kode_produk=c.kode_produk)
          left outer join %s d on(a.nomor_rekening=d.nomor_rekening)
          left outer join %s e on (a.nomor_nasabah=e.nomor_nasabah)
          left outer join %s f on (d.kode_cabang=f.kode_cabang)
          left outer join %s g on (b.kode_produk=g.kode_produk)
          left outer join bagihasil_tabgir h on (a.nomor_rekening=h.nomor_rekening)
          left outer join bagihasil_deposito i on (a.nomor_rekening=i.nomor_rekening)
          left outer join %s r1 on (decode(c.kode_account, '202010000001', '29', '202020000001', '21', '22')=r1.reference_code and r1.reftype_id=120)
          left outer join %s r2 on (decode(d.kode_valuta, 'IDR', '360', 'USD', '840', 'SGD', '702')=r2.reference_code and r2.reftype_id=232)
          left outer join %s r3 on (decode(e.is_pihak_terkait, 'T', '1', '2') = r3.reference_code and r3.reftype_id=124)
          left outer join %s r4 on (f.kode_lokasi=r4.reference_code and r4.reftype_id=251)
          where c.kode_account in ('202010000001','202020000001','202030100001','202030100002','202030100003',
                                 '202030100004','202030100005','202030100006','202030200001','202030200002',
                                 '202030200003','202030200004','202030200005','202030200006')
          and c.kode_interface in  ('glnomi', 'Saldo_Plus')
          and d.status_rekening<>3
          and (extract(month from h.tanggal) = '%s' or extract(month from i.tanggal) = '%s')
          and d.kode_cabang in (%s)
          order by rc1
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
           str(bln), str(bln), listcabang
           )
    #raise Exception, s
    res = config.CreateSQL(s).RawResult
    #x = 0
    totalgbt = 0
    jmlgbt = 0
    totalgbd = 0
    jmlgbd = 0
    putpos = 0
    while not res.Eof:
      if res.total<5000000:
        if res.rc1=='21':
          totalgbt+=res.total
          jmlgbt+=1
          trc1 = res.rc1
          trd1 = res.rd1
          tri1 = res.ri1
          trc2 = res.rc2
          trd2 = res.rd2
          tri2 = res.ri2
          trc3 = res.rc3
          trd3 = res.rd3
          tri3 = res.ri3
          trc4 = res.rc4
          trd4 = res.rd4
          tri4 = res.ri4
        if res.rc1=='22':
          totalgbd+=res.total
          jmlgbd+=1
          drc1 = res.rc1
          drd1 = res.rd1
          dri1 = res.ri1
          drc2 = res.rc2
          drd2 = res.rd2
          dri2 = res.ri2
          drc3 = res.rc3
          drd3 = res.rd3
          dri3 = res.ri3
          drc4 = res.rc4
          drd4 = res.rd4
          dri4 = res.ri4
      else:
        if res.rc1=='21':
          putpos+=1 
        ins = ds.AddRecord()
        ins.JumlahRekening = res.jml
        ins.SetFieldByName('LJENIS.reference_code', res.rc1)
        #if res.rc1=='22':
        #  x +=1
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
        ins.Nisbah = round(res.nisbah, 2)
        ins.Persen = round(res.persen, 2)
        t = int(res.total/100000)
        if int(str(t)[-1])>5:
          t = (t/10)+1
        else:
          t = t/10 
        ins.Jumlah = t
      res.Next()
    if jmlgbt>0:
      ins = ds.InsertRecord(putpos)
      ins.JumlahRekening = jmlgbt
      ins.SetFieldByName('LJENIS.reference_code', trc1)
      ins.SetFieldByName('LJENIS.reference_desc', trd1)
      ins.SetFieldByName('LJENIS.refdata_id', tri1)
      ins.SetFieldByName('LJENISVALUTA.reference_code', trc2)
      ins.SetFieldByName('LJENISVALUTA.reference_desc', trd2)
      ins.SetFieldByName('LJENISVALUTA.refdata_id', tri2)
      ins.SetFieldByName('LHUBBANK.reference_code', trc3)
      ins.SetFieldByName('LHUBBANK.reference_desc', trd3)
      ins.SetFieldByName('LHUBBANK.refdata_id', tri3)
      ins.SetFieldByName('LLOKASI.reference_code', trc4)
      ins.SetFieldByName('LLOKASI.reference_desc', trd4)
      ins.SetFieldByName('LLOKASI.refdata_id', tri4)
      ins.Bulan = 0
      ins.Hari = 0
      ins.Nisbah = 0
      ins.Persen = 0
      t = int(totalgbt/100000)
      if int(str(t)[-1])>5:
        t = (t/10)+1
      else:
        t = t/10 
      ins.Jumlah = t
    if jmlgbd>0:
      ins = ds.AddRecord()
      ins.JumlahRekening = jmlgbd
      ins.SetFieldByName('LJENIS.reference_code', drc1)
      ins.SetFieldByName('LJENIS.reference_desc', drd1)
      ins.SetFieldByName('LJENIS.refdata_id', dri1)
      ins.SetFieldByName('LJENISVALUTA.reference_code', drc2)
      ins.SetFieldByName('LJENISVALUTA.reference_desc', drd2)
      ins.SetFieldByName('LJENISVALUTA.refdata_id', dri2)
      ins.SetFieldByName('LHUBBANK.reference_code', drc3)
      ins.SetFieldByName('LHUBBANK.reference_desc', drd3)
      ins.SetFieldByName('LHUBBANK.refdata_id', dri3)
      ins.SetFieldByName('LLOKASI.reference_code', drc4)
      ins.SetFieldByName('LLOKASI.reference_desc', drd4)
      ins.SetFieldByName('LLOKASI.refdata_id', dri4)
      ins.Bulan = 0
      ins.Hari = 0
      ins.Nisbah = 0
      ins.Persen = 0
      t = int(totalgbd/100000)
      if int(str(t)[-1])>5:
        t = (t/10)+1
      else:
        t = t/10 
      ins.Jumlah = t
    #raise Exception, x

    
