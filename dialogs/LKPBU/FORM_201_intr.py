REFMAP = {
  'LJENIS'           : 'R_JENIS_AKTIVITAS'
  ,'LJNSSKBDN'       : 'R_JENIS_SKBDN'
  ,'LJENISVALUTA'    : 'R_SANDI_VALUTA' 
}
  
class LKPBU_FORM_201:
  def __init__(self, formObj, parentForm):
    self.reflist  = ['LJENIS', 'LJENISVALUTA', 'LJNSSKBDN']
    self.attrlist = [
      'jumlahSKDN'
      , 'Volume'
    ]
    self.paction     = None
    self.xlstemplate = 'lkpbu/form201.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
        1: 'LJENIS_reference_code'  
      , 2: 'LJNSSKBDN_reference_code'
      , 3: 'jumlahSKDN'
      , 4: 'LJENISVALUTA_reference_code'
      , 5: 'Volume'
    }
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
      self.uipData.Keterangan=''
      self.pData_Keterangan.Enabled=0
      
  def OnEn(self, sender):
    Kode_Valuta = self.uipData.GetFieldValue('LJENISVALUTA.reference_code')
          
    self.pData_label1.Caption=Kode_Valuta[0:3]
    