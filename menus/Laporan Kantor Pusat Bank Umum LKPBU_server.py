import com.ihsan.foundation.pobjecthelper as phelper

def OnLoadMenu(config, menu):
  helper = phelper.PObjectHelper(config)
  app = helper.CreateObject('Enterprise.Global')
  app.OnLoadMenu(menu, 'Laporan Kantor Pusat Bank Umum')
