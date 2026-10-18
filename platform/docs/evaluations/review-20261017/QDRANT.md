# Avaliação de Qdrant para a 3d-engineering

Data:17/10/2026. Pesquisa em documentação oficial e comparação com a arquitetura local proposta. Nenhuma instalação, alteração de container, indexação, execução de embeddings ou benchmark. Recursos consultados não implicam que estejam disponíveis no ambiente CAD atual.

## Parecer

Qdrant é candidato útil para uma camada opcional de recuperação semântica de referências e soluções revisadas. Não o recomendo como substituto da fonte canônica de dados nem como requisito para gerar CAD. Seu benefício para este corpus ainda precisa ser demonstrado; as lacunas principais A01–A06 continuam exigindo correção do motor/contratos.

A avaliação arquitetural anterior indicava ausência de benefício demonstrado de banco vetorial. Isso permanece verdadeiro quanto a medição: esta pesquisa identifica um caso de uso plausível, não comprova ganho. A recomendação agora é especificar e comparar esse caso em piloto antes de decidir incorporar.

## O que a ferramenta oferece

- Busca por vetores e combinação de representações densas/esparsas em consultas híbridas, com fusão de rankings. [Qdrant — hybrid queries](https://qdrant.tech/documentation/search/hybrid-queries/).
- Filtros sobre metadados, inclusive condições numéricas. Podem restringir candidatos por processo, projeto, revisão, diâmetro/pitch e tipo de evidência, desde que esses dados estejam corretamente registrados. [Qdrant — filtering](https://qdrant.tech/documentation/search/filtering/).
- Cliente Python com modo local em memória ou persistido, indicado na documentação para protótipos/testes, além do servidor. Integração opcional FastEmbed para gerar embeddings. [Cliente oficial](https://github.com/qdrant/qdrant-client).
- Implantação de servidor em Docker. A configuração inicial precisa ser ajustada antes de expor acesso, pois o quickstart informa ausência de autenticação/criptografia por padrão. [Quickstart](https://qdrant.tech/documentation/quickstart/).

Consulta por similaridade retorna candidatos. Não prova dimensão, furação, força, adequação térmica ou fabricação. Score semântico não representa confiança física. Vetor textual de descrição de uma peça não equivale a comparação de sólidos STEP; isso exigiria representação geométrica e avaliação próprias.

## Casos de uso propostos

1. Recuperar uma técnica: “como prender fan removível quando a porca não é acessível por baixo?”.
2. Localizar uma lição: “parede fina criada no encontro do rasgo de ventilação com a emenda”.
3. Encontrar documentos de interface: “fonte compacta com conectores modulares e entrada traseira”.
4. Relacionar vocabulário português/inglês em documentação e briefing, se o modelo de embeddings tiver qualidade demonstrada nos dois idiomas.
5. Selecionar poucas referências relevantes para o agente em vez de carregar a biblioteca inteira.

Busca de “M3×10”, revisão específica e largura máxima continua precisando de correspondência/filtros numéricos exatos. Embeddings podem aproximar “M3×10” e “M3×16” ou famílias distintas de fonte. Filtrar e conferir a fonte canônica é obrigatório antes de propor reutilização.

## Arquitetura e propriedade dos dados

```text
Arquivos canônicos revisados + manifestos
             |
             +--> SQLite opcional: IDs, revisões, relações e consultas estruturadas
             |
             +--> Ingestão selecionada: texto + metadados + embeddings
                              |
                              v
                        Qdrant opcional
                              |
                  candidatos com IDs e trechos
                              |
              reabrir registro canônico e verificar revisão
                              |
               selecionar contexto para Codex/Claude
                              |
               requisitos e validação CAD independentes
```

O caminho de busca não deve ser dependência da execução do kernel. Banco indisponível permite consulta convencional ou continuação com contexto explícito; não pode alterar critérios CAD. SQLite e Qdrant podem ser projeções dos mesmos registros, sem sincronização direta obrigatória entre bancos e sem transação distribuída.

Payload mínimo proposto: project_scope, document_id, component_id quando houver, revision_id, source_hash, chunk_id, record_kind, lifecycle_status, evidence_kind, source_path/page/section, units e dimensões estruturadas aplicáveis. Registrar separadamente embedding_model, model_revision, vector_dimension, normalization, chunking_version e corpus_version.

Cada resultado deve apontar ao original. Alteração de modelo de embedding ou preparação do texto exige reindexação/versionamento do espaço vetorial. Mesmo número de dimensões não significa embeddings compatíveis.

Começar indexando registros e referências revisados, não logs brutos e toda a conversa. Documento longo exige segmentação que preserve tabela, unidade, contexto e seção; PDF/imagem demanda extração/OCR validada. Não inventar medidas ao indexar.

## Limites entre projetos e aprendizado

- Escopo padrão: projeto atual e biblioteca compartilhada explicitamente selecionada. Não buscar automaticamente em todos os projetos anteriores.
- Recuperar uma técnica antiga não autoriza importar suas dimensões, material, impressora ou geometria para o briefing novo.
- Registro aprovado, hipótese, defeito conhecido e item obsoleto são estados distintos. Casos com falha podem ajudar no diagnóstico, mas não devem aparecer como soluções aprovadas.
- Filtro de projeto é aplicado pela aplicação em toda consulta; ele não substitui autenticação/autorização de um serviço multiusuário. Busca por IDs também precisa respeitar o escopo.
- Conteúdo recuperado é evidência/contexto, nunca instrução executável ou autorização para alterar o projeto.
- Revalidar revisão/hash no original ao usar o resultado, inclusive quando o índice indicar status favorável.

Esses limites atendem ao cuidado já expresso pelo usuário com absorver soluções de projetos anteriores sem justificativa.

## Implantação e custo

**Piloto:** cliente local com persistência, em ambiente de avaliação separado do CAD. O cliente oficial declara esse modo adequado para prototipagem/testes. Não tratá-lo como prova de equivalência de desempenho ou concorrência com servidor.

**Uso compartilhado/concorrente:** serviço Qdrant em container separado e perfil opcional de Compose. O código do modo local bloqueia acesso concorrente ao mesmo diretório por outra instância e orienta usar servidor nesse caso. [Código oficial do cliente local](https://github.com/qdrant/qdrant-client/blob/master/qdrant_client/local/qdrant_local.py).

Manter o container CAD sem rede como hoje. Recuperação/ingestão roda em processo/container próprio; o contexto selecionado é entregue como entrada explícita do run. Não é necessário MCP para começar: uma interface CLI pode servir aos dois agentes; integração MCP seria escolha futura.

Para operação sem nuvem, selecionar modelo local de embeddings, fixar revisão/licença, provisionar arquivos antecipadamente e medir funcionamento offline. Qdrant sozinho não define a qualidade do embedding. RAM/disco, tamanho do modelo, custo de reindexação e latência dependem do corpus e precisam ser medidos. Não há orçamento de hardware estimado ou benchmark executado nesta análise.

O kit básico permanece independente de Qdrant. A variante com busca precisa documentar dependências extras e reconstrução do índice. Compartilhar fontes revisadas e receita de indexação; não assumir que um diretório de storage em uso é um backup portátil suficiente.

## Comparação com opções mais simples

| Opção | Força neste fluxo | O que permanece em aberto |
|---|---|---|
| rg/busca por arquivo | Código/identificador exato e instalação mínima | Sinônimos e linguagem natural |
| SQLite + FTS5 opcional | Texto, códigos e cruzamentos de metadados | Relevância semântica; disponibilidade de FTS5 no runtime precisa ser verificada |
| Qdrant com embeddings | Recuperação por significado e filtros | Preparação do corpus, qualidade multilíngue, revisões e custo |
| Busca híbrida Qdrant | Combinar indícios semânticos e termos técnicos | Configuração e avaliação; não substitui restrições exatas nem validação CAD |

FTS5 é mecanismo de busca textual documentado pelo SQLite: [referência oficial](https://www.sqlite.org/fts5.html). Não há necessidade demonstrada de introduzir SQLite, FTS5 e Qdrant simultaneamente antes de comparar o ganho incremental.

## Piloto e regressão propostos

Depois de estabilizar catálogo, proveniência e manifestos do plano aprovado:

1. Preparar corpus pequeno, revisado, com exemplos aprovados, negativos e revisões antigas.
2. Definir30consultas:10por intenção/sinônimo,10por código/dimensão,5sem resposta válida e5de escopo/revisão. Separar consultas de ajuste e consultas reservadas antes de configurar o ranking.
3. Comparar busca lexical atual, SQLite/FTS5 quando disponível e Qdrant semântico/híbrido com o mesmo corpus e relevância julgada previamente.
4. Medir Recall@5/MRR nas consultas com resposta, acerto de códigos, dimensões e fontes, violações de escopo, obsolescência, latência, RAM/disco e trabalho de preparação. Não considerar score de similaridade como resposta correta.
5. Exigir zero seleção indevida por projeto/revisão nas fixtures e nenhum relaxamento dos gates CAD. Conservar “não encontrado” quando não há registro válido; não forçar sempre um resultado reutilizável.
6. Testar indisponibilidade, índice antigo, documento alterado/removido, mudança do embedding e reconstrução. A falha do índice não pode afetar o estado canônico ou validar produto.
7. Só incorporar se houver ganho relevante e explicado na recuperação sem degradar correspondência técnica, escopo e simplicidade de instalação. Não generalizar confiabilidade a partir desse piloto limitado.

IDs futuros sugeridos: RET-SCOPE-01, RET-REV-01, RET-EXACT-01, RET-UNKNOWN-01, RET-REBUILD-01 e RET-OFFLINE-01. Nenhum teste foi criado ou executado agora.

## Recomendação de sequência

Manter A01–A09 como prioridade. Após contratos estáveis, experimentar busca opcional sem acoplá-la ao caminho crítico. O papel promissor de Qdrant é recuperar conhecimento técnico revisado e contexto relevante para os agentes. O papel do motor continua gerar/verificar geometria, e o das fontes/manifestos continua sustentar as evidências.
