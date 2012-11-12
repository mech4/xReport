REFMAP = {
  'LKANTOR'                     : 'R_STATUS_KANTOR'
  ,'LDATI2'                      : 'R_DATI_2'
}
  
class LKPBU_FORM_807:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LKANTOR'
      ,'LDATI2'
    ]
    self.attrlist = [
      'KCInduk'
      ,'SandiKantor'
      ,'NamaKantor'
      ,'Alamat'
      ,'KodePos'
      ,'Telepon'
      ,'NoSuratIzin'
      ,'TglSuratIzin'
      ,'TglOperasional'
      ,'NoSuratPerubahan'
      ,'TglSuratPerubahan'
      ,'TglEfektif'
      ,'NoSuratPenutupan'
      ,'TglPenutupan'
      ,'TglEffPenutupan'
      ,'NoRelokasi'
      ,'TglRelokasi'
      ,'TglEffRelokasi'
      ,'JmlKaryawan'
      ,'TglPublikasi'
      ,'Keterangan'
    ]
    self.paction     = None
    self.xlstemplate = 'lkpbu/form807.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
          1: 'LKANTOR_reference_code'
        , 2: 'KCInduk'
        , 3: 'SandiKantor'
        , 4: 'NamaKantor'
        , 5: 'Alamat'
        , 6: 'LDATI2_reference_code'
        , 7: 'KodePos'
        , 8: 'Telepon'
        , 9: 'NoSuratIzin'
        , 10: 'TglSuratIzin'
        , 11: 'TglOperasional'
        , 12: 'NoSuratPerubahan'
        , 13: 'TglSuratPerubahan'
        , 14: 'TglEfektif'
        , 15: 'NoSuratPenutupan'
        , 16: 'TglPenutupan'
        , 17: 'TglEffPenutupan'
        , 18: 'NoRelokasi'
        , 19: 'TglRelokasi'
        , 20: 'TglEffRelokasi'
        , 21: 'JmlKaryawan'
        , 22: 'TglPublikasi'
        , 23: 'Keterangan'
    }
    self.useheader = 1 #1: true, 0:false
    self.txttemplate = 'lkpbu/form807.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    self.txtmap      = ( [0,0]
      ,[2,0]
      ,[3,0]
      ,[9,0]
      ,[45,0]
      ,[45,0]
      ,[4,0]
      ,[5,0]
      ,[14,0]
      ,[40,0]
      ,[8,1]
      ,[8,1]
      ,[40,0]
      ,[8,1]
      ,[8,1]
      ,[40,0]
      ,[8,1]
      ,[8,1]
      ,[40,0]
      ,[8,1]
      ,[8,1]
      ,[10,1]
      ,[8,1]
      ,[50,0]
    )
  #--

  def refExit(self, sender):
    sName = sender.Name
    reference_desc = '%s.reference_desc' % sName
    
    uapp = self.FormObject.ClientApplication.UserAppObject
    if self.uipData.GetFieldValue(reference_desc) == '-':
      self.uipData.ClearLink(sName)
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
    