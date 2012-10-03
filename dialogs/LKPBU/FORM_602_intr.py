REFMAP = {
  'LPERIOD'                     : 'R_PERIODISASI_PELAPORAN'
}
  
class LKPBU_FORM_602:
  def __init__(self, formObj, parentForm):
    self.reflist  = ['LPERIOD']
    self.attrlist = [
      'DiluarSistem'
    , 'TerkaitSistem'
    , 'Total'
    ]
    self.paction     = None
    self.xlstemplate = 'lkpbu/form602.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
        1: 'LPERIOD_reference_code'  
      , 2: 'DiluarSistem'
      , 3: 'TerkaitSistem'
      , 4: 'Total'
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
    Kode_Valuta = self.uipData.GetFieldValue('LJENISVALUTA.reference_desc')
          
    self.pData_label1.Caption=Kode_Valuta[0:3]
    