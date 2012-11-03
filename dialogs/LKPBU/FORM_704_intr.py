REFMAP = {
  'LDELIVERY'          : 'R_DELIVERY_CHANNEL'
}
  
class LKPBU_FORM_704:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LDELIVERY'
    ]
    self.attrlist = [
      'JumlahNasabah1'
      ,'Frekuensi1'
      ,'JumlahNasabah2'
      ,'Frekuensi2'
      ,'NilaiTransaksi'
      ,'FrekuensiFraud'
      ,'NilaiFraud'
    ]
    self.paction     = None
    self.xlstemplate = 'lkpbu/form704.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
          1: 'LDELIVERY_reference_code'
        , 2: 'JumlahNasabah1'
        , 3: 'Frekuensi1'
        , 4: 'JumlahNasabah2'
        , 5: 'Frekuensi2'
        , 6: 'NilaiTransaksi'
        , 7: 'FrekuensiFraud'
        , 8: 'NilaiFraud'
    }
    self.useheader = 1 #1: true, 0:false
    self.txttemplate = 'lkpbu/form704.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    self.txtmap      = ( [0,0]
      ,[2,0]
      ,[12,1]
      ,[12,1]
      ,[12,1]
      ,[12,1]
      ,[15,1]
      ,[12,1]
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
    