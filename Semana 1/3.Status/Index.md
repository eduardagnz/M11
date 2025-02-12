### **1. Introdução**  
O relatório analisa os dados do **InteliStatus**, que registram o fluxo de veículos em um processo produtivo. O objetivo é calcular **o tempo total de produção** de cada veículo e analisar a distribuição dos tempos para identificar possíveis gargalos.

---

### **2. Importação e Exploração dos Dados**  
O primeiro passo é carregar os dados e exibi-los:  

```r
raw_data_status <- InteliStatus
InteliStatus
```
- `raw_data_status` armazena os dados originais para referência.  
- `InteliStatus` exibe os registros iniciais da tabela.

---

### **3. Transformação dos Dados**  
Os dados são ajustados para garantir que a coluna `STATUS_DATA` esteja no formato correto:  

```r
library(dplyr)
library(lubridate)

dados <- InteliStatus %>%
  mutate(STATUS_DATA = as.POSIXct(gsub("-", " ", STATUS_DATA), format="%Y %m %d %H.%M.%S"))
```
- **Bibliotecas utilizadas**:  
  - `dplyr` para manipulação dos dados.  
  - `lubridate` para trabalhar com datas e horas.  
- **Transformação aplicada**:  
  - `gsub("-", " ", STATUS_DATA)`: substitui `-` por espaço para corrigir o formato.  
  - `as.POSIXct(...)`: converte `STATUS_DATA` para um formato de data/hora utilizável.

---

### **4. Cálculo do Tempo Total de Produção**  
Para cada veículo, calcula-se o tempo entre a **primeira e a última atualização** de status.

```r
resultado <- dados %>%
  group_by(ID) %>%
  summarise(
    min_tempo = min(STATUS_DATA, na.rm = TRUE),
    max_tempo = max(STATUS_DATA, na.rm = TRUE),
    tempo_total = ifelse(
      is.na(min_tempo) | is.na(max_tempo),
      0,
      as.character(difftime(max_tempo, min_tempo, units = "secs"))
    )
  )
```
- **Passo a passo**:  
  1. **Agrupa os dados por ID do veículo**.  
  2. **Determina o primeiro e o último registro** (`min_tempo` e `max_tempo`).  
  3. **Calcula a diferença de tempo** (`difftime`).  
  4. **Se houver valores nulos**, define `tempo_total = 0`.

---

### **5. Análise do Tempo Total**  
Os tempos são convertidos para horas e agrupados em **bins (faixas) de 300 horas**.

```r
df <- resultado %>%
  mutate(tempo_total_horas = as.numeric(tempo_total) / 3600)
```
- Converte `tempo_total` (segundos) para horas.

```r
df <- df %>%
  mutate(bin_horas = cut(tempo_total_horas,
                         breaks = seq(0, 3000, by = 300),
                         include.lowest = TRUE,
                         right = FALSE))
```
- Agrupa os tempos em **intervalos de 300 horas**.

```r
df_grouped <- df %>%
  group_by(bin_horas) %>%
  summarise(contagem = n()) %>%
  ungroup()
```
- **Conta quantos veículos estão dentro de cada intervalo**.

```r
df_grouped_clean <- df_grouped %>%
  filter(contagem > 5000)
```
- **Filtra apenas os grupos com mais de 5000 veículos** (removendo outliers).

---

### **6. Gráfico de Distribuição dos Tempos de Produção**  
Cria um gráfico mostrando **quantos veículos estão em cada faixa de tempo de produção**.

```r
ggplot(df_grouped_clean, aes(x = ponto_medio, y = contagem)) +
  geom_point(size = 5, color = "steelblue") +
  geom_line(color = "steelblue", size = 1) +
  scale_x_continuous(name = "Tempo de Produção (horas)", breaks = seq(0, 3000, by = 100)) +
  scale_y_continuous(name = "Quantidade de Carros", breaks = seq(0, 120000, by = 10000), limits = c(0, 120000)) +
  labs(
    title = "Distribuição de Carros por Tempo de Produção",
    subtitle = "Agregado em intervalos de 300 horas (outliers removidos)"
  ) +
  theme_minimal(base_size = 14) +
  theme(
    plot.title = element_text(face = "bold", hjust = 0.5),
    plot.subtitle = element_text(hjust = 0.5),
    axis.text = element_text(color = "gray30")
  )
```
- **Eixo X**: tempo total de produção (horas).  
- **Eixo Y**: quantidade de veículos.  
- **Objetivo**: identificar possíveis tempos anormais na produção.

---

### **7. Análise do Tempo Médio entre Etapas da Armação**  
Os status da etapa de **armação** são filtrados para calcular os tempos médios entre cada um.

```r
status_armacao <- c("R210", "R213", "R500", "R549", "R780", "R800")

raw_Data <- raw_data_status %>%
  mutate(STATUS_DATA = ymd_hms(gsub("-", " ", STATUS_DATA))) 
```
- Define os status que fazem parte da **armação** (`status_armacao`).  
- Converte `STATUS_DATA` para um formato correto.

```r
tempo_por_id <- raw_Data %>%
  filter(STATUS %in% status_armacao) %>%
  arrange(ID, STATUS_DATA) %>%
  group_by(ID) %>%
  mutate(tempo_diferenca = difftime(lead(STATUS_DATA), STATUS_DATA, units = "secs"),
         proximo_ponto = lead(STATUS)) %>%
  filter(!is.na(tempo_diferenca)) %>%
  ungroup()
```
- **Filtra os registros** que pertencem à armação.  
- **Ordena os dados pelo tempo (`STATUS_DATA`)**.  
- **Calcula a diferença de tempo entre cada transição de status** (`difftime`).

---

### **8. Gráfico do Tempo Médio entre Pontos da Esteira**  
Este gráfico exibe os tempos médios entre cada etapa da armação.

```r
grafico <- ggplot(media_tempo_pontos, aes(x = paste(STATUS, "→", proximo_ponto), y = tempo_medio, fill = STATUS)) +
  geom_bar(stat = "identity") +
  geom_text(aes(label = paste0(round(tempo_medio, 1), "s")), vjust = -0.5, size = 4) +
  labs(title = "Tempo Médio entre os Pontos da Esteira", x = "Transição entre Pontos", y = "Tempo Médio (segundos)") +
  theme_minimal()
ggplotly(grafico)
```
- **Eixo X**: transições entre etapas.  
- **Eixo Y**: tempo médio em segundos.  
- **Objetivo**: identificar gargalos e otimizar o fluxo produtivo.

---

### **9. Filtragem de Dados para um Veículo Específico**  
Caso seja necessário visualizar o fluxo de um **veículo específico**, usa-se o seguinte filtro:

```r
dados_filtrados <- InteliStatus %>%
  filter(ID == "2024-1422099") %>%
  arrange(STATUS_DATA)
```
- **Filtra os registros do veículo com ID `2024-1422099`**.  
- **Ordena os registros pelo tempo (`STATUS_DATA`)** para facilitar a análise.

---

### **10. Conclusão**  
O relatório apresentou:
- O **tempo total de produção** de cada veículo.  
- A **distribuição dos tempos** para identificar anomalias.  
- A **análise detalhada da etapa de armação**, com tempos médios entre estágios.  
- **Filtros personalizados** para análise de veículos específicos.

Essa análise pode ser utilizada para **otimizar o fluxo produtivo e reduzir atrasos**. 