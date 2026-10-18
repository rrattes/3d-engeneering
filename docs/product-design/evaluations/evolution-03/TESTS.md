# Registro dos testes — evolução 03

Execução final: `regression-final-02.log`, 168 testes, zero falhas/skips. Histórico:123; adicionais:45. Testes comportamentais são uma avaliação separada e incompleta.

| ID | Evidência executável | Estado/limite |
|---|---|---|
| TEST-PD3-01 | test_engineering_evidence; gate integrado | PASS: critérios/proveniência/omissão/revisão/calibração |
| TEST-PD3-02 | test_engineering_evidence | PASS: datum ausente e pose incompatível bloqueados; metadados, não aderência física |
| TEST-PD3-03 | test_host + test_delivery_manifest + pilot/run02 | PASS: dependências, alteração de cor, helper e arquivo CAD |
| TEST-PD3-04 | test_delivery_manifest + pilot/run02 | PASS: anterior, falha, arquivo ausente/antigo, namespace; escritores externos não transacionais |
| TEST-PD3-05 | test_style_extensions; behavior/raw | API PASS; avaliação estética entre cinco estilos não executada nesta evolução |
| TEST-PD3-06 | test_style_extensions; behavior | Compatibilidade PASS; 20/36 respostas, julgamento comparativo final pendente |
| TEST-PD3-07 | test_summary_parity; test_integration; test_delivery_manifest | PASS: fatos/escape/estados atuais e cobertura declarada |
| TEST-PD3-08 | test_volume_permissions; BREPIntegration | PASS: lados opostos, vazio invadido, remoção protegida, união editável |
| TEST-PD3-09 | test_volume_permissions | PASS: fonte/pose/limiar/margem/Boolean/topologia mistos |

Comando reproduzível (na raiz do workspace):

```sh
docker run --rm --network none --read-only --tmpfs /tmp:rw,size=1g \
  --user 1000:1000 \
  -e PD_CANDIDATE=/workspace/docs/product-design/candidates/evolution-03/product-design \
  -e PYTHONDONTWRITEBYTECODE=1 -e VTK_DEFAULT_OPENGL_WINDOW=vtkEGLRenderWindow \
  -e MPLCONFIGDIR=/tmp/mpl -e XDG_CACHE_HOME=/tmp/cache \
  -v "$PWD:/workspace:ro" --entrypoint python cad3d-engineering:1.8.0 \
  /workspace/docs/product-design/evaluations/evolution-03/checks/run_checks.py
```

Para diagnóstico dirigido adicionar `--group host`, `cad`, `integration` ou `legacy`. `--historical` restringe aos 123 anteriores. Não executar os scripts auxiliares copiados da evolução02 (`run_productivity.py`, `run_feature_examples.py`) sem adaptar seus caminhos de saída históricos. O piloto específico desta rodada é `run_pilot.py`; usa saída run02 já existente, portanto uma repetição exige novo diretório para preservar evidências.
