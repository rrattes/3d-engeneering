# Organizador modular de bancada — relatório de conceito CAD3D

## Decisão de arquitetura

Comparei duas soluções:

| Conceito | Vantagens | Custos e riscos |
|---|---|---|
| Cestas removíveis em matriz de soquetes | Retirada vertical, acesso superior aberto e posições reconfiguráveis sem ferramenta | Encaixe depende de calibração FDM; sem retenção positiva contra levantamento ou tombamento |
| Cartuchos em trilhos laterais | Retenção lateral durante o uso | Exige curso livre nas extremidades, alinhamento ao inserir e controle de folga para evitar emperramento |

Escolhi as cestas removíveis. Para uso estacionário em bancada, a extração vertical é direta, os alívios no rebordo ajudam a pinçar ferramentas e a matriz oferece seis posições. A escolha deve ser revista se o organizador for transportado ou inclinado com frequência.

## Geometria de conceito

- Envelope interno informado: **180 × 120 × 70 mm**. Foi tratado como limite disponível, sem folga de instalação adicional porque ela não foi especificada.
- Base: **174 × 114 × 4,5 mm**, com matriz de **3 × 2** posições a **56 mm** de passo.
- Cestas atuais: três módulos abertos, cada um com envelope de **50 × 50 × 63 mm**, incluindo pinos; altura interna nominal de **57,6 mm**, largura interna nominal de **46 mm**, parede de **2 mm** e fundo de **2,4 mm**.
- Quatro pinos de **Ø4 mm** por cesta entram em soquetes cegos de **Ø5,2 mm**, profundidade de **3,2 mm**. A folga radial nominal é **0,6 mm**, ainda não calibrada.
- Alívios de pega nos quatro lados: **18 × 15 mm**. O topo permanece aberto.
- Envelope calculado da montagem: **174 × 114 × 64,5 mm**. A matriz tem outras posições disponíveis para movimentação dos módulos.

As dimensões das cestas são parâmetros de arquitetura, não estimativas das ferramentas. O modelo tem comprimento, largura e altura independentes para cada categoria em `.cad3d/params.yaml`; ajuste esses valores após medir os objetos. A configuração atual não comprova capacidade para as ferramentas reais.

## Como resolver a incerteza dos objetos

Para cada categoria, registre:

1. Quantidade de cada objeto e dimensões máximas de comprimento, largura e altura na orientação em que será guardado.
2. Espaço necessário para dedos ou pinça ao retirar o objeto e se ele pode ser empilhado.
3. Massa aproximada e se o conjunto será transportado ou permanecerá na bancada.

Meça com paquímetro ou régua e teste uma cesta de protótipo com os objetos reais. Atualize `category_a_length/width/height`, `category_b_*` e `category_c_*`; verifique se as cestas adjacentes ainda têm folga e se a base continua dentro do envelope. Depois, calibre `socket_clearance` com um corpo de prova impresso na mesma máquina, material e orientação. Não declare capacidade até concluir a prova de encaixe e retirada.

## Validação e fabricação

- **CAD3D:** B-rep válido; montagem sem interseções; trajetórias verticais amostradas para remoção das três cestas sem bloqueios.
- **Envelope:** PASS, com evidência calculada e conferida contra as dimensões CAD3D.
- **Acesso:** PASS para um percurso superior central genérico de raio **1 mm**. Isso confirma uma abertura geométrica central, não a pegada ou retirada de ferramentas ainda não medidas.
- **Capacidade para objetos:** NOT_EVALUATED, por falta de dimensões e quantidades reais.
- **Impressão:** as quatro peças cabem geometricamente no perfil Bambu Lab A1 carregado e os STEP reabriram; os STL exportados são watertight. A avaliação heurística de fabricação continua em WARNING. Não foi feita fatiagem nem validação física.
- **Revisão CAD3D:** WARNING / `CONDITIONAL_REVIEW`; não liberar como produto final antes de validar capacidade, folga impressa e retenção na bancada.

## Arquivos produzidos

- Projeto paramétrico: `src/model.py`, `.cad3d/params.yaml`, `.cad3d/assembly.yaml`.
- Contrato de engenharia e estudo de conceitos: `.cad3d/engineering.yaml`.
- Relatório legível: `RELATORIO.md`.
- Relatórios CAD3D: `build/outputs/report.json`, `build/outputs/validation.json`, `build/outputs/architecture-review.json` e `build/outputs/design-review.json`.
- Exportações STEP/STL por peça e vistas técnicas: diretório `build/outputs/`.
