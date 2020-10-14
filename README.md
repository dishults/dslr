# Datascience X Logistic Regression
## Harry Potter and a Data Scientist
#### Recreation of the Hogwarts Sorting Hat (classifier) using muggle tools (logistic regression). Plus, data analysis and visualization in different ways.

## V.1 Data Analysis
    ./describe.py datasets/dataset_train.csv
The program that takes a dataset as a parameter and displays information
for all numerical features, like so:

                   Index    Hogwarts House     First Name      Last Name
    Count    1600.000000              1600           1600           1600
    Mean      799.500000               NaN            NaN            NaN
    Std       462.024530               NaN            NaN            NaN
    Min         0.000000               NaN            NaN            NaN
    25%       399.750000               NaN            NaN            NaN
    50%       799.500000               NaN            NaN            NaN
    75%      1199.250000               NaN            NaN            NaN
    Max      1599.000000               NaN            NaN            NaN

                Birthday      Best Hand       Arithmancy      Astronomy
    Count           1600           1600      1566.000000    1568.000000
    Mean             NaN            NaN     49634.570243      39.797131
    Std              NaN            NaN     16679.806036     520.298268
    Min              NaN            NaN    -24370.000000    -966.740546
    25%              NaN            NaN     38511.500000    -489.551387
    50%              NaN            NaN     49013.500000     260.289446
    75%              NaN            NaN     60811.250000     524.771949
    Max              NaN            NaN    104956.000000    1016.211940

               Herbology    Defense Against the Dark Arts     Divination
    Count    1567.000000                      1569.000000    1561.000000
    Mean        1.141020                        -0.387863       3.153910
    Std         5.219682                         5.212794       4.155301
    Min       -10.295663                       -10.162119      -8.727000
    25%        -4.308182                        -5.259095       3.099000
    50%         3.469012                        -2.589342       4.624000
    75%         5.419183                         4.904680       5.667000
    Max        11.612895                         9.667405      10.032000

             Muggle Studies    Ancient Runes    History of Magic    Transfiguration
    Count       1565.000000      1565.000000         1557.000000        1566.000000
    Mean        -224.589915       495.747970            2.963095        1030.096946
    Std          486.344840       106.285165            4.425775          44.125116
    Min        -1086.496835       283.869609           -8.858993         906.627320
    25%         -577.580096       397.511047            2.218653        1026.209993
    50%         -419.164294       463.918305            4.378176        1045.506996
    75%          254.994857       597.492230            5.825242        1058.436410
    Max         1092.388611       745.396220           11.889713        1098.958201

                 Potions    Care of Magical Creatures         Charms         Flying
    Count    1570.000000                  1560.000000    1600.000000    1600.000000
    Mean        5.950373                    -0.053427    -243.374409      21.958012
    Std         3.147854                     0.971457       8.783640      97.631602
    Min        -4.697484                    -3.313676    -261.048920    -181.470000
    25%         3.646785                    -0.671606    -250.652600     -41.870000
    50%         5.874837                    -0.044811    -244.867765      -2.515000
    75%         8.248173                     0.589919    -232.552305      50.560000
    Max        13.536762                     3.056546    -225.428140     279.070000

## V.2 Data Visualization
#### V.2.1 Histogram
    ./histogram.py datasets/dataset_train.csv
Script which displays a histogram answering the next question:
> **Which Hogwarts course has a homogeneous score distribution between all four houses?**

![Bonus histogram](https://github.com/dishults/dslr/blob/master/images/histogram_0.png)
![Histogram](https://github.com/dishults/dslr/blob/master/images/histogram_1.png)

#### V.2.2 Scatter plot
    ./scatter_plot.py datasets/dataset_train.csv
Script which displays a scatter plot answering the next question:
> **What are the two features that are similar?**

![Bonus scatter plot](https://github.com/dishults/dslr/blob/master/images/scatter_plot_0.png)
![Scatter plot](https://github.com/dishults/dslr/blob/master/images/scatter_plot_1.png)

#### V.2.3 Pair plot
    ./pair_plot.py datasets/dataset_train.csv
Script which displays a pair plot that might help you decide on:
> **What features are you going to use for your logistic regression?**

![Pair plot](https://github.com/dishults/dslr/blob/master/images/pair_plot.png)

## V.3 Logistic Regression
Magic Hat that performs a multi-classifier using a logistic regression one-vs-all
#### Train
    ./logreg_train.py datasets/dataset_train.csv [-f]
> -f -- to find 5 courses that would make the best combination for model training

Progam that trains through gradient descent multiple sets of parameters theta for one-vs-all logistic regression based on grades from the best combination of 5 courses
> generates `weights.csv` file

#### Predict
    ./logreg_predict.py datasets/dataset_test.csv weights.csv
Program that sorts students into Hogwarts houses
> generates `houses.csv` file

    $> cat houses.csv
    Index,Hogwarts House
    0,Gryffindor
    1,Hufflepuff
    2,Ravenclaw
    3,Hufflepuff
    4,Slytherin
    5,Ravenclaw
    6,Hufflepuff
            [...]
 
## Annex - Mathematics
#### Hypothesis
<img src="https://render.githubusercontent.com/render/math?math=h_\theta (x) = g ( \theta^T x )">

#### Logistic/Sigmoid Function
<img src="https://render.githubusercontent.com/render/math?math=g(z) = \dfrac{1}{1 %2B e^{-z}}">

#### Vectorized implementation of Gradient Descent
<img src="https://render.githubusercontent.com/render/math?math=\theta := \theta - \frac{\alpha}{m} X^T(g(X\theta) - \vec{y})">
