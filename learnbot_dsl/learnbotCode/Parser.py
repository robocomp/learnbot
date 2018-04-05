#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------
#   TODO Añadir definition de funciones.
#
#
# ------------------------------------------------------------------

from pyparsing import *
import sys

HEADER = """

# EXECUTION: python code_example.py configSimulated

global lbot
lbot = <LearnBotClient>.Client(sys.argv)


"""
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

OBRACE,CBRACE,SEMI,OPAR,CPAR = map(Literal, "{};()")

reserved_words = ( Keyword('def') | Keyword('=') | Keyword('funtion.') | Keyword('>=') | Keyword('<=') | Keyword('<') | Keyword('>') | Keyword('deactive') | Keyword('active') | Keyword('not') | Keyword('True') | Keyword('False') | Keyword('or') | Keyword('and') | Keyword('main') | Keyword('if') | Keyword('else') | Keyword('elif') | Keyword('when') | Keyword('while') | Keyword('end'))
iden = Word( alphanums+"_")
identifier = Group( ~reserved_words + iden ).setResultsName( "IDENTIFIER" )

QUOTE = Word( "\"" )
OR    = Word( "or" )
AND   = Word( "and" )
NOT   = Group( Word( "not" ) ).setResultsName( 'NOT' )
plus  = Word( "+" )
minus = Word( "-" )
mult  = Word( "*" )
div   = Word( "/" )
lpar  = Word( "(" )
rpar  = Word( ")" )
TRUE  = Group( Word( "True" ) ).setResultsName( 'TRUE' )
FALSE = Group( Word( "False" ) ).setResultsName( 'FALSE' )
eq    = Word( "=" )
point    = Literal('.')
coma    = Word( "," )
COLONS= Suppress(Word( ":" ))
SEMICOL= Word( ";" )
plusorminus = Literal('+') | Literal('-')
e = CaselessLiteral('E')
number = Word(nums)
integer = Combine( Optional(plusorminus) + number )
NUMS = Group( Combine( integer + Optional( point + Optional(number) ) + Optional( e + integer ) ) ).setResultsName( "NUMBER" )


L      = Literal( "<" )
NL     = Literal( ">" )
LE     = Literal( "<=" )
NLE    = Literal( ">=" )
E      = Literal( "==" )
NE     = Literal( "!=" )
END    = Literal( "end" )
SECTAB = ZeroOrMore("\t")

"""-----------------COMPARACIONES-------------------"""
COMP  = Group( L | NL | LE | NLE | E | NE ).setResultsName( "COMP" )

"""-----------------OPERADORES----------------------"""
SRMD  = Group( plus | minus | mult | div ).setResultsName( "SRMD" )

"""-----------------OPERACIONES---------------------"""
OPERATION = Group( identifier + ZeroOrMore( SRMD + identifier ) ).setResultsName( "OPERATION" )

"""-----------------OPERACIONES---------------------"""
ORAND = Group( OR | AND ).setResultsName( 'ORAND' )

"""-----------------FUNCTION-------------------------"""
FUNCTION = Group( Suppress( Literal( "function" ) ) + Suppress( point ) + identifier.setResultsName( 'name' ) + Suppress( lpar ) + Group( Optional( NUMS | identifier ) + ZeroOrMore( Suppress( coma ) + ( NUMS | identifier ) ) ).setResultsName( "args" ) + Suppress( rpar )).setResultsName( "FUNCTION" )

"""-----------------SIMPLEFUNCTION-------------------------"""
SIMPLEFUNCTION = Group( identifier.setResultsName( 'name' ) + Suppress( lpar ) + Group( Optional( NUMS | identifier ) + ZeroOrMore( Suppress( coma ) + ( NUMS | identifier ) ) ).setResultsName( "args" ) + Suppress( rpar )).setResultsName( "SIMPLEFUNCTION" )

"""-----------------PASS-------------------------"""
PASS = Group( Literal( "pass" )).setResultsName( "PASS" )

"""-----------------CONDICIONES---------------------"""
COMPOP = Group( OPERATION + COMP + OPERATION ).setResultsName( "COMPOP" )
OPTIONCONDITION =  SIMPLEFUNCTION | FUNCTION | TRUE | FALSE | COMPOP | identifier
SIMPLECONDITION = Group( Optional( NOT ) + OPTIONCONDITION ).setResultsName( "SIMPLECONDITION")
CONDITION = Group( SIMPLECONDITION + ZeroOrMore( ORAND + SIMPLECONDITION ) ).setResultsName( "CONDITION" )

