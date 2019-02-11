import re

FloatOperators= {'+': 'Op_add' ,'-': 'Op_subtract' ,'*': 'Op_multiply' ,'/':'Op_divide' ,'//':'Op_floor' ,'%': 'Op_mod','++':'Op_incr' ,'--':'Op_decr', '^':'Op_exponent'}
StringOperators = {'add': 'Op_string_add', 'repeat': 'Op_string_multiply'}
RelationalOperators = {'==':'Op_equal', '~=': 'Op_notequal', '<': 'Op_less', '<=' : 'Op_lessequal', '>': 'Op_greater', '>=':'Op_greaterequal'}
LogicalOperators = {'and': 'Op_and', 'or':'Op_or', 'not':'Op_not'}
ListOperators = {'join': 'Op_append', ':': 'Op_slice', '[' :'left_list_bracket', ']':'right_list_bracket'}
datatype = {'float' : 'float','int' : 'integer' ,'string': 'string','list': 'list', 'boolean': 'boolean'}
keyword = {'make' : 'keyword_make','return' : 'keyword_return','else':'keyword_else', 'print' : 'keyword_print', 'true' : 'keyword_true', 'false' : 'keyword_false', 'until' : 'keyword_until', 'if' : 'keyword_if', 'elseif' : 'keyword_elseif', 'put' : 'keyword_put', 'into' : 'keyword_into', 'for': 'keyword_for', 'in': 'keyword_in'}
delimiter = {';':'endline'}
punctuation = {'{' : 'left_brace', '}':'right_list_bracket', '(':'open_parenthesis', ')':'close_parenthesis', ',': 'comma'}
numerals = ['0','1','2','3','4','5','6','7','8','9']
error = {}

def RazTokenizer(file):
    f = open(file,'r')
    p = f.read()

    symbols = ['(', ')', '[',']', '"', '*', '\n', ':', ',','=','+','-'] # single-char keywords
    other_symbols = ['//', '++', '--'] # multi-char keywords
    KEYWORDS = other_symbols + list(RelationalOperators.keys()) + list(delimiter.keys()) + list(punctuation.keys()) +symbols #non alphabetic pre-defined characters
    white_space = ' '
    lexeme = ''
    DictTokens = {}
    count = 1
    tokens = []
    string = ''

    StringFlag = False
    CommentFlag = False
    for i,char in enumerate(p):
        # count += 1
        if CommentFlag == False:
            if char == '"' and StringFlag == False: #check if next character start a string
                StringFlag = True
                lexeme += char
            elif StringFlag == True and char != '"':  #add char to lexeme until string closed
                lexeme += char
            elif StringFlag == True and char == '"': #string closed -> add lexeme to tokens
                lexeme += char
                tokens.append(lexeme)
                lexeme = ''
                StringFlag = False
            elif char == "'" and StringFlag == False: #detect a comment
                # lexeme+= char
                CommentFlag = True
                CommentLine = count
            elif CommentFlag == True and ((count - CommentLine) > 3):
                CommentFlag = False
                error['comment'] = (CommentLine,'Unended Comment')
            else:
                if char != white_space and StringFlag == False:
                    lexeme += char # adding a char each time
                if (i+1 < len(p)) and StringFlag == False: # prevents error
                    if (p[i+1] == white_space or p[i+1:i+3] in KEYWORDS or p[i+1] in KEYWORDS or lexeme in KEYWORDS) and StringFlag == False: # if next char == ' '
                        if lexeme != '' :
                            lexeme = re.sub(r"[\t]*", "", lexeme)
                            tokens.append(lexeme)
                            try:
                                tokens.remove('')

                            except:
                                pass
                            if lexeme == '\n':
                              tokens.remove('\n')
                              for i in tokens:
                                  if i in ['+','-','/']:
                                    pos = tokens.index(i)
                                    if (pos + 1 < len(tokens)):
                                      if tokens[pos+1] == i:
                                          del tokens[pos]
                                          del tokens[pos]
                                          tokens.insert(pos,str(i*2))

                              if len(tokens) != 0:
                                DictTokens[count] = tokens
                              tokens = []
                              count += 1
                            if lexeme == '\t':
                              tokens.remove('\t')
                        lexeme = ''
        else:
            if char != "'":
                if char == '\n':
                    count += 1
                else:
                    pass
            else:
                CommentFlag = False
                continue

    return DictTokens

