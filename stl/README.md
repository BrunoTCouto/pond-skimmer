# STLs por versão

Cada pasta é um **conjunto que encaixa entre si**. Não misture corpo de uma
versão com cesto de outra — o encaixe do cesto muda a cada versão.

| Pasta | Conjunto | Status | Par que encaixa |
|---|---|---|---|
| [`v1.0-instalado/`](v1.0-instalado/) | corpo turbo (ABS) + cesto v3 (PLA) — o que está **no lago** | impresso e instalado, set/2026 | `corpo150_turbo` ↔ `cesto150_v3` ou `cesto150_v4` |
| [`v2.0-petg/`](v2.0-petg/) | corpo com anel de assento a 45° + cesto v5 (72 fendas) | pronto pra imprimir em PETG | `corpo150_petg` ↔ `cesto150_v5` **somente** |

O corpo (coroa de 80 mm, 80 fendas de 3 mm) é o mesmo nas duas versões; o que
muda é **como o cesto se apoia**:

```
v1.0  cesto v3: 3 pilares sobem até o topo da coroa e apoiam por abinhas
      cesto v4: cone de 13° casa com o chanfro do furo da saia (trava, tipo cone Morse)
v2.0  cesto v5: borda a 45° encosta num anel de assento dentro da saia (batente, solta fácil)
```

Como nasce cada arquivo: `python scripts/skimmer150.py` gera todos, direto
nas pastas. STL nunca é editado à mão. Detalhes de cada versão no
[CHANGELOG](../CHANGELOG.md); o que está fisicamente instalado (com SHA-256)
em [docs/IMPRESSO.md](../docs/IMPRESSO.md).

Antes de imprimir um cesto, confira o par:

```bash
python tools/check_fit.py stl/<versao>/corpo*.stl stl/<versao>/cesto*.stl
```
