# GLOBAL VARS
xl_filename = ''

class fReportEditor:
  def __init__(self, formObj, parentForm):
    pass
  #--
  
  def form_show(sender, param):
      global xl_filename
      
      app = sender.ClientApplication
      main_ui = sender.GetUIPartByName('main_ui')
  
      ph = app.CreateValues(['mlnop', main_ui.mlnop])
      ph = sender.CallServerMethod('PreparingSchedule', ph)
      rec = ph.FirstRecord
      if rec.Is_Err:
          raise Exception, 'PERINGATAN!:' +  rec.Err_Message
  
      packet = ph.Packet
      if packet.StreamWrapperCount > 0:
        sw = packet.GetStreamWrapper(0)
      else:
        raise Exception, 'PERINGATAN!. Download stream not found'
  
      #localfile = '%s/schedule_murabahah.xls' % (app.temporarydir)
      #sw.SaveToFile(localfile)
      tmp_filename = app.GetTemporaryFileName("dl")
      xl_filename = tmp_filename + '.xls'
      sw.SaveToFile(xl_filename)
  
      olecont = sender.GetPanelByName('olecont')
      #olecont.CreateObjectFromFile(localfile)
      olecont.CreateObjectFromFile(xl_filename)
  
      sender.GetControlByName('main_panel.bSave').Enabled = 1
  
  def bsave_click(sender):
      global xl_filename
  
      form = sender.OwnerForm
      app = form.ClientApplication
  
      main_ui = form.GetUIPartByName('main_ui')
      
      #localfile = '%s/schedule_murabahah.xls' % (app.temporarydir)
      olecont = form.GetPanelByName('olecont')
      #olecont.SaveAsDocument(localfile)
      olecont.SaveAsDocument(xl_filename)
  
      ph = app.CreateValues(['mlnop', main_ui.mlnop])
      sw = ph.Packet.AddStreamWrapper()
      #sw.LoadFromFile(localfile)
      sw.LoadFromFile(xl_filename)
  
      ph = form.CallServerMethod('InstallmentSave', ph)
      rec = ph.FirstRecord
      if rec.Is_Err:
          raise Exception, 'PERINGATAN!:' +  rec.Err_Message
  
      app.ShowMessage('Jadwal angsuran telah berhasil disimpan!')
      sender.Enabled = 0
  
