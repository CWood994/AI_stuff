/*
 
 Author: Connor Wood
 
*/

#include <iostream>
#include <set>
#include <fstream>
#include <unordered_map>
#include <stdlib.h>
#include <limits.h>
#include <vector>

using namespace std;

enum token{
    PROGRAM, BEGIN, INT, ASSIGN, ENDOFFILE, SPACE, OPERATOR, PLUS, MINUS , MULT, END, ID, IF,THEN,ELSE,ENDIF, WHILE, INPUT, OUTPUT, CONST, SEMICOLON, FACTOR, LEFTPARAN, RIGHTPARAN, ENDWHILE, NOT, OR, EQUALS, LESSTHAN, LESSTHANEQUAL, COMMA, FUN, CALL, RETURN
};

string tokenNames[]={"PROGRAM", "BEGIN","INT", "ASSIGN", "ENDOFFILE", "SPACE", "OPERATOR", "PLUS", "MINUS" , "MULT", "END", "ID", "IF","THEN","ELSE","ENDIF", "WHILE", "INPUT", "OUTPUT", "CONST", "SEMICOLON", "FACTOR", "LEFTPARAN", "RIGHTPARAN", "ENDWHILE", "NOT", "OR", "EQUALS", "LESSTHAN", "LESSTHANEQUAL", "COMMA", "FUN", "CALL", "RETURN"};


/************ Class Pre-Declarations ************/
class Factor;
class Expr;
class Output;
class Input;
class IfThenElse;
class Assign;
class Decl;
class StmtSeq;
class DeclSeq;
class Stmt;
class Loop;

/************ Class Pre-Declarations ************/
class Program{
    DeclSeq* ds; StmtSeq* ss;
    public:
    
    Program();
    void parse();
    void exec();
};

class DeclSeq{
    DeclSeq* ds; Decl* d;
public:
    
    DeclSeq();
    void parse();
    void exec();
};

class StmtSeq{
    Stmt* s; StmtSeq* ss;
public:
    
    StmtSeq();
    void parse();
    void exec();
};

class Stmt{
     Assign* s1; IfThenElse* s2; Loop* s3; Input* s4; Output* s5;
public:
    int altNo;
    Stmt();
    void parse();
    void exec();
};

class Decl{ //no id list, put all into hashmap
    
public:
    
    Decl();
    void parse();
    void exec();
};

class Assign{
    string id; Expr* expr;
public:
    
    Assign();
    void parse();
    void exec();
};

class Cmpr{
    Expr* e1; Expr* e2; token t;
public:
    
    Cmpr();
    void parse();
    int exec(); // 1 true, 0 false
};

class Cond{
    int altNo; Cmpr* cmpr; Cond* cond; //altNo: 1,2,3
public:
    
    Cond();
    void parse();
    int exec();
};

class Input{
    string id;
public:
    
    Input();
    void parse();
    void exec();
};

class IfThenElse{
    Cond* c; StmtSeq* ss; StmtSeq* ssElse;
public:
    
    IfThenElse();
    void parse();
    void exec();
};

class Loop{
    Cond* c; StmtSeq* ss;
public:
    
    Loop();
    void parse();
    void exec();
};


class Term{
    Factor* factor; Term* term;
    public:
    
    Term();
    void parse();
    int exec();
};

class Expr{
    Term* term; token op; Expr* expr;
    public:
    
    Expr();
    void parse();
    int exec();
};

class ExprList{
    Expr* expr; ExprList* el;
public:
    
    ExprList();
    void parse();
    vector<int> exec();
};

class Factor{
    int value; string id; Expr* expr; int isCALL; ExprList* el; // 1 if is call
    public:
    
    Factor();
    void parse();
    int exec();
};

class Function{
public:
    unordered_map<string, int> localIDmap; string id; StmtSeq* ss; Expr* returnValue; vector<string> params;

    
    Function();
    void parse();
    int exec(vector<int> formalParams);
    Function* clone();
};

class Scanner{
    string content; int pos; ifstream infile; token curToken; string curID; int curValue;
    public:
    Scanner(string filename);
    
    token currentToken();
    void nextToken();
    string getID();
    int getValue();
    
    void match(token t);
    bool check(token t);
    void close();
};

