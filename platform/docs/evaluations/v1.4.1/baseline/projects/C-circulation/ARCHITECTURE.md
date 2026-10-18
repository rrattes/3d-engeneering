# Decisão de arquitetura — módulo passivo de três câmaras

## Requisitos e incógnitas

- Envelope máximo: 160 × 100 × 90 mm, fornecido pelo usuário.
- Três câmaras conectadas em série, com entrada e saída acessíveis para mangueiras.
- Abertura para limpeza e geometria que facilite enchimento e ventilação.
- A vazão pretendida, o desnível disponível e as mangueiras ainda serão definidos.

## Alternativas consideradas

1. **Câmara comum com duas divisórias abertas no topo:** simples de fabricar e limpar, mas cria um percurso de superfície livre, depende da orientação e não controla a passagem entre câmaras.
2. **Labirinto fechado com canais elevados/sifões:** pode reduzir mistura direta, mas retém ar nos pontos altos e dificulta inspeção e limpeza.
3. **Três câmaras em série com transferências baixas e tampa removível:** percurso definido no corpo, cavidades acessíveis quando aberta e portas altas para enchimento/ventilação. Exige junta e fixação da tampa, que precisam de especificação e ensaio.

## Escolha

Selecionada a alternativa 3. O corpo é uma peça com três câmaras e duas divisórias; cada divisória tem um vão baixo de 30 × 16 mm. Bocais retos provisórios de 22 mm externos e 16 mm internos, com 18 mm de projeção, conectam as câmaras às mangueiras. A tampa é removível e contém um furo de 6 mm sobre cada câmara para enchimento/ventilação. O CAD nominal mede 160 × 78 × 58 mm, incluindo bocais e tampa.

A circulação é passiva somente sob diferença de carga suficiente. Não se infere vazão, perda de carga, autoescorva, remoção completa de ar ou estanqueidade. Os vãos baixos e as portas superiores são uma hipótese de projeto para avaliar em protótipo, não evidência de desempenho. Os três furos de purga precisam de tampões vedados durante operação; tampões não foram modelados.

## Interfaces e manutenção

Os bocais ficam nas faces opostas do eixo X. Diâmetros e comprimento são provisórios porque a mangueira não foi especificada; o bocal é liso e não inclui farpas ou retenção positiva, portanto verificar ajuste e abraçadeira antes da fabricação. A tampa expõe diretamente as três câmaras e os vãos. Junta e fixadores não foram modelados; a interface da tampa no assembly CAD representa apenas apoio/contato nominal.

## Verificação e limites da evidência

O percurso central foi amostrado contra o B-rep com raio declarado de 6 mm e passo de 2 mm. Esse ensaio comprova somente espaço livre amostrado. Ensaios futuros devem medir vazão em função do desnível, verificar vazamentos, facilidade de limpeza, compatibilidade da conexão e ar residual em orientações de uso. Nenhum CFD ou desempenho hidráulico foi realizado ou alegado.
