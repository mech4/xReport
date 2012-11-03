REFMAP = {
  'LJENIS'                      : 'R_KEWAJIBAN_LAINNYA'
  ,'LJENISVALUTA'                : 'R_JENIS_VALUTA'
  ,'LGOLPENAGIH'                 : 'R_SANDI_PIHAK_KETIGA'
  ,'LHUBBANK'                    : 'R_HUBUNGAN_DENGAN_BANK'
}
  
class LBUS_FORM_24:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LJENIS'
      ,'LJENISVALUTA'
      ,'LGOLPENAGIH'
      ,'LHUBBANK'
    ]
    self.attrlist = [
      'Hari'
      ,'Persen'
      ,'Jumlah'
      ,'Bulan'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form24.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'LJENIS_reference_code'
        , 2: 'LJENISVALUTA_reference_code'
        , 3: 'LGOLPENAGIH_reference_code'
        , 4: 'LHUBBANK_reference_code'
        , 5: 'Bulan'
        , 6: 'Hari'
        , 7: 'Persen'
        , 8: 'Jumlah'
    }
    self.useheader = 2 #1: true, 0:false, 2:row header only (LBUS)
    self.txttemplate = 'lbus/form24.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    #       jenis 3 untuk zerofill 99,99
    self.txtmap      = ( [0,0]
      , [2,0]
      , [3,0]
      , [3,0]
      , [1,0]
      , [2,1]
      , [3,1]
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
    