def writeTokenFile(file,classIdentifier): #write '.out' file
  fName = file[:-4] +'.out'
  f = open(fName,'w')
  for i in classIdentifier:
    for j in classIdentifier[i]:
      string = '<'+ str(j[1]) + ',' + str(j[0])+'>'
      f.write(string)

def writeSymbolTable(file,symbolTable):
  fName = file[:-4] +'.sym'
  f = open(fName,'w')
  for i in symbolTable:
    string = '<' + str(i) + ' ,' + str(symbolTable[i]) + '> \n'
    f.write(string) #write symbol table

def classIdentifier(DictTokens,a):
  classDict = {}
  Int = False

  for i in DictTokens:
    temp = []
    for j in DictTokens[i]:
      if j in FloatOperators.keys():
        temp.append((j,FloatOperators[j]))
      elif j in StringOperators.keys():
        temp.append((j,StringOperators[j]))
      elif j in LogicalOperators.keys(): 
        temp.append ((j,LogicalOperators[j]))
      elif j in RelationalOperators.keys():
        temp.append((j,RelationalOperators[j]))
      elif j in ListOperators.keys():
        temp.append((j,ListOperators[j]))
      elif j in datatype.keys():
        temp.append((j,datatype [j]))
      elif j in keyword:
        temp.append((j,'keyword'))
      elif j in delimiter.keys():
        temp.append((j,delimiter[j]))
      elif j in punctuation.keys():
        temp.append((j,punctuation[j]))

      elif j in [k for k,v in a.values()]:
        xyz = (([key for key, (value,idd) in a.items() if value == j]), 'identifier')
        xyz = (xyz[0][0], xyz[1])
        temp.append(xyz)
      else:
        temp.append((j,'unidentified'))
    classDict[i] = temp
  return (classDict )

def unidentified(classDict):
  unidList = []
  for i in classDict:
    for j in classDict[i]:
      if (j[1]) == 'unidentified':
        unidList.append(j)
  return set(unidList)

def symboltable(DictTokens):
  symbolTable = {}
  count=1
  Type = ''
  Declaration = False
  FunctionDef = False
  for i in DictTokens:
    for j in (DictTokens[i]):
      if j == 'make':
        FunctionDef = True
      elif FunctionDef == True and j not in ['(',')']:
        symbolTable[count] = (j,'Identifier')
        count += 1
      elif FunctionDef == True and j == '(':
        continue
      elif FunctionDef == True and j == ')':
        FunctionDef = False
      elif j in ['float', 'list', 'boolean', 'for'] and Declaration == False:
        Declaration = True
      elif Declaration == True:
        symbolTable[count] = (j,'Identifier')
        count += 1
        Declaration = False
        Type = ''
      else:
        Int = False
        Float = False
        Var = False
        Stri = False
        for q in j:
          if q in numerals and Stri == False and Var == False and Float == False:
            Int = True
          elif q == '.' and Stri == False:
            Float = True
            Int = False
          elif q in numerals and Float == True and Stri == False and Var == False:
            pass
          elif q == '"':
            Stri = True
          else:
            Var = True
            Int = False
            Float = False
            Stri = False

        if Int == True:
          symbolTable[count]=((j,'integer'))
          count+=1
        elif Float == True:
          symbolTable[count]=((j,'float_number'))
          count+=1
        elif Stri == True:
          symbolTable[count]=((j, 'String'))
          count+=1
        else:
          continue

  return symbolTable

def errorDetection(classIdentifier):
  '''Delete invalid char tokens'''
  symbols = ['`','!','@','#','$','%','^','&','|']

  for i in classIdentifier:
    count = -1
    for j in classIdentifier[i]:
      count+=1
      if j[1] == 'unidentified':
        if j[0] in symbols:
          error[j[0]] = (i,'invalid character')
          del ((classIdentifier[i])[count])

  # '''Delete undefined varaibles'''
        else:
          error[j[0]] = (i,'undefined variable')
          del ((classIdentifier[i])[count])

  return classIdentifier,error

def WriteError(errorDict,file):
  fName = file[:-4] +'.err'
  f = open(fName,'w')
  for i in errorDict:
    Error = 'Line number ' + str((errorDict[i])[0]) + ': ' + str((errorDict[i])[1]) + ' ' + str(i) + '\n'
    f.write(Error)


def main():
  i = 'mergesort.raz'
  tokenizer = RazTokenizer(i)
  a = symboltable(tokenizer) #symbol table
  b = classIdentifier(tokenizer,a)
  c = errorDetection(b)
  print(c)
  writeTokenFile(i,c[0])
  writeSymbolTable(i,a)
  WriteError(error,i)


main()