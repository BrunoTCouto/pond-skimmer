# Changelog

Uma pasta em `stl/` por pedido do dono; **pasta é imutável** — mudança nova é
versão nova. Tags git marcam o que foi impresso e instalado; o que está
fisicamente no lago está em [docs/IMPRESSO.md](docs/IMPRESSO.md).

## v2.3-petg-45-folga — atual (não impressa ainda) — 2026-09-04

"A versão de antes tava boa — fecha a versão boa." Volta o anel de assento a
45° da v2.0/v2.1, mantendo a folga de 0,7 mm no colar que veio da v2.2.
`corpo150_v2.3.stl` + `cesto150_v2.3.stl` (72 fendas, colar Ø135).
Verificação: 1 corpo cada, 0 colisões em 0/+20/+50 mm, 0,4 mm de acomodação
no anel, 52% do perímetro aberto (240 mm de vertedouro equivalente).

## v2.2-petg-prateleira — 2026-09-04

"Chanfro de suporte mais fácil de imprimir: parte de baixo sobe inclinado,
parte de cima reta." Assento vira prateleira reta de 2,2 mm com 60° embaixo;
cesto com colar reto Ø135 (folga 0,7 mm — a v2.0/v2.1 tinham 0,2–0,6, apertado
pra PETG). Imprime; na orientação invertida é equivalente ao 45°. Superada.

## v2.1-petg-72fendas — 2026-09-04

"Dá pra aumentar a quantidade de vãos na lateral do cesto?" Fendas da parede
do cesto 36 → 72 (43% aberta, o dobro). Corpo igual à v2.0.

## v2.0-petg — 2026-09-04

"Fazer todos os modelos novos, preparar tudo pro PETG." Corpo com **anel de
assento a 45° dentro da saia** (z −9 a −4,8; r 64,5 → 68,7), sem o chanfro do
furo; cesto sem pilares, borda a 45° que assenta no anel, 36 fendas, colar
Ø136. Motivação: o cone de 13° do v4 trava (cone Morse); o anel de 45° é um
batente que autocentra e solta fácil.

## v1.0-instalado — tag `v1.0-instalado` — 2026-09-03/04

O que está no lago.

- `corpo150_turbo.stl` — ABS. Coroa 80 mm, 80 fendas de 3 mm a 20°, costelas
  ~2,4 mm, parede 4 mm, 2 anéis de travamento, canais na borda a cada 2
  fendas, saia Ø136→142 com chanfro interno de 13° no furo.
- `cesto150_v3.stl` — PLA (provisório). 3 pilares 8×3 com abinha no topo da
  coroa e reforço de 45° na base; 36 fendas de 2 mm; fundo em cone; botão.
- `cesto150_v4.stl` — também encaixa nesse corpo (assenta no chanfro de 13°;
  nunca impresso — o cone raso trava).

## v0 — original (superada, arquivos não preservados)

Coroa de 55 mm com 36 fendas de 3 mm + banda giratória no cesto. Impressa; a
água passou por cima (vertedouro equivalente ~85 mm). Lição em
`docs/DISCOVERY.md`.
