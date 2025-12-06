int troca(int v[], int n) {
        int tmp;
        int i;
        tmp = v[i];

    return 0;
}

float media(int v[], int n) {
    int i;
    float s;
    s = 0.0;
    for (i = 0; i < n; i = i + 1) {
        s = s + v[i] / 1.0;
    }
    return s / n;
}

char primeiro_char(char s[]) {
    return s[0];
}

int compara(int a, int b) {
    if (a == b)
        return 1;
    else
        return 0;
}

int usa_operadores(int x, int y) {
    int r;
    r = 0;
    if (x > 0 && y > 0) {
        r = 1;
    } else if (x <= 0 || y <= 0) {
        r = -1;
    } else {
        ;
    }
    return r;
}

int conta_ate(int limite) {
    int i;
    i = 0;
    while (i < limite) {
        if (i == 3) {
            i = i + 1;
            continue;
        }
        if (i == 7) {
            break;
        }
        i = i + 1;
    }
    return i;
}

int argumentos_variados(int a, int b[], char c[]) {
    int t;
    t = 0;
    t = soma(a, b[0]);
    b[1] = t;
    c[0] = 'z';
    return b[1] = 42;
}

int main() {
    int arr[10];
    int n;
    int i;
    float m;
    char name[20];
    int res;

    n = 5;
    arr[0] = 10;
    arr[1] = 20;
    arr[2] = 30;
    arr[3] = 40;
    arr[4] = 50;
    arr[5] = 0;

    for (i = 0; i < n; i = i + 1) {
        arr[i] = arr[i] + i * 2;
    }

    troca(arr, n);

    m = media(arr, n);

    res = soma(arr[0], arr[1]);

    if ((res >= 30 && res < 100) || ! (res == 0)) {
        res = usa_operadores(res, n);
    } else {
        res = -999;
    }

    i = 0;
    while (i < 10 && (arr[i] % 2) == 0) {
        i = i + 1;
    }

    name[0] = 'H';
    name[1] = 'i';

    char pc;
    pc = primeiro_char(name);

    int a, b, c;
    a = 1; b = 2; c = 3;

    a = b = c = 5;

    argumentos_variados(a, arr, name);

    return (res + a) ;
}
