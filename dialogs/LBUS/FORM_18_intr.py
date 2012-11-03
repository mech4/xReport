REFMAP = {
  'LSIFAT'                      : 'R_SIFAT_SIMPANAN_WADIAH'
  ,'LJENIS'                      : 'R_JENIS_SIMPANAN_WADIAH'
  ,'LJENISVALUTA'                : 'R_JENIS_VALUTA'
  ,'LGOLPEMILIK'                 : 'R_SANDI_PIHAK_KETIGA'
  ,'LHUBBANK'                    : 'R_HUBUNGAN_DENGAN_BANK'
  ,'LLOKASI'                     : 'R_DATI_2'
}
  
class LBUS_FORM_18:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LSIFAT'
      ,'LJENIS'
      ,'LJENISVALUTA'
      ,'LGOLPEMILIK'
      ,'LHUBBANK'
      ,'LLOKASI'
    ]
    self.attrlist = [
      'JumlahRekening'
      ,'PersenBonus'
      ,'Jumlah'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form18.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'JumlahRekening'
        , 2: 'LSIFAT_reference_code'
        , 3: 'LJENIS_reference_code'
        , 4: 'LJENISVALUTA_reference_code'
        , 5: 'LGOLPEMILIK_reference_code'
        , 6: 'LHUBBANK_reference_code'
        , 7: 'LLOKASI_reference_code'
        , 8: 'PersenBonus'
        , 9: 'Jumlah'
    }
    self.useheader = 2 #1: true, 0:false, 2:row header only (LBUS)
    self.txttemplate = 'lbus/form18.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    #       jenis 3 untuk zerofill 99,99
    self.txtmap      = ( [0,0]
      , [8,1]
      , [1,0]
      , [2,0]
      , [3,0]
      , [3,0]
      , [1,0]
      , [4,0]
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
    