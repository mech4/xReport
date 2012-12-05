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
  app = config.AppObject
  app.ConCreate('out')
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
        select a.*, b.saldo, 
        r1.reference_code c1, 
        r1.reference_desc d1,
        r1.refdata_id i1,
        r2.reference_code c2, 
        r2.reference_desc d2,
        r2.refdata_id i2,
        r3.reference_code c3, 
        r3.reference_desc d3,
        r3.refdata_id i3,
        r4.reference_code c4, 
        r4.reference_desc d4,
        r4.refdata_id i4,
        r5.reference_code c5, 
        r5.reference_desc d5,
        r5.refdata_id i5,
        r6.reference_code c6, 
        r6.reference_desc d6,
        r6.refdata_id i6,
        to_char(a.jangkawaktubulanmulai, '00')||to_char(a.jangkawaktutahunmulai) jangkamulai, 
        to_char(a.jangkawaktubulanjt, '00')||to_char(a.jangkawaktutahunjt) jangkajt, 
        r7.reference_code c7, 
        r7.reference_desc d7,
        r7.refdata_id i7,
        a.persentasemargin,
        r8.reference_code c8, 
        r8.reference_desc d8,
        r8.refdata_id i8,
        r9.reference_code c9, 
        r9.reference_desc d9,
        r9.refdata_id i9,
        r10.reference_code c10, 
        r10.reference_desc d10,
        r10.refdata_id i10,
        r11.reference_code c11, 
        r11.reference_desc d11,
        r11.refdata_id i11
        from %(PrevMonth)s a join %(RekeningTransaksi)s b on (a.nomorrekening=b.nomor_rekening
                                         or substr(a.nomorrekening,1,3)||'A'||substr(a.nomorrekening,4,15)=b.nomor_rekening)
        left outer join %(ReferenceData)s r1 on (r1.reference_code=a.statuspiutang and r1.reftype_id=219)
        left outer join %(ReferenceData)s r2 on (r2.reference_code=a.jenispenggunaan and r2.reftype_id=235)
        left outer join %(ReferenceData)s r3 on (r3.reference_code=a.orientasipenggunaan and r3.reftype_id=108)
        left outer join %(ReferenceData)s r4 on (r4.reference_code=a.sandivaluta and r4.reftype_id=232)
        left outer join %(ReferenceData)s r5 on (r5.reference_code=a.golongandebitur and r5.reftype_id=225)
        left outer join %(ReferenceData)s r6 on (r6.reference_code=a.hubungandenganbank and r6.reftype_id=124)
        left outer join %(ReferenceData)s r7 on (r7.reference_code=a.kolektibilitas and r7.reftype_id=230)
        left outer join %(ReferenceData)s r8 on (r8.reference_code=a.golonganpiutang and r8.reftype_id=247)
        left outer join %(ReferenceData)s r9 on (r9.reference_code=a.sektorekonomi and r9.reftype_id=224)
        left outer join %(ReferenceData)s r10 on (r10.reference_code=a.lokasiproyek and r10.reftype_id=251)
        left outer join %(ReferenceData)s r11 on (r11.reference_code=a.golonganpenjamin and r11.reftype_id=328)
        where a.bakidebetbulanlapor>0 and b.kode_cabang in (%(ParamCabang)s)  
    ''' % {
           'PrevMonth' : config.MapDBTableName('lbus.lbus_form_06'),
           'RekeningTransaksi' :config.MapDBTableName('pbscore.rekeningtransaksi'),
           'ReferenceData' : config.MapDBTableName('enterprise.referencedata'),
           'ParamCabang' : listcabang
    }
    #query data bln lalu
    #raise Exception, s
    res = config.CreateSQL(s).RawResult
    a = 0
    while not res.Eof and a<10:
      a+=1
      app.ConWriteln('Proc rec #%s' % str(a))     
      ins = ds.AddRecord()
      ins.NomorRekening = res.nomorrekening
      ins.JumlahRekening = res.jumlahrekening
      ins.SetFieldByName('LSTATUSPIUTANG.refdata_id', res.i1)
      ins.SetFieldByName('LSTATUSPIUTANG.reference_code', res.c1)
      ins.SetFieldByName('LSTATUSPIUTANG.reference_desc', res.d1)
      ins.SetFieldByName('LJENISPENGGUNAAN.refdata_id', res.i2)
      ins.SetFieldByName('LJENISPENGGUNAAN.reference_code', res.c2)
      ins.SetFieldByName('LJENISPENGGUNAAN.reference_desc', res.d2)
      ins.SetFieldByName('LORIENTPENGGUNAAN.refdata_id', res.i3)
      ins.SetFieldByName('LORIENTPENGGUNAAN.reference_code', res.c3)
      ins.SetFieldByName('LORIENTPENGGUNAAN.reference_desc', res.d3)
      ins.SetFieldByName('LJENISVALUTA.refdata_id', res.i4)
      ins.SetFieldByName('LJENISVALUTA.reference_code', res.c4)
      ins.SetFieldByName('LJENISVALUTA.reference_desc', res.d4)
      ins.SetFieldByName('LGOLDEBITUR.refdata_id', res.i5)
      ins.SetFieldByName('LGOLDEBITUR.reference_code', res.c5)
      ins.SetFieldByName('LGOLDEBITUR.reference_desc', res.d5)
      ins.SetFieldByName('LHUBBANK.refdata_id', res.i6)
      ins.SetFieldByName('LHUBBANK.reference_code', res.c6)
      ins.SetFieldByName('LHUBBANK.reference_desc', res.d6)
      ins.Mulai = res.jangkamulai
      ins.JatuhTempo = res.jangkajt
      ins.SetFieldByName('LKOLEKTIBILITAS.refdata_id', res.i7)
      ins.SetFieldByName('LKOLEKTIBILITAS.reference_code', res.c7)
      ins.SetFieldByName('LKOLEKTIBILITAS.reference_desc', res.d7)
      ins.PersenMargin = res.persentasemargin
      ins.SetFieldByName('LGOLPIUTANG.refdata_id', res.i8)
      ins.SetFieldByName('LGOLPIUTANG.reference_code', res.c8)
      ins.SetFieldByName('LGOLPIUTANG.reference_desc', res.d8)
      ins.SetFieldByName('LSEKTOREKONOMI.refdata_id', res.i9)
      ins.SetFieldByName('LSEKTOREKONOMI.reference_code', res.c9)
      ins.SetFieldByName('LSEKTOREKONOMI.reference_desc', res.d9)
      ins.SetFieldByName('LLOKASIPROYEK.refdata_id', res.i10)
      ins.SetFieldByName('LLOKASIPROYEK.reference_code', res.c10)
      ins.SetFieldByName('LLOKASIPROYEK.reference_desc', res.d10)
      ins.SetFieldByName('LGOLPENJAMIN.refdata_id', res.i11)
      ins.SetFieldByName('LGOLPENJAMIN.reference_code', res.c11)
      ins.SetFieldByName('LGOLPENJAMIN.reference_desc', res.d11)
      ins.BagDijamin = res.bagianyangdijamin
      ins.HargaAwal = res.hargajualawal
      ins.SaldoHargaPokok = res.saldohargapokok
      ins.SaldoMargin = res.saldomargin
      ins.DebetBlnLalu = res.bakidebetbulanlapor
      saldo = res.saldo/100000
      if int(str(saldo)[-1])>5:
        saldo = int((saldo/10)+1)
      else:
        saldo = int(saldo/10)
      if saldo<0:
        saldo = saldo*-1
      ins.DebetBlnLap = saldo
      ins.AgunanPPAP = res.agunan
      ins.PPAPDibentuk = res.ppap
      res.Next()
      #isi data bln lalu
      
def Tst(self):     
      
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
        r4.refdata_id i4
        from (select nomor_rekening, count(nomor_rekening) jml from %s
        group by nomor_rekening) a join %s fa on (a.nomor_rekening=fa.nomor_rekening) 
        left outer join %s b on (a.nomor_rekening=b.nomor_rekening)
        left outer join %s c on (a.nomor_rekening=c.nomor_rekening)
        left outer join %s d on (b.nomor_nasabah=d.nomor_nasabah)
        left outer join %s e on (fa.facility_no=e.facility_no)
        left outer join %s r1 on (r1.reference_code=decode(c.status_piutang,'10','10','20') and r1.reftype_id=219)
        left outer join %s r2 on (r2.reference_code=decode(e.currency_code,'IDR','360','USD','840','SIN','702') and r2.reftype_id=232)
        left outer join %s s1 on (d.ref_hub_bank=s1.id)
        left outer join %s r3 on (r3.reference_code=s1.kode_1 and r3.reftype_id=124)
        left outer join %s r4 on (to_number(r4.reference_code)=to_number(fa.overall_col_level) and r4.reftype_id=235)
        where e.kode_cabang in (%s)
    ''' % ( 
           config.MapDBTableName('financing.finmurabahahaccount'),
           config.MapDBTableName('financing.finaccount'),
           config.MapDBTableName('core.rekeningcustomer'),
           config.MapDBTableName('financing.finaccadditionaldata'),
           config.MapDBTableName('financing.fincustadditionaldata'),
           config.MapDBTableName('financing.finfacility'),
           config.MapDBTableName('enterprise.referencedata'),
           config.MapDBTableName('enterprise.referencedata'),
           config.MapDBTableName('financing.sandi'),
           config.MapDBTableName('enterprise.referencedata'),
           config.MapDBTableName('enterprise.referencedata'),
           listcabang
           )
    res = config.CreateSQL(s).RawResult
    while not res.Eof:
      ins = ds.AddRecord()
      ins.NomorRekening = res.nomor_rekening
      ins.JumlahRekening = res.jml
      ins.SetFieldByName('LSTATUSPIUTANG.reference_code', res.c1)
      ins.SetFieldByName('LSTATUSPIUTANG.reference_desc', res.d1)
      ins.SetFieldByName('LSTATUSPIUTANG.refdata_id', res.i1)
      ins.SetFieldByName('LJENISVALUTA.reference_code', res.c2)
      ins.SetFieldByName('LJENISVALUTA.reference_desc', res.d2)
      ins.SetFieldByName('LJENISVALUTA.refdata_id', res.i2)
      ins.SetFieldByName('LHUBBANK.reference_code', res.c3)
      ins.SetFieldByName('LHUBBANK.reference_desc', res.d3)
      ins.SetFieldByName('LHUBBANK.refdata_id', res.i3)
      ins.Mulai = toDate(res.tgl_mulai)
      ins.JatuhTempo = toDate(res.tgl_tempo)
      ins.SetFieldByName('LKOLEKTIBILITAS.reference_code', res.c4)
      ins.SetFieldByName('LKOLEKTIBILITAS.reference_desc', res.d4)
      ins.SetFieldByName('LKOLEKTIBILITAS.refdata_id', res.i4)
      res.Next()