"""-----------------asignacion-VARIABLES------------"""
CHAINBETTENQUOTE = Group( QuotedString( '"' ) ).setResultsName( "STRING" )
ASSIGSTRING = Group( ( CHAINBETTENQUOTE | NUMS ) + ZeroOrMore( SRMD + ( CHAINBETTENQUOTE | NUMS ) ) ).setResultsName( 'ASSIGSTRING' )
NUMVAR    = Group( SECTAB + identifier.setResultsName( "name" ) + Suppress( eq ) + OPERATION ).setResultsName( "NUMVAR" )
BOOLVAR   = Group( SECTAB + identifier.setResultsName( "name" ) + Suppress( eq ) + CONDITION ).setResultsName( "BOOLVAR" )
STRINGVAR = Group( SECTAB + identifier.setResultsName( "name" ) + Suppress( eq ) + ASSIGSTRING ).setResultsName( "STRINGVAR")   # Solved error var =  0

"""-----------------LINEA---------------------------"""
LINE   = Forward()
LINES  = Group( LINE + ZeroOrMore( LINE ) )

"""-----------------bloque-IF-----------------------"""
ELSE   = Forward()
ELSEIF  = Forward()
INIF   = LINES  &    ( ZeroOrMore( ELSEIF ) + Optional( ELSE ) )

ELSEIF << Group( SECTAB + Suppress( Literal( "elif" ) ) + Group( CONDITION ).setResultsName('condition') + COLONS + LINES.setResultsName('content') ).setResultsName( "ELIF" )
ELSE   << Group( SECTAB + Suppress( Literal( "else" ) ) +                                                  COLONS + LINES.setResultsName('content') ).setResultsName( "ELSE" )
IF     =  Group( SECTAB + Suppress( Literal( "if"   ) ) + Group( CONDITION ).setResultsName('condition') + COLONS + LINES.setResultsName('content') + Group( ZeroOrMore( ELSEIF ) + Optional( ELSE ) ).setResultsName( "OPTIONAL" ) + Suppress( Literal( "end" ) ) ).setResultsName( "IF" )

"""-----------------LOOP----------------------------"""
BLOQUEWHILE    = Group( SECTAB + Suppress( Literal( "while" ) ) + Group( CONDITION ).setResultsName('condition') + COLONS + LINES.setResultsName('content') + Suppress( Literal("end") ) ).setResultsName("WHILE")

"""-----------------WHEN+CONDICION------------------"""
BLOQUEWHENCOND = Group( SECTAB + Suppress( Literal( "when" ) ) + identifier.setResultsName("name") + Optional( Suppress( eq )+ Group( CONDITION ).setResultsName( 'condition' ) ) + COLONS + LINES.setResultsName('content') + Literal("end") ).setResultsName( "WHEN" )

"""-----------------ACTIVE-CONDITION----------------"""
ACTIVE   = Group( Suppress( Literal( "active" ) )   + identifier.setResultsName( "name" ) ).setResultsName( "ACTIVE" )
DEACTIVE = Group( Suppress( Literal( "deactive" ) ) + identifier.setResultsName( "name" ) ).setResultsName( "DEACTIVE" )


"""-----------------LINEA---------------------------"""
LINE << ( SIMPLEFUNCTION | FUNCTION | IF | BLOQUEWHILE | BOOLVAR | NUMVAR | ACTIVE | DEACTIVE | STRINGVAR | PASS )

"""-----------------DEF----------------------------"""
DEF = Group( Suppress( Literal ( "def " ) ) + identifier.setResultsName("name") + Suppress( lpar ) + Suppress( rpar ) + COLONS + LINES.setResultsName('content') + Suppress( Literal("end") ) ).setResultsName( "DEF" ) # TODO

"""-----------------MAIN----------------------------"""
MAIN = Group( Suppress( Literal( "main" ) ) + COLONS + LINES.setResultsName( 'content' ) ).setResultsName( "MAIN" ) + Suppress( Literal("end") )
LB =  ZeroOrMore(DEF) + ( MAIN | ZeroOrMore( BLOQUEWHENCOND ) )
LB.ignore( pythonStyleComment )

ini = []

def __parserFromFile(file):
    with open(file) as f:
        text = f.read()
        ret = __parserFromString(text)
        print ret
        return ret

def __parserFromString(text):
    try:
        LB.ignore(pythonStyleComment)
        ret = LB.parseString(text)
        return ret
    except Exception as e:
        print("line: {}".format(e.line))
        print("    "+" "*e.col+"^") + bcolors.ENDC
        raise e
        exit(-1)

