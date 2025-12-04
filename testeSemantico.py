
if __name__ == "__main__":
    main()


def soma_int(a: int, b: int) -> int:
    r = a + b     
    f = a + 0.5     
    a = f     
    return 0     


def mistura_tipos(x: int, y: float) -> float:
    k = x     
    z = y     
    k = y     
    z = x     
    x = k     
    y = z     
    return 0     


def helper(h: int) -> int:
    k = h * 2     
    putint( k )     
    return 0     


def usa_funcoes(a: int, b: float) -> int:
    x = getint( )     
    y = getfloat( )     
    x = getfloat( )     
    y = getint( )     
    helper( x )     
    mistura_tipos( a , b )     
    return 0     


def main() -> int:
    a = getint( )     
    b = getfloat( )     
    i = 10     
    f = 2.5     
    i = i + 1     
    f = f + 1.0     
    i = f     
    f = i     
    for i = 0 i < 3 i = i + 1 :
        i = 100         
        putint( i )         
    putint( i )     
    i = 0     
    while i < 3 :
        i = 42         
        putint( i )         
    usa_funcoes( a , b )     
    putchar( 65 )     
    putstr( 0 )     
    return 0     