class Output{
    Expr* expr;
    public:
    
    Output();
    void parse();
    void exec();
};

/************ Implementations ************/

unordered_map<string, int> IDmap;
unordered_map<string, Function*> FUNmap;
Scanner* scanner;


/**  Scanner **/
    Scanner::Scanner(string filename){
        infile.open (filename); string buffer = ""; content = ""; pos = 0;
        
        while(!infile.eof())
        {
            getline(infile,buffer);
            content += " " + buffer;
        }
        
        nextToken();
    }

    token Scanner::currentToken(){
        return curToken;
    }

    void Scanner::nextToken(){
        curToken = ENDOFFILE;
        while(pos<content.length()){
            if(isspace(static_cast<unsigned char>(content[pos]))){
                curToken = SPACE;
                pos++;
            }else if(content.substr(pos, 6) == "output"){
                pos+= 6;
                curToken = OUTPUT; break;
            }else if(content.substr(pos, 3) == "fun"){
                pos+= 3;
                curToken = FUN; break;
            }else if(content.substr(pos, 4) == "call"){
                pos+= 4;
                curToken = CALL; break;
            }else if(content.substr(pos, 6) == "return"){
                pos+= 6;
                curToken = RETURN; break;
            }else if(content.substr(pos, 7) == "program"){
                pos+= 7;
                curToken = PROGRAM; break;
            }else if(content.substr(pos, 5) == "begin"){
                    pos+= 5;
                    curToken = BEGIN; break;
            }else if(content.substr(pos, 8) == "endwhile"){
                pos+= 8;
                curToken = ENDWHILE; break;
            }else if(content.substr(pos, 5) == "endif"){
                pos+= 5;
                curToken = ENDIF; break;
            }else if(content.substr(pos, 3) == "end"){
                pos+= 3;
                curToken = END; break;
            }else if(content.substr(pos, 3) == "int"){
                pos+= 3;
                curToken = INT; break;
            }else if(content.substr(pos, 2) == "if"){
                pos+= 2;
                curToken = IF; break;
            }else if(content.substr(pos, 4) == "then"){
                pos+= 4;
                curToken = THEN; break;

            }else if(content.substr(pos, 4) == "else"){
                pos+= 4;
                curToken = ELSE; break;
            }else if(content.substr(pos, 5) == "while"){
                pos+= 5;
                curToken = WHILE; break;
            }else if(content.substr(pos, 5) == "input"){
                pos+= 5;
                curToken = INPUT; break;
            }else if(content.substr(pos, 1) == "!"){
                pos+= 1;
                curToken = NOT; break;
            }else if(content.substr(pos, 2) == "or"){
                pos+= 2;
                curToken = OR; break;
            }else if(content.substr(pos, 1) == "="){
                pos+= 1;
                curToken = EQUALS; break;
            }else if(content.substr(pos, 2) == "<="){
                pos+= 2;
                curToken = LESSTHANEQUAL; break;
            }else if(content.substr(pos, 1) == "<"){
                pos+= 1;
                curToken = LESSTHAN; break;
            }else if(content.substr(pos, 1) == ";"){
                pos+= 1;
                curToken = SEMICOLON;break;
            }else if(content.substr(pos, 1) == "+"){
                pos+= 1;
                curToken = PLUS;break;
            }else if(content.substr(pos, 1) == "-"){
                pos+= 1;
                curToken = MINUS;break;
            }else if(content.substr(pos, 1) == "*"){
                pos+= 1;
                curToken = MULT;break;
            }else if(content.substr(pos, 1) == "("){
                pos+= 1;
                curToken = LEFTPARAN;break;
            }else if(content.substr(pos, 1) == ")"){
                pos+= 1;
                curToken = RIGHTPARAN;break;
            }else if(content.substr(pos, 1) == ","){
                pos+= 1;
                curToken = COMMA;break;
            }else if(content.substr(pos,2)==":="){
                pos+=2;
                curToken = ASSIGN;break;
            }else if(isalnum(content[pos])){ //const or id
                int length = 0;
                curToken = CONST;
                char temp = content[pos+length];
                
                while(!isspace(static_cast<unsigned char>(temp)) && temp!=';'&& temp!='+'&& temp!='-'&& temp!='*'&& temp!='('&& temp!=')'&& temp!=','&& temp!='<'&& temp!='='&& temp!=':' && pos<content.length() ){

                    if(!isdigit(content[pos+length])){
                        curToken = ID;
                    }
                    
                    temp = content[pos + ++length];
                }
                
                if(curToken==CONST){
                    curValue = atoi(content.substr(pos,length).c_str());
                }else{
                    curID = content.substr(pos,length);
                    if(IDmap.find(curID) != IDmap.end()){
                        curValue = IDmap.find(getID())->second;
                    }
                }
                
                pos+=length;
                break;

            }else{
                cout << "ERROR: Unexpected token starting with " << content[pos] << "\n";
                exit(0);
            }
        }
    }

    string Scanner::getID(){
        return curID;
    }

    int Scanner::getValue(){
        if(curToken==ID && IDmap.find(curID)== IDmap.end()){
            cout << "ERROR: Undeclared variable: " << getID() << "\n";
            exit(0);
        }
        return curValue;
    }

    //match and exit if error
    void Scanner::match(token t){
        if(currentToken()!=t){
            cout << "ERROR: Expected " << tokenNames[t] << " Recieved " << tokenNames[currentToken()] << "\n";
            exit(0);
        }
        nextToken();
    }

    bool Scanner::check(token t){
        return currentToken()==t;
    }

    void Scanner::close(){
        infile.close();
        if(curToken != ENDOFFILE && curToken != SPACE){
            cout << "ERROR: Unexpected token at end of file: " << tokenNames[curToken] << "\n";
            exit(0);
        }
    }

