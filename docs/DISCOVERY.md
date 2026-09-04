# Discovery — o que aprendemos fazendo o skimmer

Diário das decisões, erros e medições do projeto, na ordem em que aconteceram.
Serve de memória pra quem (humano ou Claude) for mexer de novo.

## 1. Ponto de partida

- Arquivo: `Skimmer.3mf` do Bambu Studio, 2 plates (`Outside.STEP`,
  `Inside.STEP`), só malhas (150k/200k faces). Sem CAD paramétrico → não dá
  pra "mudar uma medida"; a saída foi remodelar do zero em Python.
- Medidas do original (extraídas da malha, eixo Y): luva Ø110 interna
  (~120 mm), cone Ø110→140 (50 mm), cesta ranhurada Ø140/146 (80 mm). Cesto
  interno Ø139,8 (folga 0,1 mm) com fendas que giram pra regular a abertura.
- Restrições do dono: cano de **150 mm** e **o nível da água não pode subir**
  da borda do cano. O original é um "pescoço" de 130 mm em cima do cano —
  incompatível com a segunda restrição.

## 2. Medidas do cano

- Externo "150" medido; interno **143–145**; parede **3 mm** (PVC esgoto).
- Saia de centragem: Ø136 na ponta → **Ø142 na borda**. Nunca pode chegar em
  143: se a saia calçar antes da flange apoiar, a peça fica suspensa e os
  canais de entrada sobem junto.

## 3. Hidráulica (a lição cara)

O cano nu é um vertedouro de **450 mm** de perímetro. Qualquer coisa que se
coloque em cima dele reduz o perímetro aberto na **linha d'água** — e é só
isso que define o nível:

    Q ≈ 1,7 · L · h^1,5     (vertedouro; L = perímetro aberto, h = lâmina)

- v1: fenda de 3 mm a cada 12 mm (25% aberto) × banda do cesto (79%) → L ≈
  **85 mm**. Com a bomba do lago (estimada em 2–3 L/s pela foto), h > 55 mm
  → passou por cima da coroa.
![altura não é vazão](images/nivel_altura_nao_ajuda.png)

- Coisas que **não** mudam o nível: altura da coroa (fenda seca é parede),
  grade em vez de fenda (paga barra nas duas direções: 3×3 com barra de 2 =
  36% aberto, pior que fenda), formato do furo.
- Coisas que mudam: costela mais fina (limite de impressão ~2,4 mm), vão
  maior (passa peixe), perímetro maior (v2).
- turbo: 80 fendas × 3 mm, costela 2,4 mm, sem banda → 54% → L ≈ **248 mm**.
  Estimativa: h ≈ 28 mm a 2 L/s, 37 mm a 3 L/s (cano nu: 19 / 25 mm).
- Entupimento: com 30% das fendas tapadas h sobe ~25%. Limpar a coroa faz
  parte.
- Qualquer barreira de 3 mm sempre pede alguns mm de lâmina a mais que o
  cano aberto. Se isso for inaceitável, só a v2 (cerca) resolve.

## 4. Peixes

- O que barra peixe é a **menor dimensão** do vão, não a inclinação.
- Fendas diagonais valem por outro motivo: soltam detrito (nada fica
  entalado em pé) e são ~15% mais compridas → deu pra estreitar 5→3 mm sem
  perder área.
- Cesto com fendas de 2,5 mm atrás de uma coroa de 3 mm retém só a faixa
  2,5–3: quase nada. Um alevino que passou pela coroa seguia pro cano → bomba.
  **Regra: fendas do cesto (2 mm) menores que o gate da coroa (3 mm)** —
  tudo que entra fica no cesto, vivo, até a limpeza.
- Peixe no cesto não asfixia (água corrente), mas apanha da queda d'água e
  seca se a bomba desligar. Não é lugar de peixe.

## 5. CSG com manifold3d — pegadinhas que custaram iterações

1. `Manifold.cylinder(h, r_baixo, r_topo)`: a ordem é **base → topo**. Cone
   invertido aconteceu **três vezes** (saia, transição do cesto, e de novo na
   v2). Sintoma: peça em vários corpos ou dimensões espelhadas.
2. Dois sólidos que se tocam só num plano (z=0) **não viram um corpo**:
   `split()` do trimesh mostra 2 shells. Sempre um "anel de solda" com
   sobreposição volumétrica (ex.: `tube(71.5, 70.2, -2, 3.5)` entre saia e
   flange).
3. Corte inclinado (fenda diagonal) numa parede cilíndrica: a caixa reta
   deriva tangencialmente e precisa começar bem pra dentro (r=50–58) pra cobrir
   a parede curva nos extremos. Aí ela **morde** o que estiver dentro (o cone
   do fundo). Solução: `cortes ^ tube(anel da parede)`.
4. Chanfro embaixo da aba do cesto colidia com o topo da coroa. Flat-on-flat
   com balanço de ≤2,7 mm imprime bem; não vale chanfro.
5. Reforço triangular plano num furo redondo: as pontas passam do raio do
   furo (r 71,6 > 70). Clipar com `^ tube(69.3, ...)`.
6. Verificação que sempre roda antes de entregar: `split()` = 1 corpo;
   `contains()` do corpo sobre os vértices do cesto em 0/+20/+50 mm de
   inserção = 0; perímetro aberto amostrado em grade (θ, z) nas duas paredes
   em série; corte (r, z) plotado com o cano sobreposto.

## 6. Impressão

- Corpo: de cabeça pra baixo (topo da coroa na mesa) com chanfro de 45° entre
  coroa e flange pra não haver balanço horizontal. 80 torres de 2,4 × 4 mm:
  os 2 anéis de travamento existem pra amarrar as torres na impressão, não
  só pra rigidez.
- Cesto: em pé. Cone do fundo a 45°, botão com cone de 45° sob a cabeça.
- **Anel apoiado em 4 pilares = anel no ar** entre os pilares (~100 mm sem
  apoio). Não imprime; suporte em árvore de 8 cm dentro do cesto é ridículo.
  → v3: cada pilar termina na sua própria abinha; 3 pilares (assenta sem
  balançar, 5% de bloqueio).
- v4 elimina os pilares: o cesto assenta num cone de 13° que casa com o
  chanfro interno da saia (r 68 @ z-10 → 70,3 @ z0). Desce ~1,4 mm e trava
  com contato de área; nada acima da borda. Feito pra reimpressão em PETG.
- Materiais: ABS e PETG são definitivos em água. PLA dura semanas/meses (só
  amolece >55 °C), mas é quebradiço.
- Bambu Studio com suporte automático planta árvores pras abinhas de 2,7 mm.
  Deixar **desligado**.

## 7. Ambiente

- OpenSCAD não instalado; `manifold3d` + `trimesh` no venv resolvem tudo,
  inclusive booleans robustos e `section()` pra cortes.
- `trimesh.section` precisa de `scipy`, `shapely`, `networkx`, `rtree`;
  `proximity.signed_distance` é lento — `contains()` com amostragem `[::4]`
  basta.
- macOS não tem `timeout`.
- O sandbox do Claude Code barra `cp` para `~/Downloads` e SSH pro GitHub;
  entregar via SendUserFile e usar HTTPS (`gh auth`).
- O scratchpad é volátil: foi apagado uma vez e o script teve que ser
  reconstruído. **Por isso existe este repo.**
