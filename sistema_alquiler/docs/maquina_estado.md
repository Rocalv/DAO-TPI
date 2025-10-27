stateDiagram-v2
    [*] --> Disponible : registrar_vehiculo()

    Disponible --> Alquilado : registrar_alquiler()
    Disponible --> EnMantenimiento : enviar_a_mantenimiento()
    Disponible --> FueraServicio : marcar_fuera_servicio()

    Alquilado --> Disponible : finalizar_alquiler()
    Alquilado --> FueraServicio : vehiculo_danado()

    EnMantenimiento --> Disponible : finalizar_mantenimiento()
    EnMantenimiento --> FueraServicio : fuera_servicio_definitivo()

    FueraServicio --> Disponible : reparar_y_reactivar()

    Disponible --> [*] : eliminar_vehiculo()
    FueraServicio --> [*] : baja_definitiva()
