import heapq

class GeradorCongruenteLinear:
    def __init__(self, semente, a, c, m):
        self.semente = semente
        self.a = a
        self.c = c
        self.m = m
        self.valor_atual = semente

    def next_random(self):
        # Atualiza o valor atual com o Método Congruente Linear
        self.valor_atual = (self.a * self.valor_atual + self.c) % self.m
        # Retorna o número pseudoaleatório normalizado entre 0 e 1
        return self.valor_atual / self.m

# Parâmetros do gerador Congruente Linear
semente = 12345
a = 1664525
c = 1013904223
m = 2**32

# Criação do gerador
gerador = GeradorCongruenteLinear(semente, a, c, m)

# Inicialização da fila
fila = []
clientes_perdidos = 0
eventos = []
capacidade_fila = 5
num_servidores = 1
estado_fila = 0
tempo_global = 0

# Inicialização das variáveis de rastreamento de estado
tempo_estado = {i: 0 for i in range(capacidade_fila + 1)}
tempo_ultimo_estado = 0

def sorteio(a, b):
    nextRandom = gerador.next_random()
    return a + (b - a) * nextRandom

def chegada(evento):
    global tempo_global, estado_fila, tempo_ultimo_estado

    tempo_evento, tipo_evento = evento
    tempo_global = tempo_evento

    # Atualiza o tempo no estado anterior
    tempo_estado[estado_fila] += tempo_global - tempo_ultimo_estado
    tempo_ultimo_estado = tempo_global

    if estado_fila < capacidade_fila:
        fila.append(tempo_global)
        estado_fila += 1

        if estado_fila <= num_servidores:
            tempo_atendimento = sorteio(3, 5)
            heapq.heappush(eventos, (tempo_global + tempo_atendimento, 'saida'))
    else:
        global clientes_perdidos
        clientes_perdidos += 1

    tempo_chegada = sorteio(2, 5)
    heapq.heappush(eventos, (tempo_global + tempo_chegada, 'chegada'))

def saida(evento):
    global tempo_global, estado_fila, tempo_ultimo_estado

    tempo_evento, tipo_evento = evento
    tempo_global = tempo_evento

    # Atualiza o tempo no estado anterior
    tempo_estado[estado_fila] += tempo_global - tempo_ultimo_estado
    tempo_ultimo_estado = tempo_global

    if fila:
        fila.pop(0)
        estado_fila -= 1

        if estado_fila >= num_servidores:
            tempo_atendimento = sorteio(3, 5)
            heapq.heappush(eventos, (tempo_global + tempo_atendimento, 'saida'))

def main():
    global eventos, tempo_ultimo_estado

    # Inicializa o primeiro evento
    tempo_inicial = 2.0
    heapq.heappush(eventos, (tempo_inicial, 'chegada'))

    count = 100000
    while count > 0:
        evento = heapq.heappop(eventos)
        if evento[1] == 'chegada':
            chegada(evento)
        elif evento[1] == 'saida':
            saida(evento)
        count -= 1

    # Atualiza o tempo para o último estado após a simulação
    tempo_estado[estado_fila] += tempo_global - tempo_ultimo_estado

    # Calcula o tempo total de simulação
    tempo_total = tempo_global

    # Imprime resultados
    print("Tempo total de simulação:", tempo_total)
    print("Clientes perdidos:", clientes_perdidos)
    print("Número de clientes na fila ao final:", estado_fila)
    print("Tamanho final da fila:", len(fila))
    print("Tempo acumulado em cada estado:")

    for estado, tempo in tempo_estado.items():
        probabilidade = tempo / tempo_total
        print(f"Estado {estado}: Tempo acumulado = {tempo:.2f} minutos, Probabilidade = {probabilidade:.4f}")

if __name__ == "__main__":
    main()
