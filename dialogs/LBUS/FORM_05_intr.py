REFMAP = {
  'LJENIS'                      : 'R_SURT_BRHARGA_YANG_DIMIL'
  ,'LJENISVALUTA'                : 'R_JENIS_VALUTA'
  ,'LGOLPENERBIT'                : 'R_SANDI_PIHAK_KETIGA'
  ,'LHUBBANKPENERBIT'            : 'R_HUBUNGAN_DENGAN_BANK'
  ,'LTUJUANPEMILIKAN'            : 'R_TUJUAN_PEMILIKAN'
  ,'LKOLEKTIBILITAS'             : 'R_KOLEKTIBILITAS'
  ,'LGOLPENJAMIN'                : 'R_BANK_DAN_PIHAK_KE3'
}
  
class LBUS_FORM_05:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LJENIS'
      ,'LJENISVALUTA'
      ,'LGOLPENERBIT'
      ,'LHUBBANKPENERBIT'
      ,'LTUJUANPEMILIKAN'
      ,'LKOLEKTIBILITAS'
      ,'LGOLPENJAMIN'
    ]
    self.attrlist = [
      'Mulai'
      ,'JatuhTempo'
      ,'BagHas'
      ,'BagianDijamin'
      ,'Nominal'
      ,'Jumlah'
      ,'AgunanPPAP'
      ,'PPAPDibentuk'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form05.xls'
    self.xlstopline  = 2
    self.xlsmap      = {
          1: 'LJENIS_reference_code'
        , 2: 'LJENISVALUTA_reference_code'
        , 3: 'LGOLPENERBIT_reference_code'
        , 4: 'LHUBBANKPENERBIT_reference_code'
        , 5: 'LTUJUANPEMILIKAN_reference_code'
        , 6: 'Mulai'
        , 7: 'JatuhTempo'
        , 8: 'LKOLEKTIBILITAS_reference_code'
        , 9: 'BagHas'
        , 10: 'LGOLPENJAMIN_reference_code'
        , 11: 'BagianDijamin'
        , 12: 'Nominal'
        , 13: 'Jumlah'
        , 14: 'AgunanPPAP'
        , 15: 'PPAPDibentuk'
    }
    self.useheader = 2 #1: true, 0:false
    self.txttemplate = 'lbus/form05.txt'
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
      , [1,0]
      , [6,1]
      , [6,1]
      , [1,0]
      , [4,3]
      , [3,0]
      , [4,3]
      , [12,1]
      , [12,1]
      , [12,1]
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
    