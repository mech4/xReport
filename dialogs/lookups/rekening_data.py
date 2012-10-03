import os
import sys
  
def biodata(config, params, returns):
  status = returns.CreateValues(
     ['norek',''],
     ['nonas',''],
     ['nanas',''],
     ['koje','']
  )
  mlu = config.ModLibUtils
  #raise Exception, params.FirstRecord.rekening
  
  norek  = "SELECT rt.nomor_rekening, rl.nomor_nasabah, nsb.nama_nasabah, rt.kode_jenis "
  norek += "FROM RekeningTransaksi rt, Nasabah nsb, RekeningLiabilitas rl " 
  norek += "WHERE rt.nomor_rekening = rl.nomor_rekening and rl.nomor_nasabah = nsb.nomor_nasabah AND rt.nomor_rekening LIKE %s " %mlu.QuotedStr(params.FirstRecord.rekening)
  rekening = config.CreateSQL(norek).RawResult
  if not rekening.eof:
    status.norek = rekening.nomor_rekening
    status.nonas = rekening.nomor_nasabah
    status.nanas = rekening.nama_nasabah
    status.koje = rekening.kode_jenis

def qcard(config, params, returns):
  mlu = config.ModLibUtils
  st = returns.CreateValues(['field',''])
  
  sqn = "SELECT id_individu FROM NasabahIndividu WHERE nomor_nasabah = %s " %mlu.QuotedStr(params.FirstRecord.cusno)
  sqn_ind = config.CreateSQL(sqn).RawResult
  
  ind  = "SELECT nama_lengkap, alamat_rumah_jalan, alamat_rumah_rtrw, alamat_rumah_kelurahan, alamat_rumah_kecamatan, "
  ind += "alamat_rumah_kota_kabupaten, alamat_rumah_kode_pos, alamat_rumah_provinsi, nomor_identitas, telepon_rumah_nomor, tanggal_lahir, jenis_kelamin "
  ind += "FROM Individu WHERE id_individu = %s " %(sqn_ind.id_individu)
  individu = config.CreateSQL(ind).RawResult
  #raise Exception, ('123', sqn_ind.id_individu, params.FirstRecord.cusno)
  
  dsstring = ''
  flds = ''
  for i in range(individu.FieldCount):    
    dsstring += individu.GetFieldName(i)+':'+CvrtType(individu.GetFieldType(i))+', '
    flds += individu.GetFieldName(i)+';'
  
  rdata = returns.AddNewDatasetEx('hasilsql', dsstring)
  st.field = flds.rstrip(';')
  
def CvrtType(x):
  if x==1:
     return 'string'
  if x==2:
     return 'integer'
  if x==3:
     return 'datetime'
  if x==4:
     return 'float'
       
def api2fungsilain():
  
  '''while not individu.Eof:
    newrecord = rdata.AddRecord()
    for i in range(individu.FieldCount):
      newrecord.SetFieldByName(individu.GetFieldName(i), individu.GetFieldValueAt[i])
    individu.Next()
  
  i = config.MapDBTableName("core.Individu")
  
  norek  = "SELECT rt.nomor_rekening, rl.nomor_nasabah, nsb.nama_nasabah, rt.kode_jenis "
  norek += "FROM RekeningTransaksi rt, Nasabah nsb, RekeningLiabilitas rl " 
  norek += "WHERE rt.nomor_rekening = rl.nomor_rekening and rl.nomor_nasabah = nsb.nomor_nasabah AND rt.nomor_rekening LIKE %s " %mlu.QuotedStr(params.FirstRecord.rekening)
  rekening = config.CreateSQL(norek).RawResult
  if not rekening.eof:
    status.norek = rekening.nomor_rekening
    status.nonas = rekening.nomor_nasabah
    status.nanas = rekening.nama_nasabah
    status.koje = rekening.kode_jenis'''
  pass
