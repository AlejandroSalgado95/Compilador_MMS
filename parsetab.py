
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = "leftandorleft><equalsnot_equalsleftminus+left*/and char circle clear color cte_c cte_f cte_i cte_s do else equals float for global id if int main minus module not_equals or pendown penup point program read return size then to var void while write\n     PROGRAMA : program  SEM_GLOBAL_NAME  SEM_ADD_FUNC ';' PROGRAMA_OPTS PRINCIPAL \n               | program  SEM_GLOBAL_NAME  SEM_ADD_FUNC ';' PRINCIPAL \n    \n    PROGRAMA_OPTS :  DEC_V FUNCS\n                    | DEC_V\n                    | FUNCS\n    \n    PRINCIPAL : SEM_MAIN_NAME SEM_ADD_FUNC '(' ')' SEM_ADD_GLOBAL_VARIABLES BLOQUE\n    \n    DEC_V : DEC_V var  TIPO_SIMPLE ':' LISTA_VAR ';' \n            | var TIPO_SIMPLE ':' LISTA_VAR ';'\n    \n    LISTA_VAR : LISTA_VAR ',' VARIABLE_FIX\n               | VARIABLE_FIX\n    \n    TIPO_SIMPLE : int \n                 | float \n                 | char\n    \n    FUNCS :  FUNCS FUNC_TYPES module SEM_FUNC_NAME SEM_ADD_FUNC '(' ')' SEM_ADD_GLOBAL_VARIABLES BLOQUE\n           | FUNCS FUNC_TYPES module SEM_FUNC_NAME SEM_ADD_FUNC '(' PARAMS ')' SEM_ADD_GLOBAL_VARIABLES BLOQUE\n           | FUNCS FUNC_TYPES module SEM_FUNC_NAME SEM_ADD_FUNC '(' PARAMS ')' DEC_V SEM_ADD_GLOBAL_VARIABLES BLOQUE \n           | FUNCS FUNC_TYPES module SEM_FUNC_NAME SEM_ADD_FUNC '(' ')' DEC_V SEM_ADD_GLOBAL_VARIABLES BLOQUE\n           | FUNC_TYPES module SEM_FUNC_NAME SEM_ADD_FUNC '(' ')' SEM_ADD_GLOBAL_VARIABLES BLOQUE\n           | FUNC_TYPES module SEM_FUNC_NAME SEM_ADD_FUNC '(' PARAMS ')' SEM_ADD_GLOBAL_VARIABLES BLOQUE\n           | FUNC_TYPES module SEM_FUNC_NAME SEM_ADD_FUNC '(' PARAMS ')' DEC_V SEM_ADD_GLOBAL_VARIABLES BLOQUE\n           | FUNC_TYPES module SEM_FUNC_NAME SEM_ADD_FUNC '(' ')' DEC_V SEM_ADD_GLOBAL_VARIABLES BLOQUE\n\n    \n    FUNC_TYPES :  char\n                 | float \n                 | int\n                 | void\n    \n    PARAMS : PARAMS ',' TIPO_SIMPLE PARAM_NAME\n            | TIPO_SIMPLE PARAM_NAME\n    \n  PARAM_NAME : id\n  \n    VARIABLE_FIX : id '[' cte_i ']' \n                  | id\n    \n    VARIABLE : id '[' EXPRESION ']' \n              | id\n    \n    BLOQUE : '{' LOOP_ESTATUTO return EXPRESION ';' '}' \n              | '{' LOOP_ESTATUTO '}' \n              | '{' return EXPRESION ';' '}' \n              | '{' '}'\n    \n    LOOP_ESTATUTO : LOOP_ESTATUTO ESTATUTO \n                    | ESTATUTO\n    \n    EXPRESION :  EXPRESION and EXP_R\n                | EXPRESION or EXP_R\n                | EXP_R\n    \n    EXP_R :  EXP_A '>' EXP_A \n            | EXP_A '<' EXP_A \n            | EXP_A equals EXP_A  \n            | EXP_A not_equals EXP_A \n            | EXP_A\n    \n    EXP_A :  EXP_A '+' TERMINO \n            | EXP_A minus TERMINO \n            | TERMINO\n    \n    TERMINO : TERMINO '*' FACTOR \n             | TERMINO '/' FACTOR \n             | FACTOR\n    \n    ESTATUTO : ASIGNACION ';' \n              | CONDICION \n              | WHILE \n              | FOR \n              | LLAMADA ';' \n              | LECTURA ';'  \n              | ESCRITURA ';' \n              | LLAMADA_BI ';'\n    \n    FACTOR : LLAMADA \n            | CTE  \n            | VARIABLE \n            | '(' EXPRESION ')' \n    \n    CTE : cte_i \n         | cte_f \n         | cte_c\n    \n    LLAMADA : id '(' LLAMADA_OPTS ')' \n             | id '(' ')'\n    \n    LLAMADA_OPTS : LLAMADA_OPTS ',' EXPRESION \n                 | EXPRESION \n    \n    ASIGNACION : VARIABLE '=' EXPRESION\n    \n    CONDICION : if '(' EXPRESION ')' then BLOQUE \n               | if '(' EXPRESION ')' then BLOQUE else BLOQUE\n    \n    WHILE : while '(' EXPRESION ')' do BLOQUE\n    \n    FOR : for ASIGNACION to EXPRESION do BLOQUE\n    \n    LECTURA : read '(' LECTURA_OPTS ')'\n    \n    LECTURA_OPTS : LECTURA_OPTS ',' id \n                  | id\n    \n    ESCRITURA : write '(' ESCRITURA_OPTS ')'\n    \n    ESCRITURA_OPTS :   ESCRITURA_OPTS ',' cte_s\n                       | ESCRITURA_OPTS ',' EXPRESION \n                       | cte_s \n                       | EXPRESION\n    \n    LLAMADA_BI :   POINT \n                 | CIRCLE\n                 | PENUP\n                 | PENDOWN \n                 | COLOR \n                 | SIZE \n                 | CLEAR\n    \n    CLEAR : clear '(' ')'\n    \n    POINT : point '(' EXPRESION ',' EXPRESION ')'\n    \n    CIRCLE : circle '(' EXPRESION ')' \n    \n    PENUP : penup '(' ')'\n    \n    PENDOWN : pendown '(' ')'\n    \n    COLOR : color '(' cte_s ')' \n    \n    SIZE : size '(' EXPRESION ')' \n    \n    SEM_GLOBAL_NAME : id\n  \n    SEM_MAIN_NAME : main\n  \n    SEM_FUNC_NAME : id\n  \n  SEM_ADD_FUNC : \n  \n  SEM_ADD_GLOBAL_VARIABLES : \n  "
    
