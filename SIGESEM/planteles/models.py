from django.db import models

class Plantel(models.Model):
    nombre = models.CharField(max_length=100)
    tipo_estudio = models.CharField(max_length=100)
    cursos = models.CharField(max_length=200)
    duracion_curso = models.IntegerField(default=0)


    def __str__(self):
        return self.nombre

class CategoriaDiscente(models.Model):
    nombre_categoria = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre_categoria

class EntidadFederativa(models.Model):
    nombre_entidad = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_entidad

class Discente(models.Model):
    matricula = models.CharField(max_length=9, unique=True, null=True, blank=True)
    
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    id_plantel = models.ForeignKey(Plantel, on_delete=models.CASCADE)
    id_categoria = models.ForeignKey(CategoriaDiscente, on_delete=models.CASCADE)
    id_entidad = models.ForeignKey(EntidadFederativa, on_delete=models.CASCADE)
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    fecha_ingreso = models.DateField()
    fecha_egreso = models.DateField(null=True, blank=True)
    antiguedad = models.IntegerField()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class TipoBaja(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Baja(models.Model):
    id_discente = models.ForeignKey('Discente', on_delete=models.CASCADE)
    tipo_baja = models.ForeignKey('TipoBaja', on_delete=models.CASCADE)
    fecha_baja = models.DateField()
    motivo = models.TextField()

    def __str__(self):
        return f"{self.id_discente} - {self.tipo_baja} ({self.fecha_baja})"



class CasoMedicoLegal(models.Model):
    id_discente = models.ForeignKey(Discente, on_delete=models.CASCADE)
    fecha_caso = models.DateField()
    descripcion = models.TextField()
    acciones_adoptadas = models.TextField()

class Egresado(models.Model):
    id_plantel = models.ForeignKey(Plantel, on_delete=models.CASCADE)
    fecha_egreso = models.DateField()

class Infresado(models.Model):
    id_plantel = models.ForeignKey(Plantel, on_delete=models.CASCADE)
    fecha_ingreso = models.DateField()

class EfectivoDiscente(models.Model):
    id_plantel = models.ForeignKey(Plantel, on_delete=models.CASCADE)
    cant_hombre = models.IntegerField(default=0)
    cant_mujer = models.IntegerField(default=0)
    cant_total = models.IntegerField(default=0)


class EfectivoEntidad(models.Model):
    id_entidad = models.ForeignKey(EntidadFederativa, on_delete=models.CASCADE)
    id_plantel = models.ForeignKey(Plantel, on_delete=models.CASCADE)
    cantidad = models.FloatField()
    fecha_registro = models.DateField()

class EfectivoCasoMedicoLegal(models.Model):
    id_plantel = models.OneToOneField(Plantel, on_delete=models.CASCADE)
    cant_hombre = models.IntegerField(default=0)
    cant_mujer = models.IntegerField(default=0)
    cant_total = models.IntegerField(default=0)

    def __str__(self):
        return f"Efectivo Casos Médicos Legales - {self.id_plantel}"

class EfectivoBaja(models.Model):
    id_plantel = models.OneToOneField(Plantel, on_delete=models.CASCADE)
    cant_hombre = models.PositiveIntegerField(default=0)
    cant_mujer = models.PositiveIntegerField(default=0)
    cant_total = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Bajas - {self.id_plantel.nombre}"
