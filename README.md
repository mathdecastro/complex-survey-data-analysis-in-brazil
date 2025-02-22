# Complex survey data analysis in Brazil using R
### 1. Introduction - A little bit of context
John is an US citizen interested in answering these questions that are important for your master's degree project:
- Which state of Brazil had the **lowest** percentage of people employed in the 4th quarter of 2024;
- Which state of Brazil had the **highest** percentage of people employed in the 4th quarter of 2024;

### 2. Libraries used

```r
# INSTALL THE PACKAGES "PNADcIBGE" AND "expss"
install.packages("PNADcIBGE")
install.packages("expss")

# LOAD THE LIBRARIES
library(PNADcIBGE)
library(tidyverse)
library(expss)
library(survey)
```

### 3. Selecting a list of variables of interest

```r
variables = c("UF","V2001","V2005","V2007","V2009",
              "V2010","VD3004","VD4001","VD4002","VD4020",
              "VD4035", "VD4003", "VD4005", "VD4004A")
```

### 4. Choosing the year and the quarter with the function "*get_pnadc*" and getting the data

```r
data = get_pnadc(year = 2024,
                 quarter = 4,
                 vars = variables)
```

### 5. Calculating the percentage

```r
# CALCULATING THE TOTAL OF PEOPLE EMPLOYED AND NOT EMPLOYED USING THE WEIGHTS CALCULATED BY "V1028" VARIABLE
indicators = data$variables %>%
 tab_cells(UF) %>%
 tab_cols(VD4002) %>%
 tab_weight(weight = V1028) %>%
 tab_stat_cases(total_statistic = "w_cases",
 total_label = "Total") %>%
 tab_pivot()

# TRANSFORMING THE DATA INTO A DATA FRAME AND RENAMING THE COLUMNS
indicators = as.data.frame(indicators)
colnames(indicators) = c("state", "people_employed", "people_not_employed")

# CREATING THE "PEOPLE NOT EMPLOYED" PERCENTAGE
indicators = indicators %>%
  mutate(people_not_employed_percentage = people_not_employed/(people_employed+people_not_employed)*100)

# DELETING THE ROW WITH THE TOTAL
indicators = indicators[-c(28),]

# ADDING ACRONYM OF THE STATE AND REGION OF THE STATE
indicators$state = c("RO", "AC", "AM", "RR", "PA", "AP", "TO", "MA", "PI", "CE", "RN", "PB", "PE", "AL", "SE", "BA", "MG", "ES", "RJ", "SP", "PR", "SC", "RS", "MS", "MT", "GO", "DF")
indicators$region = c(rep("N", 7),rep("NE", 9), rep("SE", 4), rep("S", 3), rep("CO", 4))

# SELECTING THE COLUMNS
indicators = indicators %>%
  select(state, region, people_not_employed_percentage)
```

#### The dataframe will be like this

| state | region | people_not_employed_percentage |
| --- | --- | ---|
| RO | N | 2.763382 |
| AC | N | 7.281652 |
| AM | N | 8.320457 |
| RR | N | 6.605799 |
| PA | N | 7.164774 |
| AP | N | 8.718797 |
| TO | N	| 5.058599 |
| MA | NE	| 6.863770 |
| PI | NE | 7.530549 |
| CE | NE	| 6.487631 |
| RN | NE	| 8.546885 |
| PB | NE	| 8.427995 |
| PE | NE	| 10.195519 |
| AL | NE	| 8.095677 |
| SE | NE	| 8.447182 |
| BA | NE	| 9.945569 |
| MG | SE	| 4.282403 |
| ES | SE	| 3.901851 |
| RJ | SE	| 8.201856 |
| SP | SE	| 5.923215 |
| PR | S | 3.251394 |
| SC | S | 2.670805 |
| RS | S | 4.530450 |
| MS | CO	| 3.737735 |
| MT | CO	| 2.464903 |
| GO | CO	| 4.815546 |
| DF | CO	| 9.067315 |
