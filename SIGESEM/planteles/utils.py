from .models import CasoMedicoLegal, EfectivoCasoMedicoLegal, Discente

def actualizar_efectivo_casos(plantel):
    # Contar casos médicos legales para hombres en ese plantel
    casos_hombres = CasoMedicoLegal.objects.filter(
        id_discente__id_plantel=plantel,
        id_discente__genero='M'
    ).count()
    
    # Contar casos para mujeres en ese plantel
    casos_mujeres = CasoMedicoLegal.objects.filter(
        id_discente__id_plantel=plantel,
        id_discente__genero='F'
    ).count()
    
    # Total casos (hombres + mujeres)
    total_casos = casos_hombres + casos_mujeres
    
    # Obtener o crear el registro de efectivo para ese plantel
    efectivo, creado = EfectivoCasoMedicoLegal.objects.get_or_create(id_plantel=plantel)
    
    # Actualizar los campos
    efectivo.cant_hombre = casos_hombres
    efectivo.cant_mujer = casos_mujeres
    efectivo.cant_total = total_casos
    
    # Guardar cambios
    efectivo.save()
