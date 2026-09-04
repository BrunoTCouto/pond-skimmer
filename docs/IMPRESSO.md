# O que está instalado no lago

Nota de referência: se um dia precisar reimprimir **exatamente** o que está lá,
ou saber se um STL novo ainda encaixa, é isto aqui. Tag git: `v1.0-instalado`.

| Peça | Arquivo | Material | Impresso em | SHA-256 do STL |
|---|---|---|---|---|
| Corpo | `stl/v1.0-instalado/corpo150_turbo.stl` | ABS (Bambu P1S, 0.20 mm Strength, 6 paredes) | 2026-09-03 | `074b1c6b4e48bdd89bbbf02e807f4427c8351a55aac63afd9d6b18c8bbf55f60` |
| Cesto | `stl/v1.0-instalado/cesto150_v3.stl` | PLA genérico (provisório até o PETG) | 2026-09-04 | `d25568b3e3782798a476feef0245259df0fc708bc4a71bad1f325fb9b63d41ca` |

Conferir se o arquivo atual ainda é o impresso:

```bash
shasum -a 256 stl/v1.0-instalado/corpo150_turbo.stl stl/v1.0-instalado/cesto150_v3.stl
```

Se o hash mudou, o script foi alterado e o STL **não** é mais o que está no
lago — o par de referência continua sendo o hash acima (recuperável com
`git show v1.0-instalado:stl/v1.0-instalado/corpo150_turbo.stl > corpo_impresso.stl`).

## Observações de campo

- Cano: PVC esgoto, externo 149–151, interno 143–145, parede 3 mm.
- A saia (Ø142 na borda) entra com folga; a flange apoia na borda.
- Cesto v3 apoia pelas 3 abinhas no topo da coroa, em qualquer ângulo.
- Plano: substituir **as duas peças** pelo conjunto PETG (v2.0) — corpo com
  anel de assento + cesto v5. Aí este arquivo deve ser atualizado e uma tag
  `v2.0-instalado` criada.
