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
       select refdata_id from %s where reference_code='20' and reftype_id=247
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
          insert into lbus_form06 (
          NOMORREKENING,
          JUMLAHREKENING,
          LSTATUSPIUTANG_REFDATA_ID,
          LJENISPENGGUNAAN_REFDATA_ID,
          LORIENTPENGGUNAAN_REFDATA_ID,
          LJENISVALUTA_REFDATA_ID,
          LGOLDEBITUR_REFDATA_ID,
          LHUBBANK_REFDATA_ID,
          MULAI,
          JATUHTEMPO,
          LKOLEKTIBILITAS_REFDATA_ID,
          PERSENMARGIN,
          LGOLPIUTANG_REFDATA_ID,
          LSEKTOREKONOMI_REFDATA_ID,
          LLOKASIPROYEK_REFDATA_ID,
          LGOLPENJAMIN_REFDATA_ID,
          BAGDIJAMIN,
          HARGAAWAL,
          SALDOHARGAPOKOK,
          SALDOMARGIN,
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
          r1.refdata_id i1_status_piutang,
          nvl(r2.refdata_id, %(jenis_code)s) i2_jenis_penggunaan,
          nvl(r3.refdata_id, %(ori_code)s) id3_orientasi_penggunaan,
          r4.refdata_id id4_kode_valuta,
          nvl(r5.refdata_id, %(gd_code)s) id5_gol_debitur,
          r6.refdata_id id6_hub_dgn_bank,
          to_char(b.dropping_date, 'mmyyyy') blnthn_mulai,
          to_char(nvl(b.due_date, add_months(b.dropping_date, 12)), 'mmyyyy') blnthn_jatuh_tempo,
          r11.refdata_id id11_kolektibilitas,
          b.targeted_eqv_rate*100 persen,
          nvl(r7.refdata_id, %(gp_code)s) id7_gol_piutang,
          nvl(r8.refdata_id, %(sektor_code)s) id8_sektor_ekonomi,
          r9.refdata_id id9_lokasi_proyek,
          nvl(r10.refdata_id, %(penjamin_code)s) id10_gol_penjamin,
          d.bagian_yang_dijamin bag_dijamin,
          round((a.base_price)/1000000, 0) harga,
          round(((g.p_saldo+g.p_arrear_balance+g.p_mmd_balance)*-1)/1000000, 0) pokok,
          0 ditangguhkan,
          round(((h.p_saldo+h.p_arrear_balance)*-1)/1000000, 0) baki_lalu,
          round(((g.p_saldo+g.p_arrear_balance)*-1)/1000000, 0) baki_lapor,
          round((agu.total_agunan)/1000000, 0) agunan,
          round(b.reserved_common_balance/1000000, 0) ppap,
          seq_lbus_form06.nextval seq,
          %(ReportId)s report_id
          from %(FinMurabahah)s a left outer join %(FinAccount)s b on (a.nomor_rekening=b.nomor_rekening)
          left outer join %(RekeningCustomer)s c on (a.nomor_rekening=c.nomor_rekening)
          left outer join %(AdditionalAcc)s d on (a.nomor_rekening=d.nomor_rekening)
          left outer join %(AdditionalCust)s e on (c.nomor_nasabah=e.nomor_nasabah)
          left outer join %(FinFacility)s f on (b.facility_no=f.facility_no)
          left outer join %(SaldoRekening)s g on (a.nomor_rekening=g.nomor_rekening and g.tanggal=to_date('%(TglLaporan)s', 'dd-mm-yyyy'))
          left outer join %(SaldoRekening)s h on (a.nomor_rekening=h.nomor_rekening and h.tanggal=to_date('%(TglBlnLalu)s', 'dd-mm-yyyy'))
          left outer join %(Cabang)s j on (g.kode_cabang=j.kode_cabang)
          left outer join (select fca.NOREK_FINACCOUNT, sum(fcs.valuation) total_agunan from %(ColMap)s fca, %(ColAssets)s fcs
                          where fca.NOREK_FINCOLLATERALASSET=fcs.nomor_rekening
                          group by fca.NOREK_FINACCOUNT ) agu
                on (a.nomor_rekening=agu.norek_finaccount)
          left outer join %(Nasabah)s i on (c.nomor_nasabah=i.nomor_nasabah)
          left outer join %(RefData)s r1 on (r1.reference_code=decode(b.restructure_counter,0,'20','10') and r1.reftype_id=219)
          left outer join %(RefData)s r2 on (r2.reference_code=d.lbus_jenis_penggunaan and r2.reftype_id=235)
          left outer join %(RefData)s r3 on (r3.reference_code=d.lbus_orientasi_penggunaan and r3.reftype_id=108)
          left outer join %(RefData)s r4 on (r4.reference_code=decode(f.currency_code,'IDR','360','USD','840','SIN','702') and r4.reftype_id=232)
          left outer join %(RefData)s r5 on (r5.reference_code=e.lbus_golongan_debitur and r5.reftype_id=225)
          left outer join %(RefData)s r6 on (r6.reference_code=decode(i.is_pihak_terkait, 'T','1','2') and r6.reftype_id=124)
          left outer join %(RefData)s r7 on (r7.reference_code=d.lbus_golongan_piutang and r7.reftype_id=247)
          left outer join %(RefData)s r8 on (r8.reference_code=d.lbus_sektor_ekonomi_sid and r8.reftype_id=224)
          left outer join %(RefData)s r9 on (r9.reference_code=nvl(d.lbus_lokasi_proyek, j.kode_lokasi) and r9.reftype_id=251)
          left outer join %(RefData)s r10 on (r10.reference_code=d.lbus_penjamin and r10.reftype_id=328)
          left outer join %(RefData)s r11 on (r11.reference_code=decode(b.overall_col_level, 1,'1',2,'2',3,'3',4,'4',5,'5') and r11.reftype_id=230)
          where g.kode_cabang in (%(ListCabang)s)
          and b.dropping_date <= to_date('%(TglLaporan)s', 'dd-mm-yyyy')
          and (g.p_saldo+g.p_arrear_balance)<>0
  ''' % {
          "jenis_code" : str(jenis_code),
          "ori_code" : str(ori_code),
          "gd_code" : str(gd_code),
          "gp_code" : str(gp_code),
          "sektor_code" : str(sektor_code),
          "penjamin_code" : str(penjamin_code),
          "ReportId" : str(report_id),
          "FinMurabahah" : config.MapDBTableName('financing.finmurabahahaccount'),
          "FinAccount" : config.MapDBTableName('financing.finaccount'),
          "FinSchedule" : config.MapDBTableName('financing.finpaymentschedule'), 
          "RekeningCustomer" : config.MapDBTableName('core.rekeningcustomer'),
          "Nasabah" : config.MapDBTableName('core.nasabah'),
          "AdditionalAcc" : config.MapDBTableName('financing.finaccadditionaldata'),
          "AdditionalCust" : config.MapDBTableName('financing.fincustadditionaldata'),
          "FinFacility" : config.MapDBTableName('financing.finfacility'),
          "SaldoRekening" : config.MapDBTableName('tmp.cknom_base_daily'),
          "RefData" : config.MapDBTableName('enterprise.referencedata'),
          "ColAssets" : config.MapDBTableName('financing.fincollateralasset'),
          "ColMap" : config.MapDBTableName('financing.fincollateralaccount'),
          "Cabang" : config.MapDBTableName('enterprise.cabang'),
          "TglLaporan" : '%s-%s-%s' % (str(repdate[2]).zfill(2),str(repdate[1]).zfill(2),str(repdate[0]).zfill(4)),
          "TglBlnLalu" : '%s-%s-%s' % (str(lastmonthdate[2]).zfill(2),str(lastmonthdate[1]).zfill(2),str(lastmonthdate[0]).zfill(4)),
          "ListCabang" : listcabang
  }
  #app.ConWriteln(s)
  #app.ConRead('c')
  config.ExecSQL(s)
  #--
