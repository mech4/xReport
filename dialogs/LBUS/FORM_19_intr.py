REFMAP = {
  'LJENIS'                      : 'R_JENIS_INV_TIDAK_TERIKAT'
  ,'LJENISVALUTA'                : 'R_JENIS_VALUTA'
  ,'LGOLPEMILIK'                 : 'R_SANDI_PIHAK_KETIGA'
  ,'LHUBBANK'                    : 'R_HUBUNGAN_DENGAN_BANK'
  ,'LLOKASI'                     : 'R_DATI_2'
}
  
class LBUS_FORM_19:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LJENIS'
      ,'LJENISVALUTA'
      ,'LGOLPEMILIK'
      ,'LHUBBANK'
      ,'LLOKASI'
    ]
    self.attrlist = [
      'JumlahRekening'
      ,'Bulan'
      ,'Hari'
      ,'Nisbah'
      ,'Persen'
      ,'Jumlah'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form19.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'JumlahRekening'
        , 2: 'LJENIS_reference_code'
        , 3: 'LJENISVALUTA_reference_code'
        , 4: 'LGOLPEMILIK_reference_code'
        , 5: 'LHUBBANK_reference_code'
        , 6: 'LLOKASI_reference_code'
        , 7: 'Bulan'
        , 8: 'Hari'
        , 9: 'Nisbah'
        , 10: 'Persen'
        , 11: 'Jumlah'
    }
    self.useheader = 2 #1: true, 0:false, 2:row header only (LBUS)
    self.txttemplate = 'lbus/form19.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    #       jenis 3 untuk zerofill 99,99
    self.txtmap      = ( [0,0]
      , [8,1]
      , [2,0]
      , [3,0]
      , [3,0]
      , [1,0]
      , [4,0]
      , [3,1]
      , [2,1]
      , [4,3]
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
    