def __generatePy(lines):
    list_var = []
    text = "time_global_start = time.time()"

    text += "\ndef elapsedTime(umbral):\n\tglobal time_global_start\n\ttime_global = time.time()-time_global_start\n\treturn time_global < umbral\n\n"
    thereareWhens = False
    for x in lines:
        if x.getName() is 'WHEN':
            thereareWhens = True
            list_var.append("time_" + str(x.name[0]))
            list_var.append(str(x.name[0]) + "_start")
            list_var.append( x.name[0] )
        elif x.getName in ['NUMVAR', 'BOOLVAR', 'STRINGVAR']:
            list_var.append(x.name[0])

    global ini
    for x in lines:
        text = __process(x, list_var, text)

    if thereareWhens is True:
        text += "\n\nwhile True:\n"
        for line in ini:
            text += "\t" + line
        for x in lines:
            if x.getName() is 'WHEN':
                text += "\twhen_" + str( x.name[0] ) + "()\n"
    return text

def __process(line, list_var=[], text="", index=0):
    # print "------------Procesando ",line
    TYPE = line.getName()
    # print "\t",TYPE, line

    if TYPE is 'MAIN':
        for cLine in line.content:
            text += __process(cLine, [], "",0)

    elif TYPE is 'DEF':
        text = __processDEF(line, list_var, text,1)
    elif TYPE is 'WHEN':
        text = __processWHEN(line, list_var, text)
    elif TYPE is 'WHILE':
        text = __processWHILE(line,text,index)
    elif TYPE is 'IF':
        text = __processIF(line,text,index)
    elif TYPE is 'ELIF':
        text = __processELIF(line,text,index)
    elif TYPE is 'ELSE':
        text = __processELSE(line,text,index)
    elif TYPE is 'ACTIVE':
        text = __processACTIVE(line, text, index)
    elif TYPE is 'DEACTIVE':
        text = __processDEACTIVE(line, text, index)
    elif TYPE in ['NUMVAR', 'BOOLVAR', 'STRINGVAR']:
        text = __processASSIG(line, text, index)
    elif TYPE is 'OPERATION':
        text = __processOP(line, text, index)
    elif TYPE is 'FUNCTION':
        text = __processFUNCTION(line, text, index)
    elif TYPE is 'SIMPLEFUNCTION':
        text = __processSIMPLEFUNCTION(line, text, index)
    elif TYPE is 'CONDITION':
        text = __processCONDITION(line, text, index)
    elif TYPE is 'ASSIGSTRING':
        text = __processASSIGSTRING(line, text, index)
    elif TYPE in ['FALSE','TRUE','IDENTIFIER', 'SRMD']:
        text = line[0]
    elif TYPE is 'SIMPLECONDITION':
        text = __processSIMPLECONDITION(line, text, index)
    elif TYPE is 'PASS':
        text += "\t" * index + "pass\n"
    return text


def __processDEF(line,list_var, text="", index=0):
    text += "def " + line.name[0] + "():\n"
    for x in list_var:
        text += "\t"*index + "global " + x + "\n"
    for field in line.content:
        text = __process(field, [], text, index) + "\n\n"
    return text

def __processFUNCTION(line, text="", index=0):
    if text is not "":
        text += "\t"*index
    text += "functions.get(\"" + line.name[0] + "\")(lbot"
    for x in line.args:
        text += ", " + x[0]
    text += ")"
    return text

def __processSIMPLEFUNCTION(line, text="", index=0):
    if text is not "":
        text += "\t"*index
    text += line.name[0] + "("
    if len(line.args) is not 0:
        for x in line.args:
            text += x[0] + ","
        text = text[:-1] + ")"
    else:
        text += ")"
    return text

# ---------------------------------------
# Process NUMVAR, BOOLVAR, STRINGVAR
# ---------------------------------------

def __processASSIG(line, text="", index=0):
    # print "------------------------__processASSIG-----", line[1]
    text += "\t"*index + line.name[0] + " = " + __process(line[1])
    return text

def __processASSIGSTRING(line, text="", index=0):
    for field in line:
        if field.getName() is 'STRING':
            text += "\"" + field[0] + "\" "
        elif field.getName() is 'NUMBER':
            text += "str(" + field[0] + ") "
        else:
            text += field[0] + " "
    return text

def __processACTIVE(line, text="", index=0):
    text += "\t"*index + line.name[0] + " = True\n"
    return text

def __processDEACTIVE(line, text="", index=0):
    text += "\t"*index + line.name[0] + " = False\n"
    return text

def __processWHILE(line, text="", index=0):
    print "-----------------------------------------------------",index
    text += "\n" + "\t"*index + "while "
    for c in line.condition:
        text += __process(line.condition[0])
    text += ":\n"

    index+=1
    for field in line.content:
        text = __process(field, [], text, index) + "\n"

    index-=1
    return text

