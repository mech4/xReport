# attribute manipulation utilities
# for client-side objects

# warning: this code should be place inside clientscript's folder of application
# this file is placed in python library only to ensure the latest copy


class ClientAttrUtil:

  class record: pass

  def transferAttributes(self, transfers, dest, src):
    # dest is either record, dictionary, TPClassUIRecord, TrtfQuery or TrtfPClassUI
    # src is either record, dictionary, TPClassUIRecord, TrtfQuery or TrtfPClassUI
    # transfers are list of transfer instructions
    #    each transfer instruction is a string with following syntax:
    #    <instruction> ::= <simple transfer> | <assignment>
    #    <simple transfer> ::= <identifier> | <dotted identifier series>  # denotes transfer from dest.<identifier> = src.<identifier>
    #    <assignment> ::= (<identifier> | <dotted identifier series>) "=" (<identifier> | <dotted identifier series>)
    # example:
    # 'a' means dest.a = src.a
    # 'a=b' means dest.a = src.b
    
    # internal type reps
    # 0 = python object
    # 1 = dict
    # 2 = TPClassUIRecord
    # 3 = TrtfQuery
    # 4 = TrtfPClassUI
    
    srcType = None
    dstType = None
    srcGetFunc = None
    dstSetFunc = None
    
    def defineType(obj):
      if type(obj) is dict:
        return 1
      else:
        sType = str(type(obj))
        if sType == "<type 'instance'>":
          return 0
        if sType == "<type 'PyPClassUIRecord'>":
          return 2
        elif sType == "<type 'PyrtfQuery'>":
          return 3
        elif sType == "<type 'PyrtfPClassUI'>":
          return 4
        else:
          raise Exception, "Unrecognized type %s" % sType
        #--
      #--
    #--
    
    def defineGetFunc(obj, type_id):
      if type_id == 0:
        f = obj.__dict__.__getitem__
      elif type_id == 1:
        f = obj.__getitem__
      elif type_id == 2:
        f = obj.GetFieldByName
      elif type_id == 3:
        f = obj.GetFieldValue
      elif type_id == 4:
        f = obj.GetFieldValue
      else:
        raise Exception, "defineGetFunc: Unsupported type_id"
      #--
      return f
    #--
    
    def defineSetFunc(obj, type_id):
      if type_id == 0:
        f = obj.__dict__.__setitem__
      elif type_id == 1:
        f = obj.__setitem__
      elif type_id == 2:
        f = obj.SetFieldByName
      elif type_id == 3:
        f = obj.SetFieldValue
      elif type_id == 4:
        f = obj.SetFieldValue
      else:
        raise Exception, "defineSetFunc: Unsupported type_id"
      #--
      return f
    
    
    def transfer(inst):
      tmp = inst.split("=", 1)
      if len(tmp) == 1:
        fieldName = tmp[0]
        dstSetFunc(fieldName, srcGetFunc(fieldName))
      else:
        srcFieldName = tmp[1]
        dstFieldName = tmp[0]
        rvalue = srcGetFunc(srcFieldName)
        dstSetFunc(dstFieldName, rvalue)
      #--
    #--
      
    srcType = defineType(src)
    dstType = defineType(dest)
    dstSetFunc = defineSetFunc(dest, dstType)
    srcGetFunc = defineGetFunc(src, srcType)
    for transferItem in transfers:
      transfer(transferItem)
    
    pass
  #--
#-- Class ClientAttrUtil
  
  
  
  
