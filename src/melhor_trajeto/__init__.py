import random


class MelhorTrajeto:

  tamanho_populacao: int
  qtde_geracoes: int
  qtde_amostra_selecao: int
  probabilidade_mutacao: float

  def __init__( self,
                tamanho_populacao: int=100,
                qtde_geracoes: int=50,
                qtde_amostra_selecao: int=10,
                probabilidade_mutacao: float=0.10):
    self.tamanho_populacao = tamanho_populacao
    self.qtde_geracoes = qtde_geracoes
    self.qtde_amostra_selecao = qtde_amostra_selecao
    self.probabilidade_mutacao = probabilidade_mutacao

  def __calcular_distancia_total_rota__(self, centro_distribuicao, rota, entregas):
    distancia_Total = 0
    if len(rota) > 0:
      distancia_Total += self.__calcular_distancia_pontos__(centro_distribuicao, entregas[rota[0]])
      for i in range(len(rota) - 1):
        endereco1 = rota[i]
        endereco2 = rota[i + 1]
        distancia_Total += self.__calcular_distancia_pontos__(entregas[endereco1], entregas[endereco2])
    return distancia_Total

  def __calcular_distancia_pontos__(self, ponto1: tuple[float, float], ponto2: tuple[float, float]):
    return ((ponto2[0] - ponto1[0])**2 + (ponto2[1] - ponto1[1])**2) ** 0.5

  def __gerar_populacao__(self, entregas, tamanho_populacao) -> list[str]:
    return [(self.__gerar_rota_aleatoria__(entregas), 0) for _ in range(self.tamanho_populacao)]

  def __gerar_rota_aleatoria__(self, entregas):
    rota = list(entregas.keys())
    random.shuffle(rota)
    return rota

  def __realizar_selecao__(self, populacao, qtde_amostra_selecao):
    amostragem = random.sample(populacao, qtde_amostra_selecao)
    return min(amostragem, key=lambda x: x[1])

  def __realizar_cruzamento__(self, entregas, individuo1, individuo2):
    indice_cruzamento = random.randint(1, len(entregas) - 1)
    descendente = individuo1[0][:indice_cruzamento]
    descendente += self.__realizar_mutacao__([endereco for endereco in individuo2[0] if endereco not in descendente], self.probabilidade_mutacao)
    return descendente

  def __realizar_mutacao__(self, pontos_entrega_parciais: list, probabilidade_mutacao: float):
    mutantes = pontos_entrega_parciais
    if random.random() < self.probabilidade_mutacao and len(pontos_entrega_parciais) >= 2:
      indice_mutacao = random.randint(0, len(pontos_entrega_parciais) - 2)
      mutante_tmp = mutantes[indice_mutacao]
      mutantes[indice_mutacao] = mutantes[indice_mutacao +1]
      mutantes[indice_mutacao+1] = mutante_tmp
    return mutantes

  def gerar_melhor_trajeto(self, centro_distribuicao: tuple[float, float], entregas: dict[str, tuple[float, float]]):
    populacao = self.__gerar_populacao__(entregas,self.tamanho_populacao)
    for _ in range(self.qtde_geracoes):
      for ix in range(len(populacao)):
        populacao[ix] = (populacao[ix][0], self.__calcular_distancia_total_rota__(centro_distribuicao, populacao[ix][0], entregas))
      populacao_temp = []
      for _ in range(self.tamanho_populacao):
        individuo1 = self.__realizar_selecao__(populacao, self.qtde_amostra_selecao)
        individuo2 = self.__realizar_selecao__(populacao, self.qtde_amostra_selecao)
        descendente = self.__realizar_cruzamento__(entregas, individuo1, individuo2)
        populacao_temp.append((descendente, self.__calcular_distancia_total_rota__(centro_distribuicao, descendente, entregas)))
      populacao = populacao_temp
    melhor_trajeto = min(populacao, key=lambda x: x[1])
    return melhor_trajeto
