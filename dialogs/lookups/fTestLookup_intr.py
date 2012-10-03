class frmTestLookup:
  def __init__(self, formObj, parentForm):
    pass
    
  def LookupExit(self, sender):
    uapp = self.FormObject.ClientApplication.UserAppObject 
    return uapp.stdLookup(self.pInput_Nasabah, "nasabah@lookupNasabah", "Nasabah", "nomor_nasabah;nama_singkat") 
  #--
  
  
#--