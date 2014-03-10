import com.ihsan.util.xmlio as xutil
import com.ihsan.foundation.pobjecthelper as phelper
import sys, os, shutil
import zipfile
import pyFlexcel
import xlsxwriter

def FormOnSetDataEx(uideflist, params):
  # procedure(uideflist: TPClassUIDefList; params: TPClassUIDataPacket)
  key = params.FirstRecord.key
  uideflist.SetData('uipForm', key)
  config = uideflist.config
  dtsformid = key.split('=')[-1]
  s = '''
    select * from dtsmap where dtsformid=%s
  ''' % dtsformid
  res = config.CreateSQL(s).RawResult
  uipForm = uideflist.GetPClassUIByName('uipForm')
  rec = uipForm.Dataset.GetRecord(0)
  rec.oldDataSize = rec.DataSize  
  if not res.Eof:
    rec.mapType = res.dtsmaptype
    rec.OldMapType = res.dtsmaptype
  else:
    rec.mapType = 'M'
  
def LoadStructure(config, parameter, returns):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)
  rec = parameter.FirstRecord
  formId = rec.formId
  formType = rec.formType
  tempChange = rec.tempChange
  #tempChange = 1
  dataSize = rec.dataSize
  app = config.AppObject
  mlu = config.ModLibUtils
  app.ConCreate('out')
  helper = phelper.PObjectHelper(config)
  storeDir  = config.HomeDir+'data\\DTS\\'
  instanceDir = config.HomeDir+'data\\instance\\'
  xlsDir = config.HomeDir+'data\\templates\\'
  status = returns.CreateValues(
      ['Is_Err', ''],
      ['tempLoc', '']
  )
  fieldData = returns.AddNewDatasetEx(
       'formFields',
       ';'.join([
       'lv:integer',
       'kode:string',
       'desc:string',
       ])
    )
  config.BeginTransaction()
  try:
    #Getting DTS data
    s = '''
      select 
        (select dtsfoldername from dtsfolder e where parentid is null and e.dtsid=d.dtsid) fname,
        d.*, b.dtsfilename, a.dtsformcode, d.dtsid 
      from dtsform a, dtsfile b, dtsfolder c, dts d
      where a.dtsformid=b.dtsfileid
      and b.dtsfolderid = c.dtsfolderid
      and c.dtsid=d.dtsid
      and a.dtsformid=%s
    ''' % str(formId)
    DTS = config.CreateSQL(s).RawResult
    def recurse(meta, lv=0, valuableOnly=True, saveToDB=False, helper=None, parent=None, formId=0, app=None, debugMode=False):
        output = []
        if len(meta.childrens) == 0:
            output.append((lv, meta.name, meta.QN, meta.desc, meta.datatype, meta.enumName))
            if debugMode:
              app.ConWriteln('{0} {2}:{1} - {3} [{4} {5}]'.format(lv, meta.name, meta.QN, meta.desc, meta.datatype, meta.enumName))
            if saveToDB:
              inputMeta = helper.CreatePObject('DTSMeta') 
              inputMeta.DTSFormId = formId
              inputMeta.MetaName = meta.name
              inputMeta.MetaLevel = lv
              inputMeta.MetaQName = meta.QN
              inputMeta.MetaType = meta.datatype
              inputMeta.MetaDesc = meta.desc
              inputMeta.MetaEnum = meta.enumName
              inputMeta.MetaParent = parent
            return output
        else:
            if ((not valuableOnly) or (meta.hasValue)):# and (meta.datatype != 'Table'):
              if meta.hasValue:
                mtype = meta.datatype
              else:
                mtype = 'Empty'
              output.append((lv, meta.name, meta.QN, meta.desc, mtype, meta.enumName))
              if debugMode:
                app.ConWriteln('{0} {2}:{1} - {3} [{4} {5}]'.format(lv, meta.name, meta.QN, meta.desc, meta.datatype, meta.enumName))
              if saveToDB:
                inputMeta = helper.CreatePObject('DTSMeta') 
                inputMeta.DTSFormId = formId
                inputMeta.MetaName = meta.name
                inputMeta.MetaLevel = lv
                inputMeta.MetaQName = meta.QN
                inputMeta.MetaType = mtype
                inputMeta.MetaDesc = meta.desc
                inputMeta.MetaEnum = meta.enumName
                inputMeta.MetaParent = parent
                parent = inputMeta.DTSMetaId
            lv+=1
            for order, child in sorted(meta.childrens):
                output = recurse(child, lv, valuableOnly, saveToDB, helper, parent, formId) + output
            lv-=1
            return output
    if DTS.Eof:
      raise Exception, 'DTS not found.'
    DTSRoot = DTS.dtslocation + DTS.fname
    rf = xutil.XMLFolder()
    rf.setRoot(DTSRoot, False)
    iFile = rf.findFile(DTS.dtsfilename)
    app.ConWriteln('Searching file {0}'.format(DTS.dtsfilename))
    if len(iFile) < 1:
      raise Exception, 'Form file not found.'
    iFile = iFile[0]
    iFileLocation = iFile.getFullPath()
    xlsLocation = iFileLocation.replace(storeDir, xlsDir)
    xlsLocation = xlsLocation.replace('.xsd', '.xlsx')
    # if location not exists then create
    if DTS.templatelocation in (None, 'None', ''):
      fullzipname = DTS.dtslocation + DTS.dtsname + '.zip'
      DTSzip = zipfile.ZipFile(fullzipname)
      zipRoot = DTSzip.namelist()[0].replace('/','')
      xlsloc = DTS.dtslocation.replace(storeDir, xlsDir)
      if not os.path.isdir(xlsloc):
        os.mkdir(xlsloc)
      DTSzip.extractall(xlsloc)
      xlsRoot = xlsloc + zipRoot
      for zp, zd, zf in os.walk(xlsRoot):
        for zzfile in zf:
          os.remove(zp+'\\'+zzfile)
      s = "update dts set templatelocation = '{0}' where dtsid={1}".format(xlsloc, str(DTS.dtsid))
      config.ExecSQL(s)
    iForm = xutil.xbrlSchema(iFile.fileName, iFile.folder)
    app.ConWriteln('Reading meta structure from {0}'.format(DTS.dtsformcode))
    #type check intercept
    if tempChange==1:
      s = '''
        delete from dtsmeta where dtsformid=%s
      ''' % str(formId)
      config.ExecSQL(s)
      if os.path.exists(xlsLocation):
        os.remove(xlsLocation)
      if os.path.exists(xlsLocation.rstrip('x')):
        os.remove(xlsLocation.rstrip('x'))
      s = '''
        delete from dtsformula where dtsformid=%s
      ''' % str(formId)
      config.ExecSQL(s)
    #--
    #for enum set default=True
    #then process captured enum
    #try get meta from DB
    s = '''
      select * from dtsmeta where dtsformid=%s and metatype<>'Empty' order by dtsmetaid
    ''' % str(formId)
    formMeta = config.CreateSQL(s).RawResult
    if formMeta.Eof:
      app.ConWriteln('Meta not exist in database, reading from file.')
      starttime = mlu.Now()
      iForm.getMetaStructure()
      proctime = mlu.DecodeTime(mlu.Now()-starttime)
      app.ConWriteln('Read finished in {0} hr {1} min {2} sec {3} ms '.format(proctime[0],proctime[1],proctime[2],proctime[3]))
      iMeta = iForm.metaStructure
      process = iMeta.getRoot()
      if not os.path.exists(xlsLocation):
        wbook = xlsxwriter.Workbook(xlsLocation)
        wsheet = wbook.add_worksheet('Report')
        fmt2 = wbook.add_format()
        fmt2.set_bold()
        fmt2.set_bg_color('yellow')
        fmt2.set_align('center')
        row = 0
        col = 0
        if formType == 'F':
          wsheet.write(row, col, 'Kode', fmt2)
          wsheet.write(row, col + 1, 'Deskripsi', fmt2)
          wsheet.write(row, col + 2, 'Value', fmt2)
          row+=1
        dataStructure = recurse(process, 0, True, debugMode=False)
        dataStructure.reverse()
        #app.ConWriteln('Len data structure found : {0}'.format(len(dataStructure)))
        for idx in range(len(dataStructure)):
          #app.ConWriteln('Setting field for : {0}'.format(dataStructure[idx][1]))
          if formType == 'F':
            wsheet.write(row, col, dataStructure[idx][1])
            wsheet.write(row, col + 1, dataStructure[idx][3])
            row += 1
          else:
            wsheet.write(row, col, dataStructure[idx][1])
            wsheet.write(row + 1, col, dataStructure[idx][3], fmt2)
            wsheet.set_column(col, col, len(dataStructure[idx][3])+2)
            col += 1
        if formType == 'F':
          wsheet.set_column(0, 0, None, None, {'hidden':True})
          wsheet.set_column(1, 1, 100)
        else:
          wsheet.set_row(0, None, None, {'hidden':True})
        app.ConWriteln('Creating template for : {0}'.format(DTS.dtsformcode))
        wbook.close()
      metaTree = recurse(process)
      metaTree.reverse()
      metaForDB = recurse(process, 0 , False, True, helper, None, formId)
      metaForDB.reverse()
      app.ConWriteln('Saving meta to database.')
      for ele in metaTree:
        rec = fieldData.AddRecord()
        rec.lv = ele[0]
        rec.kode = ele[1]
        rec.desc = ele[3]
        # save meta to DB join upon calling
        ''' 
      for ele in metaForDB:
        inputMeta = helper.CreatePObject('DTSMeta')
        inputMeta.DTSFormId = formId
        inputMeta.MetaName = ele[1]
        inputMeta.MetaLevel = ele[0]
        inputMeta.MetaQName = ele[2]
        inputMeta.MetaType = ele[4]
        inputMeta.MetaDesc = ele[3]
        inputMeta.MetaEnum = ele[5]
      '''
      app.ConWriteln('Saving enum found to database.')
      for enumName in rf.enum.keys():
        s = '''
          select * from dtsenum where dtsid={0} and dtsenumname='{1}' 
        '''.format(str(DTS.dtsid), enumName)
        checkEnum = config.CreateSQL(s).RawResult
        if checkEnum.Eof:
          enumClass = rf.enum[enumName]
          enumList = enumClass.members
          for enumCode in enumList.keys():
            inputEnum = helper.CreatePObject('DTSEnum')
            inputEnum.DTSId = DTS.dtsid
            inputEnum.DTSEnumName = enumName
            inputEnum.DTSEnumValue = enumCode
            inputEnum.DTSEnumDesc = enumList[enumCode]
    else: #read from db
      app.ConWriteln('Read meta from database.')
      while not formMeta.Eof:
        rec = fieldData.AddRecord()
        rec.lv = formMeta.MetaLevel
        rec.kode = formMeta.MetaName
        rec.desc = formMeta.MetaDesc
        formMeta.Next()
    #--
    s = '''
      select count(*) jml from dtsformula where dtsformid=%s
    ''' % str(formId)
    formulaCheck = config.CreateSQL(s).RawResult.jml
    if formulaCheck<1: 
      ###################################################### BEGIN FRM ################################################
      ##FRM## -- read formula test block
      fDebug = False
      app.ConWriteln('Reading formula data')
      valCount = 0
      def advSeek(rootSearch, tag, attrib, value, app=None):
        rbTag = rootSearch.seek(tag)
        if app:
          app.ConWriteln(str(len(rbTag)))
        rbAttr = []
        rbVal = []
        if attrib == '__text':
          for ele in rbTag:
            if ele.text == value:
              rbVal.append(ele)
        else:
          for ele in rbTag:
            if ele.attrib.has_key(attrib):
              rbAttr.append(ele)
          for ele in rbAttr:
            if ele.attrib[attrib] == value:
              rbVal.append(ele)
        if app:
          app.ConWriteln(str(len(rbVal)))
        return rbVal
      #--
      def formulaToEval(frmstr):
        retstr = frmstr.strip()
        #change nilled()
        retstr = retstr.replace('nilled','"" == ')
        #change ge
        retstr = retstr.replace('ge','>=')
        #change le
        retstr = retstr.replace('le','<=')
        #change eq
        retstr = retstr.replace('eq','==')
        #change gt
        retstr = retstr.replace('&gt;','>')
        retstr = retstr.replace('gt','>')
        #change lt
        retstr = retstr.replace('&lt;','<')
        retstr = retstr.replace('lt','<')
        #change ne
        retstr = retstr.replace('ne','!=')
        #change true
        retstr = retstr.replace('true()','True')
        #change false
        retstr = retstr.replace('false()','False')
        #change true
        retstr = retstr.replace('true','True')
        #change false
        retstr = retstr.replace('false','False')
        #change &#10;
        retstr = retstr.replace('&#10;','')
        #repair single '='
        fele = retstr.split('=')
        if len(fele)>1:
          ftidy = ''
          can_use = True
          for i in fele:
            if len(i)<1:
              can_use = False
          if can_use:
            for i in range(len(fele)):
              thisPart = fele[i].strip() 
              if i>0:
                prevPart = fele[i-1].strip()
                if prevPart[-1] not in ('>','<','!','=') and thisPart[0] not in ('>','<','!','='):
                  ftidy+=' == '+thisPart
                else:
                  ftidy+='= '+thisPart
              else:
                ftidy+=thisPart
            retstr = ftidy
        #end of repair single '=' menjadi '=='
        #number handled natively
        #retstr = retstr.replace('number','')
        if retstr[:2]=='if':
          #matches using in
          while len(retstr.split('matches'))>1: 
            oldmatchesstr = 'matches'+retstr.split('matches',1)[-1].split(')')[0]+')'
            matchesstr = retstr.split('matches',1)[-1].split('(',1)[-1].split(')')[0]
            leftmatchesstr, rightmatchesstr = matchesstr.split(',')
            rightmatchesstr = rightmatchesstr.replace('&quot;','').replace('"','')
            inmember = rightmatchesstr.split('|')
            inblock = ' '+leftmatchesstr + ' in '+ str(inmember).replace("'",'"')+' '
            retstr = retstr.replace(oldmatchesstr, inblock)
          strcond, strres = retstr.split('then', 1)
          strtru, strfals = strres.split('else', 1)
          retstr = strtru + ' ' + strcond + ' else ' + strfals
          if 'then' in retstr:
            ret1, ret2 = retstr.split('else',1)
            strcond, strres = ret2.split('then', 1)
            strtru, strfals = strres.split('else', 1)
            retstr = ret1 + ' else ( ' + strtru + ' ' + strcond + ' else ' + strfals + ' ) '
        return retstr
      #--
      flinkbases = iForm.linkbases['formula']
      if len(flinkbases) < 1:
        raise Exception, 'Formula linkbases not found on this schema.'
        app.ConWriteln('Formula linkbases not found on this schema.')
      else:
        flinkbase = flinkbases[0]
      flinkbase.readFromFile()
      #''' freeze for test
      ##get calc
      if fDebug:
        app.ConWriteln('--== Calc Formula ==--')
      calcFormulas = flinkbase.rootElement.seek('formula')
      n = 0
      for formulaElement in calcFormulas:
        n+=1
        forvardesc = {}
        feId = ''
        forid = formulaElement.attrib['xlink:title'] 
        cn = formulaElement.seek('qname')
        # DTS.dtsid :  dtsid@dtsformula
        # formId : dtsformid@dtsformula
        # forid : formulaname@dtsformula
        # "c" : formulatype@dtsformula 
        # formulaToEval(formulaElement.attrib['value']+' ') : rumus@dtsformula
        # cn[0].text.split(':')[-1] : applyfor@dtsformula
        # "" : message@dtsformula
        # "f" : exectype@dtsformula
        #'''
        iCalc = helper.CreatePObject('DTSFormula')
        iCalc.DTSId = DTS.dtsid
        iCalc.DTSFormId = formId
        iCalc.FormulaName = forid
        iCalc.FormulaType = "c"
        iCalc.Rumus = formulaToEval(formulaElement.attrib['value']+' ')
        iCalc.ApplyFor = cn[0].text.split(':')[-1]
        iCalc.ExecType = "f"
        #'''
        if fDebug:
          app.ConWriteln("{0} - {1} [{2}]".format(n,forid,cn[0].text))
        varsrc = advSeek(flinkbase.rootElement, 'variableArc', 'xlink:from', forid)
        for vele in varsrc:
          varfil = advSeek(flinkbase.rootElement, 'variableFilterArc', 'xlink:from', vele.attrib['xlink:to'])
          for fele in varfil:
            varcnf = advSeek(flinkbase.rootElement, 'conceptName', 'xlink:title', fele.attrib['xlink:to'])
            for cele in varcnf:
              varref = cele.seek('qname')
              for rele in varref:
                fieldCode = rele.text
                fieldCodeTag = fieldCode.split(':')[-1]
                refValue = ''
                forvardesc[vele.attrib['name']] = fieldCodeTag
        newfrmstr = formulaElement.attrib['value']+' '
        translatedfrm = newfrmstr
        for key in forvardesc.keys():
          # key : varname@dtsformulavars
          # forvardesc[key] : varsource@dtsformulavars
          #'''
          iCalcVar = helper.CreatePObject('DTSFormulaVars')
          iCalcVar.DTSFormulaId = iCalc.DTSFormulaId
          iCalcVar.VarName = key
          iCalcVar.VarSource = forvardesc[key]
          #'''
          translatedfrm = translatedfrm.replace('$%s ' % key, forvardesc[key]+' ')
        if fDebug:
          app.ConWriteln("     {0} = {1}".format(cn[0].text.split(':')[-1], newfrmstr))
          app.ConWriteln("     {0} = {1}".format(cn[0].text.split(':')[-1], translatedfrm))
          app.ConWriteln("    exc : {0}".format("form"))
          app.ConWriteln(' ')
      ##-- end get calc
      valCount += n
      ##get ea
      if fDebug:
        app.ConWriteln('--== EA Formula ==--')
      eaFormulas = flinkbase.rootElement.seek('existenceAssertion')
      n = 0
      for ea in eaFormulas:
        n+=1
        exectype = "r"
        forid = ea.attrib['xlink:title']
        # dtsid :  dtsid@dtsformula
        # formId : dtsformid@dtsformula
        # forid : formulaname@dtsformula
        # "e" : formulatype@dtsformula 
        # "" : rumus@dtsformula
        # "" : applyfor@dtsformula
        #'''
        iEa = helper.CreatePObject('DTSFormula')
        iEa.DTSId = DTS.dtsid
        iEa.DTSFormId = formId
        iEa.FormulaName = forid
        iEa.FormulaType = "e"
        #'''
        if fDebug:
          app.ConWriteln("{0} - {1}".format(n,forid))
        ##get msg
        vaa = advSeek(flinkbase.rootElement, 'arc', 'xlink:from', forid)      # arc
        msgtext = ''
        if len(vaa)>0:
          vaa = vaa[0]
          msg = advSeek(flinkbase.rootElement, 'message', 'xlink:label', vaa.attrib['xlink:to'])
          msgtext = msg[0].text.replace('&gt;','>').replace('&lt;','<').replace('"',' ')
          # msg : message@dtsformula
        else:
          msgtext = "tidak lolos validasi {0}".format(forid)
        if fDebug:
          app.ConWriteln("    msg : {0}".format(msgtext))
        iEa.Message = msgtext
        ##get test field     
        vava = advSeek(flinkbase.rootElement, 'variableArc', 'xlink:from', forid)    # variableArc
        for vafv in vava:
          varname = vafv.attrib['name']
          # varname : varname@dtsformulavars
          #'''
          iEaVar = helper.CreatePObject('DTSFormulaVars')
          iEaVar.DTSFormulaId = iEa.DTSFormulaId
          iEaVar.VarName = varname
          #'''
          vavfa = advSeek(flinkbase.rootElement, 'variableFilterArc', 'xlink:from', vafv.attrib['xlink:to'])     # variableFilterArc
          for vacn in vavfa:
            cnData = advSeek(flinkbase.rootElement, 'conceptName', 'xlink:title', vacn.attrib['xlink:to']) 
            for cn in cnData:
              varref = cn.seek('qname')
              for rele in varref:
                fieldCode = rele.text
                fieldCodeTag = fieldCode.split(':')[-1]
                if ("dummy" in fieldCodeTag) or (formType == 'F'): exectype = "f" 
                if fDebug:
                  app.ConWriteln('    check exists for : {0}'.format(fieldCode))
                # fieldCodeTag : varsource@dtsformulavars
                #'''
                iEaVar.VarSource = fieldCodeTag
                #'''
        #'''
        iEa.ExecType = exectype
        #''' 
        # exectype : exectype@dtsformula
        if fDebug:
          app.ConWriteln("    exc : {0}".format("row" if exectype=="r" else "form"))
          app.ConWriteln(' ')
      ##--end get ea
      #'''
      valCount += n
      ## get va
      if fDebug:
        app.ConWriteln('--== VA Formula ==--')
      vaFormulas = flinkbase.rootElement.seek('valueAssertion')
      n = 0
      for va in vaFormulas:
        n+=1
        forid = va.attrib['xlink:label'] 
        rumus = formulaToEval(va.attrib['test']+' ').replace('&quot;','"')
        rumusolah = rumus
        exectype = "r"
        # dtsid :  dtsid@dtsformula
        # formId : dtsformid@dtsformula
        # va.attrib['id'] : formulaname@dtsformula
        # "v" : formulatype@dtsformula 
        # rumus : rumus@dtsformula
        # "" : applyfor@dtsformula
        #'''
        iVa = helper.CreatePObject('DTSFormula')
        iVa.DTSId = DTS.dtsid
        iVa.DTSFormId = formId
        iVa.FormulaName = va.attrib['id']
        iVa.FormulaType = "v"
        iVa.Rumus = rumus
        #'''
        if fDebug:
          app.ConWriteln("{0} - {1}".format(n,forid))
          app.ConWriteln("     {0}".format(va.attrib['test']+' '))
          app.ConWriteln("     {0}".format(rumus))
        ##get msg
        varchanged = 0
        vaa = advSeek(flinkbase.rootElement, 'arc', 'xlink:from', forid)      # arc
        msgtext = ''
        if len(vaa)>0:
          vaa = vaa[0]
          msg = advSeek(flinkbase.rootElement, 'message', 'xlink:label', vaa.attrib['xlink:to'])
          msgtext = msg[0].text.replace('&gt;','>').replace('&lt;','<').replace('"',' ')
        else:
          msgtext = "tidak lolos validasi {0}.".format(va.attrib['id'])
        #'''
        iVa.Message = msgtext
        #'''                     
        vava = advSeek(flinkbase.rootElement, 'variableArc', 'xlink:from', forid)    # variableArc
        prevVars = []
        for vafv in vava:
          varname = vafv.attrib['name']
          # varname : varname@dtsformulavars
          vavfa = advSeek(flinkbase.rootElement, 'variableFilterArc', 'xlink:from', vafv.attrib['xlink:to'])     # variableFilterArc
          fieldCodeTag = ''
          cPhrase = None
          PhraseTableCode = DTS.dtsformcode
          for vacn in vavfa:
            genData = advSeek(flinkbase.rootElement, 'general', 'xlink:title', vacn.attrib['xlink:to']) 
            if len(genData)>0:
              for gn in genData:
                cPhrase = gn.attrib['test'].replace('&gt;','>').replace('&lt;','<').replace('&quot;','"').replace("'",'"')
                cPhrase = cPhrase.replace('./../','')
                cPhrase = cPhrase.replace('=',' eq ')
                cPhrase = '[ '+cPhrase+' ]'
                if '@id' in msgtext: 
                  iVa.exectype = 'r'
                else:
                  iVa.exectype = 'f'
          for vacn in vavfa:
            cnData = advSeek(flinkbase.rootElement, 'conceptName', 'xlink:title', vacn.attrib['xlink:to'])       # try trapping conceptName 
            for cn in cnData:
              varref = cn.seek('qname')
              for rele in varref:
                fieldCode = rele.text
                fieldCodeTag = fieldCode.split(':')[-1]
                # fieldCodeTag : varsource@dtsformulavars
                #'''
                iVaVar = helper.CreatePObject('DTSFormulaVars')
                iVaVar.DTSFormulaId = iVa.DTSFormulaId
                iVaVar.VarName = varname
                #'''
                #'''
                if cPhrase:
                  iVaVar.VarSource = PhraseTableCode+' '+cPhrase.replace('.', fieldCode)+' '+fieldCode
                else:
                  iVaVar.VarSource = fieldCodeTag
                iVaVar.VarType = "s"
                #''' 
                pvrec = (varname, cPhrase+' '+fieldCode if cPhrase else fieldCodeTag, 's')
                prevVars.append(pvrec)
          if fieldCodeTag<>'':
            rumusolah = rumusolah.replace('$%s' % varname, fieldCodeTag)
            varchanged += 1
            rumustemp = rumusolah
        if rumusolah.find('$') >= 0:                                                   # if not trapped try orFilter
          for vafv in vava:
            varname = vafv.attrib['name']
            # varname : varname@dtsformulavars
            vavfa = advSeek(flinkbase.rootElement, 'variableFilterArc', 'xlink:from', vafv.attrib['xlink:to'])     # variableFilterArc
            fieldCodeTag = ''
            for vaor in vavfa:
              orData = advSeek(flinkbase.rootElement, 'orFilter', 'xlink:title', vaor.attrib['xlink:to'])
              oCount = 0
              for orFil in orData:
                if fDebug:
                  app.ConWriteln(orFil.attrib['xlink:title'])
                ovfa = advSeek(flinkbase.rootElement, 'variableFilterArc', 'xlink:from', orFil.attrib['xlink:title'])  
                for vacn in ovfa:
                  if varchanged < 1:
                    rumusolah = rumus
                  else:
                    rumusolah = rumustemp
                  fieldCodeTag = ''
                  cnData = advSeek(flinkbase.rootElement, 'conceptName', 'xlink:title', vacn.attrib['xlink:to'])
                  #app.ConWriteln('''{$%s/name()}''' % str(varname))
                  if oCount>0:
                    # dtsid :  dtsid@dtsformula
                    # formId : dtsformid@dtsformula
                    # va.attrib['id'] : formulaname@dtsformula
                    # "v" : formulatype@dtsformula 
                    # rumus : rumus@dtsformula
                    # "" : applyfor@dtsformula
                    #'''
                    iVa = helper.CreatePObject('DTSFormula')
                    iVa.DTSId = DTS.dtsid
                    iVa.DTSFormId = formId
                    iVa.FormulaName = va.attrib['id']
                    iVa.FormulaType = "v"
                    iVa.Rumus = rumus
                    #'''
                    for pvrec in prevVars:
                      ipVar = helper.CreatePObject('DTSFormulaVars')
                      ipVar.DTSFormulaId = iVa.DTSFormulaId
                      ipVar.VarName = pvrec[0]
                      ipVar.VarSource = pvrec[1]
                      ipVar.VarType = pvrec[2]
                    if fDebug:
                      app.ConWriteln("    exc : {0}".format("row" if exectype=="r" else "form"))
                      app.ConWriteln(' ')
                    #'''
                    iVa.ExecType = exectype
                    #'''
                    n += 1
                    if fDebug:
                      app.ConWriteln("{0} - {1}".format(n,forid))
                      app.ConWriteln("     {0}".format(va.attrib['test']+' '))
                      app.ConWriteln("     {0}".format(rumus))
                  for cn in cnData:
                    varref = cn.seek('qname')
                    for rele in varref:
                      fieldCode = rele.text
                      fieldCodeTag = fieldCode.split(':')[-1]
                      if 'name()' in msgtext and str(varname) in msgtext:
                        msgownerblock = '{'+msgtext.split('{')[-1].split('}')[0]+'}'
                        msgownerblock = msgownerblock.replace(str(varname),'%s')
                        msgotext = msgtext.replace(msgownerblock % str(varname),fieldCodeTag)
                        iVa.Message = msgotext
                      else:
                        msgotext = msgtext
                        iVa.Message = msgotext
                      #'''
                      iVaVar = helper.CreatePObject('DTSFormulaVars')
                      iVaVar.DTSFormulaId = iVa.DTSFormulaId
                      iVaVar.VarName = varname
                      #'''
                      #'''
                      iVaVar.VarSource = fieldCodeTag
                      iVaVar.VarType = "m"
                      #''' 
                  if fieldCodeTag<>'':
                    rumusolah = rumusolah.replace('$%s' % varname, fieldCodeTag)
                  if fDebug:
                    app.ConWriteln("     {0}".format(rumusolah))
                    app.ConWriteln("    msg : {0}".format(msgotext))
                    # msgtext : message@dtsformula
                  #'''
                  iVa.ExecType = exectype
                  iVa.Message = msgotext
                  #''' 
                  oCount += 1
        else:
          if fDebug:
            app.ConWriteln("     {0}".format(rumusolah))
            app.ConWriteln("    msg : {0}".format(msgtext))
            # msgtext : message@dtsformula
          #'''
          iVa.Message = msgtext
          #''' 
          pass
        if rumusolah.find('$') >= 0:                                               # if still not trapped try generalVariable
          for vafv in vava:
            varname = vafv.attrib['name']
            # varname : varname@dtsformulavars
            #'''
            iVaVar = helper.CreatePObject('DTSFormulaVars')
            iVaVar.DTSFormulaId = iVa.DTSFormulaId
            iVaVar.VarName = varname
            #'''
            gvData = advSeek(flinkbase.rootElement, 'generalVariable', 'xlink:title', vafv.attrib['xlink:to'])
            for gv in gvData:
              lookup = gv.attrib['select'].replace('&gt;','>').replace('&lt;','<').replace('&quot;'," ")
              if fDebug:
                app.ConWriteln('     {0} : {1}'.format(varname,lookup))
              #'''
              iVaVar.VarSource = lookup
              iVaVar.VarType = "l"
              #'''
          if '@id' in msgtext:
            exectype = "r"
          else:
            exectype = "i"
          if fDebug:
            app.ConWriteln("     {0}".format(rumusolah))
            app.ConWriteln("    msg : {0}".format(msgtext))
            # msgtext : message@dtsformula
          #'''
          iVa.Message = msgtext
          #''' 
        if fDebug:
          app.ConWriteln("    exc : {0}".format("row" if exectype=="r" else "form"))
          app.ConWriteln(' ')
        # exectype : exectype@dtsformula
        #'''
        iVa.ExecType = exectype
        #''' 
      ##-- end get va
      valCount += n
      if fDebug:
        app.ConWriteln('Total validation rule : {0}'.format(valCount))
        app.ConWriteln('Press Cancel...')
        app.ConRead('a')
      ###################################################### END FRM ################################################
    #app.ConWriteln('Done.')
    #app.ConRead('pause')
    status.tempLoc = xlsLocation.replace('.xlsx','.txt')
    config.Commit()
  except:
    app.ConRead(' ')
    config.Rollback()
    status.Is_Err = str(sys.exc_info()[1])

  return 1

def SaveSetting(config, parameter, returns):
  # config: ISysConfig object
  # parameter: TPClassUIDataPacket
  # returnpacket: TPClassUIDataPacket (undefined structure)
  rec = parameter.FirstRecord
  formId = rec.formId
  isEmpty = rec.isEmpty
  formType = rec.formType
  dataSize = rec.dataSize
  status = returns.CreateValues(
      ['Is_Err', '']
  )
  config.BeginTransaction()
  try:                                 
    s = '''update dtsform set isempty='{0}', formtype='{1}', tempready='T', datasize='{3}'
           where dtsformid={2}'''.format(isEmpty, formType, str(formId), dataSize)
    config.ExecSQL(s)
    config.Commit()
  except:
    config.Rollback()
    status.Is_Err = str(sys.exc_info()[1])

  return 1

