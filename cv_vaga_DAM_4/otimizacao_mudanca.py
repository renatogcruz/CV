"""
Created on April 18, 2020
    @author: Renato Godoi da Cruz
    email: renatogcruz@hotmail.com
"""

from random import random

class Produto():
    """Cria a classe Produtos"""
    def __init__(self, nome, espaco, valor):
        self.nome = nome
        self.espaco = espaco
        self.valor = valor

#Classe indivíduo I 
#(indivíduos representam as soluções)
#(um conj. de individuos formam uma população)
#(O cromossomo representa uma solução)
#(O indiv. pode ser o próprio cromossomo ou pode conter o cromossomo como atributo [dependendo do caso])
#(gelad. = 0, iphone = 1, notebook = 0, ... (formam o cromossomo '0, 1, 0, ...' que nada mais é do que um conjunto de string")

class Individuo():
    """Cria a classe Indivíduo"""
    def __init__(self, espacos, valores, limite_espacos, geracao=0):
        self.espacos = espacos
        self.valores = valores
        self.limite_espacos = limite_espacos
        self.nota_avaliacao = 0              #somatório dos valores da carga
        self.espaco_usado = 0                #espaço total usado pela carga
        self.geracao = geracao
        self.cromossomo = []
        
        #GERAÇÃO INICIAL este 'for' inicia a primeira população (aleatória)
        for i in range(len(espacos)):        #esse for vai de gero até o espaço que ainda tem para carregar ou não um produto
            if random() < 0.5:               #gera um num. entre 0 e 1 (valores que compõe o cromossomo)
                self.cromossomo.append("0")
            else:
                self.cromossomo.append("1")

    def avaliacao(self):
        """Função para avaliar os indívuos (conjuntos de cromossomos)"""
        nota = 0
        soma_espacos = 0
        for i in range(len(self.cromossomo)):
           if self.cromossomo[i] == '1':
               nota += self.valores[i]
               soma_espacos += self.espacos[i]
        if soma_espacos > self.limite_espacos:
            nota = 1
        self.nota_avaliacao = nota
        self.espaco_usado = soma_espacos

    #CROSSOVER combina pedaços de cromossomos de dois genitores gerando filhos mais aptos
    def crossover(self, outro_individuo):
        """Determina o ponto de crossover"""
        corte = int(round(random()  * len(self.cromossomo)))                     #um número randômico (0 ou 1) vai multiplicar pelo tamanho do cromossomo (round é para arredondar)
        
        filho1 = outro_individuo.cromossomo[0:corte] + self.cromossomo[corte::]  #o filho recebe parte do cromossomo (de 0 até corte) do outro indíviduo
        filho2 = self.cromossomo[0:corte] + outro_individuo.cromossomo[corte::]  #o outro_ind é o individuo2 
        
        filhos = [Individuo(self.espacos, self.valores, self.limite_espacos, self.geracao + 1),
                  Individuo(self.espacos, self.valores, self.limite_espacos, self.geracao + 1)]
        filhos[0].cromossomo = filho1   #filho 1 e 2 na verdade está criando cromossomos
        filhos[1].cromossomo = filho2
        return filhos
    
    def mutacao(self, taxa_mutacao):
        """Função para mutação"""
        #print("Antes %s " % self.cromossomo)
        for i in range(len(self.cromossomo)):
            if random() < taxa_mutacao:
                if self.cromossomo[i] == '1':
                    self.cromossomo[i] = '0'
                else:
                    self.cromossomo[i] = '1'
        #print("Depois %s " % self.cromossomo)
        return self
        
