# Toy-modeler — proposta de design

**Estado:** especificação implementada como toy-modeler 1.0.0 e promovida. **Escopo:** brinquedos e protótipos pessoais, sem finalidade de venda.

## O que é próprio de um brinquedo

A pergunta inicial é: **o que a pessoa faz com a peça e por que deseja repetir?** A experiência pode ser aberta e imaginativa; não exige regras ou pontuação. A skill deve projetar uma sequência observável: convite para tocar → ação → resposta perceptível → nova possibilidade de brincar.

| Engenharia mecânica comum | Brinquedo acrescenta |
|---|---|
| Articulação gira no curso previsto | Poses interessantes, estabilidade, expressão e facilidade de manipular |
| Roda gira livremente | Trajetória, velocidade, comportamento ao empurrar e modo de reiniciar |
| Mola retorna | Resposta tátil, ritmo, surpresa e prazer de repetir |
| Peças encaixam | Descoberta, transformação e combinações novas |
| Forma e acabamento | Identidade, pegada, escala para as mãos e pistas visuais sobre o uso |

O ganho da `toy-modeler` é converter intenções como “divertido”, “articulado” ou “transformável” em geometria, mecanismos e interações testáveis. Ela trabalha com faz de conta, construção, movimento, manipulação sensorial, desafio e coleção, inclusive combinações desses padrões.

## Responsabilidades e fluxo

`toy-modeler` define experiência e contratos de interação. `3d-engineering` faz CAD, tolerâncias, movimento, montagem, impressão e arquivos fabricáveis. `product-design` é opcional para identidade visual, que deve reforçar a leitura da interação e respeitar a engenharia. A skill nova não edita as existentes.

1. **Conceito:** usuário pretendido, tema, cenário, ação, resposta, repetição e variações.
2. **Arquitetura lúdica:** partes manipuláveis, estados/poses, acessórios, modularidade e transformação.
3. **Mecanismos:** selecionar juntas, rodas, encaixes, engrenagens, molas ou flexuras pela resposta desejada.
4. **CAD e protótipo:** modelar com `3d-engineering`; imprimir e observar se a interação ocorre como planejado.
5. **Iteração:** ajustar pegada, resistência, aparência, clareza e vontade de repetir; revalidar mudanças geométricas.
6. **Revisão proporcional:** conferir integridade e riscos evidentes do protótipo, sem trilha de certificação.

## Contrato de experiência

Entrada: ideia/tema; usuário pretendido; contexto; padrão de brincadeira; ação principal; resposta visual, sonora, tátil ou de movimento; materiais/processo; política de peças compradas; tamanho e custo. Faixa etária pode ficar indefinida durante exploração, sem alegar adequação infantil.

`toy_brief.json` registra: promessa de brincadeira; loop convite/ação/resposta/repetição; estados e transformação; onde segurar/girar/empurrar/apertar; repertório de poses/usos/combinações; peças e mecanismos; critérios de observação do protótipo. Para ação única, registrar a riqueza e repetibilidade da resposta em vez de exigir artificialmente três usos. Documentos derivados mostram mapa de interação, CAD/STL/STEP reais, montagem e notas de prototipagem. Riscos e pendências entram em registro breve.

## Catálogo inicial

| Brincadeira | Recursos mecânicos | Avaliação no piloto |
|---|---|---|
| Faz de conta/personagens | Juntas de fricção, dobradiças, acessórios | Poses, expressão, estabilidade |
| Construção/transformação | Encaixes, módulos, deslizantes | Configurações úteis, montagem intuitiva |
| Movimento | Rodas, eixos, cames, engrenagens | Trajetória, feedback e reinício |
| Tátil/sensorial | Flexura, mola, catraca, textura | Força, retorno, som/sensação |
| Desafio/descoberta | Labirinto, trava, sequência | Pistas, progressão e variedade |
| Coleção/mundo | Conexões, cenários, acessórios | Compatibilidade e novas histórias |

Cada mecanismo terá eixo/curso, graus de liberdade, batentes, retenção, folgas e **resposta de brincadeira pretendida**. Reusar `pin_hinge` e verificação de movimento da plataforma. Para mola impressa, força, retorno e durabilidade são hipóteses até avaliação física. Motores, baterias, ímãs e projéteis ficam fora do primeiro piloto.

## Critérios de qualidade

1. A ação principal é legível ao ver ou pegar a peça.
2. A ação produz resposta perceptível e coerente.
3. O uso pode ser repetido sem remontagem trabalhosa.
4. A peça oferece variação de poses, trajetórias, combinações ou histórias quando isso serve ao conceito.
5. Pegada, escala, alcance e resistência servem ao usuário pretendido.
6. O comportamento pode ser reproduzido por impressão e montagem documentadas.
7. A revisão física observa desprendimento, ruptura e beliscões evidentes; CAD não substitui inspeção.

Como referência de perigos, o [Inmetro](https://www.gov.br/inmetro/pt-br/acesso-a-informacao/perguntas-frequentes/avaliacao-da-conformidade/brinquedos/quais-sao-os-requisitos-gerais-exigidos-para-os-brinquedos) menciona quedas, puxões e torções. Certificação e liberação comercial estão fora do escopo.

## Pilotos

(A) Personagem articulado com poses expressivas; (B) carrinho com comportamento próprio; (C) objeto de apertar com retorno por flexura cativa. Comparar ao fluxo atual em variedade de interação, clareza, resposta percebida, mecanismo e CAD. Registrar observações reais apenas quando houver protótipo físico.
