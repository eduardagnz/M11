## **1. Exploração inicial do dataset**  
A primeira parte do código tem como objetivo entender a estrutura e o conteúdo dos dados.

### **1.1. Visualização inicial**
- `head(InteliFalhas, n=10)`: Exibe as 10 primeiras linhas do dataset para uma visão geral.
- `str(InteliFalhas)`: Retorna a estrutura dos dados, mostrando os tipos das colunas (numérico, fator, string etc.).
- `summary(InteliFalhas)`: Apresenta estatísticas básicas como:
  - Média, mínimo, máximo e quartis para colunas numéricas.
  - Contagem de valores únicos para colunas categóricas.

---

## **2. Limpeza e seleção de colunas**
A limpeza do dataset foca na remoção de colunas consideradas desnecessárias para a análise.

### **2.1. Remoção de colunas**
O código cria um novo dataframe, `final_data`, selecionando apenas colunas que são consideradas relevantes:

```r
final_data <- InteliFalhas[, c("ID", "DATA DETECCAO", "PONTO","LOC_ID","POS_ID","TYPE_ID")]
```

As colunas removidas e os motivos são:
- **Descrições de IDs** → Como os IDs já representam informações únicas, não é necessário manter colunas adicionais que apenas descrevem esses IDs.
- **Linha e coluna cartesiana da posição da falha** → Parece que essas coordenadas não são essenciais, já que a posição da falha (`POS_ID`) já encapsula essa informação.
- **`view_id`** → O motivo da remoção dessa coluna não foi finalizado no texto, mas pode ser por não agregar valor na análise.

### **2.2. Colunas mantidas no dataset final**
- **`ID`** → Identificador único do veículo.
- **`DATA DETECCAO`** → Data e hora da detecção da falha.
- **`PONTO`** → Etapa do processo em que a falha foi identificada (Ex.: ZP, Rodagem, Água).
- **`LOC_ID`** → Parte do carro afetada (Ex.: Tampa traseira, Alavanca do freio manual).
- **`POS_ID`** → Posição da falha dentro da peça (Ex.: Direita, Esquerda, Superior esquerda).
- **`TYPE_ID`** → Tipo de erro detectado (Ex.: Repuxado de cola, Resíduo de soldagem).

---

## **3. Instalação e carregamento de pacotes**
O código verifica se os pacotes necessários estão instalados e os instala automaticamente se não estiverem:

```r
packages <- c("ggplot2", "dplyr", "corrplot", "FactoMineR", "factoextra")

install_if_missing <- function(pkg) {
  if (!require(pkg, character.only = TRUE)) {
    install.packages(pkg, dependencies = TRUE)
    library(pkg, character.only = TRUE)
  }
}

lapply(packages, install_if_missing)

cat("Todas as bibliotecas foram instaladas e carregadas com sucesso!\n")
```

Isso assegura que todas as bibliotecas utilizadas nos gráficos e na análise estatística estarão disponíveis.

---

## **4. Visualizações gráficas**
A análise gráfica é dividida em três partes:
1. **Gráficos univariados** → Frequência de falhas em cada variável.
2. **Gráficos bivariados** → Relação entre duas variáveis.
3. **Análise multivariada** → Matriz de correlação e PCA.

### **4.1. Gráficos Univariados (Distribuição de variáveis)**
Esses gráficos mostram a contagem de falhas em diferentes categorias.

- **Contagem de falhas por PONTO**  
  Mostra onde as falhas ocorrem ao longo do processo de fabricação.

  ```r
  ggplot(final_data, aes(x = PONTO)) + 
    geom_bar(fill = "steelblue") + 
    theme_minimal() + 
    coord_flip() +
    labs(title = "Contagem de falhas por PONTO", x = "PONTO", y = "Contagem")
  ```

- **Contagem de falhas por TYPE_ID (Tipo de erro)**  
  Exibe os tipos de erro mais frequentes.

  ```r
  ggplot(final_data, aes(x = as.factor(TYPE_ID))) + 
    geom_bar(fill = "darkorange") + 
    theme_minimal() + 
    labs(title = "Contagem de falhas por TYPE_ID", x = "Tipo de erro", y = "Contagem")
  ```

- **Contagem de falhas por LOC_ID (Parte afetada)**  
  Identifica quais partes do carro têm mais falhas.

  ```r
  ggplot(final_data, aes(x = as.factor(LOC_ID))) + 
    geom_bar(fill = "purple") + 
    theme_minimal() + 
    labs(title = "Contagem de falhas por LOC_ID", x = "Parte do carro", y = "Contagem")
  ```

### **4.2. Gráficos Bivariados (Relação entre variáveis)**
Aqui, analisamos como uma variável influencia outra.

- **Distribuição de TYPE_ID por PONTO**  
  Exibe a distribuição dos tipos de erro em cada etapa do processo.

  ```r
  ggplot(final_data, aes(x = PONTO, fill = as.factor(TYPE_ID))) + 
    geom_bar(position = "dodge") + 
    theme_minimal() + 
    coord_flip() +
    labs(title = "Distribuição de TYPE_ID por PONTO", x = "PONTO", y = "Contagem")
  ```

- **Distribuição de TYPE_ID por LOC_ID**  
  Mostra quais partes do carro estão mais associadas a determinados tipos de falhas.

  ```r
  ggplot(final_data, aes(x = as.factor(LOC_ID), fill = as.factor(TYPE_ID))) + 
    geom_bar(position = "dodge") + 
    theme_minimal() + 
    labs(title = "Distribuição de TYPE_ID por LOC_ID", x = "LOC_ID", y = "Contagem")
  ```

---

## **5. Análise Multivariada**
Agora, analisamos correlações entre variáveis numéricas e aplicamos **Análise de Componentes Principais (PCA)**.

### **5.1. Matriz de Correlação**
Cria uma matriz para entender como as variáveis numéricas se relacionam.

```r
cor_matrix <- cor(final_data %>% select(LOC_ID, POS_ID, TYPE_ID))
corrplot(cor_matrix, method = "circle", type = "upper")
```
- Um gráfico circular (`corrplot`) representa os coeficientes de correlação entre as variáveis.

### **5.2. Análise de Componentes Principais (PCA)**
O PCA reduz a dimensionalidade dos dados para identificar padrões.

```r
pca_res <- PCA(final_data %>% select(LOC_ID, POS_ID, TYPE_ID), graph = FALSE)
```

Visualização dos componentes principais:

```r
fviz_pca_var(pca_res, col.var = "blue")
```
- O gráfico exibe como cada variável influencia os componentes principais.

---

## **6. Relatório Final**
O notebook finaliza documentando as mudanças feitas e justificando as escolhas de colunas.

- **Alterações realizadas**
  - Remoção de descrições desnecessárias (`ID` já representa a informação única).
  - Exclusão de colunas de posição cartesiana (`POS_ID` já captura essa informação).

- **Colunas finais**
  - `ID`, `DATA DETECCAO`, `PONTO`, `LOC_ID`, `POS_ID`, `TYPE_ID`.

---

## **Resumo**
Esse notebook executa um **pipeline de análise de dados**, que inclui:
1. **Exploração** → Estrutura e estatísticas do dataset.
2. **Limpeza** → Remoção de colunas irrelevantes.
3. **Visualização** → Gráficos para detectar padrões.
4. **Análise avançada** → Correlação e PCA.
5. **Relatório** → Documentação das mudanças.

Ele é útil para **entender onde e quais falhas acontecem no processo de fabricação de veículos**! 🚗💨