# Formula 1 Race Predictor and Analysis
> [!NOTE]  
> Currently collecting race data.

## Overview
I've been a Formula 1 fan for a while now, always been fascinated with the intensity of this sport and how incredibly fit these drivers have to be in order to perform. Another incredible thing is just how much data is collected behind Formula 1, it's as much of a sport as it is a science experiment. I mean, a [single F1 car can have over 250 sensors on the car during race weekend](https://www.mercedesamgf1.com/news/feature-data-and-electronics-in-f1-explained). Can you image how much data is being collected just during a race with 250 sensors? Now, I’ve always been a spectator, but I was curious about what kind of data is being collected and what data I could access. I also wanted to see if I can find out: What are the biggest factors to winning? Is it the driver? Is it getting pole? Does weather increase or decrease drivers’ performance?

Some of these questions are what inspired this project. I wanted to dig deeper into the immense amount of data collected in Formula One and see if I can uncover trends or patterns that could influence race outcomes or winners.

### Why this project?
Well first, this is mostly for my curiosity. I always wondered what happens behind the scenes with all the data that is being collected. I want to highlight what factors greatly impact the probability of a driver wining a race but also discover any other factors for insight on Formula One racing. I hope that with this project, I could obtain insight on optimizing race strategies but also give analysis to a wider audience.

### Workflow
Project Definition → Data Collection → Data Cleaning → Data Analysis → Modeling → Evaluation → Interpreting Results

## Data Collection
For data collection, I am primarily using the [FastF1](https://docs.fastf1.dev/) API. I am also scraping [Formula 1's website](https://www.formula1.com/en/results/2024/races) to fill in the gaps in FastF1's data. For example, FastF1's API only has race dates from the 2018 season onwards, at the current moment of writing this, it is not significantly important but having multiple options especially from Formula One is beneficial.

### Races
For my first dataset collected for races, the data scraped from Formula 1’s website contains information of each season from 1950-2024 along with the winner, constructor of the winner, laps, and URL of each race. For the second dataset for races collected from FastF1's API, the dataset contains season, round number, grand prix, country, and location.
| Season | Grand Prix       | Date       | Winner                 | Constructor            | Laps | Time         | URL                                                                 |
|--------|------------------|------------|------------------------|------------------------|------|--------------|---------------------------------------------------------------------|
| 1950   | Great Britain    | 1950-05-13 | Nino FarinaFAR         | Alfa Romeo             | 70   | 2:13:23.600  | [Link](https://www.formula1.com/en/results/1950/races/94/great-britain/race-result) |
| 1950   | Monaco           | 1950-05-21 | Juan Manuel FangioFAN  | Alfa Romeo             | 100  | 3:13:18.700  | [Link](https://www.formula1.com/en/results/1950/races/95/monaco/race-result)      |
| 1950   | Indianapolis     | 1950-05-30 | Johnnie ParsonsPAR     | Kurtis Kraft Offenhauser | 138 | 2:46:55.970  | [Link](https://www.formula1.com/en/results/1950/races/96/indianapolis/race-result) |
| 1950   | Switzerland      | 1950-06-04 | Nino FarinaFAR         | Alfa Romeo             | 42   | 2:02:53.700  | [Link](https://www.formula1.com/en/results/1950/races/97/switzerland/race-result) |
| 1950   | Belgium          | 1950-06-18 | Juan Manuel FangioFAN  | Alfa Romeo             | 35   | 2:47:26.000  | [Link](https://www.formula1.com/en/results/1950/races/98/belgium/race-result)    |

<div align="center">
    <i>Table 1: Race data scraped from Formula 1 website.</i>
</div>
<br>

| Season | Round Number | Event Name            | Country       | Location      | Event Date |
|--------|--------------|-----------------------|---------------|---------------|------------|
| 1950   | 1            | British Grand Prix   | UK            | Silverstone   | NaN        |
| 1950   | 2            | Monaco Grand Prix    | Monaco        | Monte-Carlo   | NaN        |
| 1950   | 3            | Indianapolis 500     | USA           | Indianapolis  | NaN        |
| 1950   | 4            | Swiss Grand Prix     | Switzerland   | Bern          | NaN        |
| 1950   | 5            | Belgian Grand Prix   | Belgium       | Spa           | NaN        |

<div align="center">
    <i>Table 1.1: Race data collected from FastF1 API.</i>
</div>
