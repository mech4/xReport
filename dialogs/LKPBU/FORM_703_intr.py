REFMAP = {
      'LMETODE' : 'R_METODE_PENAWARAN'
      ,'LNEGARAPENERBIT' : 'R_KODE_NEGARA'
      ,'LNEGARAKUSTODIAN' : 'R_KODE_NEGARA'
      ,'LGOLPEMILIK' : 'R_GOL_PEMILIK_KLN'
      ,'LKLASNASABAH' : 'R_KLAS_NASABAH_LN'
      ,'LJENISVALUTA' : 'R_JENIS_VALUTA'
}
  
class LKPBU_FORM_703:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LMETODE'
      ,'LNEGARAPENERBIT'
      ,'LNEGARAKUSTODIAN'
      ,'LGOLPEMILIK'
      ,'LKLASNASABAH'
      ,'LJENISVALUTA'
    ]
    self.attrlist = [
      'NamaProduk'
      ,'JenisProduk'
      ,'Keterangan1'
      ,'Keterangan2'
      ,'Penerbit'
      ,'Kustodian'
      ,'TanggalBankMenjualProduk'
      ,'TanggalJT'
      ,'JumlahPemilik'
      ,'JumlahPenjualan'
      ,'JumlahOutstanding'
      ,'FeeBasedIncome'
    ]
    self.paction     = None
    self.xlstemplate = 'lkpbu/form703.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
          1: 'NamaProduk'
        , 2: 'JenisProduk'
        , 3: 'Keterangan1'
        , 4: 'LMETODE_reference_code'
        , 5: 'Keterangan2'
        , 6: 'Penerbit'
        , 7: 'LNEGARAPENERBIT_reference_code'
        , 8: 'Kustodian'
        , 9: 'LNEGARAKUSTODIAN_reference_code'
        , 10: 'TanggalBankMenjualProduk'
        , 11: 'TanggalJT'
        , 12: 'LGOLPEMILIK_reference_code'
        , 13: 'LKLASNASABAH_reference_code'
        , 14: 'JumlahPemilik'
        , 15: 'LJENISVALUTA_reference_code'
        , 16: 'JumlahPenjualan'
        , 17: 'JumlahOutstanding'
        , 18: 'FeeBasedIncome'
    }
    self.useheader = 1 #1: true, 0:false
    self.txttemplate = 'lkpbu/form703.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    self.txtmap      = ( [0,0]
      ,[50,0]
      ,[50,0]
      ,[50,0]
      ,[1,0]
      ,[50,0]
      ,[50,0]
      ,[2,0]
      ,[50,0]
      ,[2,0]
      ,[8,1]
      ,[8,1]
      ,[3,0]
      ,[1,0]
      ,[4,1]
      ,[3,0]
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
    