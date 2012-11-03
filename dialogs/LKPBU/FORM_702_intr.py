REFMAP = {
      'LSIFAT' : 'R_SIFAT_REKSADANA'
      ,'LJENIS' : 'R_JENIS_REKSADANA'
      ,'LVALUTAASAL' : 'R_JENIS_VALUTA'
      ,'LTERKAIT' : 'R_PT_ASURANSI'
      ,'LSPONSOR' : 'R_PT_ASURANSI'
}
  
class LKPBU_FORM_702:
  def __init__(self, formObj, parentForm):
    self.reflist  = [
      'LSIFAT'
      ,'LJENIS'
      ,'LVALUTAASAL'
      ,'LTERKAIT'
      ,'LSPONSOR'
    ]
    self.attrlist = [
      'BulanData'
      ,'NamaReksa'
      ,'Subscription'
      ,'Redemption'
      ,'NAVperunit'
      ,'TotalUnit'
      ,'PorsiAset'
      ,'FeeBasedIncome'
      ,'NamaManajerInvestasi'
      ,'Keterangan'
      ,'NamaBank'
      ,'TotalNAV'
      ,'NominalSponsor'
      ,'NoEfektif'
      ,'NoPenegasan'
    ]
    self.paction     = None
    self.xlstemplate = 'lkpbu/form702.xls'
    self.xlstopline  = 7
    self.xlsmap      = {
          1: 'BulanData'
        , 2: 'NamaReksa'
        , 3: 'LSIFAT_reference_code'
        , 4: 'LJENIS_reference_code'
        , 5: 'LVALUTAASAL_reference_code'
        , 6: 'Subscription'
        , 7: 'Redemption'
        , 8: 'NAVperunit'
        , 9: 'TotalUnit'
        , 10: 'PorsiAset'
        , 11: 'FeeBasedIncome'
        , 12: 'NamaManajerInvestasi'
        , 13: 'Keterangan'
        , 14: 'LTERKAIT_reference_code'
        , 15: 'NamaBank'
        , 16: 'TotalNAV'
        , 17: 'LSPONSOR_reference_code'
        , 18: 'NominalSponsor'
        , 19: 'NoEfektif'
        , 20: 'NoPenegasan'
    }
    self.useheader = 1 #1: true, 0:false
    self.txttemplate = 'lkpbu/form702.txt'
    #txtmap dimulai dari index 1 sesuai xlsmap (index 0 diisi [0,0]
    #format [len, jenis] : 
    #       jenis 0 untuk spasi 
    #       jenis 1 untuk zerofill int
    #       jenis 2 untuk zerofill x,5
    self.txtmap      = ( [0,0]
      ,[2,1]
      ,[50,0]
      ,[1,0]
      ,[2,0]
      ,[3,0]
      ,[15,1]
      ,[15,1]
      ,[15,1]
      ,[15,1]
      ,[8,2]
      ,[15,1]
      ,[9,0]
      ,[50,0]
      ,[1,0]
      ,[9,0]
      ,[15,1]
      ,[1,0]
      ,[15,1]
      ,[20,0]
      ,[20,0]            
    )
  #--


  def refExit(self, sender):
    sName = sender.Name
    reference_desc = '%s.reference_desc' % sName
    
    uapp = self.FormObject.ClientApplication.UserAppObject
    if self.uipData.GetFieldValue(reference_desc) == '-':
      self.uipData.ClearLink(sName)
      return 1
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
    