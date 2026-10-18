# Relatório de projeto — módulo de circulação passiva

## Arquitetura escolhida

Foi escolhida uma passagem em série com três câmaras, duas transferências inferiores, tampa removível e um bocal em cada extremidade. Ela oferece acesso direto às câmaras após a remoção da tampa; os furos superiores permitem enchimento e ventilação durante o ensaio. As alternativas e a justificativa estão em [ARCHITECTURE.md](ARCHITECTURE.md).

O corpo tem dimensões CAD de 160 × 78 × 54 mm. A tampa acrescenta 4 mm, resultando em envelope conjunto nominal de **160 × 78 × 58 mm**, dentro do máximo de 160 × 100 × 90 mm. Cada transferência mede 30 × 16 mm. Os bocais são tubos retos de 22 mm externos, 16 mm internos e 18 mm de projeção. Há três furos de 6 mm na tampa, um sobre cada câmara.

## Evidência CAD

- O build gerou sólidos B-rep válidos para `body` e `cover`.
- A geometria da rota entrada–saída foi amostrada contra o B-rep: **PASS**, 810 pontos amostrados, passo de 2 mm e raio livre declarado de 6 mm, sem amostras bloqueadas.
- A revisão da arquitetura e a revisão de projeto ficaram em **WARNING**, pois interfaces, fixação/vedação, fabricação e comportamento em uso ainda exigem decisão ou evidência física.
- A validação CAD geral está em **FAIL**: a validade geométrica passou, mas a validade da montagem está **NOT_EVALUATED** porque a trajetória de remoção da tampa não foi validada. Retenção estrutural e estanqueidade da tampa também não foram provadas.
- As vistas incluem isométrica, ortográficas, tampa oculta, interface e corte Y=39 mm para mostrar as três câmaras e as transferências.

O teste de rota é apenas uma verificação geométrica amostrada. Ele não mede vazão, perda de carga, turbulência, autoescorva, retenção ou remoção de ar, vazamentos ou facilidade real de limpeza. **Nenhum CFD foi executado e nenhum desempenho hidráulico é alegado.**

## Decisões pendentes para protótipo

1. Selecionar mangueira e confirmar se o bocal liso de 22 mm OD/16 mm ID atende; definir abraçadeira ou outro método de retenção.
2. Definir junta, fixadores e força de aperto da tampa; executar ensaio de estanqueidade.
3. Projetar tampões vedados para as três portas de purga e validar o fechamento junto com a tampa.
4. Medir vazão em função do desnível/carga disponível e observar ar residual em diferentes orientações.
5. Verificar dimensões, limpeza, obstrução e compatibilidade do material no protótipo.

## Arquivos gerados

- Contrato paramétrico e parâmetros: `.cad3d/engineering.yaml`, `.cad3d/params.yaml`.
- Modelo: `src/model.py`; montagem: `.cad3d/assembly.yaml`.
- STEP/STL: `build/outputs/body.step`, `body.stl`, `cover.step`, `cover.stl`.
- Relatórios legíveis por máquina: `build/outputs/validation.json`, `architecture-review.json`, `design-review.json`, `report.json`.
- Imagens técnicas: `build/outputs/A_assembly_iso.png` a `H_interface_cover-seat.png`. A vista `E_section.png` mostra a seção longitudinal no plano Y=39 mm.
