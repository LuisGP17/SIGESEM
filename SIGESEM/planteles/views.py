from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse




#Panel principal
@login_required
def dashboard(request):
    total_discentes = Discente.objects.count()
    total_bajas = Baja.objects.count()
    total_casos = CasoMedicoLegal.objects.count()
    total_planteles = Plantel.objects.count()

    return render(request, 'planteles/dashboard.html', {
        'total_discentes': total_discentes,
        'total_bajas': total_bajas,
        'total_casos': total_casos,
        'total_planteles': total_planteles,
    })



@login_required
def dashboard(request):
    total_discentes = Discente.objects.count()
    total_hombres = Discente.objects.filter(genero='M').count()
    total_mujeres = Discente.objects.filter(genero='F').count()
    total_bajas = Baja.objects.count()
    total_casos = CasoMedicoLegal.objects.count()
    total_planteles = Plantel.objects.count()

    contexto = {
        'total_discentes': total_discentes,
        'total_hombres': total_hombres,
        'total_mujeres': total_mujeres,
        'total_bajas': total_bajas,
        'total_casos': total_casos,
        'total_planteles': total_planteles
    }
    return render(request, 'planteles/dashboard.html', contexto)


#Discentes

def crear_objeto(request, modelo_form, template='planteles/agregar_discente.html'):
    form = modelo_form(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('lista')
    return render(request, template, {'form': form})


def lista_discentes(request):
    genero = request.GET.get('genero')
    if genero in ['M', 'F', 'O']:
        discentes = Discente.objects.filter(genero=genero)
    else:
        discentes = Discente.objects.all()
    return render(request, 'planteles/lista.html', {'objetos': discentes, 'titulo': 'Discentes'})


def editar_discente(request, pk):
    discente = get_object_or_404(Discente, pk=pk)
    if request.method == 'POST':
        form = DiscenteForm(request.POST, instance=discente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Discente actualizado correctamente.')
            return redirect('lista')
    else:
        form = DiscenteForm(instance=discente)

    return render(request, 'planteles/formulario.html', {
        'form': form,
        'titulo': 'Editar Discente'
    })


#baja Discente

def nuevo_tipo_baja(request):
    if request.method == 'POST':
        form = TipoBajaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de baja registrado correctamente.')
            return redirect('nuevo_tipo_baja')
    else:
        form = TipoBajaForm()
    return render(request, 'planteles/form_tipo_baja.html', {'form': form})




def nueva_baja(request):
    if request.method == 'POST':
        form = BajaForm(request.POST)
        if form.is_valid():
            matricula = form.cleaned_data['matricula'].strip().upper()
            try:
                discente = Discente.objects.get(matricula=matricula)

                # Guardar la baja
                nueva_baja = Baja(
                    id_discente=discente,
                    tipo_baja=form.cleaned_data['tipo_baja'],
                    fecha_baja=form.cleaned_data['fecha_baja'],
                    motivo=form.cleaned_data['motivo']
                )
                nueva_baja.save()

                # Actualizar EfectivoBaja
                efectivo, creado = EfectivoBaja.objects.get_or_create(id_plantel=discente.id_plantel)
                if discente.genero == 'M':
                    efectivo.cant_hombre += 1
                elif discente.genero == 'F':
                    efectivo.cant_mujer += 1
                efectivo.cant_total = efectivo.cant_hombre + efectivo.cant_mujer
                efectivo.save()

                # Eliminar al discente
                discente.delete()

                messages.success(request, "✅ Baja registrada correctamente.")
                return redirect('nueva_baja')
            except Discente.DoesNotExist:
                messages.error(request, "❌ No se encontró un discente con esa matrícula.")
        else:
            messages.error(request, "❌ Corrige los errores del formulario.")
    else:
        form = BajaForm()

    return render(request, 'planteles/form_baja.html', {'form': form})

def editar_baja(request, id):
    baja = get_object_or_404(Baja, id=id)
    if request.method == 'POST':
        form = BajaForm(request.POST, instance=baja)
        if form.is_valid():
            form.save()
            messages.success(request, "Baja actualizada correctamente.")
            return redirect('lista_bajas')
    else:
        form = BajaForm(instance=baja)
    return render(request, 'planteles/formulario_baja.html', {
        'form': form,
        'titulo': 'Editar Baja'
    })

def eliminar_baja(request, id):
    baja = get_object_or_404(Baja, id=id)
    if request.method == 'POST':
        baja.delete()
        messages.success(request, "Baja eliminada correctamente.")
        return redirect('lista_bajas')
    # En caso de GET, podrías mostrar una confirmación o redirigir
    return render(request, 'planteles/confirmar_eliminacion.html', {
        'objeto': baja,
        'titulo': 'Confirmar eliminación de baja'
    })


@login_required
def tu_vista(request):
    ...


def lista_bajas(request):
    bajas = Baja.objects.select_related('id_discente', 'tipo_baja').all().order_by('-fecha_baja')
    return render(request, 'planteles/lista_bajas.html', {'objetos': bajas, 'titulo': 'Bajas registradas'})


#Plantel

def lista_planteles(request):
    planteles = Plantel.objects.all()
    return render(request, 'planteles/lista_planteles.html', {'planteles': planteles})

def nuevo_plantel(request):
    if request.method == 'POST':
        form = PlantelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_planteles')
    else:
        form = PlantelForm()
    return render(request, 'planteles/formulario_plantel.html', {'form': form, 'titulo': 'Nuevo Plantel'})

def editar_plantel(request, id):
    plantel = get_object_or_404(Plantel, id=id)
    if request.method == 'POST':
        form = PlantelForm(request.POST, instance=plantel)
        if form.is_valid():
            form.save()
            return redirect('lista_planteles')
    else:
        form = PlantelForm(instance=plantel)
    return render(request, 'planteles/formulario_plantel.html', {'form': form, 'titulo': 'Editar Plantel'})

def eliminar_plantel(request, id):
    plantel = get_object_or_404(Plantel, id=id)
    if request.method == 'POST':
        plantel.delete()
        return redirect('lista_planteles')
    return render(request, 'planteles/confirmar_eliminar.html', {'plantel': plantel})




def lista_usuarios(request):
    return HttpResponse("Vista de usuarios (en construcción)")

#Casos medicos legales

def nuevo_caso_medico_legal(request):
    if request.method == 'POST':
        form = CasoMedicoLegalForm(request.POST)
        if form.is_valid():
            caso = form.save(commit=False)
            caso.id_discente = form.cleaned_data['matricula']  # Aquí matricula es el objeto Discente
            caso.save()
            messages.success(request, 'El caso médico-legal se ha guardado exitosamente.')
            return redirect('nuevo_caso')
    else:
        form = CasoMedicoLegalForm()
    return render(request, 'casos/formulario.html', {
        'form': form,
        'titulo': 'Registrar Caso Médico-Legal'
    })


def editar_caso(request, id):
    caso = get_object_or_404(CasoMedicoLegal, id=id)
    if request.method == 'POST':
        form = CasoMedicoLegalForm(request.POST, instance=caso)
        if form.is_valid():
            caso = form.save(commit=False)
            caso.id_discente = form.cleaned_data['matricula']  # matricula es objeto Discente
            caso.save()
            messages.success(request, 'El caso médico-legal se ha actualizado exitosamente.')
            return redirect('lista_casos')
    else:
        form = CasoMedicoLegalForm(instance=caso)

    return render(request, 'casos/formulario.html', {
        'form': form,
        'titulo': 'Editar Caso Médico-Legal'
    })


def eliminar_caso(request, pk):
    caso = get_object_or_404(CasoMedicoLegal, pk=pk)
    caso.delete()
    messages.success(request, 'El caso médico-legal ha sido eliminado correctamente.')
    return redirect('lista_casos')

def lista_casos(request):
    casos = CasoMedicoLegal.objects.select_related('id_discente', 'id_discente__id_plantel')
    return render(request, 'planteles/lista_casos.html', {
        'titulo': 'Casos Médico-Legales Registrados',
        'objetos': casos
    })
