def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF) #CREA ESTACI璐窷 DE INTERFAZ
    wlan.active(True)       # ACTIVA LA INTERFAZ
    if not wlan.isconnected():    #REVISA SI LA ESTACI璐窷 ES CONECTADA A WLAN
        print('connecting to network...')
        wlan.connect('INFINITUM3B24_2.4', 'Gt4AmMEUSS')   #SE CONECTA
        while not wlan.isconnected():   #REVISA SI LA ESTACI璐窷 ES CONECTADA A WLAN
            pass
    print('network config:', wlan.ifconfig()) #OBTIENE LA INTERFAZ -> IP/subred/puerta de enlace/servidor DNS
