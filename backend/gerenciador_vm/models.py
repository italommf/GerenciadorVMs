from django.db import models

class Maquinas_Virtuais(models.Model):

    endereco_computador = models.CharField(
        max_length = 255, 
        null = False
    )

    nome_de_usuario = models.CharField(
        max_length = 255, 
        null = False
    )

    favoritada = models.BooleanField(
        default = False
    )
    
    senha = models.CharField(
        max_length = 255, 
        null = False
    )

    resolucao = models.CharField(
        max_length=50, 
        null=True, 
        blank=True
    )

    usar_todos_os_monitores = models.BooleanField(
        default = False
    )

    area_de_transferencia = models.BooleanField(
        default = True
    )

    area_de_trabalho = models.IntegerField(
        default = 1
    )
    
    def __str__(self):
        return f'{self.nome_de_usuario} - {self.endereco_computador}'
        
    class Meta:

        verbose_name = 'Máquina Virtual' 
        verbose_name_plural = 'Máquinas Virtuais' 
        
    
class Robotizacoes(models.Model):
        
    nome_do_robo = models.CharField(
        max_length = 255, 
        null = False
    )

    unidade = models.CharField(
        max_length = 255, 
        null = False
    )

    agendador = models.BooleanField(
        default = False
    )

    maquina_virtual = models.ForeignKey(
        Maquinas_Virtuais, 
        related_name = 'robos', 
        on_delete = models.CASCADE
    ) 

    def __str__(self):
        return f'{self.nome_do_robo} - Área de Trabalho {self.area_de_trabalho}'

    class Meta:

        verbose_name = 'Robotização'
        verbose_name_plural = 'Robotizações'


class VMProcesso(models.Model):

    maquina_virtual = models.ForeignKey(
        Maquinas_Virtuais, 
        on_delete = models.CASCADE
    )

    process_id = models.IntegerField()

    criado_em = models.DateTimeField(
        auto_now_add = True
    )

    nome_usuario = models.CharField(
        max_length = 255, 
        null = True, 
        blank = True
    )

    def __str__(self):
        return f'Processo {self.process_id} da VM {self.maquina_virtual} (Usuário: {self.nome_usuario})'