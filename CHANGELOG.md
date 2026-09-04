# Changelog

Versões do conjunto (corpo + cesto). Tags git marcam o que foi impresso; o que
está fisicamente no lago está em [docs/IMPRESSO.md](docs/IMPRESSO.md).

## v2.0 — conjunto PETG (não impresso ainda)

Reimpressão definitiva das duas peças, preparada em 2026-09-04.

- `stl/v2.0-petg/corpo150_petg.stl`: coroa turbo idêntica à v1.0 (80 fendas × 3 mm,
  80 mm, 2 anéis, parede 4 mm) + **anel de assento a 45° dentro da saia**
  (z −9 a −4,8; r 64,5 → 68,7). Impresso de ponta-cabeça o anel cresce pra
  dentro a 45° e termina reto — imprime sem suporte. Sem o chanfro do furo.
- `stl/v2.0-petg/cesto150_v5.stl`: borda a 45° que assenta no anel (batente
  positivo, autocentrante, não trava); colar Ø135 com 0,7 mm de folga no furo
  da saia; topo em z −3 (nada acima da borda do cano);
  **72 fendas** de 2 mm na parede (43% aberta, o dobro do v3/v4); fundo em
  cone com 72 fendas de 2 mm; botão.
- Pares: `corpo150_petg` ↔ `cesto150_v5` **somente**. O v5 não tem onde
  apoiar no corpo v1.0 (cai 8 mm até bater na saia).
- Verificação: 1 corpo cada, 0 colisões em 0/+20/+50 mm, assenta no anel
  com 0,4 mm de acomodação, perímetro aberto 52% → 240 mm de vertedouro
  equivalente.

## v1.0 — instalado (tag `v1.0-instalado`)

O que está no lago desde 2026-09-03/04.

- `stl/v1.0-instalado/corpo150_turbo.stl` — ABS. Coroa 80 mm, 80 fendas de 3 mm a 20°,
  costelas ~2,4 mm, parede 4 mm, 2 anéis de travamento, canais na borda a
  cada 2 fendas, saia Ø136→142 com chanfro interno de 13° no furo.
- `stl/v1.0-instalado/cesto150_v3.stl` — PLA (provisório). 3 pilares 8×3 com abinha no topo
  da coroa e reforço de 45° na base; 36 fendas de 2 mm a 30° na parede;
  fundo em cone; botão.
- Também compatível com esse corpo: `stl/v1.0-instalado/cesto150_v4.stl` (assenta no
  chanfro de 13° da saia; nunca impresso — o cone raso trava, ver DISCOVERY).

## v0 — v1 original (superada, arquivos não preservados)

- Coroa de 55 mm com 36 fendas de 3 mm + banda giratória no cesto (regulagem
  0–3 mm). Impressa; a água passou por cima da coroa (vertedouro equivalente
  ~85 mm). Lição registrada em `docs/DISCOVERY.md`.
