if __name__ == "__main__":
    print("🚢 ¡BIENVENIDO A HUNDIR LA FLOTA! 🚢\n")
    
    try:
        # 1. Crear y colocar barcos
        jugador_flota = colocar_barcos(crear_tablero())
        jugador_disparos = crear_tablero()
        
        rival_flota = colocar_barcos(crear_tablero())
        rival_disparos = crear_tablero()
        
        # Contadores de impactos (Total: 18 casillas)
        impactos_jugador = 0
        impactos_rival = 0
        META_VICTORIA = 18

        # 2. Bucle principal
        while True:
            # Mostrar tableros principales del jugador
            print("\n" + "="*30 + " TU FLOTA " + "="*30)
            print(jugador_flota)
            print("\n" + "="*30 + " TUS DISPAROS " + "="*30)
            print(jugador_disparos)

            # Turno Jugador
            if turno_disparo_jugador(rival_flota, jugador_disparos) == "tocado":
                impactos_jugador += 1
                if impactos_jugador == META_VICTORIA:
                    print("\n🎉 ¡VICTORIA! ¡Has destruido toda la flota enemiga!")
                    break

            # Turno Rival 
            if turno_disparo_rival(jugador_flota, rival_disparos) == "tocado":
                impactos_rival += 1
                if impactos_rival == META_VICTORIA:
                    print("\n💀 ¡DERROTA! La máquina ha hundido todos tus barcos.")
                    break

    except RuntimeError as e:
        print(f"\n❌ Error: {e}")
    except KeyboardInterrupt:
        print("\n\n👋 Partida cancelada.")