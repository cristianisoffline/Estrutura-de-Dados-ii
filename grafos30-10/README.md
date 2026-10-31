# Grafo com BFS e DFS: simulação de bloqueio de conexões

Trabalho de grafos: modelo próprio com 8 vértices, implementação de busca em largura (BFS) e busca em profundidade (DFS), simulação de conexões indisponíveis e comparação dos caminhos antes e depois do bloqueio.

## Requisitos do trabalho

- [x] Desenvolver modelo próprio com 7 ou mais vértices (foram usados 8)
- [x] Implementar BFS e DFS
- [x] Simular indisponibilidade de 1 ou mais conexões
- [x] Mostrar o caminho antes e depois do bloqueio
- [x] Explicar as escolhas (seção "Escolhas de projeto")

## O modelo

Grafo não direcionado e sem pesos, com 8 vértices e 11 arestas. O desenho foi feito no Graph Online.

Arestas: `1-2, 1-3, 2-3, 2-4, 3-4, 4-5, 4-6, 5-6, 6-7, 6-8, 7-8`

O grafo tem dois grupos de vértices bem ligados internamente: o bloco `{1, 2, 3, 4}` e o bloco `{5, 6, 7, 8}`. Os dois blocos se conectam apenas por `4-6` e por `4-5`, e isso torna o bloqueio dessas conexões interessante para a simulação.

<img width="935" height="390" alt="image" src="https://github.com/user-attachments/assets/cf6af4ce-c6a5-47b0-b926-e71f5399ab28" />

Diagrama sem bloqueios

<img width="935" height="376" alt="image" src="https://github.com/user-attachments/assets/81986cac-19ff-4102-8071-75dab572801a" />

Diagrama com bloqueio 4-6

<img width="935" height="378" alt="image" src="https://github.com/user-attachments/assets/1e1ec16b-20ba-4a4a-af92-afbbd0637645" />

Diagrama com o bloqueio 4-5


## O que o programa faz

Calcula o caminho do vértice 1 até o vértice 8 em três situações:

1. Grafo completo, sem bloqueios.
2. Com a conexão `4-6` indisponível.
3. Cenário extremo: com `4-6` e `4-5` indisponíveis, o que separa o grafo em duas partes.

Para cada situação, BFS e DFS mostram o caminho encontrado, a quantidade de conexões e a ordem de visita dos vértices.

## Resultado obtido

| Situação                         | BFS                           | DFS                           |
|----------------------------------|-------------------------------|-------------------------------|
| Antes do bloqueio                | 1 → 2 → 4 → 6 → 8 (4 conexões) | 1 → 2 → 4 → 6 → 8 (4 conexões) |
| `4-6` bloqueada                  | 1 → 2 → 4 → 5 → 6 → 8 (5 conexões) | 1 → 2 → 4 → 5 → 6 → 8 (5 conexões) |
| `4-6` e `4-5` bloqueadas         | nenhum caminho disponível     | nenhum caminho disponível     |

Ao bloquear `4-6`, o trajeto desvia por `5` e passa de 4 para 5 conexões. Ao bloquear também `4-5`, a conexão entre os dois blocos deixa de existir, e os dois algoritmos percorrem só o bloco `{1, 2, 3, 4}` sem chegar ao destino.

Neste grafo BFS e DFS encontram o mesmo caminho e visitam os vértices na mesma ordem (1, 2, 3, 4, 5, 6, 7, 8). Isso acontece por causa da forma do grafo e da ordem em que as arestas foram cadastradas, e não porque os algoritmos sejam equivalentes: o BFS garante o menor caminho em número de conexões, enquanto o DFS apenas acha um caminho.

## Escolhas de projeto

- **Lista de adjacência (`dict` de listas):** o grafo é esparso, então a estrutura ocupa O(V+E) de memória e percorrer os vizinhos de um vértice é direto.
- **Bloqueio por conjunto de arestas:** a conexão é marcada como bloqueada (`frozenset` com os dois vértices) em vez de ser removida. Assim é possível bloquear e desbloquear sem reconstruir o grafo, e o `frozenset` faz a aresta valer nos dois sentidos.
- **BFS com fila (`deque`):** explora por camadas. Em grafo sem pesos, o primeiro caminho que chega ao destino é o de menor número de conexões.
- **DFS com pilha, versão iterativa:** vai fundo por um ramo antes de voltar e acha um caminho, não necessariamente o mais curto. A versão iterativa evita estourar o limite de recursão do Python em grafos grandes.
- **Dicionário de pais:** tanto o BFS quanto o DFS guardam de qual vértice chegaram em cada um, e o caminho é reconstruído de trás para frente a partir do destino.

## Complexidade

BFS e DFS têm custo O(V + E) em tempo, com V vértices e E arestas, e O(V) de memória extra para visitados, fila ou pilha e pais.

## Estrutura

```
grafo_metro.py   código completo (modelo, BFS, DFS, simulação)
README.md        este arquivo
```
