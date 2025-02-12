### **1. Introdução**  
O relatório analisa os dados da tabela **InteliVeiculo**, que contém informações sobre os veículos fabricados. O objetivo é visualizar:  
- **A quantidade de veículos por modelo**  
- **A variação de cores por modelo**  
- **A variação completa considerando cor e configuração**  

---

### **2. Importação e Exploração dos Dados**  
Os dados são carregados e exibidos para análise inicial:  

```r
raw_data <- InteliVeiculo
raw_data
```
- `raw_data` armazena a tabela original **InteliVeiculo**.

---

### **3. Importação de Bibliotecas**  
Para manipulação e visualização dos dados, são carregadas as seguintes bibliotecas:

```r
library(dplyr)
library(ggplot2)
library(plotly)
```
- `dplyr`: facilita a transformação e filtragem dos dados.  
- `ggplot2`: permite a criação de gráficos estatísticos.  
- `plotly`: converte gráficos estáticos em interativos.

---

### **4. Quantidade de Modelos Fabricados**  
O total de veículos fabricados é agrupado por modelo.

```r
modelos_mais_fabricados <- raw_data %>%
  group_by(MODELL) %>%
  summarise(qtd_fabricada = n(), .groups = "drop") %>%
  arrange(desc(qtd_fabricada))
```
- **Agrupa os dados pelo modelo (`MODELL`)**.  
- **Conta quantos veículos foram produzidos por modelo (`qtd_fabricada`)**.  
- **Ordena os modelos do mais fabricado para o menos fabricado**.  

#### **Gráfico da Quantidade de Modelos Fabricados**  

```r
grafico <- ggplot(modelos_mais_fabricados, aes(x = reorder(MODELL, qtd_fabricada), y = qtd_fabricada, fill = MODELL)) +
  geom_bar(stat = "identity") +
  geom_text(aes(label = qtd_fabricada), hjust = -0.2, size = 4) +
  coord_flip() +
  labs(title = "Modelos mais fabricados",
       x = "Modelo",
       y = "Quantidade Fabricada") +
  theme_minimal() +
  theme(legend.position = "none")

ggplotly(grafico)
```
- **Eixo X**: modelos dos veículos.  
- **Eixo Y**: quantidade de veículos fabricados.  
- **Objetivo**: identificar os modelos mais e menos fabricados.

---

### **5. Variação de Cores por Modelo**  
O número de variações de cores (FARBAU + FARBIN) é contado para cada modelo.

```r
variacoes_cor <- raw_data %>%
  group_by(MODELL, FARBAU, FARBIN) %>%
  summarise(qtd = n(), .groups = "drop") %>%
  group_by(MODELL) %>%
  summarise(qtd_variacoes = n(), .groups = "drop") %>%
  arrange(desc(qtd_variacoes))
```
- **Agrupa os veículos pelo modelo e combinações de cor externa (`FARBAU`) e cor interna (`FARBIN`)**.  
- **Conta quantas combinações únicas existem para cada modelo**.  
- **Ordena os modelos do que tem mais variações de cores para o que tem menos**.  

#### **Gráfico da Variação de Cores por Modelo**  

```r
grafico <- ggplot(variacoes_cor, aes(x = reorder(MODELL, qtd_variacoes), y = qtd_variacoes, fill = MODELL)) +
  geom_bar(stat = "identity") +
  geom_text(aes(label = qtd_variacoes), hjust = -0.2, size = 4) +
  coord_flip() +
  labs(title = "Variações de Cor (FARBAU + FARBIN) por Modelo",
       x = "Modelo",
       y = "Quantidade de Variações") +
  theme_minimal() +
  theme(legend.position = "none")

ggplotly(grafico)
```
- **Eixo X**: modelos dos veículos.  
- **Eixo Y**: quantidade de variações de cores disponíveis.  
- **Objetivo**: entender quais modelos possuem maior diversidade de cores.

---

### **6. Variação Completa por Modelo (Cor + Configuração)**  
Aqui, são analisadas as variações completas considerando **cor externa, cor interna e configuração do veículo (`PR`)**.

```r
variacoes_completas <- raw_data %>%
  group_by(MODELL, FARBAU, FARBIN, PR) %>%
  summarise(qtd = n(), .groups = "drop") %>%
  group_by(MODELL) %>%
  summarise(qtd_variacoes = n(), .groups = "drop") %>%
  arrange(desc(qtd_variacoes))
```
- **Agrupa por modelo, cor e configuração (`PR`)**.  
- **Conta quantas combinações únicas existem para cada modelo**.  
- **Ordena os modelos que possuem mais variações para os que possuem menos**.  

#### **Gráfico da Variação Completa por Modelo**  

```r
grafico <- ggplot(variacoes_completas, aes(x = reorder(MODELL, qtd_variacoes), y = qtd_variacoes, fill = MODELL)) +
  geom_bar(stat = "identity") +
  geom_text(aes(label = qtd_variacoes), hjust = -0.2, size = 4) +
  coord_flip() +
  labs(title = "Variações de Cores e Configurações por Modelo",
       x = "Modelo",
       y = "Quantidade de Variações") +
  theme_minimal() +
  theme(legend.position = "none")

ggplotly(grafico)
```
- **Eixo X**: modelos dos veículos.  
- **Eixo Y**: quantidade de variações considerando cor + configuração.  
- **Objetivo**: entender quais modelos possuem maior diversidade de personalização.

---

### **7. Relatório de Análise**  

A análise revelou que:  
✔️ Alguns modelos possuem **grande variação de cores e configurações**, enquanto outros são mais padronizados.  
✔️ O modelo mais fabricado pode não ser necessariamente o que tem mais variações de cores ou configurações.  
✔️ Nenhuma coluna precisa ser removida, pois todas fornecem informações essenciais.  

#### **Decisão sobre Outliers**  
- Como os dados representam veículos **reais e já fabricados**, **não é necessário remover outliers**.  
- Histogramas, boxplots e gráficos de dispersão **não são necessários** nesta análise, pois não há valores extremos inválidos.  

---

### **8. Colunas e Descrição**  

| **Coluna**   | **Descrição** |
|-------------|--------------|
| **`ID`**  | Identificador único do carro. |
| **`MODELL`** | Código do modelo e motorização (6 caracteres). |
| **`FARBAU`** | Cor externa do veículo. |
| **`FARBIN`** | Cor interna do veículo. |
| **`ZIEL_LAND`** | País de destino do veículo. |
| **`PR`** | Código de configuração do carro (exemplo: `MOT:M7B` representa motor específico). |

---

### **9. Conclusão**  
O relatório apresentou:  
✅ **A quantidade de veículos fabricados por modelo**.  
✅ **A variação de cores disponíveis para cada modelo**.  
✅ **A diversidade completa considerando cores e configurações**.  
✅ **A decisão de não remover outliers, pois os dados representam veículos reais**.  

 Essa análise ajuda a entender **a produção e a personalização dos veículos**, sendo útil para decisões estratégicas de fabricação.