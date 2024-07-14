from src.melhor_trajeto import MelhorTrajeto

localizacao_centro_distribuicao = (3.13, 1.44)

entregas = {
    'Cliente A': (0.11, 0.22),
    'Cliente B': (1.11, 2.22),
    'Cliente C': (3.11, 1.22),
    'Cliente D': (5.11, 3.22),
    'Cliente E': (2.11, 4.22)
}

melhor_trajeto = MelhorTrajeto()
trajeto = melhor_trajeto.gerar_melhor_trajeto(localizacao_centro_distribuicao, entregas)
print("Melhor trajeto:", trajeto[0])
print("Total Distance:", round(trajeto[1], 2))
