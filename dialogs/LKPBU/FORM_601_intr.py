REFMAP = {
  'LJENISPRODUK'                : 'R_JENIS_PRODUK_LKPBU'
}
  
class LKPBU_FORM_601:
  def __init__(self, formObj, parentForm):
    self.reflist  = ['LJENISPRODUK']
    self.attrlist = [
      'Keterangan'
    , 'BagHas'
    , 'Penalti'
    , 'BiayaAdm'
    , 'Kegagalan'
    , 'Saldo'
    , 'Lain'
    , 'Jumlah'
    ]
    self.paction     = None
    self.xlstemplate = 'lkpbu/form601.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
        1: 'LJENISPRODUK_reference_code'  
      , 2: 'Keterangan'
      , 3: 'BagHas'
      , 4: 'Penalti'
      , 5: 'BiayaAdm'
      , 6: 'Kegagalan'
      , 7: 'Saldo'
      , 8: 'Lain'
      , 9: 'Jumlah'
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
    