/** Term **/

    Term::Term(){
        factor = NULL; term = NULL;
    }
    
    void Term::parse(){
        factor = new Factor();
        factor->parse();
        
        if(scanner->check(MULT)){
            scanner->nextToken();
            
            term = new Term();
            term->parse();
        }
    }
    
    int Term::exec(){
        if(term != NULL){
            return (factor->exec() * term->exec());
        }else{
            return factor->exec();
        }
    }


/** EXPR **/
    
    Expr::Expr(){
        term = NULL; op = OPERATOR; expr = NULL;
    }
    
    void Expr::parse(){
        term = new Term();
        term->parse();
        if(scanner->check(PLUS) || scanner->check(MINUS)){
            op = scanner->check(PLUS) ? PLUS : MINUS;
            scanner->nextToken();
            
            expr = new Expr();
            expr->parse();
        }
    }
    
    int Expr::exec(){
        if(op == OPERATOR){
            return term->exec();
        }else if(op == PLUS){
            return (term->exec() + expr->exec());
        }else{
            return (term->exec() - expr->exec());
        }
    }


/** Factor **/

    Factor::Factor(){
        expr = NULL; el = NULL; id="";isCALL=0;
    }

    void Factor::parse(){
        if(scanner->check(CONST)){
            value = scanner->getValue();
            scanner->nextToken();
        }else if(scanner->check(ID)){
            if(IDmap.find(scanner->getID())== IDmap.end()){
                cout << "ERROR: Undeclared variable: " << scanner->getID() << "\n";
                exit(0);
            }
            id = scanner->getID();
            scanner->nextToken();
        }else if(scanner->check(CALL)){
            isCALL=1;
            scanner->match(CALL);
            if(!scanner->check(ID)){
                cout << "ERROR: Expected ID, recieved " <<  scanner->currentToken() << "\n";
                exit(0);
            }
            id = scanner->getID();
            scanner->nextToken();
            
            scanner->match(LEFTPARAN);
            el = new ExprList();
            el->parse();
            scanner->match(RIGHTPARAN);
        }else{
            scanner->match(LEFTPARAN);
            
            expr=new Expr();
            expr->parse();
            
            scanner->match(RIGHTPARAN);
        }
    }

    int Factor::exec(){
        if(expr != NULL){
            value = expr->exec();
        }else if(isCALL == 1){
            vector<int> temp = el->exec();
            value = FUNmap[id]->clone()->exec(temp);
        }else if(id!=""){
            value = IDmap[id];
            if(value==INT_MIN){
                cout << "ERROR: Undefined Variable: " << id <<"\n";
                exit(0);
            }
        }
        return value;
    }

