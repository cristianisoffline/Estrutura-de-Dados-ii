"""
Desafio individual - Grafos, BFS e DFS (Estrutura de Dados II)

PROBLEMA
    Se uma conexão aérea fica indisponível (pane de navegação), ainda existe
    caminho de Brasília até Natal? Qual é a rota alternativa?

GRAFO
    G = (V, E), não dirigido, em lista de adjacência (dict).
    V: 10 aeroportos | E: 14 conexões (ver ARESTAS).

BUSCAS
    BFS: fila. Retorna o caminho com MENOS conexões.
    DFS: pilha. Retorna ALGUM caminho (não garante o menor).

CENÁRIO (único)
    Antes : rede integral
    Depois: conexão Salvador-Recife indisponível

CONCLUSÃO
    A BFS encontra a melhor rota alternativa (pelo norte, mesmo nº de voos).
    A DFS só garante que existe caminho, não que seja o menor.

USO
    python rede_nordeste_bfs_dfs.py   ->   gera 'diagrama.png' (precisa de matplotlib)
"""

from collections import deque

ARESTAS = [
    ("Brasília", "Salvador"), ("Brasília", "Belo Horizonte"), ("Brasília", "Teresina"),
    ("Belo Horizonte", "Salvador"), ("Salvador", "Aracaju"), ("Salvador", "Recife"),
    ("Aracaju", "Maceió"), ("Maceió", "Recife"), ("Recife", "Natal"),
    ("Recife", "Fortaleza"), ("Natal", "Fortaleza"), ("Fortaleza", "Teresina"),
    ("Fortaleza", "São Luís"), ("Teresina", "São Luís"),
]
ORIGEM, DESTINO = "Brasília", "Natal"
BLOQUEIO = ("Salvador", "Recife")


def construir_grafo(arestas):
    grafo = {}
    for a, b in arestas:
        grafo.setdefault(a, []).append(b)
        grafo.setdefault(b, []).append(a)
    return grafo


def bloquear(grafo, a, b):
    """Cópia do grafo sem a conexão a-b."""
    return {v: [w for w in viz if {v, w} != {a, b}] for v, viz in grafo.items()}


def bfs(grafo, origem, destino):
    fila = deque([(origem, [origem])])
    visitados = {origem}
    while fila:
        atual, caminho = fila.popleft()
        if atual == destino:
            return caminho
        for v in grafo[atual]:
            if v not in visitados:
                visitados.add(v)
                fila.append((v, caminho + [v]))
    return None


def dfs(grafo, origem, destino):
    pilha = [(origem, [origem])]
    visitados = set()
    while pilha:
        atual, caminho = pilha.pop()
        if atual in visitados:
            continue
        visitados.add(atual)
        if atual == destino:
            return caminho
        for v in reversed(grafo[atual]):
            if v not in visitados:
                pilha.append((v, caminho + [v]))
    return None


def mostrar(c):
    return "sem caminho" if c is None else f"{' -> '.join(c)} ({len(c) - 1} voos)"


def testes(grafo):
    assert bfs(grafo, ORIGEM, DESTINO) is not None
    assert len(bfs(grafo, ORIGEM, DESTINO)) <= len(dfs(grafo, ORIGEM, DESTINO))
    assert bfs(grafo, "Natal", "Natal") == ["Natal"]
    g2 = bloquear(grafo, *BLOQUEIO)
    assert "Recife" not in g2["Salvador"] and "Salvador" not in g2["Recife"]
    assert "Recife" in grafo["Salvador"]  # original intacto
    assert bfs(g2, ORIGEM, DESTINO) is not None
    print("Testes ok.\n")


POSICOES = {
    "Brasília": (0.5, 4.0), "Belo Horizonte": (2.5, 0.0), "Salvador": (5.5, 2.0),
    "Aracaju": (8.5, 0.5), "Maceió": (11.0, 2.0), "Recife": (10.0, 4.5),
    "Natal": (11.0, 7.5), "Fortaleza": (7.0, 8.0), "Teresina": (3.5, 7.0),
    "São Luís": (1.5, 9.5),
}


def desenhar(caminho, arquivo="diagrama.png"):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib não instalado: diagrama não gerado.")
        return
    rota = {frozenset(p) for p in zip(caminho, caminho[1:])}
    fig, ax = plt.subplots(figsize=(9, 7))
    for a, b in ARESTAS:
        (x1, y1), (x2, y2) = POSICOES[a], POSICOES[b]
        par = frozenset((a, b))
        if par == frozenset(BLOQUEIO):
            ax.plot([x1, x2], [y1, y2], "--", color="#D62828", lw=3)
        elif par in rota:
            ax.plot([x1, x2], [y1, y2], "-", color="#1B9E5A", lw=5)
        else:
            ax.plot([x1, x2], [y1, y2], "-", color="#B8B0C4", lw=2)
    for v, (x, y) in POSICOES.items():
        ax.scatter(x, y, s=2300, color="#1B9E5A" if v in caminho else "#5B2A86", zorder=3)
        ax.text(x, y, v.replace(" ", "\n"), color="white", ha="center", va="center",
                fontsize=8, zorder=4)
    ax.set_title(f"{ORIGEM} -> {DESTINO} com {BLOQUEIO[0]}-{BLOQUEIO[1]} indisponível\n"
                 "verde = rota da BFS | vermelho tracejado = bloqueio")
    ax.axis("off")
    ax.margins(0.12)
    fig.tight_layout()
    fig.savefig(arquivo, dpi=130)
    print(f"Diagrama salvo em {arquivo}")


def main():
    grafo = construir_grafo(ARESTAS)
    testes(grafo)
    print(f"Consulta: {ORIGEM} -> {DESTINO}\n")
    print("ANTES (rede integral)")
    print("  BFS:", mostrar(bfs(grafo, ORIGEM, DESTINO)))
    print("  DFS:", mostrar(dfs(grafo, ORIGEM, DESTINO)))
    g2 = bloquear(grafo, *BLOQUEIO)
    c_bfs = bfs(g2, ORIGEM, DESTINO)
    print(f"\nDEPOIS ({BLOQUEIO[0]}-{BLOQUEIO[1]} indisponível)")
    print("  BFS:", mostrar(c_bfs))
    print("  DFS:", mostrar(dfs(g2, ORIGEM, DESTINO)))
    desenhar(c_bfs)


if __name__ == "__main__":
    main()
