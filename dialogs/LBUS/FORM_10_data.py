import com.ihsan.foundation.appserver as appserver
import com.ihsan.util.modman as modman
import sys
import com.ihsan.util.attrutil as attrutil
import com.ihsan.foundation.pobjecthelper as phelper

# application-level modules, loaded via modman
modman.loadStdModules(globals(), 
  [
    "scripts#form_loaditem"
  ]
)

app = None

def FormOnSetDataEx(uideflist, params):
  global app
  
  config = uideflist.config
  helper = phelper.PObjectHelper(config)
  app = config.AppObject
  app.ConCreate('out')
  if params.DatasetCount == 0 or params.GetDataset(0).Structure.StructureName != 'data':
    return
  
  rec = params.FirstRecord
  reportAttr = {}
  attrutil.transferAttributes(helper, 
   ['class_id', 'period_id', 'branch_id']
   , reportAttr, rec)
  
  oReport   = helper.GetObjectByNames('Report', reportAttr)
  if oReport.isnull:
    # create data
    config.BeginTransaction()
    try:
      oReport = helper.CreatePObject('Report', reportAttr)
      createData(config, rec, oReport) 
      
      config.Commit()
    except:
      config.Rollback()
      raise Exception, str(sys.exc_info()[1])
    #--
    
  form_loaditem.setData(uideflist, params)

