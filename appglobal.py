import com.ihsan.foundation.pobjecthelper as phelper
#import com.ihsan.lib.trace as trace
#import rpdb2

# globals
warn = 0
warnMsg = ''

def BeforeLogin(config, appid, userid, password):
  global warn, warnMsg
  #import rpdb2; rpdb2.start_embedded_debugger("000")
      
  helper = phelper.PObjectHelper(config)
  app = helper.CreateObject('Enterprise.Global')
  warn, warnMsg = app.Login(userid, password)
      
  return 1

def BeforeLogout(config):
  helper = phelper.PObjectHelper(config)
  app = helper.CreateObject('Enterprise.Global')
  app.BeforeLogout()
    
def OnGetUserInfo(config, userid, userinfo):
  helper = phelper.PObjectHelper(config)    
  app = helper.CreateObject('Enterprise.Global')
  app.OnGetUserInfo(userid, userinfo)
        
def AfterSuccessfulLogin(config, reclogin, password):
  global warn, warnMsg
  
  helper = phelper.PObjectHelper(config)
  app = helper.CreateObject('Enterprise.Global')
  app.AfterSuccessfulLogin(reclogin)                            

def AfterFailedLogin(config, appid, userid, password): 
  pass
  
def BeforeChangePassword(config, new_password, confirm_password): pass
def AfterChangePassword(config, new_password):
  helper = phelper.PObjectHelper(config)
  app = helper.CreateObject('Enterprise.Global')
  app.AfterChangePassword(new_password)

def BeforeRestoreSession(config, session_name):
  app = config.AppObject
  if session_name == 'core' and not app.lookuprsession(session_name):
    sysvar = config.SysVarIntf
    host = sysvar.GetStringSysVar('CORELINK', 'core_host') 
    uid = sysvar.GetStringSysVar('CORELINK', 'core_login')
    paswd = sysvar.GetStringSysVar('CORELINK', 'core_password') 
    app.rlogin(host, 'ibank2.core/migrasi19', uid, paswd, 'core')
  #--
#--    
