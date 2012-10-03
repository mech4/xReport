REFMAP = {
  'LINDIKEL'                    : 'R_INDIVIDU_KELOMPOK'
  ,'LHUBBANK'                    : 'R_HUB_KETERKAITAN'
  ,'LSTATUSHUB'                  : 'R_DETAIL_HUB_BANK'
  ,'LJENISDANA'                  : 'R_JENIS_DANA'
  ,'LBENTUKJAMINAN'              : 'R_BENTUK_JAMINAN'
  ,'LPENERBIT'                   : 'R_BANK_DAN_PIHAK_KE3'
  ,'LPEMERINGKAT'                : 'R_PEMERINGKAT'
  ,'LPENATA'                     : 'R_BANK_DAN_PIHAK_KE3'
  ,'Kualitas'                    : 'R_KUALITAS'
}
  
class LBBU_FORM_7:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LINDIKEL'
      ,'LHUBBANK'
      ,'LSTATUSHUB'
      ,'LJENISDANA'
      ,'LBENTUKJAMINAN'
      ,'LPENERBIT'
      ,'LPEMERINGKAT'
      ,'LPENATA'
      ,'LKUALITAS'
    ]
    self.attrlist = [
      'GrupKelompok'
      ,'JangkaAwal'
      ,'JangkaTempo'
      ,'JmlRp'
      ,'JmlVa'
      ,'Kurs'
      ,'Modal'
      ,'NilaiJaminan'
      ,'Peringkat'
      ,'TglPemeringkat'
      ,'JaminanAwal'
      ,'JaminanTempo'
      ,'Pencairan'
      ,'TglPencairan'
      ,'Nominal'
      ,'Persen'
      ,'Keterangan'
    ]
    self.paction     = None
    self.xlstemplate = 'lbus/form7.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
          1: 'Nama'
        , 2: 'LINDIKEL_reference_code'
        , 3: 'GrupKelompok'
        , 4: 'LHUBBANK_reference_code'
        , 5: 'LSTATUSHUB_reference_code'
        , 6: 'LJENISDANA_reference_code'
        , 7: 'JangkaAwal'
        , 8: 'JangkaTempo'
        , 9: 'JmlRp'
        , 10: 'JmlVa'
        , 11: 'Kurs'
        , 12: 'Modal'
        , 13: 'LBENTUKJAMINAN_reference_code'
        , 14: 'NilaiJaminan'
        , 15: 'LPENERBIT_reference_code'
        , 16: 'Peringkat'
        , 17: 'LPEMERINGKAT_reference_code'
        , 18: 'TglPemeringkat'
        , 19: 'LPENATA_reference_code'
        , 20: 'JaminanAwal'
        , 21: 'JaminanTempo'
        , 22: 'Pencairan'
        , 23: 'TglPencairan'
        , 24: 'Nominal'
        , 25: 'Persen'
        , 26: 'LKUALITAS_reference_code'
        , 27: 'Keterangan'
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
    