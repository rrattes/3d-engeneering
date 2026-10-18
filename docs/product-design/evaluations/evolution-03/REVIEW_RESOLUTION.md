# Resolução da revisão

I1: `report_ref` agora vincula o envelope reconhecido; o gate revalida schema, revisão, fonte e parâmetros, e restringe o pointer de cada check ao envelope. Controles negativos de fonte/parâmetros re-pinados falharam antes e passaram após a correção (`red-review-evidence.log`, `green-review-evidence.log`).

I2: referências opcionais visuais/de decisão entram na inspeção. São exigidos schema, revisão, vínculos de contrato/candidata e hashes; revisão visual valida imagens e variantes declaradas. Ausência/divergência impede publicação consistente. Logs `red-review-delivery.log`, `green-review-delivery.log`; testes adicionais na regressão final.

I3: `solid_fragments` verifica pertença de faces/arestas/vértices aos sólidos tanto no importador BREP v2 quanto nos intermediários booleanos. Controle de Compound misto falhou antes, passou depois. Logs `red-review-volume.log`, `green-review-volume.log`.

M1: cobertura visual desconhecida usa NOT_EVALUATED/null. Quando manifesto/revisão estão atuais e vinculados, expõe variantes e contagem declaradas, sem aprovar aparência. Testes de cobertura/binding na regressão final.

Verificação final pelo implementador: 168 testes OK. Revisor independente encerrou após gravar REVIEW.md; tentativa de conclusão atingiu limite de uso. Não alegar nova revisão independente das correções.