_lr_action_items = {'program':([0,],[2,]),'$end':([1,8,19,51,62,104,189,217,],[0,-2,-1,-6,-36,-34,-35,-33,]),'id':([2,25,26,27,28,30,32,35,46,52,57,60,61,62,63,65,66,67,75,103,104,105,114,118,119,120,121,122,123,124,125,128,129,130,131,132,133,137,143,150,151,152,153,154,155,156,157,158,159,164,189,205,208,210,211,217,226,227,228,231,],[4,-11,-12,-13,34,34,40,40,40,76,99,76,76,-36,-38,-54,-55,-56,127,76,-34,-37,76,-53,-57,-58,-59,-60,76,76,76,76,76,170,76,76,76,76,99,76,76,76,76,76,76,76,76,76,76,76,-35,76,222,76,76,-33,-73,-75,-76,-74,]),';':([3,4,5,38,39,40,42,53,64,68,69,70,71,76,79,80,81,82,83,84,85,93,106,107,108,109,110,111,112,113,115,116,117,148,161,166,176,177,180,190,191,192,193,194,195,196,197,198,199,200,204,206,207,209,212,213,214,229,],[-102,-99,6,45,-10,-30,49,-9,118,119,120,121,122,-32,-85,-86,-87,-88,-89,-90,-91,-29,149,-41,-46,-49,-52,-61,-62,-63,-65,-66,-67,188,-72,-69,-95,-96,-92,-39,-40,-42,-43,-44,-45,-47,-48,-50,-51,-64,-68,-31,-77,-80,-94,-97,-98,-93,]),'var':([6,9,45,49,55,58,95,96,101,102,142,147,],[12,21,-8,-7,12,12,21,12,21,12,21,21,]),'main':([6,7,9,10,20,45,49,62,104,139,144,181,182,185,186,189,215,216,217,],[14,14,-4,-5,-3,-8,-7,-36,-34,-18,-14,-21,-19,-17,-15,-35,-20,-16,-33,]),'char':([6,9,10,12,20,21,45,48,49,50,62,97,104,139,144,181,182,185,186,189,215,216,217,],[15,15,15,27,15,27,-8,27,-7,27,-36,27,-34,-18,-14,-21,-19,-17,-15,-35,-20,-16,-33,]),'float':([6,9,10,12,20,21,45,48,49,50,62,97,104,139,144,181,182,185,186,189,215,216,217,],[16,16,16,26,16,26,-8,26,-7,26,-36,26,-34,-18,-14,-21,-19,-17,-15,-35,-20,-16,-33,]),'int':([6,9,10,12,20,21,45,48,49,50,62,97,104,139,144,181,182,185,186,189,215,216,217,],[17,17,17,25,17,25,-8,25,-7,25,-36,25,-34,-18,-14,-21,-19,-17,-15,-35,-20,-16,-33,]),'void':([6,9,10,20,45,49,62,104,139,144,181,182,185,186,189,215,216,217,],[18,18,18,18,-8,-7,-36,-34,-18,-14,-21,-19,-17,-15,-35,-20,-16,-33,]),'(':([11,14,23,33,34,36,41,43,61,73,74,76,77,78,86,87,88,89,90,91,92,103,114,123,124,125,128,129,131,132,133,137,150,151,152,153,154,155,156,157,158,159,164,205,210,211,],[-102,-100,31,-102,-101,-102,48,50,114,124,125,128,130,131,132,133,134,135,136,137,138,114,114,114,114,114,114,114,114,114,114,114,114,114,114,114,114,114,114,114,114,114,114,114,114,114,]),'module':([13,15,16,17,18,22,],[28,-22,-23,-24,-25,30,]),':':([24,25,26,27,29,],[32,-11,-12,-13,35,]),')':([31,48,50,56,59,76,98,99,107,108,109,110,111,112,113,115,116,117,128,134,135,138,160,162,163,165,166,167,169,170,171,172,173,175,178,179,184,190,191,192,193,194,195,196,197,198,199,200,204,206,221,222,223,224,225,],[37,55,58,96,102,-32,-27,-28,-41,-46,-49,-52,-61,-62,-63,-65,-66,-67,166,176,177,180,200,201,202,204,-69,-71,207,-79,209,-83,-84,212,213,214,-26,-39,-40,-42,-43,-44,-45,-47,-48,-50,-51,-64,-68,-31,-70,-78,-81,-82,229,]),'{':([37,44,45,49,55,58,94,95,96,100,101,102,140,141,142,145,146,147,183,187,218,219,220,230,],[-103,52,-8,-7,-103,-103,52,-103,-103,52,-103,-103,52,52,-103,52,52,-103,52,52,52,52,52,52,]),',':([38,39,40,42,53,56,59,76,93,98,99,107,108,109,110,111,112,113,115,116,117,165,166,167,169,170,171,172,173,174,184,190,191,192,193,194,195,196,197,198,199,200,204,206,221,222,223,224,],[46,-10,-30,46,-9,97,97,-32,-29,-27,-28,-41,-46,-49,-52,-61,-62,-63,-65,-66,-67,205,-69,-71,208,-79,210,-83,-84,211,-26,-39,-40,-42,-43,-44,-45,-47,-48,-50,-51,-64,-68,-31,-70,-78,-81,-82,]),'[':([40,76,127,],[47,129,129,]),'cte_i':([47,61,103,114,123,124,125,128,129,131,132,133,137,150,151,152,153,154,155,156,157,158,159,164,205,210,211,],[54,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,115,]),'return':([52,60,62,63,65,66,67,104,105,118,119,120,121,122,189,217,226,227,228,231,],[61,103,-36,-38,-54,-55,-56,-34,-37,-53,-57,-58,-59,-60,-35,-33,-73,-75,-76,-74,]),'}':([52,60,62,63,65,66,67,104,105,118,119,120,121,122,149,188,189,217,226,227,228,231,],[62,104,-36,-38,-54,-55,-56,-34,-37,-53,-57,-58,-59,-60,189,217,-35,-33,-73,-75,-76,-74,]),'if':([52,60,62,63,65,66,67,104,105,118,119,120,121,122,189,217,226,227,228,231,],[73,73,-36,-38,-54,-55,-56,-34,-37,-53,-57,-58,-59,-60,-35,-33,-73,-75,-76,-74,]),'while':([52,60,62,63,65,66,67,104,105,118,119,120,121,122,189,217,226,227,228,231,],[74,74,-36,-38,-54,-55,-56,-34,-37,-53,-57,-58,-59,-60,-35,-33,-73,-75,-76,-74,]),'for':([52,60,62,63,65,66,67,104,105,118,119,120,121,122,189,217,226,227,228,231,],[75,75,-36,-38,-54,-55,-56,-34,-37,-53,-57,-58,-59,-60,-35,-33,-73,-75,-76,-74,]),'read':([52,60,62,63,65,66,67,104,105,118,119,120,121,122,189,217,226,227,228,231,],[77,77,-36,-38,-54,-55,-56,-34,-37,-53,-57,-58,-59,-60,-35,-33,-73,-75,-76,-74,]),'write':([52,60,62,63,65,66,67,104,105,118,119,120,121,122,189,217,226,227,228,231,],[78,78,-36,-38,-54,-55,-56,-34,-37,-53,-57,-58,-59,-60,-35,-33,-73,-75,-76,-74,]),'point':([52,60,62,63,65,66,67,104,105,118,119,120,121,122,189,217,226,227,228,231,],[86,86,-36,-38,-54,-55,-56,-34,-37,-53,-57,-58,-59,-60,-35,-33,-73,-75,-76,-74,]),'circle':([52,60,62,63,65,66,67,104,105,118,119,120,121,122,189,217,226,227,228,231,],[87,87,-36,-38,-54,-55,-56,-34,-37,-53,-57,-58,-59,-60,-35,-33,-73,-75,-76,-74,]),'penup':([52,60,62,63,65,66,67,104,105,118,119,120,121,122,189,217,226,227,228,231,],[88,88,-36,-38,-54,-55,-56,-34,-37,-53,-57,-58,-59,-60,-35,-33,-73,-75,-76,-74,]),'pendown':([52,60,62,63,65,66,67,104,105,118,119,120,121,122,189,217,226,227,228,231,],[89,89,-36,-38,-54,-55,-56,-34,-37,-53,-57,-58,-59,-60,-35,-33,-73,-75,-76,-74,]),'color':([52,60,62,63,65,66,67,104,105,118,119,120,121,122,189,217,226,227,228,231,],[90,90,-36,-38,-54,-55,-56,-34,-37,-53,-57,-58,-59,-60,-35,-33,-73,-75,-76,-74,]),'size':([52,60,62,63,65,66,67,104,105,118,119,120,121,122,189,217,226,227,228,231,],[91,91,-36,-38,-54,-55,-56,-34,-37,-53,-57,-58,-59,-60,-35,-33,-73,-75,-76,-74,]),'clear':([52,60,62,63,65,66,67,104,105,118,119,120,121,122,189,217,226,227,228,231,],[92,92,-36,-38,-54,-55,-56,-34,-37,-53,-57,-58,-59,-60,-35,-33,-73,-75,-76,-74,]),']':([54,76,107,108,109,110,111,112,113,115,116,117,166,168,190,191,192,193,194,195,196,197,198,199,200,204,206,],[93,-32,-41,-46,-49,-52,-61,-62,-63,-65,-66,-67,-69,206,-39,-40,-42,-43,-44,-45,-47,-48,-50,-51,-64,-68,-31,]),'cte_f':([61,103,114,123,124,125,128,129,131,132,133,137,150,151,152,153,154,155,156,157,158,159,164,205,210,211,],[116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,]),'cte_c':([61,103,114,123,124,125,128,129,131,132,133,137,150,151,152,153,154,155,156,157,158,159,164,205,210,211,],[117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,]),'else':([62,104,189,217,226,],[-36,-34,-35,-33,230,]),'=':([72,76,127,206,],[123,-32,-32,-31,]),'*':([76,109,110,111,112,113,115,116,117,166,196,197,198,199,200,204,206,],[-32,158,-52,-61,-62,-63,-65,-66,-67,-69,158,158,-50,-51,-64,-68,-31,]),'/':([76,109,110,111,112,113,115,116,117,166,196,197,198,199,200,204,206,],[-32,159,-52,-61,-62,-63,-65,-66,-67,-69,159,159,-50,-51,-64,-68,-31,]),'>':([76,108,109,110,111,112,113,115,116,117,166,196,197,198,199,200,204,206,],[-32,152,-49,-52,-61,-62,-63,-65,-66,-67,-69,-47,-48,-50,-51,-64,-68,-31,]),'<':([76,108,109,110,111,112,113,115,116,117,166,196,197,198,199,200,204,206,],[-32,153,-49,-52,-61,-62,-63,-65,-66,-67,-69,-47,-48,-50,-51,-64,-68,-31,]),'equals':([76,108,109,110,111,112,113,115,116,117,166,196,197,198,199,200,204,206,],[-32,154,-49,-52,-61,-62,-63,-65,-66,-67,-69,-47,-48,-50,-51,-64,-68,-31,]),'not_equals':([76,108,109,110,111,112,113,115,116,117,166,196,197,198,199,200,204,206,],[-32,155,-49,-52,-61,-62,-63,-65,-66,-67,-69,-47,-48,-50,-51,-64,-68,-31,]),'+':([76,108,109,110,111,112,113,115,116,117,166,192,193,194,195,196,197,198,199,200,204,206,],[-32,156,-49,-52,-61,-62,-63,-65,-66,-67,-69,156,156,156,156,-47,-48,-50,-51,-64,-68,-31,]),'minus':([76,108,109,110,111,112,113,115,116,117,166,192,193,194,195,196,197,198,199,200,204,206,],[-32,157,-49,-52,-61,-62,-63,-65,-66,-67,-69,157,157,157,157,-47,-48,-50,-51,-64,-68,-31,]),'and':([76,106,107,108,109,110,111,112,113,115,116,117,148,160,161,162,163,166,167,168,173,174,175,179,190,191,192,193,194,195,196,197,198,199,200,203,204,206,221,224,225,],[-32,150,-41,-46,-49,-52,-61,-62,-63,-65,-66,-67,150,150,150,150,150,-69,150,150,150,150,150,150,-39,-40,-42,-43,-44,-45,-47,-48,-50,-51,-64,150,-68,-31,150,150,150,]),'or':([76,106,107,108,109,110,111,112,113,115,116,117,148,160,161,162,163,166,167,168,173,174,175,179,190,191,192,193,194,195,196,197,198,199,200,203,204,206,221,224,225,],[-32,151,-41,-46,-49,-52,-61,-62,-63,-65,-66,-67,151,151,151,151,151,-69,151,151,151,151,151,151,-39,-40,-42,-43,-44,-45,-47,-48,-50,-51,-64,151,-68,-31,151,151,151,]),'to':([76,107,108,109,110,111,112,113,115,116,117,126,161,166,190,191,192,193,194,195,196,197,198,199,200,204,206,],[-32,-41,-46,-49,-52,-61,-62,-63,-65,-66,-67,164,-72,-69,-39,-40,-42,-43,-44,-45,-47,-48,-50,-51,-64,-68,-31,]),'do':([76,107,108,109,110,111,112,113,115,116,117,166,190,191,192,193,194,195,196,197,198,199,200,202,203,204,206,],[-32,-41,-46,-49,-52,-61,-62,-63,-65,-66,-67,-69,-39,-40,-42,-43,-44,-45,-47,-48,-50,-51,-64,219,220,-68,-31,]),'cte_s':([131,136,210,],[172,178,223,]),'then':([201,],[218,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'PROGRAMA':([0,],[1,]),'SEM_GLOBAL_NAME':([2,],[3,]),'SEM_ADD_FUNC':([3,11,33,36,],[5,23,41,43,]),'PROGRAMA_OPTS':([6,],[7,]),'PRINCIPAL':([6,7,],[8,19,]),'DEC_V':([6,55,58,96,102,],[9,95,101,142,147,]),'FUNCS':([6,9,],[10,20,]),'SEM_MAIN_NAME':([6,7,],[11,11,]),'FUNC_TYPES':([6,9,10,20,],[13,13,22,22,]),'TIPO_SIMPLE':([12,21,48,50,97,],[24,29,57,57,143,]),'SEM_FUNC_NAME':([28,30,],[33,36,]),'LISTA_VAR':([32,35,],[38,42,]),'VARIABLE_FIX':([32,35,46,],[39,39,53,]),'SEM_ADD_GLOBAL_VARIABLES':([37,55,58,95,96,101,102,142,147,],[44,94,100,140,141,145,146,183,187,]),'BLOQUE':([44,94,100,140,141,145,146,183,187,218,219,220,230,],[51,139,144,181,182,185,186,215,216,226,227,228,231,]),'PARAMS':([48,50,],[56,59,]),'LOOP_ESTATUTO':([52,],[60,]),'ESTATUTO':([52,60,],[63,105,]),'ASIGNACION':([52,60,75,],[64,64,126,]),'CONDICION':([52,60,],[65,65,]),'WHILE':([52,60,],[66,66,]),'FOR':([52,60,],[67,67,]),'LLAMADA':([52,60,61,103,114,123,124,125,128,129,131,132,133,137,150,151,152,153,154,155,156,157,158,159,164,205,210,211,],[68,68,111,111,111,111,111,111,111,111,111,111,111,111,111,111,111,111,111,111,111,111,111,111,111,111,111,111,]),'LECTURA':([52,60,],[69,69,]),'ESCRITURA':([52,60,],[70,70,]),'LLAMADA_BI':([52,60,],[71,71,]),'VARIABLE':([52,60,61,75,103,114,123,124,125,128,129,131,132,133,137,150,151,152,153,154,155,156,157,158,159,164,205,210,211,],[72,72,113,72,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,]),'POINT':([52,60,],[79,79,]),'CIRCLE':([52,60,],[80,80,]),'PENUP':([52,60,],[81,81,]),'PENDOWN':([52,60,],[82,82,]),'COLOR':([52,60,],[83,83,]),'SIZE':([52,60,],[84,84,]),'CLEAR':([52,60,],[85,85,]),'PARAM_NAME':([57,143,],[98,184,]),'EXPRESION':([61,103,114,123,124,125,128,129,131,132,133,137,164,205,210,211,],[106,148,160,161,162,163,167,168,173,174,175,179,203,221,224,225,]),'EXP_R':([61,103,114,123,124,125,128,129,131,132,133,137,150,151,164,205,210,211,],[107,107,107,107,107,107,107,107,107,107,107,107,190,191,107,107,107,107,]),'EXP_A':([61,103,114,123,124,125,128,129,131,132,133,137,150,151,152,153,154,155,164,205,210,211,],[108,108,108,108,108,108,108,108,108,108,108,108,108,108,192,193,194,195,108,108,108,108,]),'TERMINO':([61,103,114,123,124,125,128,129,131,132,133,137,150,151,152,153,154,155,156,157,164,205,210,211,],[109,109,109,109,109,109,109,109,109,109,109,109,109,109,109,109,109,109,196,197,109,109,109,109,]),'FACTOR':([61,103,114,123,124,125,128,129,131,132,133,137,150,151,152,153,154,155,156,157,158,159,164,205,210,211,],[110,110,110,110,110,110,110,110,110,110,110,110,110,110,110,110,110,110,110,110,198,199,110,110,110,110,]),'CTE':([61,103,114,123,124,125,128,129,131,132,133,137,150,151,152,153,154,155,156,157,158,159,164,205,210,211,],[112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,]),'LLAMADA_OPTS':([128,],[165,]),'LECTURA_OPTS':([130,],[169,]),'ESCRITURA_OPTS':([131,],[171,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> PROGRAMA","S'",1,None,None,None),
  ('PROGRAMA -> program SEM_GLOBAL_NAME SEM_ADD_FUNC ; PROGRAMA_OPTS PRINCIPAL','PROGRAMA',6,'p_programa','parser.py',33),
  ('PROGRAMA -> program SEM_GLOBAL_NAME SEM_ADD_FUNC ; PRINCIPAL','PROGRAMA',5,'p_programa','parser.py',34),
  ('PROGRAMA_OPTS -> DEC_V FUNCS','PROGRAMA_OPTS',2,'p_programa_opts','parser.py',43),
  ('PROGRAMA_OPTS -> DEC_V','PROGRAMA_OPTS',1,'p_programa_opts','parser.py',44),
  ('PROGRAMA_OPTS -> FUNCS','PROGRAMA_OPTS',1,'p_programa_opts','parser.py',45),
  ('PRINCIPAL -> SEM_MAIN_NAME SEM_ADD_FUNC ( ) SEM_ADD_GLOBAL_VARIABLES BLOQUE','PRINCIPAL',6,'p_principal','parser.py',51),
  ('DEC_V -> DEC_V var TIPO_SIMPLE : LISTA_VAR ;','DEC_V',6,'p_dec_v','parser.py',56),
  ('DEC_V -> var TIPO_SIMPLE : LISTA_VAR ;','DEC_V',5,'p_dec_v','parser.py',57),
  ('LISTA_VAR -> LISTA_VAR , VARIABLE_FIX','LISTA_VAR',3,'p_lista_var','parser.py',81),
  ('LISTA_VAR -> VARIABLE_FIX','LISTA_VAR',1,'p_lista_var','parser.py',82),
  ('TIPO_SIMPLE -> int','TIPO_SIMPLE',1,'p_tipo_simple','parser.py',87),
  ('TIPO_SIMPLE -> float','TIPO_SIMPLE',1,'p_tipo_simple','parser.py',88),
  ('TIPO_SIMPLE -> char','TIPO_SIMPLE',1,'p_tipo_simple','parser.py',89),
  ('FUNCS -> FUNCS FUNC_TYPES module SEM_FUNC_NAME SEM_ADD_FUNC ( ) SEM_ADD_GLOBAL_VARIABLES BLOQUE','FUNCS',9,'p_funcs','parser.py',97),
  ('FUNCS -> FUNCS FUNC_TYPES module SEM_FUNC_NAME SEM_ADD_FUNC ( PARAMS ) SEM_ADD_GLOBAL_VARIABLES BLOQUE','FUNCS',10,'p_funcs','parser.py',98),
  ('FUNCS -> FUNCS FUNC_TYPES module SEM_FUNC_NAME SEM_ADD_FUNC ( PARAMS ) DEC_V SEM_ADD_GLOBAL_VARIABLES BLOQUE','FUNCS',11,'p_funcs','parser.py',99),
  ('FUNCS -> FUNCS FUNC_TYPES module SEM_FUNC_NAME SEM_ADD_FUNC ( ) DEC_V SEM_ADD_GLOBAL_VARIABLES BLOQUE','FUNCS',10,'p_funcs','parser.py',100),
  ('FUNCS -> FUNC_TYPES module SEM_FUNC_NAME SEM_ADD_FUNC ( ) SEM_ADD_GLOBAL_VARIABLES BLOQUE','FUNCS',8,'p_funcs','parser.py',101),
  ('FUNCS -> FUNC_TYPES module SEM_FUNC_NAME SEM_ADD_FUNC ( PARAMS ) SEM_ADD_GLOBAL_VARIABLES BLOQUE','FUNCS',9,'p_funcs','parser.py',102),
  ('FUNCS -> FUNC_TYPES module SEM_FUNC_NAME SEM_ADD_FUNC ( PARAMS ) DEC_V SEM_ADD_GLOBAL_VARIABLES BLOQUE','FUNCS',10,'p_funcs','parser.py',103),
  ('FUNCS -> FUNC_TYPES module SEM_FUNC_NAME SEM_ADD_FUNC ( ) DEC_V SEM_ADD_GLOBAL_VARIABLES BLOQUE','FUNCS',9,'p_funcs','parser.py',104),
  ('FUNC_TYPES -> char','FUNC_TYPES',1,'p_func_types','parser.py',112),
  ('FUNC_TYPES -> float','FUNC_TYPES',1,'p_func_types','parser.py',113),
  ('FUNC_TYPES -> int','FUNC_TYPES',1,'p_func_types','parser.py',114),
  ('FUNC_TYPES -> void','FUNC_TYPES',1,'p_func_types','parser.py',115),
  ('PARAMS -> PARAMS , TIPO_SIMPLE PARAM_NAME','PARAMS',4,'p_params','parser.py',123),
  ('PARAMS -> TIPO_SIMPLE PARAM_NAME','PARAMS',2,'p_params','parser.py',124),
  ('PARAM_NAME -> id','PARAM_NAME',1,'p_param_name','parser.py',129),
  ('VARIABLE_FIX -> id [ cte_i ]','VARIABLE_FIX',4,'p_variable_fix','parser.py',137),
  ('VARIABLE_FIX -> id','VARIABLE_FIX',1,'p_variable_fix','parser.py',138),
  ('VARIABLE -> id [ EXPRESION ]','VARIABLE',4,'p_variable','parser.py',151),
  ('VARIABLE -> id','VARIABLE',1,'p_variable','parser.py',152),
  ('BLOQUE -> { LOOP_ESTATUTO return EXPRESION ; }','BLOQUE',6,'p_bloque','parser.py',157),
  ('BLOQUE -> { LOOP_ESTATUTO }','BLOQUE',3,'p_bloque','parser.py',158),
  ('BLOQUE -> { return EXPRESION ; }','BLOQUE',5,'p_bloque','parser.py',159),
  ('BLOQUE -> { }','BLOQUE',2,'p_bloque','parser.py',160),
  ('LOOP_ESTATUTO -> LOOP_ESTATUTO ESTATUTO','LOOP_ESTATUTO',2,'p_loop_estatuto','parser.py',165),
  ('LOOP_ESTATUTO -> ESTATUTO','LOOP_ESTATUTO',1,'p_loop_estatuto','parser.py',166),
  ('EXPRESION -> EXPRESION and EXP_R','EXPRESION',3,'p_expresion','parser.py',171),
  ('EXPRESION -> EXPRESION or EXP_R','EXPRESION',3,'p_expresion','parser.py',172),
  ('EXPRESION -> EXP_R','EXPRESION',1,'p_expresion','parser.py',173),
  ('EXP_R -> EXP_A > EXP_A','EXP_R',3,'p_exp_r','parser.py',178),
  ('EXP_R -> EXP_A < EXP_A','EXP_R',3,'p_exp_r','parser.py',179),
  ('EXP_R -> EXP_A equals EXP_A','EXP_R',3,'p_exp_r','parser.py',180),
  ('EXP_R -> EXP_A not_equals EXP_A','EXP_R',3,'p_exp_r','parser.py',181),
  ('EXP_R -> EXP_A','EXP_R',1,'p_exp_r','parser.py',182),
  ('EXP_A -> EXP_A + TERMINO','EXP_A',3,'p_exp_a','parser.py',187),
  ('EXP_A -> EXP_A minus TERMINO','EXP_A',3,'p_exp_a','parser.py',188),
  ('EXP_A -> TERMINO','EXP_A',1,'p_exp_a','parser.py',189),
  ('TERMINO -> TERMINO * FACTOR','TERMINO',3,'p_termino','parser.py',194),
  ('TERMINO -> TERMINO / FACTOR','TERMINO',3,'p_termino','parser.py',195),
  ('TERMINO -> FACTOR','TERMINO',1,'p_termino','parser.py',196),
  ('ESTATUTO -> ASIGNACION ;','ESTATUTO',2,'p_estatuto','parser.py',201),
  ('ESTATUTO -> CONDICION','ESTATUTO',1,'p_estatuto','parser.py',202),
  ('ESTATUTO -> WHILE','ESTATUTO',1,'p_estatuto','parser.py',203),
  ('ESTATUTO -> FOR','ESTATUTO',1,'p_estatuto','parser.py',204),
  ('ESTATUTO -> LLAMADA ;','ESTATUTO',2,'p_estatuto','parser.py',205),
  ('ESTATUTO -> LECTURA ;','ESTATUTO',2,'p_estatuto','parser.py',206),
  ('ESTATUTO -> ESCRITURA ;','ESTATUTO',2,'p_estatuto','parser.py',207),
  ('ESTATUTO -> LLAMADA_BI ;','ESTATUTO',2,'p_estatuto','parser.py',208),
  ('FACTOR -> LLAMADA','FACTOR',1,'p_factor','parser.py',213),
  ('FACTOR -> CTE','FACTOR',1,'p_factor','parser.py',214),
  ('FACTOR -> VARIABLE','FACTOR',1,'p_factor','parser.py',215),
  ('FACTOR -> ( EXPRESION )','FACTOR',3,'p_factor','parser.py',216),
  ('CTE -> cte_i','CTE',1,'p_cte','parser.py',221),
  ('CTE -> cte_f','CTE',1,'p_cte','parser.py',222),
  ('CTE -> cte_c','CTE',1,'p_cte','parser.py',223),
  ('LLAMADA -> id ( LLAMADA_OPTS )','LLAMADA',4,'p_llamada','parser.py',228),
  ('LLAMADA -> id ( )','LLAMADA',3,'p_llamada','parser.py',229),
  ('LLAMADA_OPTS -> LLAMADA_OPTS , EXPRESION','LLAMADA_OPTS',3,'p_llamada_opts','parser.py',234),
  ('LLAMADA_OPTS -> EXPRESION','LLAMADA_OPTS',1,'p_llamada_opts','parser.py',235),
  ('ASIGNACION -> VARIABLE = EXPRESION','ASIGNACION',3,'p_asignacion','parser.py',240),
  ('CONDICION -> if ( EXPRESION ) then BLOQUE','CONDICION',6,'p_condicion','parser.py',245),
  ('CONDICION -> if ( EXPRESION ) then BLOQUE else BLOQUE','CONDICION',8,'p_condicion','parser.py',246),
  ('WHILE -> while ( EXPRESION ) do BLOQUE','WHILE',6,'p_while','parser.py',251),
  ('FOR -> for ASIGNACION to EXPRESION do BLOQUE','FOR',6,'p_for','parser.py',256),
  ('LECTURA -> read ( LECTURA_OPTS )','LECTURA',4,'p_lectura','parser.py',261),
  ('LECTURA_OPTS -> LECTURA_OPTS , id','LECTURA_OPTS',3,'p_lectura_opts','parser.py',266),
  ('LECTURA_OPTS -> id','LECTURA_OPTS',1,'p_lectura_opts','parser.py',267),
  ('ESCRITURA -> write ( ESCRITURA_OPTS )','ESCRITURA',4,'p_escritura','parser.py',272),
  ('ESCRITURA_OPTS -> ESCRITURA_OPTS , cte_s','ESCRITURA_OPTS',3,'p_escritura_opts','parser.py',277),
  ('ESCRITURA_OPTS -> ESCRITURA_OPTS , EXPRESION','ESCRITURA_OPTS',3,'p_escritura_opts','parser.py',278),
  ('ESCRITURA_OPTS -> cte_s','ESCRITURA_OPTS',1,'p_escritura_opts','parser.py',279),
  ('ESCRITURA_OPTS -> EXPRESION','ESCRITURA_OPTS',1,'p_escritura_opts','parser.py',280),
  ('LLAMADA_BI -> POINT','LLAMADA_BI',1,'p_llamada_bi','parser.py',285),
  ('LLAMADA_BI -> CIRCLE','LLAMADA_BI',1,'p_llamada_bi','parser.py',286),
  ('LLAMADA_BI -> PENUP','LLAMADA_BI',1,'p_llamada_bi','parser.py',287),
  ('LLAMADA_BI -> PENDOWN','LLAMADA_BI',1,'p_llamada_bi','parser.py',288),
  ('LLAMADA_BI -> COLOR','LLAMADA_BI',1,'p_llamada_bi','parser.py',289),
  ('LLAMADA_BI -> SIZE','LLAMADA_BI',1,'p_llamada_bi','parser.py',290),
  ('LLAMADA_BI -> CLEAR','LLAMADA_BI',1,'p_llamada_bi','parser.py',291),
  ('CLEAR -> clear ( )','CLEAR',3,'p_clear','parser.py',296),
  ('POINT -> point ( EXPRESION , EXPRESION )','POINT',6,'p_point','parser.py',301),
  ('CIRCLE -> circle ( EXPRESION )','CIRCLE',4,'p_circle','parser.py',306),
  ('PENUP -> penup ( )','PENUP',3,'p_penup','parser.py',311),
  ('PENDOWN -> pendown ( )','PENDOWN',3,'p_pendown','parser.py',316),
  ('COLOR -> color ( cte_s )','COLOR',4,'p_color','parser.py',321),
  ('SIZE -> size ( EXPRESION )','SIZE',4,'p_size','parser.py',326),
  ('SEM_GLOBAL_NAME -> id','SEM_GLOBAL_NAME',1,'p_sem_global_name','parser.py',347),
  ('SEM_MAIN_NAME -> main','SEM_MAIN_NAME',1,'p_sem_main_name','parser.py',356),
  ('SEM_FUNC_NAME -> id','SEM_FUNC_NAME',1,'p_sem_func_name','parser.py',367),
  ('SEM_ADD_FUNC -> <empty>','SEM_ADD_FUNC',0,'p_sem_add_func','parser.py',375),
  ('SEM_ADD_GLOBAL_VARIABLES -> <empty>','SEM_ADD_GLOBAL_VARIABLES',0,'p_sem_add_global_variables','parser.py',382),
]
