def ordena(vetor: int, tam: int) -> int:
    topo = None
    bolha = None
    # Simulando for de C usando while em python
    topo = tam - 1 
    while topo > 1 :

        # Simulando for de C usando while em python
        bolha = 0 
        while bolha < topo :

            if vetor [ bolha ] > vetor [ bolha + 1 ] :
                aux = None
                aux = vetor [ bolha + 1 ]                 
                vetor [ bolha + 1 ] = vetor [ bolha ]                 
                vetor [ bolha ] = aux                 
            bolha = bolha + 1 
        topo = topo - 1 


def prompt(i: int) -> int:
    print( "Digite o " )     
    print( i )     
    print( "o inteiro: " )     


def main() -> int:
    buffer = [0] * 15 
    i = None
    print( "ENTRADA \n" )     
    # Simulando for de C usando while em python
    i = 0 
    while i < 15 :

        prompt( i + 1 )         
        buffer [ i ] = int(input( ) )        
        i = i + 1 
    ordena( buffer , 15 )     
    print( "SAIDA \n" )     
    # Simulando for de C usando while em python
    i = 0 
    while i < 15 :

        print( buffer [ i ] )         
        i = i + 1 



if __name__ == "__main__":
    main()