def createData(config, rec, oReport):
  global app
  
  def toDate(val):
    if val not in (None,'',0):
      if type(val)==type(0.0):
        val = config.ModLibUtils.DecodeDate(val)
      return '%s%s' % (str(val[1]).zfill(2), str(val[0]))
    else:
      return "''"
  def Jutaan(val):
    if val in (None,''):
      return 0
    val = val/100000
    if int(str(val)[-1])>5:
      val = int((val/10)+1)
    else:
      val = int(val/10)
    if val<0:
      val = val*-1
    return val
  #--
  
  mlu = config.ModLibUtils
  s = '''
    select kode_cabang from branchmember where branch_id=%s
  ''' % (str(rec.branch_id))
  branchmembers = config.CreateSQL(s).RawResult
  listcabang = ''
  while not branchmembers.Eof:
    if listcabang != '':
      listcabang+=', '
    listcabang+=mlu.QuotedStr(branchmembers.kode_cabang)
    branchmembers.Next()
  pid = rec.period_id
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
  s = '''
      select a.*, c.p_saldo, 
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
      replace(to_char(a.jangkawaktubulanmulai, '00')||to_char(a.jangkawaktutahunmulai, '0000'),' ','')  jangkamulai, 
      replace(to_char(a.jangkawaktubulanjt, '00')||to_char(a.jangkawaktutahunjt, '0000'),' ','') jangkajt, 
      decode(fa.overall_col_level, 1, 0.01, 2, 0.05, 3, 0.15, 4, 0.5, 5, 1) ppapval,
      c.p_saldo+c.p_arrear_balance+c.p_mmd_balance pokok,
      c.p_mmd_balance margin,
      r7.reference_code c7, 
      r7.reference_desc d7,
      r7.refdata_id i7,
      a.nisbahbagihasil,
      a.persentasebagihasil,
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
      r11.refdata_id i11,
      r12.reference_code c12, 
      r12.reference_desc d12,
      r12.refdata_id i12,
      r13.reference_code c13, 
      r13.reference_desc d13,
      r13.refdata_id i13
      from %(PrevMonth)s a join %(RekeningTransaksi)s b on (a.nomorrekening=b.nomor_rekening
                                       or substr(a.nomorrekening,1,3)||'A'||substr(a.nomorrekening,4,15)=b.nomor_rekening)
      left outer join %(FinAcc)s fa on (b.nomor_rekening=fa.nomor_rekening)
      left outer join %(SaldoRekening)s c on (b.nomor_rekening=c.nomor_rekening)
      left outer join %(ReferenceData)s r1 on (r1.reference_code=a.statuspembiayaan and r1.reftype_id=220)
      left outer join %(ReferenceData)s r2 on (r2.reference_code=a.jenispenggunaan and r2.reftype_id=235)
      left outer join %(ReferenceData)s r3 on (r3.reference_code=a.orientasipenggunaan and r3.reftype_id=108)
      left outer join %(ReferenceData)s r4 on (r4.reference_code=a.sandivaluta and r4.reftype_id=232)
      left outer join %(ReferenceData)s r5 on (r5.reference_code=a.golongandebitur and r5.reftype_id=225)
      left outer join %(ReferenceData)s r6 on (r6.reference_code=a.hubungandenganbank and r6.reftype_id=124)
      left outer join %(ReferenceData)s r7 on (r7.reference_code=a.kolektibilitas and r7.reftype_id=230)
      left outer join %(ReferenceData)s r8 on (r8.reference_code=a.golonganpembiayaan and r8.reftype_id=247)
      left outer join %(ReferenceData)s r9 on (r9.reference_code=a.sektorekonomi and r9.reftype_id=224)
      left outer join %(ReferenceData)s r10 on (r10.reference_code=a.lokasiproyek and r10.reftype_id=251)
      left outer join %(ReferenceData)s r11 on (r11.reference_code=a.golonganpenjamin and r11.reftype_id=328)
      left outer join %(ReferenceData)s r12 on (r12.reference_code=a.sifat and r12.reftype_id=223)
      left outer join %(ReferenceData)s r13 on (r13.reference_code=a.jenis and r13.reftype_id=236)
      where a.bakidebetbulanlapor>0 and b.kode_cabang in (%(ParamCabang)s)  
  ''' % {
         'PrevMonth' : config.MapDBTableName('lbus.lbus_form_10'),
         'RekeningTransaksi' :config.MapDBTableName('pbscore.rekeningtransaksi'),
         'ReferenceData' : config.MapDBTableName('enterprise.referencedata'),
         'SaldoRekening' : config.MapDBTableName('tmp.cknom_base_pby'),
         'FinAcc' : config.MapDBTableName('financing.finaccount'),
         'ParamCabang' : listcabang
  }
  #query data bln lalu
  #raise Exception, s
  res = config.CreateSQL(s).RawResult
  a = 0
  while not res.Eof:
    a+=1
    if a % 100 == 0 : app.ConWriteln('Proses row data ke-%s' % str(a))     
    #ins = ds.AddRecord()
    ins = config.CreatePObject('LBUS_FORM10')
    ins.report_id = oReport.report_id

    ins.NomorRekening = res.nomorrekening
    ins.JumlahRekening = res.jumlahrekening
    ins.LSTATUSPEMBIAYAAN_refdata_id = res.i1
    ins.LJENISPENGGUNAAN_refdata_id = res.i2
    ins.LORIENTPENGGUNAAN_refdata_id = res.i3
    ins.LJENISVALUTA_refdata_id = res.i4
    ins.LGOLDEBITUR_refdata_id = res.i5
    ins.LHUBBANK_refdata_id = res.i6
    ins.BlnThnMulai = res.jangkamulai
    ins.BlnThnTempo = res.jangkajt
    ins.LKOLEKTIBILITAS_refdata_id = res.i7
    ins.Nisbah = res.nisbahbagihasil
    ins.PersenBagiHasil = res.persentasebagihasil
    ins.LGOLPEMBIAYAAN_refdata_id = res.i8
    ins.LSEKTOREKONOMI_refdata_id = res.i9
    ins.LLOKASIPROYEK_refdata_id = res.i10
    ins.LGOLPENJAMIN_refdata_id = res.i11
    ins.LSIFAT_refdata_id = res.i12
    ins.LJENIS_refdata_id = res.i13
    ins.BagDijamin = res.bagianyangdijamin
    #ins.HargaAwal = res.hargajualawal
    #ins.SaldoHargaPokok = Jutaan(res.pokok)
    #ins.SaldoMargin = Jutaan(res.margin)
    ins.DebetBlnLalu = res.bakidebetbulanlapor
    baki = Jutaan(res.pokok)+Jutaan(res.margin)
    ins.DebetBlnLap = baki
    ins.AgunanPPAP = res.agunan
    if baki in (None,'',0) or res.ppapval in (None,'',0):
      ppap = 0
    else:
      ppap = int(baki*res.ppapval) 
    ins.PPAPDibentuk = ppap
    res.Next()
    #isi data bln lalu
  #-- while
  
  s = '''
       select refdata_id from %s where reference_code='29' and reftype_id=235
  ''' % config.MapDBTableName('enterprise.referencedata')
  jenis_code = config.CreateSQL(s).RawResult.refdata_id    
  s = '''
       select refdata_id from %s where reference_code='9' and reftype_id=108
  ''' % config.MapDBTableName('enterprise.referencedata')
  ori_code = config.CreateSQL(s).RawResult.refdata_id    
  s = '''
       select refdata_id from %s where reference_code='20' and reftype_id=249
  ''' % config.MapDBTableName('enterprise.referencedata')
  gp_code = config.CreateSQL(s).RawResult.refdata_id    
  s = '''
       select refdata_id from %s where reference_code='886' and reftype_id=225
  ''' % config.MapDBTableName('enterprise.referencedata')
  gd_code = config.CreateSQL(s).RawResult.refdata_id    
  s = '''
       select refdata_id from %s where reference_code='9900' and reftype_id=224
  ''' % config.MapDBTableName('enterprise.referencedata')
  sektor_code = config.CreateSQL(s).RawResult.refdata_id    
  s = '''
       select refdata_id from %s where reference_code='000' and reftype_id=328
  ''' % config.MapDBTableName('enterprise.referencedata')
  penjamin_code = config.CreateSQL(s).RawResult.refdata_id    
  s = '''
      select a.*,                                                   
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
      r6.refdata_id i6,
      r7.reference_code c7, 
      r7.reference_desc d7,
      r7.refdata_id i7,
      nvl(rse.refdata_id, %(id_sektor)s) id_se,
      fa.dropping_amount,
      fa.payment_balance,
      round(a.profit_share,2) pshare,
      round(fa.targeted_eqv_rate,2) teqv_rate,
      nvl(agu.total_agunan, fa.dropping_amount) valuation
      from %(FinMusyarakah)s a join %(FinAccount)s fa on (a.nomor_rekening=fa.nomor_rekening) 
      join %(FinSchedule)s sch on (fa.id_schedule=sch.id_schedule and sch.completion_status='F')
      left outer join %(RekeningCustomer)s b on (a.nomor_rekening=b.nomor_rekening)
      left outer join %(AccAdditional)s c on (a.nomor_rekening=c.nomor_rekening)
      left outer join %(CustAdditional)s d on (b.nomor_nasabah=d.nomor_nasabah)
      left outer join %(Sandi)s s1 on (d.ref_sektor_ekonomi=s1.id)
      left outer join map_sektor_ekonomi mse on (s1.kode_1=mse.sid)
      left outer join %(ReferenceData)s rse on (mse.lbu=rse.reference_code and rse.reftype_id=224)
      left outer join %(FinFacility)s e on (fa.facility_no=e.facility_no)
      left outer join %(Nasabah)s f on (b.nomor_nasabah=f.nomor_nasabah)
      left outer join %(SaldoRekening)s g on (a.nomor_rekening=g.nomor_rekening)
      left outer join %(Cabang)s h on (g.kode_cabang=h.kode_cabang)
      left outer join (select fca.NOREK_FINACCOUNT, sum(fcs.valuation) total_agunan from %(ColMap)s fca, %(Collateral)s fcs
                      where fca.NOREK_FINCOLLATERALASSET=fcs.nomor_rekening
                      group by fca.NOREK_FINACCOUNT ) agu
            on (a.nomor_rekening=agu.norek_finaccount)
      left outer join %(ReferenceData)s r1 on (r1.reference_code=decode(c.status_piutang,'10','10','20') and r1.reftype_id=219)
      left outer join %(ReferenceData)s r2 on (r2.reference_code=decode(e.currency_code,'IDR','360','USD','840','SIN','702') and r2.reftype_id=232)
      left outer join %(ReferenceData)s r3 on (r3.reference_code=decode(f.is_pihak_terkait, 'T','1','2') and r3.reftype_id=124)
      left outer join %(ReferenceData)s r4 on (r4.reference_code=decode(fa.overall_col_level, 1,'1',2,'2',3,'3',4,'4',5,'5') and r4.reftype_id=230)
      left outer join %(ReferenceData)s r5 on (r5.reference_code=decode(a.finmusyarakahaccount_type, 'D', '10', '20') and r5.reftype_id=236)
      left outer join %(ReferenceData)s r6 on (r6.reference_code=decode(fa.financing_model, 'T', '9', '1') and r6.reftype_id=223)
      left outer join %(ReferenceData)s r7 on (r7.reference_code=h.kode_lokasi and r7.reftype_id=251)
      where g.kode_cabang in (%(ParamCabang)s)
           and fa.dropping_date <= to_date('%(TanggalLaporan)s','dd-mm-yyyy')
           and not exists (select null from %(PrevMonth)s ne where 
                                  a.nomor_rekening=ne.nomorrekening or 
                                  a.nomor_rekening=substr(ne.nomorrekening,1,3)||'A'||substr(ne.nomorrekening,4,15)
           )
  ''' % { 
       'FinMusyarakah' : config.MapDBTableName('financing.finmusyarakahaccount'),
       'FinAccount' : config.MapDBTableName('financing.finaccount'),
       'FinSchedule' : config.MapDBTableName('financing.finpaymentschedule'), 
       'RekeningCustomer' : config.MapDBTableName('core.rekeningcustomer'),
       'AccAdditional' : config.MapDBTableName('financing.finaccadditionaldata'),
       'CustAdditional' : config.MapDBTableName('financing.fincustadditionaldata'),
       'FinFacility' : config.MapDBTableName('financing.finfacility'),
       'ReferenceData' : config.MapDBTableName('enterprise.referencedata'),
       'PrevMonth' : config.MapDBTableName('lbus.lbus_form_10'),
       'Nasabah' : config.MapDBTableName('core.Nasabah'),
       'Cabang'  : config.MapDBTableName('enterprise.cabang'),
       'SaldoRekening' : config.MapDBTableName('tmp.cknom_base_pby'),
       'ParamCabang' : listcabang,
       'Collateral' : config.MapDBTableName('financing.fincollateralasset'),
       'ColMap' : config.MapDBTableName('financing.fincollateralaccount'),
       'Sandi' : config.MapDBTableName('financing.sandi'),
       'id_sektor' : str(sektor_code),
       'TanggalLaporan' : config.FormatDateTime('dd-mm-yyyy', repdate)
         }
  res = config.CreateSQL(s).RawResult
  #i=0
  while not res.Eof:
  #while not res.Eof:
    a+=1
    if a % 100 == 0 : app.ConWriteln('Proses Row data ke-%s' % str(a))
    #ins = ds.AddRecord()
    ins = config.CreatePObject('LBUS_FORM10')
    ins.report_id = oReport.report_id

    ins.NomorRekening = res.nomor_rekening
    ins.JumlahRekening = 1

    ins.LSTATUSPEMBIAYAAN_refdata_id = res.i1

    ins.LJENISVALUTA_refdata_id = res.i2
    ins.LHUBBANK_refdata_id = res.i3
    ins.BlnThnMulai = toDate(res.tgl_mulai)
    ins.BlnThnTempo = toDate(res.tgl_tempo)
    ins.LKOLEKTIBILITAS_refdata_id = res.i4
    ins.LJENIS_refdata_id = res.i5
    ins.LSIFAT_refdata_id = res.i6
    ins.LLOKASIPROYEK_refdata_id = res.i7

    ins.LJENISPENGGUNAAN_refdata_id = jenis_code
    ins.LORIENTPENGGUNAAN_refdata_id = ori_code
    ins.LSEKTOREKONOMI_refdata_id = res.id_se
    ins.LGOLPENJAMIN_refdata_id = penjamin_code
    ins.LGOLDEBITUR_refdata_id = gd_code
    ins.LGOLPEMBIAYAAN_refdata_id = gp_code

    ins.Nisbah = res.pshare
    ins.PersenBagiHasil = res.teqv_rate
    ins.Plafond = Jutaan(res.dropping_amount)
    ins.DebetBlnLap = Jutaan(res.dropping_amount+res.payment_balance)
    ins.AgunanPPAP = Jutaan(res.valuation)
    res.Next()

  #app.ConRead('ok')

