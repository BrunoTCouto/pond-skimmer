# pond-skimmer — instruções para o Claude

Skimmer de lago para cano PVC de 150 mm (ID 143–145, parede 3 mm), gerado por
script paramétrico (`manifold3d` + `trimesh`). Leia `README.md` e
`docs/DISCOVERY.md` antes de mexer — as lições de hidráulica e de CSG estão
lá e já custaram várias impressões.

## Regras

- **Fonte de verdade é o script**, não o STL. Mudança = editar constante no
  topo de `scripts/skimmer150.py` e regenerar. STL nunca é editado à mão.
- O corpo `stl/corpo150_turbo.stl` está **impresso e instalado**. Cesto novo
  tem que encaixar nele: rodar `tools/check_fit.py` contra esse STL exato
  antes de entregar (0 colisão assentado e em +20/+50 mm; 1 corpo; estanque).
- Gate de peixe: coroa **3 mm**; fendas do cesto **2 mm** (sempre menores
  que a coroa). Não mexer sem falar com o dono.
- Nível do lago = perímetro aberto na linha d'água. Altura de coroa, grade e
  formato de furo **não** mudam o nível. Não propor de novo.
- Toda peça nova precisa imprimir **sem suporte**: em pé (cesto) ou de cabeça
  pra baixo (corpo); balanço horizontal máximo ~2,7 mm; nada de anel apoiado
  em pilares.
- `Manifold.cylinder(h, r_base, r_topo)`. Sólidos que só se tocam num plano
  não se fundem — anel de solda. Cortes inclinados confinados ao anel da
  parede. Fins/reforços planos clipados ao raio do furo.
- Código e comentários em inglês; docs e conversa com o dono em pt-BR.
- Entregar STL via SendUserFile (o sandbox barra `cp ~/Downloads`).

## Comandos

```bash
python3 -m venv venv && ./venv/bin/pip install -r requirements.txt
cd stl && ../venv/bin/python ../scripts/skimmer150.py
../venv/bin/python ../tools/check_fit.py corpo150_turbo.stl cesto150_v4.stl
```