/** Output **/

    Output::Output(){
        expr = NULL;
    }
    
    void Output::parse(){
        scanner->match(OUTPUT);

        expr = new Expr();
        expr->parse();

        scanner->match(SEMICOLON);
    }
    
    void Output::exec(){
        cout << expr->exec() << "\n";
    }

/** Statment **/


    Stmt::Stmt(){
        altNo = 0; s1 = NULL; s2 = NULL; s3 = NULL; s4 = NULL; s5 = NULL;
    }
    
    void Stmt::parse(){
        if(scanner->currentToken()==ID){
            altNo = 1;
            s1 = new Assign();
            s1->parse();
            return;
        }
        else if(scanner->currentToken()==IF){
            altNo = 2;
            s2 = new IfThenElse();
            s2->parse();
            return;
        }
        else if(scanner->currentToken()==WHILE){
            altNo = 3;
            s3 = new Loop();
            s3->parse();
            return;
        }
        else if(scanner->currentToken()==INPUT){
            altNo = 4;
            s4 = new Input();
            s4->parse();
            return;
        }
        else if(scanner->currentToken()==OUTPUT){
            altNo = 5;
            s5 = new Output();
            s5->parse();
            return;
        }
    }
    
    void Stmt::exec(){
        if(altNo == 1){
            s1->exec();
            return;
        } else if(altNo == 2){
            s2->exec();
            return;
        } else if(altNo == 3){
            s3->exec();
            return;
        } else if(altNo == 4){
            s4->exec();
            return;
        } else if(altNo == 5){
            s5->exec();
            return;
        }
    }

/** Program **/

    Program::Program(){
        ds = NULL; ss = NULL;
    }
    void Program::parse(){
        scanner->match(PROGRAM);
        
        ds = new DeclSeq();
        ds->parse();
        
        scanner->match(BEGIN);
        
        ss = new StmtSeq();
        ss->parse();
        
        scanner->match(END); 
        
    }
    void Program::exec(){
        ds->exec();
        ss->exec();
    }

/** DeclSeq **/

    DeclSeq::DeclSeq(){
        ds =  NULL; d = NULL;
    }
    void DeclSeq::parse(){

        d = new Decl();
        d->parse();
        
        if(scanner->currentToken()==INT || scanner->currentToken()==FUN){
            ds = new DeclSeq();
            ds->parse();
        }
        
    }
    void DeclSeq::exec(){
        
    }

/** StmtSeq **/     int altNo; Assign* s1; IfThenElse* s2; Loop* s3; Input* s4; Output* s5;


    StmtSeq::StmtSeq(){
        s = NULL; ss = NULL;
    }
    void StmtSeq::parse(){
        s= new Stmt();
        
        if(scanner->currentToken()==ID){
            s->altNo=1;
            s->parse();
        }else if(scanner->currentToken()==IF){
            s->altNo=2;
            s->parse();
        }else if(scanner->currentToken()==WHILE){
            s->altNo=3;
            s->parse();
        }else if(scanner->currentToken()==INPUT){
            s->altNo=4;
            s->parse();
        }else if(scanner->currentToken()==OUTPUT){
            s->altNo=5;
            s->parse();
        }else{
            cout << "ERROR: unexpected token: " << scanner->currentToken() << "\n";
            exit(0);
        }
        
        if (scanner->currentToken()== ID|| scanner->currentToken()==IF || scanner->currentToken()==WHILE ||scanner->currentToken()==INPUT||scanner->currentToken()==OUTPUT){
            ss= new StmtSeq();
            ss->parse();
        }
    }
    void StmtSeq::exec(){
        s->exec();
        if (ss!=NULL) ss->exec();
    }


/** Decl **/
    
    Decl::Decl(){
        
    }
    void Decl::parse(){
        if(scanner->check(FUN)){
            Function* fun = new Function();
            fun->parse();
        }else{
            scanner->match(INT);
            while (scanner->currentToken()==ID || scanner->currentToken()==COMMA) {
                if(scanner->currentToken()==ID){
                    if(IDmap[scanner->getID()] == INT_MIN){
                        cout << "ERROR: Redeclaration of variable: " << scanner->getID() << "\n";
                        exit(0);
                    }
                    IDmap[scanner->getID()] = INT_MIN;
                    scanner->nextToken();
                }else{
                    scanner->nextToken();
                }
            }
            
            scanner->match(SEMICOLON);
        }
    }
    void Decl::exec(){
        
    }

