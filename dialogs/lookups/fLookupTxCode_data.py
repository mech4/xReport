import os
import sys
import com.ihsan.lib.remotequery as remotequery

def runQuery(config, params, returns):
  rqsql = remotequery.RQSQL(config)
  rqsql.handleOperation(params, returns)
#--

def initQuery(config, params, returns):
  rqsql = remotequery.RQSQL(config)
  rqsql.SELECTFROMClause = '''SELECT tx_code,
    description,
    subsystem_code,
    sub_tx_code,
    is_reserved
    FROM %s''' % (config.MapDBTableName("SystemTxCode"))
  fr = params.FirstRecord
  if fr.prefix == "":
    rqsql.WHEREClause = "1 = 1"
  else:
    rqsql.WHEREClause = "tx_code LIKE '%s%%'" % fr.prefix
  rqsql.setAltOrderFieldNames("tx_code;subsystem_code")
  rqsql.keyFieldName = "tx_code"
  rqsql.setBaseOrderFieldNames("tx_code")
  rqsql.initOperation(returns)
#--
  