def __processWHEN(line, list_var, text="", index=0):
    global ini
    text += "\ndef when_" + str(line.name[0]) + "():\n"
    index += 1
    # list_var.append("time_" + str(line.name[0]))
    # list_var.append(str(line.name[0]) + "_start")
    for x in list_var:
        text += "\t"*index + "global " + x + "\n"
    # text += "\t"*index + "global " + "time_" + str(line.name[0]) + "\n"
    # text += "\t"*index + "global " + str(line.name[0]) + "_start\n"

    text += "\t"*index + "if time_" + str(line.name[0]) + " is 0:\n\t\t"+ str(line.name[0]) + "_start = time.time()\n"

    text += "\t"*index + "if " + str(line.name[0]) + ":\n"
    index += 1
    for cline in line.content:
        text = __process(cline, [], text, index) + "\n"
    index-=1
    text += "\t\ttime_" + str(line.name[0]) + " = time.time() -" + str(line.name[0]) + "_start\n\telse:\n\t\ttime_" + str(line.name[0]) + " = 0\n"

    if line.condition is not "":
        ini.append( line.name[0] + " = " + __process(line.condition[0]) + "\n")

    text ="time_" + str(line.name[0]) + " = 0\n"+str(line.name[0]) + "_start = time.time()\n" + text

    if line.condition is "":
        text = line.name[0] + " =  None\n" + text
    return text

def __processOP(line, text="", index=0):
    # print "------------------------__processOP------------"
    for field in line:
        text += field[0] + " "
    # print "-----------------------end-__processOP------------"
    return text

def __processCOMPOP(line, text="", index=0):
    for field in line:
        TYPE = field.getName()
        if TYPE is 'OPERATION':
            text += __process(field)
        elif TYPE is 'COMP':
            text += field[0] + " "
    return text

def __processSIMPLECONDITION(line, text="", index=0):
    # print "------------------------", line
    for field in line:
        TYPE = field.getName()
        if TYPE is 'NOT':
            text += "not "
        elif TYPE in ['IDENTIFIER','SIMPLEFUNCTION','FUNCTION','TRUE','FALSE']:
            text += __process(field)
        elif TYPE is "COMPOP":
            text += __processCOMPOP(field)
        # else:
            # text += field
    return text

def __processCONDITION(line, text="", index=0):
    for field in line:
        if field.getName() is 'SIMPLECONDITION':
            text += __process(field) + " "
        elif field.getName() is 'ORAND':
            text += field[0] + " "
    return text

def __processELIF(line, text="", index=0):
    text += "\t"*index + "elif "
    for c in line.condition:
        text += __process(line.condition[0])
    text += ":\n"
    index+=1
    for field in line.content:
        text = __process(field, [], text, index) + "\n"
    return text

def __processELSE(line, text="", index=0):
    text += "\t"*index + "else:\n"
    index+=1
    for field in line.content:
        text = __process(field, [], text, index) + "\n"
    return text

def __processIF(line, text="", index=0):
    text += "\t"*index + "if "
    for c in line.condition:
        text += __process(line.condition[0])
    text += ":\n"

    index+=1
    for field in line.content:
        text = __process(field, [], text, index) + "\n"

    index-=1
    for field in line.OPTIONAL:
        text = "\t"*index + __process(field, [], text, index)
    return text

def parserLearntBotCode(inputFile, outputFile, physicalRobot=False):
    print "----------------------------------" + inputFile + "----------------------------------------------"
    try:
        text = __generatePy( __parserFromFile( inputFile ) )
        print "------------------",text
        if physicalRobot:
            header = HEADER.replace('<LearnBotClient>','LearnBotClientPR')
        else:
            header = HEADER.replace('<LearnBotClient>','LearnBotClient')
        with open( outputFile ,'w') as f:
            f.write( header )
            f.write( text )
    except Exception as e:
        print e
        raise e


if __name__ == "__main__":
    argv = sys.argv[1:]
    if len( argv ) is not 2:
        print bcolors.FAIL + "You must give 2 arguments"
        print "\timputfile\tFile to parser"
        print "\toutputfile\tFile to parser" + bcolors.ENDC
        exit(-1)
    if argv[0] == argv[1]:
        print bcolors.FAIL + "Imputfile must be different to outputfile" + bcolors.ENDC
        exit(-1)
    print bcolors.OKGREEN + "Generating file " + argv[1] + bcolors.ENDC
    text = __generatePy( __parserFromFile( argv[0] ) )
    print bcolors.OKGREEN + "Generating file " + argv[1] + "\t[100%]" + bcolors.ENDC
    with open( argv[1] ,'w') as f:
        f.write( header )
        f.write( text )