def FormOnSetDataEx_1(uideflist, params):
  def toDate(val):
    if val not in (None,'',0):
      if type(val)==type(0.0):
        val = config.ModLibUtils.DecodeDate(val)
      return '%s%s' % (str(val[1]).zfill(2), str(val[0]))
    else:
      return "''"
  def Jutaan(val):
    if val in (None,''):
      return 0
    val = val/100000
    if int(str(val)[-1])>5:
      val = int((val/10)+1)
    else:
      val = int(val/10)
    if val<0:
      val = val*-1
    return val
  config = uideflist.config
  if params.DatasetCount == 0 or params.GetDataset(0).Structure.StructureName != 'data':
    return
  
  app = config.AppObject
  app.ConCreate('out')

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
        select a.*,                                                   
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
        r6.refdata_id i6,
        fa.dropping_amount,
        fa.payment_balance,
        round(a.profit_share,2) pshare,
        round(fa.targeted_eqv_rate,2) teqv_rate,
        0 valuation
        from %(FinMusyarakah)s a join %(FinAccount)s fa on (a.nomor_rekening=fa.nomor_rekening) 
        join %(FinSchedule)s sch on (fa.id_schedule=sch.id_schedule and sch.completion_status='F')
        left outer join %(RekeningCustomer)s b on (a.nomor_rekening=b.nomor_rekening)
        left outer join %(AccAdditional)s c on (a.nomor_rekening=c.nomor_rekening)
        left outer join %(CustAdditional)s d on (b.nomor_nasabah=d.nomor_nasabah)
        left outer join %(FinFacility)s e on (fa.facility_no=e.facility_no)
        left outer join %(Nasabah)s f on (b.nomor_nasabah=f.nomor_nasabah)
        left outer join %(SaldoRekening)s g on (a.nomor_rekening=g.nomor_rekening)
        left outer join %(ReferenceData)s r1 on (r1.reference_code=decode(c.status_piutang,'10','10','20') and r1.reftype_id=219)
        left outer join %(ReferenceData)s r2 on (r2.reference_code=decode(e.currency_code,'IDR','360','USD','840','SIN','702') and r2.reftype_id=232)
        left outer join %(ReferenceData)s r3 on (r3.reference_code=decode(f.is_pihak_terkait, 'T','1','2') and r3.reftype_id=124)
        left outer join %(ReferenceData)s r4 on (r4.reference_code=decode(fa.overall_col_level, 1,'1',2,'2',3,'3',4,'4',5,'5') and r4.reftype_id=230)
        left outer join %(ReferenceData)s r5 on (r5.reference_code=decode(a.finmusyarakahaccount_type, 'D', '10', '20') and r5.reftype_id=236)
        left outer join %(ReferenceData)s r6 on (r6.reference_code=decode(fa.financing_model, 'T', '9', '1') and r6.reftype_id=223)
        where g.kode_cabang in (%(ParamCabang)s)
             and fa.dropping_date <= to_date('%(TanggalLaporan)s','dd-mm-yyyy')
             and not exists (select null from %(PrevMonth)s ne where 
                                    a.nomor_rekening=ne.nomorrekening or 
                                    a.nomor_rekening=substr(ne.nomorrekening,1,3)||'A'||substr(ne.nomorrekening,4,15)
    ''' % { 
         'FinMusyarakah' : config.MapDBTableName('financing.finmusyarakahaccount'),
         'FinAccount' : config.MapDBTableName('financing.finaccount'),
         'FinSchedule' : config.MapDBTableName('financing.finpaymentschedule'), 
         'RekeningCustomer' : config.MapDBTableName('core.rekeningcustomer'),
         'AccAdditional' : config.MapDBTableName('financing.finaccadditionaldata'),
         'CustAdditional' : config.MapDBTableName('financing.fincustadditionaldata'),
         'FinFacility' : config.MapDBTableName('financing.finfacility'),
         'ReferenceData' : config.MapDBTableName('enterprise.referencedata'),
         'PrevMonth' : config.MapDBTableName('lbus.lbus_form_10'),
         'Nasabah' : config.MapDBTableName('core.Nasabah'),
         'SaldoRekening' : config.MapDBTableName('tmp.cknom_base_pby'),
         'ParamCabang' : listcabang,
         'Collateral' : config.MapDBTableName('financing.fincollateralasset'),
         'TanggalLaporan' : config.FormatDateTime('dd-mm-yyyy', repdate)
           }
    res = config.CreateSQL(s).RawResult
    i=0
    while not res.Eof:
    #while not res.Eof:
      i+=1
      app.ConWriteln('Proses Row data ke-%s' % str(i))
      ins = ds.AddRecord()
      ins.NomorRekening = res.nomor_rekening
      ins.JumlahRekening = 1
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
      ins.Nisbah = res.pshare
      ins.PersenBagiHasil = res.teqv_rate
      ins.Plafond = Jutaan(res.dropping_amount)
      ins.DebetBlnLap = Jutaan(res.dropping_amount+res.payment_balance)
      ins.AgunanPPAP = Jutaan(res.valuation)
      res.Next()









#--

def Backup_LastMonth(config): #backup script
    s = '''
        select a.*, c.p_saldo, 
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
        decode(fa.overall_col_level, 1, 0.01, 2, 0.05, 3, 0.15, 4, 0.5, 5, 1) ppapval,
        c.p_saldo+c.p_arrear_balance+c.p_mmd_balance pokok,
        c.p_mmd_balance margin,
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
        left outer join %(FinAcc)s fa on (b.nomor_rekening=fa.nomor_rekening)
        left outer join %(SaldoRekening)s c on (b.nomor_rekening=c.nomor_rekening)
        left outer join %(ReferenceData)s r1 on (r1.reference_code=a.statuspembiayaan and r1.reftype_id=220)
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
           'PrevMonth' : config.MapDBTableName('lbus.lbus_form_10'),
           'RekeningTransaksi' :config.MapDBTableName('pbscore.rekeningtransaksi'),
           'ReferenceData' : config.MapDBTableName('enterprise.referencedata'),
           'SaldoRekening' : config.MapDBTableName('tmp.cknom_base_pby'),
           'FinAcc' : config.MapDBTableName('financing.finaccount'),
           'ParamCabang' : listcabang
    }
    #query data bln lalu
    #raise Exception, s
    res = config.CreateSQL(s).RawResult
    a = 0
    while not res.Eof:
      a+=1
      app.ConWriteln('Proses row data ke-%s' % str(a))     
      ins = ds.AddRecord()
      ins.NomorRekening = res.nomorrekening
      ins.JumlahRekening = res.jumlahrekening
      ins.SetFieldByName('LSTATUSPEMBIAYAAN.refdata_id', res.i1)
      ins.SetFieldByName('LSTATUSPEMBIAYAAN.reference_code', res.c1)
      ins.SetFieldByName('LSTATUSPEMBIAYAAN.reference_desc', res.d1)
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
      #ins.HargaAwal = res.hargajualawal
      #ins.SaldoHargaPokok = Jutaan(res.pokok)
      #ins.SaldoMargin = Jutaan(res.margin)
      ins.DebetBlnLalu = res.bakidebetbulanlapor
      baki = Jutaan(res.pokok)+Jutaan(res.margin)
      ins.DebetBlnLap = baki
      ins.AgunanPPAP = res.agunan
      if baki in (None,'',0) or res.ppapval in (None,'',0):
        ppap = 0
      else:
        ppap = int(baki*res.ppapval) 
      ins.PPAPDibentuk = ppap
      res.Next()
      #isi data bln lalu
