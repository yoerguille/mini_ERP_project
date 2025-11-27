from django.db import models
from django.utils import timezone

class Client(models.Model):

    TIPOS_CLIENTE = [
        ("club deportivo", "Club deportivo"),
        ("colegio", "Colegio"),
        ("ayuntamiento", "Ayuntamiento"),
        ("universidad", "Universidad"),
        ("empresa", "Empresa"),
        ("particular", "Particular"),
    ]

    name = models.CharField(
        verbose_name='Nombre',
        max_length=255,
    )

    tipo = models.CharField(
        verbose_name='Tipo de Cliente',
        choices=TIPOS_CLIENTE
    )

    cif_nif = models.CharField(
        verbose_name='CIF/NIF',
        max_length=20,
        blank=True,
        null=True,
    )

    t_number = models.CharField(
        verbose_name='Nº teléfono',
        max_length=30,
        null=True,
        blank=True
    )

    email= models.EmailField(
        blank=True,
    )

    direccion=models.TextField(
        verbose_name='Direccion',
        max_length=100,
        blank=True,
        null=True,
    )

    other=models.TextField(
        verbose_name='Otra información',
        blank=True,
        null=True,
    )

    created_at=models.DateTimeField(
        verbose_name='Fecha de Creación',
        default=timezone.now,
        )

    def __str__(self):
        return self.name
    
    def clean(self):
        if self.name:
            self.name = self.name.strip().title()
        

class ClientContact(models.Model):
    client=models.ForeignKey(
        'Client',
        on_delete=models.CASCADE,
        related_name='relacionados',
    )

    first_name = models.CharField(
        verbose_name='Nombre',
        max_length=255,
    )

    last_name =models.CharField(
        verbose_name='Apellidos',
        max_length=255,
    )

    cargo = models.CharField(
        verbose_name='Cargo',
        max_length=30,
        null=True,
        blank=True,
    )

    t_number = models.CharField(
        verbose_name='Nº teléfono',
        max_length=30,
        null=True,
        blank=True
    )

    email= models.EmailField(
        blank=True,
    )

    def __str__(self):
        return f"{self.first_name} ({self.client.name})"
    

class ClientFile(models.Model):
    client=models.ForeignKey(
        'Client',
        on_delete=models.CASCADE,
        related_name='files',
    )

    file = models.FileField(
        verbose_name="Archivos",
        upload_to="clients_files",
        null=True,
        blank=True,
    )

    descripcion = models.TextField(
        verbose_name='Descripcion de archivo',
        null=True,
        blank=True,
    )

    created_at=models.DateTimeField(
        verbose_name='Fecha de Creación de archivo',
        default=timezone.now,
        )
    
    def __str__(self):
        return self.file.name