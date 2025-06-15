
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Discente, EfectivoDiscente
from .models import CasoMedicoLegal, Baja, EfectivoBaja
from .utils import actualizar_efectivo_casos


def actualizar_efectivo(plantel):
    if plantel is None:
        return  # evitar errores si no tiene plantel asignado

    hombres = Discente.objects.filter(id_plantel=plantel, genero='M').count()
    mujeres = Discente.objects.filter(id_plantel=plantel, genero='F').count()
    total = hombres + mujeres

    efectivo, creado = EfectivoDiscente.objects.get_or_create(
        id_plantel=plantel)
    efectivo.cant_hombre = hombres
    efectivo.cant_mujer = mujeres
    efectivo.cant_total = total
    efectivo.save()


@receiver(post_save, sender=Discente)
def actualizar_efectivo_discente_save(sender, instance, **kwargs):
    actualizar_efectivo(instance.id_plantel)


@receiver(post_delete, sender=Discente)
def actualizar_efectivo_discente_delete(sender, instance, **kwargs):
    actualizar_efectivo(instance.id_plantel)


# Para actualizar el efectivo de los casos medicos legales
@receiver(post_save, sender=CasoMedicoLegal)
def actualizar_efectivo_casos_save(sender, instance, **kwargs):
    actualizar_efectivo_casos(instance.id_discente.id_plantel)


@receiver(post_delete, sender=CasoMedicoLegal)
def actualizar_efectivo_casos_delete(sender, instance, **kwargs):
    actualizar_efectivo_casos(instance.id_discente.id_plantel)

@receiver(post_save, sender=Baja)
def actualizar_efectivo_baja(sender, instance, created, **kwargs):
    if created:
        discente = instance.id_discente
        efectivo, _ = EfectivoBaja.objects.get_or_create(
            id_plantel=discente.id_plantel)

        if discente.genero == 'M':
            efectivo.cant_hombre += 1
        elif discente.genero == 'F':
            efectivo.cant_mujer += 1
        # Para otros géneros, si quieres contar, añade lógica aquí

        efectivo.cant_total = efectivo.cant_hombre + efectivo.cant_mujer
        efectivo.save()
