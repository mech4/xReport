REFMAP = {
  'LJENIS'           : 'R_TUJUAN_JAMINAN'
  , 'LJENISVALUTA'   : 'R_JENIS_VALUTA'
  , 'LPEMILIK'       : 'R_GOLONGAN_PEMILIK'
  , 'LHUBBANK'       : 'R_HUBUNGAN_DENGAN_BANK'
}
  
class LBUS_FORM_26:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LJENIS'
      ,'LJENISVALUTA'
      ,'LPEMILIK'
      ,'LHUBBANK'
    ]
    self.attrlist = [
      'JatuhTempo'
      ,'PersentaseBonus'
      ,'Jumlah'
      ,'Mulai'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form26.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'LJENIS_reference_code'
        , 2: 'LJENISVALUTA_reference_code'
        , 3: 'LPEMILIK_reference_code'
        , 4: 'LHUBBANK_reference_code'
        , 5: 'Mulai'
        , 6: 'JatuhTempo'
        , 7: 'PersentaseBonus'
        , 8: 'Jumlah'
    }
    self.useheader = 2 #1: true, 0:false, 2:row header only (LBUS)
    self.txttemplate = 'lbus/form26.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    #       jenis 3 untuk zerofill 99,99
    self.txtmap      = ( [0,0]
      , [1,0]
      , [3,0]
      , [2,0]
      , [1,0]
      , [6,1]
      , [6,1]
      , [4,3]
      , [12,1]
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
    