# -*- coding: utf-8 -*-
from random import randint
from jogador import Jogador
from tabuleiro import Tabuleiro

class JogadorIA(Jogador):
    def __init__(self, tabuleiro: Tabuleiro, tipo: int):
        super().__init__(tabuleiro, tipo)
        self.oponente = Tabuleiro.JOGADOR_X if tipo == Tabuleiro.JOGADOR_0 else Tabuleiro.JOGADOR_0

    def getJogada(self) -> (int, int):
        jogada = self.regra_vitoria_bloqueio()
        if jogada:
            return jogada

        jogada = self.regra_dupla_sequencia()
        if jogada:
            return jogada

        if self.matriz[1][1] == Tabuleiro.DESCONHECIDO:
            return (1, 1)

        jogada = self.regra_canto_oposto()
        if jogada:
            return jogada

        jogada = self.regra_canto_vazio()
        if jogada:
            return jogada

        return self.regra_jogada_aleatoria()

    def regra_vitoria_bloqueio(self):
        for i in range(3):
            if self.check_sequence([(i, 0), (i, 1), (i, 2)]):
                return self.find_empty([(i, 0), (i, 1), (i, 2)])
            if self.check_sequence([(0, i), (1, i), (2, i)]):
                return self.find_empty([(0, i), (1, i), (2, i)])

        if self.check_sequence([(0, 0), (1, 1), (2, 2)]):
            return self.find_empty([(0, 0), (1, 1), (2, 2)])
        if self.check_sequence([(0, 2), (1, 1), (2, 0)]):
            return self.find_empty([(0, 2), (1, 1), (2, 0)])

        return None

    def regra_dupla_sequencia(self):
        for l in range(3):
            for c in range(3):
                if self.matriz[l][c] == Tabuleiro.DESCONHECIDO:
                    self.matriz[l][c] = self.tipo
                    if self.count_winning_sequences() > 1:
                        self.matriz[l][c] = Tabuleiro.DESCONHECIDO
                        return (l, c)
                    self.matriz[l][c] = Tabuleiro.DESCONHECIDO
        return None

    def regra_canto_oposto(self):
        cantos = [(0, 0), (0, 2), (2, 0), (2, 2)]
        opostos = {(0, 0): (2, 2), (0, 2): (2, 0), (2, 0): (0, 2), (2, 2): (0, 0)}

        for canto in cantos:
            if self.matriz[canto[0]][canto[1]] == self.oponente:
                oposto = opostos[canto]
                if self.matriz[oposto[0]][oposto[1]] == Tabuleiro.DESCONHECIDO:
                    return oposto
        return None

    def regra_canto_vazio(self):
        cantos = [(0, 0), (0, 2), (2, 0), (2, 2)]
        for canto in cantos:
            if self.matriz[canto[0]][canto[1]] == Tabuleiro.DESCONHECIDO:
                return canto
        return None

    def regra_jogada_aleatoria(self):
        lista = []
        for l in range(3):
            for c in range(3):
                if self.matriz[l][c] == Tabuleiro.DESCONHECIDO:
                    lista.append((l, c))
        return lista[randint(0, len(lista)-1)] if lista else None

    def check_sequence(self, positions):
        values = [self.matriz[x][y] for x, y in positions]
        return values.count(self.tipo) == 2 and values.count(Tabuleiro.DESCONHECIDO) == 1

    def find_empty(self, positions):
        for x, y in positions:
            if self.matriz[x][y] == Tabuleiro.DESCONHECIDO:
                return (x, y)
        return None

    def count_winning_sequences(self):
        count = 0
        for i in range(3):
            if self.check_sequence([(i, 0), (i, 1), (i, 2)]):
                count += 1
            if self.check_sequence([(0, i), (1, i), (2, i)]):
                count += 1
        if self.check_sequence([(0, 0), (1, 1), (2, 2)]):
            count += 1
        if self.check_sequence([(0, 2), (1, 1), (2, 0)]):
            count += 1
        return count
