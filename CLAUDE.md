# pond-skimmer — instruções para o Claude

Skimmer de lago para cano PVC de 150 mm (ID 143–145, parede 3 mm), gerado por
script paramétrico (`manifold3d` + `trimesh`). Leia `README.md` e
`docs/DISCOVERY.md` antes de mexer — as lições de hidráulica e de CSG estão
lá e já custaram várias impressões.

## Regras

- **Fonte de verdade é o script**, não o STL. Mudança = editar constante no
  topo de `scripts/skimmer150.py` e regenerar. STL nunca é editado à mão.
- `CrossSection` sempre **anti-horário** no plano (r, z): CW = furo = manifold vazio.
- **Uma pasta `stl/<versão>/` por pedido do dono, e pasta é IMUTÁVEL.**
  Qualquer mudança de geometria — mesmo um décimo de milímetro — é uma
  entrada nova em `VERSIONS` (fim de `scripts/skimmer150.py`), uma pasta
  nova com README curto (o pedido, o que mudou, arquivos) e uma entrada no
  CHANGELOG. **Nunca editar ou regenerar uma pasta existente.** Nome:
  `vX.Y-<apelido>`; arquivos `corpo150_vX.Y.stl` / `cesto150_vX.Y.stl`.
  Toda pasta tem `preview.png` (3D + corte assentado) gerado por
  `tools/render.py` (itera `VERSIONS`) e referenciado no README da pasta.
  (Isso foi exigido pelo dono depois de eu sobrescrever `v2.0-petg` três vezes.)
- Corpo e cesto de uma pasta encaixam entre si; nunca misturar pastas. Todo
  par novo passa pelo `tools/check_fit.py` (0 colisão assentado e em
  +20/+50 mm; 1 corpo; estanque; acomodação < 2 mm).
- **README = versão mais atual, sempre** — texto, tabela, figura de capa.
  Ao criar versão nova: atualizar `LATEST` em `scripts/skimmer150.py` e
  `LATEST*` em `tools/render.py`, rodar `render.py`, atualizar o README.
  Versões antigas ficam em `stl/README.md`, nas pastas e no CHANGELOG.
- O que está no lago está em `docs/IMPRESSO.md` (arquivo, material, data,
  SHA-256) e numa tag `vX.Y-instalado`. Ao imprimir e instalar: atualizar
  IMPRESSO.md, CHANGELOG.md e criar a tag.
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
./venv/bin/python scripts/skimmer150.py                    # todas as pastas de stl/
./venv/bin/python scripts/skimmer150.py v2.3-petg-45-folga # só uma
./venv/bin/python tools/check_fit.py stl/v2.3-petg-45-folga/corpo150_v2.3.stl stl/v2.3-petg-45-folga/cesto150_v2.3.stl
./venv/bin/python tools/render.py
```
