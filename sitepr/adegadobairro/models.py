from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Cliente(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	nome = models.CharField(max_length=200, null=True)
	apelido = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	telemovel = models.IntegerField(null=True)

	def __str__(self):
		return self.nome +" "+self.apelido;

class Vinho(models.Model):
	TIPO = (('Tinto','Tinto'),('Branco','Branco'),('Rose','Rose'),('Madeira','Madeira'),('Porto','Porto'),('Frisante','Frisante'))
	REGIAO = (('Alentejo', 'Alentejo'), ('Algarve','Algarve'), ('Bairrada','Bairrada'), ('Beira Atlântico','Beira Atlântico'), ('Beira Interior','Beira Interior'),
			('Dão', 'Dão'),('Douro', 'Douro'),('Lisboa', 'Lisboa'),('Madeira', 'Madeira'),('Minho', 'Minho'),('Setúbal', 'Setúbal'),('Távora-varosa', 'Távora-varosa'),
			('Tejo', 'Tejo'),('Trás-os-Montes', 'Trás-os-Montes'),('Verdes', 'Verdes'))
	vinho_imagem= models.ImageField(null=True, blank=True)
	nome=models.CharField(max_length=200, null=True)
	preco= models.FloatField(null=True)
	tipo= models.CharField(max_length=200, null=True, choices=TIPO)
	regiao =models.CharField(max_length=200, null=True, choices=REGIAO)
	colheita = models.IntegerField(null=True)
	produtor =models.CharField(max_length=200, null=True)
	precopromocao = models.FloatField(null=True, default=0)
	descricao =models.CharField(max_length=200, null=True)
	datainsercao = models.DateTimeField(auto_now_add=True, null=True)
	vendas = models.IntegerField(null=True, default=0)
	precoatual = models.FloatField(null=True, default=0)
	vinho_id = models.AutoField(primary_key=True)

	def __str__(self):
		return str(self.id);

class Pedido(models.Model):
	cliente = models.ForeignKey(Cliente, null=True, on_delete=models.SET_NULL)
	morada = models.CharField(max_length=200, null=True)
	cidade = models.CharField(max_length=200, null=True)
	nif = models.IntegerField(null=True)
	precototal = models.FloatField(null=True, default=0)
	pago = models.BooleanField(null=True, default=False)
	emloja=models.BooleanField(null=True, default=False)
	pronto = models.BooleanField(null=True, default=False)
	enviado_ou_levantado = models.BooleanField(null=True, default=False)
	data = models.DateTimeField(auto_now_add=True, null=True)
	fechado = models.BooleanField(null=False, default=False)
	pedido_id = models.AutoField(primary_key=True)

	def __str__(self):
		return str(self.id);





class Pedido_Vinho(models.Model):
	vinho = models.ForeignKey(Vinho, on_delete=models.SET_NULL, null=True)
	preco= models.FloatField(null=True)
	quantidade = models.IntegerField(null=True, default=0)
	precototal=models.FloatField(null=True, default=0)
	pedido = models.ForeignKey(Pedido, null=True, on_delete=models.SET_NULL)
	fechado = models.BooleanField(null=False, default=False)
