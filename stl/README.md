# STLs por versão

**Uma pasta por pedido, e pasta é imutável.** Cada mudança — por menor que
seja — vira uma pasta nova; a anterior fica exatamente como estava. Assim
qualquer STL que já foi baixado ou impresso continua rastreável. A versão
mais recente é a que o README principal mostra.

Corpo e cesto de uma pasta encaixam **entre si**. Não misture pastas.

| Pasta | O que mudou | Corpo | Cesto | Status |
|---|---|---|---|---|
| [`v1.0-instalado/`](v1.0-instalado/) | corpo turbo (80 fendas, coroa 80 mm) + cesto v3 em pilares | `corpo150_turbo.stl` | `cesto150_v3.stl` (`cesto150_v4.stl` também encaixa) | **no lago** — ABS + PLA |
| [`v2.0-petg/`](v2.0-petg/) | primeiro conjunto PETG: anel de assento a 45° dentro da saia; cesto sem pilares | `corpo150_v2.0.stl` | `cesto150_v2.0.stl` — 36 fendas, colar Ø136 | superada |
| [`v2.1-petg-72fendas/`](v2.1-petg-72fendas/) | fendas da parede do cesto 36 → **72** | `corpo150_v2.1.stl` | `cesto150_v2.1.stl` — 72 fendas, colar Ø136 | superada |
| [`v2.2-petg-prateleira/`](v2.2-petg-prateleira/) | assento vira prateleira reta de 2,2 mm com 60° embaixo; colar com folga 0,7 mm | `corpo150_v2.2.stl` | `cesto150_v2.2.stl` — colar reto Ø135 | superada (dono preferiu o 45°) |
| [`v2.3-petg-45-folga/`](v2.3-petg-45-folga/) | volta o anel de 45°, mantém a folga de 0,7 mm no colar | `corpo150_v2.3.stl` | `cesto150_v2.3.stl` — 72 fendas, colar Ø135 | **atual** — imprimir em PETG |

Comum a todas: coroa de 80 mm com 80 fendas de 3 mm, saia Ø136→142 dentro do
cano, aro na borda; cesto com fendas de 2 mm, fundo em cone e botão.

Como nasce cada arquivo: `python scripts/skimmer150.py` gera **todas** as
pastas a partir da tabela `VERSIONS` no fim do script (ou
`python scripts/skimmer150.py v2.3-petg-45-folga` pra uma só). STL nunca é
editado à mão. Detalhes de cada versão no [CHANGELOG](../CHANGELOG.md); o que
está fisicamente instalado (com SHA-256) em [docs/IMPRESSO.md](../docs/IMPRESSO.md).

Antes de imprimir, confira o par:

```bash
python tools/check_fit.py stl/<pasta>/corpo*.stl stl/<pasta>/cesto*.stl
```
