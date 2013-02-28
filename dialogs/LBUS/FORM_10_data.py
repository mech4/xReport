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
      return "000000"           
      
  report_id = oReport.report_id
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
  bln_lalu = bln - 1
  if bln_lalu==0:
    bln_lalu = 12
    thn_lalu = thn - 1
  else:
    thn_lalu = thn
  repdate = config.CreateSQL('''
     select max(tanggal) rd from %(TBL)s
     where extract(month from tanggal)='%(BLN)s' and extract(year from tanggal)='%(THN)s'
  ''' % { "TBL":config.MapDBTableName('tmp.cknom_base_daily'),"BLN":str(bln),"THN":str(thn)}).RawResult.rd
  lastmonthdate = config.CreateSQL('''
     select max(tanggal) rd from %(TBL)s
     where extract(month from tanggal)='%(BLN)s' and extract(year from tanggal)='%(THN)s'
  ''' % { "TBL":config.MapDBTableName('tmp.cknom_base_daily'),"BLN":str(bln_lalu),"THN":str(thn_lalu)}).RawResult.rd
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
          insert into lbus_form10 (
          NOMORREKENING,
          JUMLAHREKENING,
          LSTATUSPEMBIAYAAN_REFDATA_ID,
          LSIFAT_REFDATA_ID,
          LJENIS_REFDATA_ID,
          LJENISPENGGUNAAN_REFDATA_ID,
          LORIENTPENGGUNAAN_REFDATA_ID,
          LJENISVALUTA_REFDATA_ID,
          LGOLDEBITUR_REFDATA_ID,
          LHUBBANK_REFDATA_ID,
          BLNTHNMULAI,
          BLNTHNTEMPO,
          LKOLEKTIBILITAS_REFDATA_ID,
          NISBAH,
          PERSENBAGIHASIL,
          LGOLPEMBIAYAAN_REFDATA_ID,
          LSEKTOREKONOMI_REFDATA_ID,
          LLOKASIPROYEK_REFDATA_ID,
          LGOLPENJAMIN_REFDATA_ID,
          BAGDIJAMIN,
          PLAFOND,
          KELONGGARANTARIK,
          DEBETBLNLALU,
          DEBETBLNLAP,
          AGUNANPPAP,
          PPAPDIBENTUK,
          ITEM_ID,
          REPORT_ID
          )
          select
          a.nomor_rekening,
          1 jumlah_rekening,
          r1.refdata_id i1_status_pembiayaan,
          r13.refdata_id id13_sifat,
          r12.refdata_id id12_jenis,
          nvl(r2.refdata_id, %(jenis_code)s) i2_jenis_penggunaan,
          nvl(r3.refdata_id, %(ori_code)s) id3_orientasi_penggunaan,
          r4.refdata_id id4_kode_valuta,
          nvl(r5.refdata_id, %(gd_code)s) id5_gol_debitur,
          r6.refdata_id id6_hub_dgn_bank,
          to_char(b.dropping_date, 'mmyyyy') blnthn_mulai,
          to_char(nvl(b.due_date, add_months(b.dropping_date, 12)), 'mmyyyy') blnthn_jatuh_tempo,
          r11.refdata_id id11_kolektibilitas,
          round(a.profit_share,2) pshare,
          round(b.targeted_eqv_rate,2) persen,
          nvl(r7.refdata_id, %(gp_code)s) id7_gol_pembiayaan,
          nvl(r8.refdata_id, %(sektor_code)s) id8_sektor_ekonomi,
          r9.refdata_id id9_lokasi_proyek,
          nvl(r10.refdata_id, %(penjamin_code)s) id10_gol_penjamin,
          d.bagian_yang_dijamin bag_dijamin,
          round((b.dropping_amount)/1000000, 0) plafond,
          nvl(round((b.dropping_amount)/1000000, 0)-round(((g.p_saldo+g.p_arrear_balance)*-1)/1000000, 0), 0) kel_tarik,
          round(((h.p_saldo+h.p_arrear_balance)*-1)/1000000, 0) baki_lalu,
          round(((g.p_saldo+g.p_arrear_balance)*-1)/1000000, 0) baki_lapor,
          round((agu.total_agunan)/1000000, 0) agunan,
          round((b.reserved_common_balance+b.reserved_loss_balance)/1000000, 0) ppap,
          seq_lbus_form10.nextval seq,
          %(ReportId)s report_id
          from %(FinMusyarakah)s a left outer join %(FinAccount)s b on (a.nomor_rekening=b.nomor_rekening)
          left outer join %(RekeningCustomer)s c on (a.nomor_rekening=c.nomor_rekening)
          left outer join %(AdditionalAcc)s d on (a.nomor_rekening=d.nomor_rekening)
          left outer join %(AdditionalCust)s e on (c.nomor_nasabah=e.nomor_nasabah)
          left outer join %(FinFacility)s f on (b.facility_no=f.facility_no)
          left outer join %(SaldoRekening)s g on (a.nomor_rekening=g.nomor_rekening and g.tanggal=to_date('%(TglLaporan)s', 'dd-mm-yyyy'))
          left outer join %(SaldoRekening)s h on (a.nomor_rekening=h.nomor_rekening and h.tanggal=to_date('%(TglBlnLalu)s', 'dd-mm-yyyy'))
          left outer join %(Nasabah)s i on (c.nomor_nasabah=i.nomor_nasabah)
          left outer join %(Cabang)s j on (g.kode_cabang=j.kode_cabang)
          left outer join (select fca.NOREK_FINACCOUNT, sum(fcs.valuation) total_agunan from %(ColMap)s fca, %(ColAsset)s fcs
              where fca.NOREK_FINCOLLATERALASSET=fcs.nomor_rekening
              group by fca.NOREK_FINACCOUNT ) agu
            on (a.nomor_rekening=agu.norek_finaccount)
          left outer join %(ReferenceData)s r1 on (r1.reference_code=decode(b.restructure_counter,0,'20','10') and r1.reftype_id=220)
          left outer join %(ReferenceData)s r2 on (r2.reference_code=d.lbus_jenis_penggunaan and r2.reftype_id=235)
          left outer join %(ReferenceData)s r3 on (r3.reference_code=d.lbus_orientasi_penggunaan and r3.reftype_id=108)
          left outer join %(ReferenceData)s r4 on (r4.reference_code=decode(f.currency_code,'IDR','360','USD','840','SIN','702', '360') and r4.reftype_id=232)
          left outer join %(ReferenceData)s r5 on (r5.reference_code=e.lbus_golongan_debitur and r5.reftype_id=225)
          left outer join %(ReferenceData)s r6 on (r6.reference_code=decode(i.is_pihak_terkait, 'T','1','2') and r6.reftype_id=124)
          left outer join %(ReferenceData)s r11 on (r11.reference_code=decode(b.overall_col_level, 1,'1',2,'2',3,'3',4,'4',5,'5') and r11.reftype_id=230)
          left outer join %(ReferenceData)s r12 on (r12.reference_code=decode(a.finmusyarakahaccount_type, 'D', '10', '20') and r12.reftype_id=236)
          left outer join %(ReferenceData)s r13 on (r13.reference_code=decode(b.financing_model, 'T', '9', '1') and r13.reftype_id=223)
          left outer join %(ReferenceData)s r7 on (r7.reference_code=d.lbus_golongan_piutang and r7.reftype_id=247)
          left outer join %(ReferenceData)s r8 on (r8.reference_code=d.lbus_sektor_ekonomi_sid and r8.reftype_id=224)
          left outer join %(ReferenceData)s r9 on (r9.reference_code=nvl(d.lbus_lokasi_proyek, j.kode_lokasi) and r9.reftype_id=251)
          left outer join %(ReferenceData)s r10 on (r10.reference_code=d.lbus_penjamin and r10.reftype_id=328)
          where g.kode_cabang in (%(ListCabang)s)
          and b.dropping_date <= to_date('%(TglLaporan)s', 'dd-mm-yyyy')
          and nvl((g.p_saldo+g.p_arrear_balance)*-1,0)<>0
  ''' % {
          "jenis_code" : str(jenis_code),
          "ori_code" : str(ori_code),
          "gd_code" : str(gd_code),
          "gp_code" : str(gp_code),
          "sektor_code" : str(sektor_code),
          "penjamin_code" : str(penjamin_code),
          "ReportId" : str(report_id),
          "FinMusyarakah" : config.MapDBTableName('financing.finmusyarakahaccount'),
          "FinAccount" : config.MapDBTableName('financing.finaccount'),
          "FinSchedule" : config.MapDBTableName('financing.finpaymentschedule'), 
          "RekeningCustomer" : config.MapDBTableName('core.rekeningcustomer'),
          "Nasabah" : config.MapDBTableName('core.nasabah'),
          "AdditionalAcc" : config.MapDBTableName('financing.finaccadditionaldata'),
          "AdditionalCust" : config.MapDBTableName('financing.fincustadditionaldata'),
          "FinFacility" : config.MapDBTableName('financing.finfacility'),
          "SaldoRekening" : config.MapDBTableName('tmp.cknom_base_daily'),
          "ReferenceData" : config.MapDBTableName('enterprise.referencedata'),
          "ColAsset" : config.MapDBTableName('financing.fincollateralasset'),
          "ColMap" : config.MapDBTableName('financing.fincollateralaccount'),
          "Cabang" : config.MapDBTableName('enterprise.cabang'),
          "TglLaporan" : '%s-%s-%s' % (str(repdate[2]).zfill(2),str(repdate[1]).zfill(2),str(repdate[0]).zfill(4)),
          "TglBlnLalu" : '%s-%s-%s' % (str(lastmonthdate[2]).zfill(2),str(lastmonthdate[1]).zfill(2),str(lastmonthdate[0]).zfill(4)),
          "ListCabang" : listcabang
  }
  #app.ConWriteln(s)
  #app.ConRead('c')
  config.ExecSQL(s)
  config.Commit()

  #Hitung total row
  s = '''
        select count(*) "value" from lbus_form10 where report_id=%s 
  ''' % str(report_id)
  jmlrec = config.CreateSQL(s).RawResult.value
  
  #Balancing Sum Baki Bulan Laporan dengan Form 01 sandi 160+161
  #Ambil nilai pada form01
  s = '''
       select round(sum(balancecumulative)/1000000, 0) "value" from table(%(Saldo)s(to_date('%(TglLaporan)s', 'dd-mm-yyyy')))
       where (
  ''' % {
          "Saldo" : config.MapDBTableName('core.getdailybalanceat'),
          "TglLaporan" : '%s-%s-%s' % (str(repdate[2]).zfill(2),str(repdate[1]).zfill(2),str(repdate[0]).zfill(4)),
          "ListCabang" : listcabang
  }
  s+= '''
        account_code like '109010110001%' or account_code like '109010110011%' or account_code like '109010120001%' or account_code like '109010120011%' or 
        account_code like '109010130001%' or account_code like '109010130011%' or account_code like '109010210001%' or account_code like '109010210011%' or 
        account_code like '109010220001%' or account_code like '109010220011%' or account_code like '109010230001%' or account_code like '109010230011%' or 
        account_code like '109010310001%' or account_code like '109010310011%' or account_code like '109010320001%' or account_code like '109010320011%' or 
        account_code like '109010330001%' or account_code like '109010330011%' or account_code like '109020110001%' or account_code like '109020110011%' or 
        account_code like '109020120001%' or account_code like '109020120011%' or account_code like '109020130001%' or account_code like '109020130011%' or 
        account_code like '109020210001%' or account_code like '109020210011%' or account_code like '109020220001%' or account_code like '109020220011%' or 
        account_code like '109020230001%' or account_code like '109020230011%' or account_code like '109020310001%' or account_code like '109020310011%' or 
        account_code like '109020320001%' or account_code like '109020320011%' or account_code like '109020330001%' or account_code like '109020330011%'
  '''
  s+= '''
       ) 
       and branch_code in (%(ListCabang)s)
       and currency_code='IDR'
  ''' % {
          "Saldo" : config.MapDBTableName('core.getdailybalanceat'),
          "TglLaporan" : '%s-%s-%s' % (str(repdate[2]).zfill(2),str(repdate[1]).zfill(2),str(repdate[0]).zfill(4)),
          "ListCabang" : listcabang
  }
  totaldebetf1 = int(config.CreateSQL(s).RawResult.value)
  #Hitung total pada Form10
  s = '''
        select sum(debetblnlap) "value" from lbus_form10 where report_id=%s
  ''' % str(report_id)
  totaldebetf10 = int(config.CreateSQL(s).RawResult.value)
  #Hitung Selisih
  selisihdebet = totaldebetf1-totaldebetf10
  app.ConWriteln('Tgl Laporan : %s-%s-%s' % (str(repdate[2]).zfill(2),str(repdate[1]).zfill(2),str(repdate[0]).zfill(4)))
  app.ConWriteln('total form 01 : %s' % str(totaldebetf1))
  app.ConWriteln('total form 10 : %s' % str(totaldebetf10))
  app.ConWriteln('Selisih : %s' % str(selisihdebet))

  x_inc=1
  #Jika selisih bernilai negatif (Form06 > Form01) ubah increment menjadi decrement
  if selisihdebet<0:
    selisihdebet=selisihdebet*-1
    x_inc = -1

  #Jika selisih > jml row, hitung ulang increment dan isikan dvcount
  dvcount=0
  if selisihdebet>jmlrec:
    dvcount = int(selisihdebet/jmlrec)
    selisihdebet = selisihdebet % jmlrec

  #Cari Kandidat Adjustment Row
  s = '''
      select debetblnlalu-debetblnlap val, count(*) jml from lbus_form10 
      where report_id=%s 
      group by debetblnlalu-debetblnlap
      order by debetblnlalu-debetblnlap desc
  ''' % str(report_id)
  res = config.CreateSQL(s).RawResult
  n = 0
  val = 0
  while n<selisihdebet and not res.Eof:
    n += int(res.jml)
    val = int(res.val)
    #app.ConWriteln('Val[%s] : %s' % (str(val),str(n)))
    res.Next() 
  config.Commit()
  
  #Update baki pada adjustment row
  s = '''
          update lbus_form10 set debetblnlap=debetblnlap+%(Increment)s
          where nomorrekening in (
          select nomorrekening from (
          select rownum, a.* from (
          select nomorrekening, debetblnlap, debetblnlalu 
          from lbus_form10 
          where report_id=%(ReportId)s 
          and debetblnlalu-debetblnlap>=%(MinVal)s
          order by debetblnlap desc) a
          where rownum<=%(Selisih)s)) and report_id=%(ReportId)s
  ''' % {
          "Increment" : str(x_inc), 
          "ReportId" : str(report_id), 
          "MinVal" : str(val),
          "Selisih" : str(selisihdebet)
  }
  app.ConWriteln('Balancing Baki Debet')
  #app.ConWriteln('Query : %s' % s)
  config.ExecSQL(s)
  #Jika dvcount tidak bernilai 0
  if dvcount>0:
    s = '''
      update lbus_form10 set debetblnlap=debetblnlap+%s where report_id=%s
    ''' % (str(dvcount),str(report_id))
    config.ExecSQL(s)
  config.Commit()
  app.ConWriteln('OK')
  #app.ConRead(' ')

  #Update Kelonggaran Tarik
  s = '''
          update lbus_form10 set kelonggarantarik=plafond-debetblnlap
          where report_id=%(ReportId)s
  ''' % {
          "ReportId" : str(report_id)
  }
  app.ConWriteln('Balancing Kelonggaran Tarik')
  #app.ConWriteln('Query : %s' % s)
  config.ExecSQL(s)
  config.Commit()
  app.ConWriteln('OK')
  #app.ConRead(' ')
  #--


  #Balancing Sum PPAP dengan Form 13 sandi 56+57 Khusus+Umum
  #Ambil nilai pada form13
  s = '''
       select round(sum(balancecumulative)/1000000, 0)*-1 "value" from table(%(Saldo)s(to_date('%(TglLaporan)s', 'dd-mm-yyyy')))
       where (
  ''' % {
          "Saldo" : config.MapDBTableName('core.getdailybalanceat'),
          "TglLaporan" : '%s-%s-%s' % (str(repdate[2]).zfill(2),str(repdate[1]).zfill(2),str(repdate[0]).zfill(4)),
          "ListCabang" : listcabang
  }
  s+= '''
        account_code like '112020610001%' or
        account_code like '112020620001%' or
        account_code like '112020610002%' or
        account_code like '112020620002%'
  '''
  s+= '''
       ) 
       and branch_code in (%(ListCabang)s)
       and currency_code='IDR'
  ''' % {
          "Saldo" : config.MapDBTableName('core.getdailybalanceat'),
          "TglLaporan" : '%s-%s-%s' % (str(repdate[2]).zfill(2),str(repdate[1]).zfill(2),str(repdate[0]).zfill(4)),
          "ListCabang" : listcabang
  }
  totalppapf13 = int(config.CreateSQL(s).RawResult.value)
  #Hitung total pada Form06
  s = '''
        select sum(ppapdibentuk) "value" from lbus_form10 where report_id=%s
  ''' % str(report_id)
  totalppapf10 = int(config.CreateSQL(s).RawResult.value)
  #Hitung Selisih
  selisihppap = totalppapf13-totalppapf10
  #app.ConWriteln('Tgl Laporan : %s-%s-%s' % (str(repdate[2]).zfill(2),str(repdate[1]).zfill(2),str(repdate[0]).zfill(4)))
  app.ConWriteln('total form 13 : %s' % str(totalppapf13))
  app.ConWriteln('total form 10 : %s' % str(totalppapf10))
  app.ConWriteln('Selisih : %s' % str(selisihppap))

  x_inc=1
  #Jika selisih bernilai negatif (Form06 > Form01) ubah increment menjadi decrement
  if selisihppap<0:
    selisihppap=selisihppap*-1
    x_inc = -1
  
  #Jika selisih > jml row, hitung ulang increment dan isikan dvcount
  dvcount=0
  if selisihppap>jmlrec:
    dvcount = int(selisihppap/jmlrec)
    selisihppap = selisihppap % jmlrec

  #Cari Kandidat Adjustment Row
  s = '''
      select ppapdibentuk val, count(*) jml from lbus_form10 
      where report_id=%s 
      group by ppapdibentuk
      order by ppapdibentuk
  ''' % str(report_id)
  res = config.CreateSQL(s).RawResult
  n = 0
  val = 0
  while n<selisihdebet and not res.Eof:
    n += int(res.jml)
    val = int(res.val)
    #app.ConWriteln('Val[%s] : %s' % (str(val),str(n)))
    res.Next() 
  config.Commit()
  
  #Update baki pada adjustment row
  s = '''
          update lbus_form10 set ppapdibentuk=ppapdibentuk+%(Increment)s
          where nomorrekening in (
          select nomorrekening from (
          select rownum, a.* from (
          select nomorrekening, ppapdibentuk 
          from lbus_form10 
          where report_id=%(ReportId)s 
          and ppapdibentuk<=%(MinVal)s
          order by ppapdibentuk) a
          where rownum<=%(Selisih)s)) and report_id=%(ReportId)s
  ''' % {
          "Increment" : str(x_inc), 
          "ReportId" : str(report_id), 
          "MinVal" : str(val),
          "Selisih" : str(selisihppap)
  }
  app.ConWriteln('Balancing PPAP')
  #app.ConWriteln('Query : %s' % s)
  config.ExecSQL(s)
  #Jika dvcount tidak bernilai 0
  if dvcount>0:
    s = '''
      update lbus_form10 set ppapdibentuk=ppapdibentuk+%s where report_id=%s
    ''' % (str(dvcount),str(report_id))
    config.ExecSQL(s)
  config.Commit()
  app.ConWriteln('OK')
  #app.ConRead(' ')
  #--
