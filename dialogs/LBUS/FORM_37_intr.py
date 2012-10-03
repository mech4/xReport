REFMAP = {
  'LJENIS'                     : 'R_JENIS_PENGGUNAAN'
  , 'LJENISVALUTA'             : 'R_JENIS_VALUTA'
  , 'LBENTUKPENGHAPUSANBUKUAN' : 'R_GOLONGAN_PEMBIAYAAN'
  , 'LDEBITUR'                 : 'R_SANDI_BANK'
  , 'LHUBUNGANBANK'            : 'R_DATI_2'
  ,'LKOLEKTIBILITAS'           : 'R_KOLEKTIBILITAS'
  ,'LSEKTOREKONOMI'            : 'R_SEKTOR_EKONOMI'
}
  
class LBUS_FORM_37:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LJENIS'
      ,'LBENTUKPENGHAPUSANBUKUAN'
      ,'LJENISVALUTA'
      ,'LKOLEKTIBILITAS'
      ,'LDEBITUR'
      ,'LHUBUNGANBANK'
      ,'LSEKTOREKONOMI'
    ]
    self.attrlist = [
      'JumlahRekening'
      ,'TanggalHapusBuku'
      ,'Jumlah'
      ,'NoRekening'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form37.xls'
    self.xlstopline  = 8
    self.xlsmap      = {
          1: 'NoRekening'
        , 2: 'JumlahRekening'
        , 3: 'LJENIS_reference_code'
        , 4: 'LBENTUKPENGHAPUSANBUKUAN_reference_code'
        , 5: 'LJENISVALUTA_reference_code'
        , 6: 'LKOLEKTIBILITAS_reference_code'
        , 7: 'LDEBITUR_reference_code'
        , 8: 'LHUBUNGANBANK_reference_code'
        , 9: 'LSEKTOREKONOMI_reference_code'
        , 10: 'TanggalHapusBuku'
        , 11: 'Jumlah'
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
    