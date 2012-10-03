import com.ihsan.foundation.pobjecthelper as phelper

def OnLoadMenu(config, menu):
  helper = phelper.PObjectHelper(config)
  app = helper.CreateObject('Enterprise.Global')
  app.OnLoadMenu(menu, 'Laporan Harian Bank Umum')
