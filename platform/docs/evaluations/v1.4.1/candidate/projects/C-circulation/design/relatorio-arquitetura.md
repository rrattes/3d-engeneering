# Relatório de arquitetura — módulo de circulação passiva

## Requisitos e hipótese de projeto

- Envelope máximo informado: 160 × 100 × 90 mm.
- Módulo conceitual com três câmaras em série, entrada e saída em espigões opostos, e tampa removível para acesso de limpeza.
- Diâmetro real das mangueiras, desnível de operação, vazão e necessidade de estanqueidade não foram informados. Para modelar as interfaces, adotei espigão OD 12 mm / passagem ID 8 mm e corpo 124 × 80 × 48 mm; esses valores são hipóteses, não medições.

## Alternativas avaliadas

| Arquitetura | Vantagens | Custos e riscos |
|---|---|---|
| Câmaras alinhadas com janelas inferiores largas | Inspeção direta por cima, percurso compacto e poucas junções; tampa removível facilita limpeza. | Usa comprimento em planta; sedimentos podem se acumular nas janelas; purga ainda depende da instalação e do enchimento. |
| Câmaras empilhadas ligadas por tubos | Menor área em planta. | Trechos e junções ficam menos acessíveis, aumentam as interfaces de vedação e podem criar pontos altos propensos a reter ar. |

**Escolha:** câmaras alinhadas, com duas divisórias e aberturas inferiores nominais de 34 × 14 mm. A escolha prioriza limpeza e inspeção; não implica vazão ou purga garantidas. A escolha pode mudar quando forem conhecidos o espaço de instalação e o desnível disponível.

## Geometria paramétrica e verificação CAD

- Corpo: envelope B-rep de 160 × 80 × 48 mm, incluindo espigões de 18 mm em cada extremidade; tampa: 124 × 80 × 3 mm, posicionada com folga de 0,3 mm acima do aro.
- Envelope da montagem posicionada: 160 × 80 × 51,3 mm, dentro do limite informado.
- Os dois canais de transferência foram desenhados no fundo interno. A rota declarada usa centro em z=10 mm pelas janelas e raio de folga amostrado de 2 mm.
- `cad3d architecture validate --geometry`: rota FLOW-WATER **PASS**, 1.737 amostras sem interseção com os sólidos. É verificação de espaço geométrico amostrado, não cálculo de escoamento.
- `cad3d build`: sólidos B-rep válidos, montagem sem colisão; folga corpo/tampa 0,3 mm e trajetória de remoção da tampa aprovada em 9 posições amostradas.
- `cad3d render --view engineering`: vistas iso, ortográficas, seção, explodida, componente oculto e interface geradas e inspecionadas.
- STEP e STL exportados para os componentes `body` e `lid`.

## Limites e próximos dados necessários

- Vazão, perda de carga, priming, retenção de ar, estanqueidade e comportamento com detritos seguem **não avaliados**. Não foi executado CFD nem ensaio hidráulico.
- A tampa é uma cobertura solta com folga nominal, sem junta ou retenção; vedação e contenção contra respingos não estão demonstradas. O gap pode permitir saída de água se o nível alcançar o aro.
- Para fechar o projeto funcional: medir a mangueira, definir desnível/orientação e nível máximo de água, decidir se a tampa precisa vedar, e medir a vazão em protótipo. Ajustar os parâmetros antes de congelar a interface.
- O relatório CAD3D apresenta WARNING para arquitetura funcional e mecânica por revisão/validação física pendentes e mantém a verificação sistêmica sem aprovação enquanto a vazão e os riscos físicos não forem resolvidos.
