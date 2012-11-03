REFMAP = {
  'LDATA'                       : 'R_DATA_PE'
  ,'LSTATUSTK'                   : 'R_STATUS_NAKER'
  ,'Kewarganegaraan'             : 'R_KODE_NEGARA'
  ,'Gender'                      : 'R_GENDER_PE'
  ,'LSTATUSPE'                   : 'R_STATUS_PE'
}
  
class LKPBU_FORM_801:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LDATA'
      ,'LSTATUSTK'
      ,'Kewarganegaraan'
      ,'Gender'
      ,'LSTATUSPE'
    ]
    self.attrlist = [
      'NamaPejabat'
      ,'NamaJabatan'
      ,'AlamatSkrg'
      ,'AlamatID'
      ,'Telepon'
      ,'Faksimile'
      ,'NPWP'
      ,'NoID'
      ,'TempatLahir'
      ,'TanggalLahir'
      ,'NoPelaporan'
      ,'TanggalPelaporan'
      ,'NomorSK'
      ,'TanggalSK'
      ,'NomorSK2'
      ,'TanggalSK2'
      ,'Keterangan'
    ]
    self.paction     = None
    self.xlstemplate = 'lkpbu/form801.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
          1: 'LDATA_reference_code'
        , 2: 'NIP'
        , 3: 'NamaPejabat'
        , 4: 'LSTATUSTK_reference_code'
        , 5: 'NamaJabatan'
        , 6: 'AlamatSkrg'
        , 7: 'AlamatID'
        , 8: 'Telepon'
        , 9: 'Faksimile'
        , 10: 'NPWP'
        , 11: 'NoID'
        , 12: 'TempatLahir'
        , 13: 'TanggalLahir'
        , 14: 'Kewarganegaraan_reference_code'
        , 15: 'Gender_reference_code'
        , 16: 'NoPelaporan'
        , 17: 'TanggalPelaporan'
        , 18: 'LSTATUSPE_reference_code'
        , 19: 'NomorSK'
        , 20: 'TanggalSK'
        , 21: 'NomorSK2'
        , 22: 'TanggalSK2'
        , 23: 'Keterangan'
    }
    self.useheader = 1 #1: true, 0:false
    self.txttemplate = 'lkpbu/form801.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    self.txtmap      = ( [0,0]
      ,[1,0]
      ,[20,0]
      ,[100,0]
      ,[1,0]
      ,[50,0]
      ,[100,0]
      ,[100,0]
      ,[40,0]
      ,[40,0]
      ,[15,0]
      ,[20,0]
      ,[20,0]
      ,[8,1]
      ,[2,0]
      ,[1,0]
      ,[40,0]
      ,[8,1]
      ,[1,0]
      ,[40,0]
      ,[8,1]
      ,[40,0]
      ,[8,1]
      ,[100,0]
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
    