/** Assign **/
    
    Assign::Assign(){
        id = ""; expr = NULL;
    }
    void Assign::parse(){
        id=scanner->getID();
        scanner->nextToken();
        if(IDmap.find(id)==IDmap.end()){
            cout << "ERROR: Undeclared variable: " << id << "\n";
            exit(0);
        }
        
        scanner->match(ASSIGN);
        
        expr = new Expr();
        expr->parse();
        
        scanner->match(SEMICOLON);
    }
    void Assign::exec(){
        IDmap[id] = expr->exec();
    }

/** Cmpr **/
    
    Cmpr::Cmpr(){
        e1 = NULL; e2 = NULL; t = OPERATOR;
    }
    void Cmpr::parse(){
        e1 = new Expr();
        e1->parse();
        if(scanner->currentToken()==EQUALS){
            t=EQUALS;
            scanner->nextToken();
        }else if(scanner->currentToken()==LESSTHAN){
            t=LESSTHAN;
            scanner->nextToken();
        }else if(scanner->currentToken()==LESSTHANEQUAL){
            t=LESSTHANEQUAL;
            scanner->nextToken();
        }else{
            cout << "ERROR: Expected comparator (<,<=,=), recieved: " << scanner->currentToken() << "\n";
        }
        
        e2 = new Expr();
        e2->parse();
    }
    int Cmpr::exec(){
        if(t==EQUALS){
            return(e1->exec() == e2->exec());
        }else if(t==LESSTHAN){
            return(e1->exec() < e2->exec());
        }else{
            return(e1->exec() <= e2->exec());
        }
    }

/** Cond **/
    
    Cond::Cond(){
        altNo = 0; cmpr = NULL; cond = NULL;
    }
    void Cond::parse(){
        if(scanner->currentToken()==NOT){
            altNo=1;
            scanner->match(NOT);
            scanner->match(LEFTPARAN);
            
            cond = new Cond();
            cond->parse();
            
            scanner->match(RIGHTPARAN);
            
        }else{
            cmpr = new Cmpr();
            cmpr->parse();
            
            if(scanner->currentToken()==OR){
                altNo=2;
                scanner->match(OR);
                
                cond = new Cond();
                cond->parse();
            }
        }
    }
    int Cond::exec(){
        if(altNo==0){
            return cmpr->exec();
        }else if(altNo==1){
            return !cond->exec();
        }else{
            if (cmpr->exec()==1 || cond->exec()==1){
                return 1;
            }
            return 0;
        }
    }
    
/** Input **/
    
    Input::Input(){
        
    }
    void Input::parse(){
        scanner->match(INPUT);
        scanner->check(ID);
        id = scanner->getID();
        
        if(IDmap.find(id)==IDmap.end()){
            cout << "ERROR: Undeclared variable: " << id << "\n";
            exit(0);
        }
        
        scanner->nextToken();
        scanner->match(SEMICOLON);
        
    }
    void Input::exec(){
        int in;
        cin >> in;
        IDmap[id] = in;
        
    }

/** IfThenElse **/
    
    IfThenElse::IfThenElse(){
        c = NULL; ss = NULL; ssElse = NULL;
    }
    void IfThenElse::parse(){
        scanner->match(IF);
        
        c = new Cond();
        c->parse();
        
        scanner->match(THEN);
        
        ss = new StmtSeq();
        ss->parse();
        
        if(scanner->currentToken() == ELSE){
            scanner->match(ELSE);
            ssElse = new StmtSeq();
            ssElse->parse();
        }
        
        scanner->match(ENDIF);
        scanner->match(SEMICOLON);
    }
    void IfThenElse::exec(){
        if(c->exec() == 1){
            ss->exec();
        }else if(ssElse != NULL){
            ssElse->exec();
        }
    }