class AlgoritmoGenetico():
    """Classe que implementa o Algoritmo Genético"""
    def __init__(self, tamanho_populacao):
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.geracao = 0
        self.melhor_solucao = 0
        
    def inicializa_populacao(self, espacos, valores, limite_espacos):
        for i in range(self.tamanho_populacao):
            self.populacao.append(Individuo(espacos, valores, limite_espacos))
        self.melhor_solucao = self.populacao[0]
        
    def ordena_populacao(self):
        self.populacao = sorted(self.populacao,
                                key = lambda populacao: populacao.nota_avaliacao,
                                reverse = True)
        
    def melhor_individuo(self, individuo):
        if individuo.nota_avaliacao > self.melhor_solucao.nota_avaliacao:
            self.melhor_solucao = individuo
            
    def soma_avaliacoes(self):
        soma = 0
        for individuo in self.populacao:
           soma += individuo.nota_avaliacao
        return soma
    
    def seleciona_pai(self, soma_avaliacao):
        """Seleção dos indivíduos - método Roleta Viciada"""
        pai = -1
        valor_sorteado = random() * soma_avaliacao
        soma = 0
        i = 0
        while i < len(self.populacao) and soma < valor_sorteado:
            soma += self.populacao[i].nota_avaliacao
            pai += 1
            i += 1
        return pai
    
    def visualiza_geracao(self):
        """Função para visualizar os melhores indivíduos de cada geração"""
        melhor = self.populacao[0]
        print("G:%s -> Valor: %s Espaço: %s Cromossomo: %s" % (self.populacao[0].geracao,
                                                               melhor.nota_avaliacao,
                                                               melhor.espaco_usado,
                                                               melhor.cromossomo))
    
    def resolver(self, taxa_mutacao, numero_geracoes, espacos, valores, limite_espacos):
        self.inicializa_populacao(espacos, valores, limite_espacos)
        
        for individuo in self.populacao:
            individuo.avaliacao()
        
        self.ordena_populacao()
        
        self.visualiza_geracao()
        
        for geracao in range(numero_geracoes):
            soma_avaliacao = self.soma_avaliacoes()
            nova_populacao = []
            
            for individuos_gerados in range(0, self.tamanho_populacao, 2):
                pai1 = self.seleciona_pai(soma_avaliacao)
                pai2 = self.seleciona_pai(soma_avaliacao)
                
                filhos = self.populacao[pai1].crossover(self.populacao[pai2])
                
                nova_populacao.append(filhos[0].mutacao(taxa_mutacao))
                nova_populacao.append(filhos[1].mutacao(taxa_mutacao))
            
            self.populacao = list(nova_populacao)
            
            for individuo in self.populacao:
                individuo.avaliacao()
            
            self.ordena_populacao()
            
            self.visualiza_geracao()
            
            melhor = self.populacao[0]
            self.melhor_individuo(melhor)
        
        print("\nMelhor solução -> G: %s Valor: %s Espaço: %s Cromossomo: %s" %
              (self.melhor_solucao.geracao,
               self.melhor_solucao.nota_avaliacao,
               self.melhor_solucao.espaco_usado,
               self.melhor_solucao.cromossomo))
        
        return self.melhor_solucao.cromossomo

#EXECUTOR
if __name__ == '__main__':
    #p1 = Produto("Iphone 6", 0.0000899, 2199.12)
    lista_produtos = []
    lista_produtos.append(Produto("Geladeira dako", 0.751, 999.90))
    lista_produtos.append(Produto("Cama box casal", 1.11, 1099.08))
    lista_produtos.append(Produto("TV 55", 0.400, 4345.99))
    lista_produtos.append(Produto("Fogão Consul 4 bocas", 0.30, 899.10))
    lista_produtos.append(Produto("Lava e seca Samsung", 0.51, 3899.00))
    lista_produtos.append(Produto("Notebook Asus", 0.527, 3999.00))
    lista_produtos.append(Produto("Ventilador Panasonic", 0.496, 199.90))
    lista_produtos.append(Produto("Sofá 3 lugares", 1.77, 4915.91))
    lista_produtos.append(Produto("Microondas LG", 0.0544, 429.90))
    lista_produtos.append(Produto("Geladeira Brastemp", 0.635, 849.00))
    lista_produtos.append(Produto("Guarda-roupa 6 portas", 1.686, 599.90))

    espacos = []
    valores = []
    nomes = []
    for produto in lista_produtos:
        espacos.append(produto.espaco)
        valores.append(produto.valor)
        nomes.append(produto.nome)

    limite = 3
    tamanho_populacao = 30
    taxa_mutacao = 0.05
    numero_geracoes = 100

    ag = AlgoritmoGenetico(tamanho_populacao)
    resultado = ag.resolver(taxa_mutacao, numero_geracoes, espacos, valores, limite)

    for i in range(len(lista_produtos)):
        if resultado[i] == '1':
            print("Nome: %s R$ %s " % (lista_produtos[i].nome,
                                       lista_produtos[i].valor))