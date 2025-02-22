# Complex survey data analysis in Brazil using R
### 1. Introduction - A little bit of context
John is an US citizen interested in answering these questions that are important for your master's degree project:
- Which state of Brazil had the **lowest** percentage of people employed in the 4th quarter of 2024;
- Which state of Brazil had the **highest** percentage of people employed in the 4th quarter of 2024;

### 2. Libraries used

```r
# INSTALL THE PACKAGE "PNADcIBGE"
install.packages("PNADcIBGE")

# LOAD THE LIBRARIES
library(PNADcIBGE)
library(survey)
library(tidyverse)
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
