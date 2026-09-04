# pond-skimmer — instruções para o Claude

Skimmer de lago para cano PVC de 150 mm (ID 143–145, parede 3 mm), gerado por
script paramétrico (`manifold3d` + `trimesh`). Leia `README.md` e
`docs/DISCOVERY.md` antes de mexer — as lições de hidráulica e de CSG estão
lá e já custaram várias impressões.

## Regras

- **Fonte de verdade é o script**, não o STL. Mudança = editar constante no
  topo de `scripts/skimmer150.py` e regenerar. STL nunca é editado à mão.
- `CrossSection` sempre **anti-horário** no plano (r, z): CW = furo = manifold vazio.
- **Pares que encaixam**: `corpo150_turbo` ↔ `cesto v3`/`v4`;
  `corpo150_petg` ↔ `cesto v5`. Nunca misturar. Todo cesto novo passa pelo
  `tools/check_fit.py` contra o corpo do par (0 colisão assentado e em
  +20/+50 mm; 1 corpo; estanque; assento com acomodação < 2 mm).
- **Versionamento**: o que está no lago está em `docs/IMPRESSO.md` (arquivo,
  material, data, SHA-256) e numa tag `vN.N-instalado`. Ao imprimir e
  instalar um conjunto novo: atualizar IMPRESSO.md, CHANGELOG.md e criar a
  tag. Mudança de geometria = entrada no CHANGELOG.
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
./venv/bin/python scripts/skimmer150.py
./venv/bin/python tools/check_fit.py stl/v2.0-petg/corpo150_petg.stl stl/v2.0-petg/cesto150_v5.stl
```
