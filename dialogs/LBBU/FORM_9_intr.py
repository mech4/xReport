REFMAP = {
  'LCARA'                       : 'R_RESTRUKTURISASI'
  ,'LAKADSBLM'                   : 'R_AKAD_LBBU'
  ,'LVALSBLM'                    : 'R_JENIS_VALUTA'
  ,'LKUASBLM'                    : 'R_KUALITAS'
  ,'LVALSTLH'                    : 'R_JENIS_VALUTA'
  ,'LKUASTLH'                    : 'R_KUALITAS'
}
  
class LBBU_FORM_9:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LCARA'
      ,'LAKADSBLM'
      ,'LVALSBLM'
      ,'LKUASBLM'
      ,'LAKADSTLH'
      ,'LVALSTLH'
      ,'LKUASTLH'
    ]
    self.attrlist = [
      'NPWP'
      ,'Alamat'
      ,'Frekuensi'
      ,'PlafonSblm'
      ,'SaldoSBLM'
      ,'NisbahSBLM'
      ,'BagHasSBLM'
      ,'TunggakanSBLM'
      ,'AwalSBLM'
      ,'TempoSBLM'
      ,'TglAgunanSBLM'
      ,'NilaiAgunanSBLM'
      ,'PlafonSTLH'
      ,'SaldoSTLH'
      ,'NisbahSTLH'
      ,'BagHasSTLH'
      ,'TunggakanSTLH'
      ,'AwalSTLH'
      ,'TempoSTLH'
      ,'TglAgunanSTLH'
      ,'NilaiAgunanSTLH'
      ,'Kerugian'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form9.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
          1: 'Nama'
        , 2: 'NPWP'
        , 3: 'Alamat'
        , 4: 'LCARA_reference_code'
        , 5: 'Frekuensi'
        , 6: 'LAKADSBLM_reference_code'
        , 7: 'PlafonSblm'
        , 8: 'SaldoSBLM'
        , 9: 'LVALSBLM_reference_code'
        , 10: 'NisbahSBLM'
        , 11: 'BagHasSBLM'
        , 12: 'TunggakanSBLM'
        , 13: 'AwalSBLM'
        , 14: 'TempoSBLM'
        , 15: 'LKUASBLM_reference_code'
        , 16: 'TglAgunanSBLM'
        , 17: 'NilaiAgunanSBLM'
        , 18: 'LAKADSTLH_reference_code'
        , 19: 'PlafonSTLH'
        , 20: 'SaldoSTLH'
        , 21: 'LVALSTLH_reference_code'
        , 22: 'NisbahSTLH'
        , 23: 'BagHasSTLH'
        , 24: 'TunggakanSTLH'
        , 25: 'AwalSTLH'
        , 26: 'TempoSTLH'
        , 27: 'LKUASTLH_reference_code'
        , 28: 'TglAgunanSTLH'
        , 29: 'NilaiAgunanSTLH'
        , 30: 'Kerugian'
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
    