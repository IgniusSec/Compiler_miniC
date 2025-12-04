//  mini-c-teste.txt
//  Programa de teste para análise semântica da linguagem MINI
//  Foca em: escopo, sistema de tipos, chamadas de função e passagem de parâmetros.
//  Linhas marcadas com ERRO devem ser sinalizadas pelo analisador semântico.


//  Observação: as funções de E/S (putchar, putstr, putint, putfloat,
//  getchar, getint, getfloat) são assumidas como pré-declaradas pela
//  biblioteca embutida da linguagem. 

int soma_int(int a, int b) {
    int r;
    float f;

    r = a + b;          //  ok 
    f = a + 0.5;        //  ok: promoção int -> float 
    a = f;              //  ERRO: atribuição float -> int (conversão perigosa) 
    return 0;             //  ERRO: retorno sem valor em função int (se MINI tratar isso) 
}

float mistura_tipos(int x, float y) {
    int k;
    float z;

    k = x;              //  ok 
    z = y;              //  ok 
    k = y;              //  ERRO: float -> int 
    z = x;              //  ok: int -> float 

    x = k;              //  ok: ainda estamos no escopo da função 
    y = z;              //  ok 
    
    return 0;   
}

int helper(int h) {
    int k;
    k = h * 2;

    putint(k);          //  chamada correta: 1 argumento int 

    return 0;             //  ERRO: retorno vazio em função int (se aplicável) 
}

int usa_funcoes(int a, float b) {
    int x;
    float y;

    x = getint();       //  ok: getint sem parâmetros retorna int 
    y = getfloat();     //  ok: getfloat sem parâmetros retorna float 

    x = getfloat();     //  ERRO: float -> int 
    y = getint();       //  ok: int -> float 

    helper(x);          //  ok: 1 parâmetro int 

    mistura_tipos(a, b);    //  ok: (int, float)

    return 0;             //  ERRO (potencial): função int sem valor de retorno 
}

int main() {
    int a;
    float b;
    int i;
    float f;

    a = getint();       //  ok 
    b = getfloat();     //  ok 

    //  Testes de sistema de tipos em expressões simples 
    i = 10;             //  ok 
    f = 2.5;            //  ok (literal float) 

    i = i + 1;          //  ok 
    f = f + 1.0;        //  ok 

    i = f;              //  ERRO: float -> int 
    f = i;              //  ok: int -> float 
    

    //  Testes com for e escopo interno 
    for (i = 0; i < 3; i = i + 1) {
        i = 100;
        putint(i);      //  sempre 100 
    }

    //  Após o laço, i ainda existe com o valor do escopo externo 
    putint(i);

    //  Teste com while e variável declarada dentro do laço 
    i = 0;
    while (i < 3) {
        i = 42;
        putint(i);      //  sempre 42 
    }

    //  Chamada correta de função definida pelo usuário 
    usa_funcoes(a, b);      //  ok 

    //  Teste de putchar e putstr (assumindo assinaturas adequadas) 
    putchar(65);        //  ok: código de caractere 
    putstr(0);          //  ok: supondo índice/ponteiro inteiro 

    return 0;             //  ERRO (potencial): main int sem valor de retorno 
}
