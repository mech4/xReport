import dafsys4
import com.ihsan.util.dbutil as dbutil
import com.ihsan.util.debug  as debug
from datetime import date, timedelta

if __name__ == '__main__':
  CONFIG_FILE = "c:\\dafapp\\ibank2\\report\\regulatory\\default.cfg"
  securityContext = ["SYSTEM", "SYSTEM", "ibank2.report.regulatory", "default"]
  
  config = dafsys4.openConfig(CONFIG_FILE, securityContext)
  main(config)
#--

def main(config):
  tahun = int(raw_input("Tahun periode ?"))
  jenis = raw_input("Jenis periode ?")
  
  config.BeginTransaction()
  try:
    if jenis == 'M':
      createMonthlyPeriod(config, tahun)
    elif jenis == 'D':
      createDailyPeriod(config, tahun)
    #--
    
    config.Commit()
  except:
    config.Rollback()
    msg = debug.getExcMsg()
    raise Exception, msg
  pass

def createMonthlyPeriod(config, tahun):
  for i in range(12):
    bulan = i + 1
    period = config.CreatePObject('Period')
    period.period_code = '{0:04}{1:02}'.format(tahun, bulan)
    period.period_type = 'M'
    period.description = date(tahun, bulan, 1).strftime("%B") + " " + str(tahun) 
  #--

def createDailyPeriod(config, tahun):
  first = date(tahun, 1, 1)
  last  = date(tahun+1, 1, 1)
  d     = timedelta(days=1)
  
  cdate = first
  while cdate < last: 
    period = config.CreatePObject('Period')
    period.period_code = '{0:04}{1:02}{2:02}'.format(cdate.year, cdate.month, cdate.day)
    period.period_type = 'D'
    period.description = cdate.strftime("%A, %d %B %Y")
    
    cdate = cdate + d 
  #--
  