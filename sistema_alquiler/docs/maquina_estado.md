stateDiagram-v2
    [*] --> Disponible : registrar_vehiculo()

    Disponible --> Alquilado : registrar_alquiler()
    Disponible --> EnMantenimiento : enviar_a_mantenimiento()
    Disponible --> FueraServicio : marcar_fuera_servicio()

    Alquilado --> Disponible : finalizar_alquiler()
    Alquilado --> ConMulta : generar_multa()
    Alquilado --> FueraServicio : vehiculo_danado()

    ConMulta --> Disponible : multa_pagada()
    ConMulta --> FueraServicio : vehiculo_irrecuperable()

    EnMantenimiento --> Disponible : finalizar_mantenimiento()
    EnMantenimiento --> FueraServicio : fuera_servicio_definitivo()

    FueraServicio --> Disponible : reparar_y_reactivar()

    Disponible --> [*] : eliminar_vehiculo()
    FueraServicio --> [*] : baja_definitiva()
