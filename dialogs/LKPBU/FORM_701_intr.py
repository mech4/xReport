REFMAP = {
      'LJENISPERUSAHAAN'     : 'R_PERUSAHAAN_ASURANSI'
      ,'LPIHAK' : 'R_PT_ASURANSI' 
      ,'LJENISPENYELESAIAN' : 'R_MODEL_BISNIS'
      ,'LJENISPRODUK' : 'R_PRODUK_ASURANSI'
      ,'LVALUTAASAL' : 'R_JENIS_VALUTA'
}
  
class LKPBU_FORM_701:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LJENISPERUSAHAAN'
      ,'LPIHAK'
      ,'LJENISPENYELESAIAN'
      ,'LJENISPRODUK'
      ,'LVALUTAASAL'
    ]
    self.attrlist = [
      'BulanData'
      ,'NamaPerusahaan'
      ,'Keterangan'
      ,'NamaProduk'
      ,'JumlahPolis'
      ,'JumlahNasabah'
      ,'TotalPertanggungan'
      ,'AkumulasiAwal'
      ,'BulanLaporan'
      ,'FreeBasedIncome'
      ,'NilaiFound'
    ]
    self.paction     = None
    self.xlstemplate = 'lkpbu/form701.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
          1: 'BulanData'
        , 2: 'NamaPerusahaan'
        , 3: 'Keterangan'
        , 4: 'LJENISPERUSAHAAN_reference_code'
        , 5: 'LPIHAK_reference_code'
        , 6: 'LJENISPENYELESAIAN_reference_code'
        , 7: 'LJENISPRODUK_reference_code'
        , 8: 'NamaProduk'
        , 9: 'JumlahPolis'
        , 10: 'JumlahNasabah'
        , 11: 'LVALUTAASAL_reference_code'
        , 12: 'TotalPertanggungan'
        , 13: 'AkumulasiAwal'
        , 14: 'BulanLaporan'
        , 15: 'FreeBasedIncome'
        , 16: 'NilaiFound'
    }
    self.useheader = 1 #1: true, 0:false
    self.txttemplate = 'lkpbu/form701.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    self.txtmap      = ( [0,0]
      ,[2,1]
      ,[9,0]
      ,[50,0]
      ,[1,0]
      ,[1,0]
      ,[1,0]
      ,[2,0]
      ,[50,0]
      ,[8,1]
      ,[8,1]
      ,[3,0]
      ,[15,1]
      ,[15,1]
      ,[15,1]
      ,[15,1]
      ,[15,1]
    )
  #--
  
  def refExit(self, sender):
    sName = sender.Name
    reference_desc = '%s.reference_desc' % sName
    
    uapp = self.FormObject.ClientApplication.UserAppObject
    if self.uipData.GetFieldValue(reference_desc) == '-':
      self.uipData.ClearLink(sName)
      return 1
    else:  
      res = uapp.stdLookup(sender, "reference@lookupRefByDesc", sName, 
        "reference_desc;reference_code;refdata_id", None, 
        {'reference_name': REFMAP[sName]})
        
      return res
      
  def onenter(self, sender):
    Code = self.uipData.GetFieldValue('LJENISSURATBERHARGA.reference_code') 
    if Code =='99':
      self.uipData.Keterangan=' '
      self.pData_Keterangan.Enabled=1
    if Code !='99':
      self.uipData.Keterangan='-'
      self.pData_Keterangan.Enabled=0
      
  def OnEn(self, sender):
    Kode_Valuta = self.uipData.GetFieldValue('LJENISVALUTA.reference_desc')
          
    self.pData_label1.Caption=Kode_Valuta[0:3]
    