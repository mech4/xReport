REFMAP = {
  'LJENIS'           : 'R_PEMBELI_SKBDN'
  ,'LJENISVALUTA'    : 'R_SANDI_VALUTA' 
}
  
class LKPBU_FORM_203:
  def __init__(self, formObj, parentForm):
    self.reflist  = ['LJENIS', 'LJENISVALUTA']
    self.attrlist = [
      'jumlah'
      , 'Volume'
    ]
    self.paction     = None
    self.xlstemplate = 'lkpbu/form203.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
        1: 'LJENIS_reference_code'  
      , 2: 'jumlah'
      , 3: 'LJENISVALUTA_reference_code'
      , 4: 'Volume'
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
      self.uipData.Keterangan='-'
      self.pData_Keterangan.Enabled=0
      
  def OnEn(self, sender):
    Kode_Valuta = self.uipData.GetFieldValue('LJENISVALUTA.reference_code')
          
    self.pData_label1.Caption=Kode_Valuta[0:3]
    