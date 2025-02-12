Esse **R Notebook** tem como objetivo analisar os resultados de testes de verificação de veículos, focando na taxa de erros ao longo do tempo e no ranking de categorias com mais falhas.

---

## **1. Exploração inicial da tabela**
A primeira etapa envolve visualizar a estrutura e o conteúdo dos dados.

### **1.1. Amostra dos dados**
```r
head(InteliResultados, n=5)
```
- Exibe as **5 primeiras linhas** do dataset `InteliResultados`, permitindo uma visão geral dos dados.

### **1.2. Identificação de valores únicos em `STATUS`**
```r
unique(InteliResultados$STATUS)
```
- Retorna os valores distintos na coluna `STATUS`, verificando se há apenas `"OK"` e `"NOTOK"` ou outras possíveis classificações.

---

## **2. Limpeza e transformação de colunas**
Aqui, o foco é converter a coluna `STATUS` para um formato **binário**, tornando a análise mais eficiente.

```r
library(readr)

# Lendo o CSV
raw_data <- read_csv("./InteliResultados.csv", show_col_types = FALSE)

# Convertendo STATUS para binário (1 = OK, 0 = NOTOK)
raw_data$STATUS <- ifelse(raw_data$STATUS == "OK", 1, 0)

# Exibir as primeiras linhas para verificar a transformação
head(raw_data)
```

### **Por que converter `STATUS` para binário?**
- **Facilita cálculos estatísticos e gráficos**.
- **Melhora performance** para análises escaláveis.
- **Evita inconsistências** (diferentes grafias como `"ok"`, `"Ok"`, `"OK "`).

---

## **3. Pacotes necessários**
Antes de criar as visualizações, é necessário carregar bibliotecas para manipulação e visualização de dados.

```r
library(dplyr)
library(lubridate)
library(ggplot2)
library(plotly)
```
Essas bibliotecas permitem:
- **dplyr** → Manipulação eficiente dos dados.
- **lubridate** → Tratamento de datas e horários.
- **ggplot2** → Criação de gráficos.
- **plotly** → Transformação de gráficos estáticos em interativos.

---

## **4. Visualizações**
Agora, geramos gráficos para entender padrões nos dados.

### **4.1. Taxa de Erros por Data**
Esse gráfico exibe a evolução de falhas e acertos ao longo do tempo.

```r
# Convertendo CAPTURE_TIME para data e hora
dados <- raw_data %>%
  mutate(CAPTURE_TIME = ymd_hms(gsub("-", " ", CAPTURE_TIME))) %>%
  mutate(DATE = as.Date(CAPTURE_TIME))  # Criando coluna com a data

# Contagem de OK e NOTOK por dia
resumo <- dados %>%
  group_by(DATE, STATUS) %>%
  summarise(count = n(), .groups = "drop") %>%
  mutate(STATUS = ifelse(STATUS == 1, "OK", "NOTOK"))

# Criando gráfico de linha
grafico <- ggplot(resumo, aes(x = DATE, y = count, color = STATUS, group = STATUS)) +
  geom_line(size = 1.2) +
  geom_point(size = 2) +  # Adiciona pontos para melhor visualização
  labs(title = "Evolução de OK e NOTOK por Dia",
       x = "Data",
       y = "Quantidade",
       color = "Status") +
  theme_minimal()

# Tornando o gráfico interativo
ggplotly(grafico)
```

🔹 **O que esse gráfico mostra?**
- A **frequência de testes OK e NOTOK ao longo do tempo**.
- Identifica **picos de falhas**, indicando possíveis problemas no processo de fabricação.

---

### **4.2. Ranking de Categorias com Mais Erros**
Agora, analisamos **quais tipos de erro ocorrem com mais frequência**.

```r
# Agrupar total de erros por categoria e calcular percentual
erros_por_categoria <- raw_data %>%
  filter(STATUS == 0) %>%  # Filtra apenas erros (NOTOK)
  group_by(RESULT_DESCRIPTION) %>%
  summarise(qtd_erros = n(), .groups = "drop") %>%
  mutate(percentual = (qtd_erros / sum(qtd_erros)) * 100) %>%  # Calcula percentual
  arrange(desc(qtd_erros))  # Ordena do maior para o menor

# Criar gráfico de barras
grafico <- ggplot(erros_por_categoria, aes(x = reorder(RESULT_DESCRIPTION, qtd_erros), y = qtd_erros, fill = RESULT_DESCRIPTION)) +
  geom_bar(stat = "identity") +
  geom_text(aes(label = paste0(qtd_erros, " (", round(percentual, 1), "%)")), 
            hjust = -0.2, size = 4) +  # Adiciona rótulo com total e percentual
  coord_flip() +  # Inverte para melhor visualização
  labs(title = "Ranking de Categorias com Mais Erros (NOTOK)",
       x = "Categoria",
       y = "Quantidade de Erros") +
  theme_minimal() +
  theme(legend.position = "none")  # Remove legenda desnecessária

# Converter para gráfico interativo
ggplotly(grafico)
```

🔹 **O que esse gráfico mostra?**
- **Categorias de erro mais comuns**.
- **Percentual de impacto de cada erro**, ajudando a priorizar correções.

---

## **5. Relatório Final**
A última seção documenta as mudanças feitas e a estrutura final do dataset.

### **5.1. Descrição da Tabela**
A tabela registra o status de verificações feitas em veículos.

### **5.2. Modificações e Estrutura**
- **Removido**: `RESULT_DESCRIPTION` (redundante, pois `RESULT_ID` já representa a informação).
- **Alterado**: `STATUS` convertido para binário (`0 = NOTOK`, `1 = OK`) para facilitar análise.
- **Mantidos**:
  - `CAPTURE_TIME`: Data e hora do registro.
  - `RESULT_ID`: Código do tipo de verificação.
  - `ID_CARRO`: Identificador do veículo.

### **5.3. Estrutura da Tabela Final**
| Nome da Coluna   | Descrição |
|------------------|-----------|
| **ID_CARRO** | Identificação do veículo. |
| **RESULT_ID** | Código da verificação realizada. |
| **CAPTURE_TIME** | Data e hora do teste. |
| **STATUS** | Status do teste (**1 = OK**, **0 = NOTOK**). |

### **5.4. Considerações**
1. **Resultados condicionais ao veículo**
   - Nem todos os veículos passam pelos mesmos testes.
   - Exemplo: Apenas modelos com ar-condicionado passam pelo teste de carga de gás.

2. **Estrutura escalável**
   - Permite comparações futuras por tipo de erro e veículo.

---

## **Resumo**
Este notebook realiza um **pipeline de análise de dados**, incluindo:
✅ **Exploração** → Estrutura do dataset.  
✅ **Limpeza** → Conversão de colunas e remoção de redundâncias.  
✅ **Visualização** → Evolução de falhas e ranking de erros.  
✅ **Documentação** → Relatório sobre mudanças e estrutura final.

🚀 **Conclusão**: Esse estudo ajuda a identificar **padrões de falha em veículos**, permitindo melhorias no processo de fabricação. 🚗💡