/** Loop **/
    
    Loop::Loop(){
        c = NULL; ss = NULL;
    }
    void Loop::parse(){
        scanner->match(WHILE);
        
        c = new Cond();
        c->parse();
        
        scanner->match(BEGIN);
        
        ss = new StmtSeq();
        ss->parse();
        
        scanner->match(ENDWHILE);
        scanner->match(SEMICOLON);
    }
    void Loop::exec(){
        while(c->exec()==1){
            ss->exec();
        }
    }



/** Function **/

    Function::Function(){
        ss = NULL; returnValue = NULL;
    }
    void Function::parse(){
        scanner->match(FUN);
        
        scanner->check(ID);
        id = scanner->getID();
        
        if(FUNmap.find(id)!= FUNmap.end()){
            cout << "ERROR: Redeclaration of function: " << id << "\n";
            exit(0);
        }
        FUNmap[id] = this;
        scanner->nextToken();
        
        //IDLIST
        scanner->match(LEFTPARAN);
        while(scanner->check(ID) || scanner->check(COMMA)){
            if(scanner->check(ID)){
                if(localIDmap[scanner->getID()] == INT_MIN){
                    cout << "ERROR: Redeclaration of variable: " << scanner->getID() << "\n";
                    exit(0);
                }
                localIDmap[scanner->getID()]=INT_MIN;
                params.push_back(scanner->getID());
                scanner->nextToken();
            }else{
                scanner->match(COMMA);
                if(!scanner->check(ID)){
                    cout << "ERROR: Expected ID, recieved" << scanner->currentToken() <<"\n";
                    exit(0);
                }
            }
        }
        scanner->match(RIGHTPARAN);
               
        //DECL SEQ
        if(!scanner->check(INT)){
            cout << "ERROR: Expected int, recieved" << scanner->currentToken() <<"\n";exit(0);
        }
        while(scanner->check(INT)){
            scanner->match(INT);
            while(scanner->check(ID) || scanner->check(COMMA)){
                if(scanner->check(ID)){
                    if(localIDmap[scanner->getID()] == INT_MIN){
                        cout << "ERROR: Redeclaration of variable: " << scanner->getID() << "\n";
                        exit(0);
                    }
                    localIDmap[scanner->getID()]=INT_MIN;
                    scanner->nextToken();
                }else{
                    scanner->match(COMMA);
                    if(!scanner->check(ID)){
                        cout << "ERROR: Expected ID, recieved" << scanner->currentToken() <<"\n";exit(0);
                    }
                }
            }
            scanner->match(SEMICOLON);
        }

        IDmap.swap(localIDmap);

        scanner->match(BEGIN);
        ss=new StmtSeq();
        ss->parse();
        scanner->match(RETURN);
        returnValue = new Expr();
        returnValue->parse();
        scanner->match(SEMICOLON);
        scanner->match(END);
        scanner->match(SEMICOLON);
        IDmap.swap(localIDmap);
        
    }
    int Function::exec(vector<int> formalParams){
        for(int i=0;i<params.size();i++){
            localIDmap[params[i]] = formalParams[i];
        }
        
        IDmap.swap(localIDmap);
        ss->exec();
        int temp = returnValue->exec();
        IDmap.swap(localIDmap);
        return temp;
    }

Function* Function::clone(){
    Function* clone = new Function();
    clone->ss = ss;
    clone->returnValue = returnValue;
    clone->localIDmap =localIDmap;
    clone->id = id;
    clone->params = params;

    return clone;
}

/** Expr List **/

    ExprList::ExprList(){
        expr = NULL; el = NULL;
    }
    void ExprList::parse(){
        expr = new Expr();
        expr->parse();
        if(scanner->check(COMMA)){
            scanner->match(COMMA);
            el = new ExprList();
            el->parse();
        }
    }
    vector<int> ExprList::exec(){
        vector<int> result;
        
        result.push_back(expr->exec());
        if(el != NULL){
            vector<int> temp = el->exec();
            result.insert(result.end(), temp.begin(), temp.end());
        }
        
        return result;
    }

/** main **/

int main(int argc, char *argv[]){

    if(argc < 2){
        cout << "ERROR: Enter file name as param such as: testName.txt\n";
        exit(0);
    }
    
    scanner = new Scanner(argv[1]);
    Program* p = new Program();
    p->parse();
    scanner->close();
    p->exec();
    
    return 0;
}
