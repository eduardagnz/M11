# Análise Exploratória de Dados - Veículos

Este repositório contém a análise exploratória de dados de produção e configuração de veículos, baseada em quatro arquivos principais: **Falhas, Resultados, Status e Veículos**. Cada arquivo fornece informações essenciais para a compreensão do desempenho operacional, qualidade e distribuição dos modelos produzidos.

## Especificação dos Arquivos

Semana 1
├─ 1.Falhas
	├─ artefato_semana1_falhas.Rmd
    ├─ Index.md
├─ 2.Resultados
	├─ artefato_semana1_resultados.Rmd
	├─ Index.md
├─ 3.Status
	├─ artefato_semana1_status.Rmd
	├─ Index.md
├─ 4. Veiculos
	├─ artefato_semana1_veiculos.Rmd
	├─ Index.md
├─ README.md

### **Falhas** (`artefato_semana1_falhas.rmd`)
- **Conteúdo:** Dados sobre falhas identificadas no processo de produção dos veículos.
- **Colunas Principais:**
  - `ID` → Identificação única do veículo.
  - `MODELL` → Modelo do veículo.
  - `FALHA` → Tipo de falha detectada.
  - `DATA_DETECCAO` → Data em que a falha foi identificada.
- **Impacto no Modelo de Negócios:**
  - Permite identificar **pontos críticos na linha de produção**.
  - Auxilia na implementação de **estratégias preventivas** para reduzir falhas e desperdício.
  - Contribui para a melhoria **contínua da qualidade** e redução de custos de retrabalho.

![Falhas](../Semana%201/imgs/LeituraFalhas.png)

### **Resultados** (`artefato_semana1_resultados.rmd`)
- **Conteúdo:** Indicadores de desempenho de cada veículo produzido.
- **Colunas Principais:**
  - `ID` → Identificação única do veículo.
  - `MODELL` → Modelo do veículo.
  - `TEMPO_PRODUCAO` → Tempo total para produção.
  - `INDICE_QUALIDADE` → Nota atribuída com base nos testes de qualidade.
- **Impacto no Modelo de Negócios:**
  - Ajuda na **otimização dos tempos de produção**.
  - Permite monitorar a **qualidade dos veículos produzidos** e identificar padrões de desempenho.
  - Suporte à tomada de decisão para **melhoria nos processos e controle de qualidade**.

![Resultados](../Semana%201/imgs/LeituraResultados.png)

### **Status** (`artefato_semana1_status.rmd`)
- **Conteúdo:** Status operacional e logístico dos veículos.
- **Colunas Principais:**
  - `ID` → Identificação única do veículo.
  - `STATUS_PRODUCAO` → Indica se o veículo está em produção, finalizado ou aguardando revisão.
  - `STATUS_ENTREGA` → Estado da entrega do veículo ao cliente.
  - `DESTINO_FINAL` → Local de envio do veículo.
- **Impacto no Modelo de Negócios:**
  - Permite **controle eficiente da logística e distribuição**.
  - Auxilia na gestão de **estoques e previsão de demanda**.
  - Identifica **gargalos na entrega e na produção**, melhorando o fluxo operacional.

![Status](../Semana%201/imgs/LeituraStatus.png)

### **Veículos** (`artefato_semana1_veiculos.rmd`)
- **Conteúdo:** Detalhamento dos modelos fabricados, incluindo variação de cores e configurações.
- **Colunas Principais:**
  - `ID` → Identificação única do veículo.
  - `MODELL` → Modelo e motorizao do veículo.
  - `FARBAU` → Cor externa.
  - `FARBIN` → Cor interna.
  - `PR` → Configuração completa do carro.
- **Impacto no Modelo de Negócios:**
  - Fornece informações para **análise da preferência dos clientes**.
  - Identifica **padrões de demanda por modelos e cores**.
  - Ajuda a otimizar a **estratégia de produção e personalização dos veículos**.

![Veiculos](../Semana%201/imgs/LeituraVeiculos.png)

## Processo

![Descrição da imagem](../Semana%201/imgs/GraficosResultados.png)

![Descrição da imagem](../Semana%201/imgs/GraficoStatus.png)

![Descrição da imagem](../Semana%201/imgs/Variaveis.png)

## Conclusão
A análise exploratória desses quatro arquivos permite uma **visão completa do ciclo de produção de veículos**, desde a identificação de falhas até a distribuição ao cliente final. Isso contribui diretamente para:

**Redução de falhas e desperdícios** na linha de produção.
**Otimização de tempos e processos** de fabricação.
**Melhoria no controle de estoque e logística**.
**Aprimoramento da experiência do cliente** com modelos mais personalizados e eficientes.

