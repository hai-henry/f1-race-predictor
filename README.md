# Formula 1 Race Predictor and Analysis
> [!NOTE]  
> Currently collecting constructors' data.

- [x] Collect Races
- [X] Collect Race Results
- [x] Collect Qualifying data
- [x] Collect Sprint  Data
- [x] Collect Drivers & Driver Standings
- [ ] Collect Constructors and Constructor Standings
- [ ] Collect Lap Times
- [ ] Collect Weather Data


## Overview
I've been a Formula 1 fan for a while now, always been fascinated with the intensity of this sport and how incredibly fit these drivers have to be in order to perform. Another incredible thing is just how much data is collected behind Formula 1, it's as much of a sport as it is a science experiment. I mean, a [single F1 car can have over 250 sensors on the car during race weekend](https://www.mercedesamgf1.com/news/feature-data-and-electronics-in-f1-explained). Can you image how much data is being collected just during a race with 250 sensors? Now, I’ve always been a spectator, but I was curious about what kind of data is being collected and what data I could access. I also wanted to see if I can find out: What are the biggest factors to winning? Is it the driver? Is it getting pole? Does weather increase or decrease a driver’s performance?

Some of these questions are what inspired this project. I wanted to dig deeper into the immense amount of data collected in Formula One and see if I can uncover trends or patterns that could influence race outcomes or winners.

### Why this project?
Well first, this is mostly for my curiosity. I always wondered what happens behind the scenes with all the data that is being collected. I want to highlight what factors greatly impact the probability of a driver wining a race but also discover any other factors for insight on Formula One racing. I hope that with this project, I could obtain insight on optimizing race strategies but also give analysis to a wider audience.

### Workflow
Project Definition → Data Collection → Data Cleaning → Data Analysis → Modeling → Evaluation → Interpreting Results

## Data Collection
For data collection, I am primarily using the [FastF1](https://docs.fastf1.dev/) API. I am also scraping [Formula 1's website](https://www.formula1.com/en/results/2024/races) to fill in the gaps in FastF1's data. For example, FastF1's API only has race dates from the 2018 season onwards, at the current moment of writing this, it is not significantly important but having multiple options especially from Formula One is beneficial.

### Races
For my first dataset collected for races, the data scraped from Formula 1’s website contains information of each season from 1950-2024 along with the winner, constructor of the winner, laps, and URL of each race. For the second dataset for races collected from FastF1's API, the dataset contains season, round number, grand prix, sessions, country, and location.
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

| Season | RoundNumber | Country | Location      | OfficialEventName | EventDate           | EventName            | EventFormat   | Session1     | Session1Date | Session1DateUtc     | Session2     | Session2Date | Session2DateUtc     | Session3     | Session3Date | Session3DateUtc     | Session4     | Session4Date | Session4DateUtc     | Session5 | Session5Date | Session5DateUtc     | F1ApiSupport |
|--------|-------------|---------|---------------|--------------------|---------------------|----------------------|---------------|--------------|--------------|---------------------|--------------|--------------|---------------------|--------------|--------------|---------------------|--------------|--------------|---------------------|---------|--------------|---------------------|--------------|
| 1950   | 1           | UK      | Silverstone   |                    | 1950-05-13 00:00:00 | British Grand Prix   | conventional  | Practice 1   |              | 1950-05-11 00:00:00 | Practice 2   |              | 1950-05-11 00:00:00 | Practice 3   |              | 1950-05-12 00:00:00 | Qualifying   |              | 1950-05-12 00:00:00 | Race    |              | 1950-05-13 00:00:00 | False         |
| 1950   | 2           | Monaco  | Monte-Carlo   |                    | 1950-05-21 00:00:00 | Monaco Grand Prix    | conventional  | Practice 1   |              | 1950-05-19 00:00:00 | Practice 2   |              | 1950-05-19 00:00:00 | Practice 3   |              | 1950-05-20 00:00:00 | Qualifying   |              | 1950-05-20 00:00:00 | Race    |              | 1950-05-21 00:00:00 | False         |
| 1950   | 3           | USA     | Indianapolis  |                    | 1950-05-30 00:00:00 | Indianapolis 500     | conventional  | Practice 1   |              | 1950-05-28 00:00:00 | Practice 2   |              | 1950-05-28 00:00:00 | Practice 3   |              | 1950-05-29 00:00:00 | Qualifying   |              | 1950-05-29 00:00:00 | Race    |              | 1950-05-30 00:00:00 | False         |
| 1950   | 4           | Switzerland | Bern     |                    | 1950-06-04 00:00:00 | Swiss Grand Prix     | conventional  | Practice 1   |              | 1950-06-02 00:00:00 | Practice 2   |              | 1950-06-02 00:00:00 | Practice 3   |              | 1950-06-03 00:00:00 | Qualifying   |              | 1950-06-03 00:00:00 | Race    |              | 1950-06-04 00:00:00 | False         |
| 1950   | 5           | Belgium | Spa           |                    | 1950-06-18 00:00:00 | Belgian Grand Prix   | conventional  | Practice 1   |              | 1950-06-16 00:00:00 | Practice 2   |              | 1950-06-16 00:00:00 | Practice 3   |              | 1950-06-17 00:00:00 | Qualifying   |              | 1950-06-17 00:00:00 | Race    |              | 1950-06-18 00:00:00 | False         |
<div align="center">
    <i>Table 1.1: Raw race data collected from FastF1 API.</i>
</div>

### Results
My second dataset was the results of each races. I used FastF1's api to fetch each race from 1950-2024 and collected information such as position, grid starting poistion, time, status(will give reason for retirement, not just finish), and any other information I thought would be helpful later such as the driver information (team, country).

| Season | RoundNumber | EventName          | DriverNumber | BroadcastName | Abbreviation | DriverId   | TeamName    | TeamColor | TeamId  | FirstName | LastName     | FullName      | HeadshotUrl | CountryCode | Position | ClassifiedPosition | GridPosition | Q1  | Q2  | Q3  | Time               | Status    | Points |
|--------|-------------|--------------------|--------------|---------------|--------------|------------|-------------|-----------|---------|-----------|--------------|---------------|-------------|-------------|----------|--------------------|-------------|-----|-----|-----|--------------------|-----------|--------|
| 1950   | 1           | British Grand Prix | 2            |               | farina       | Alfa Romeo |             | alfa      | Nino    | Farina     | Nino Farina   |              |             | 1.0        | 1                  | 1.0         |     |     |     | 0 days 02:13:23.600000 | Finished  | 9.0    |
| 1950   | 1           | British Grand Prix | 3            |               | fagioli      | Alfa Romeo |             | alfa      | Luigi   | Fagioli    | Luigi Fagioli |              |             | 2.0        | 2                  | 2.0         |     |     |     | 0 days 00:00:02.600000 | Finished  | 6.0    |
| 1950   | 1           | British Grand Prix | 4            |               | reg_parnell  | Alfa Romeo |             | alfa      | Reg     | Parnell    | Reg Parnell   |              |             | 3.0        | 3                  | 4.0         |     |     |     | 0 days 00:00:52    | Finished  | 4.0    |
| 1950   | 1           | British Grand Prix | 14           |               | cabantous    | Talbot-Lago|             | lago      | Yves    | Cabantous  | Yves Cabantous|              |             | 4.0        | 4                  | 6.0         |     |     |     |                    | +2 Laps   | 3.0    |
| 1950   | 1           | British Grand Prix | 15           |               | rosier       | Talbot-Lago|             | lago      | Louis   | Rosier     | Louis Rosier  |              |             | 5.0        | 5                  | 9.0         |     |     |     |                    | +2 Laps   | 2.0    |

<div align="center">
    <i>Table 1.2: Raw race results data collected from FastF1 API.</i>
</div>

### Qualifying
The third dataset is qualifying results for each race. I also used FastF1's API here to fetch each qualifying result but noticed that FastF1's API only had qualifying data from 1994 onwards. Qualifying also had many changes and tweaks throughout Formula 1's history until 2010, where the current qualifying format is now used. So the dataset for qualifying isn't consistent. This dataset has information on drivers, their qualifying times from each stage, grid positions, and additional information from the API request.

| Season | RoundNumber | EventName            | DriverNumber | BroadcastName | Abbreviation | DriverId         | TeamName  | TeamColor | TeamId    | FirstName       | LastName     | FullName               | HeadshotUrl | CountryCode | Position | ClassifiedPosition | GridPosition | Q1               | Q2  | Q3  | Time                  | Status | Points |
|--------|-------------|----------------------|--------------|---------------|--------------|------------------|-----------|-----------|-----------|------------------|--------------|------------------------|-------------|-------------|----------|--------------------|--------------|-----|-----|-----|-----------------------|--------|--------|
| 1994   | 1           | Brazilian Grand Prix | 2            |               | nan          | senna            | Williams  |           | williams  | Ayrton           | Senna        | Ayrton Senna           |             |             | 1.0      |                    |              |     |     | 0 days 00:01:15.962000|        |        |
| 1994   | 1           | Brazilian Grand Prix | 5            |               | MSC          | michael_schumacher| Benetton  |           | benetton  | Michael          | Schumacher   | Michael Schumacher     |             |             | 2.0      |                    |              |     |     | 0 days 00:01:16.290000|        |        |
| 1994   | 1           | Brazilian Grand Prix | 27           |               | nan          | alesi            | Ferrari   |           | ferrari   | Jean             | Alesi        | Jean Alesi             |             |             | 3.0      |                    |              |     |     | 0 days 00:01:17.385000|        |        |
| 1994   | 1           | Brazilian Grand Prix | 0            |               | nan          | damon_hill       | Williams  |           | williams  | Damon            | Hill         | Damon Hill             |             |             | 4.0      |                    |              |     |     | 0 days 00:01:17.554000|        |        |
| 1994   | 1           | Brazilian Grand Prix | 30           |               | nan          | frentzen         | Sauber    |           | sauber    | Heinz-Harald     | Frentzen     | Heinz-Harald Frentzen |             |             | 5.0      |                    |              |     |     | 0 days 00:01:17.806000|        |        |

<div align="center">
    <i>Table 1.3: Raw qualifying data collected from FastF1 API.</i>
</div>

### Sprints
The sprint race weekend format is fairly new so there isn't much data to be collected for this dataset but I decided to collect aall the races that had the sprint race weekend format, the results of each sprint, and sprint qualifying(formerly known as shootout) results. I thought this data would still be helpful as drivers still raced and competed for points during sprint races.
|   season |   RoundNumber | Country       | Location    | OfficialEventName                                                        | EventDate           | EventName                 | EventFormat   | Session1   | Session1Date              | Session1DateUtc     | Session2   | Session2Date              | Session2DateUtc     | Session3   | Session3Date              | Session3DateUtc     | Session4   | Session4Date              | Session4DateUtc     | Session5   | Session5Date              | Session5DateUtc     | F1ApiSupport   |
|---------:|--------------:|:--------------|:------------|:-------------------------------------------------------------------------|:--------------------|:--------------------------|:--------------|:-----------|:--------------------------|:--------------------|:-----------|:--------------------------|:--------------------|:-----------|:--------------------------|:--------------------|:-----------|:--------------------------|:--------------------|:-----------|:--------------------------|:--------------------|:---------------|
|     2021 |            10 | Great Britain | Silverstone | FORMULA 1 PIRELLI BRITISH GRAND PRIX 2021                                | 2021-07-18 00:00:00 | British Grand Prix        | sprint        | Practice 1 | 2021-07-16 14:30:00+01:00 | 2021-07-16 13:30:00 | Qualifying | 2021-07-16 18:00:00+01:00 | 2021-07-16 17:00:00 | Practice 2 | 2021-07-17 12:00:00+01:00 | 2021-07-17 11:00:00 | Sprint     | 2021-07-17 16:30:00+01:00 | 2021-07-17 15:30:00 | Race       | 2021-07-18 15:00:00+01:00 | 2021-07-18 14:00:00 | True           |
|     2021 |            14 | Italy         | Monza       | FORMULA 1 HEINEKEN GRAN PREMIO D’ITALIA 2021                             | 2021-09-12 00:00:00 | Italian Grand Prix        | sprint        | Practice 1 | 2021-09-10 14:30:00+02:00 | 2021-09-10 12:30:00 | Qualifying | 2021-09-10 18:00:00+02:00 | 2021-09-10 16:00:00 | Practice 2 | 2021-09-11 12:00:00+02:00 | 2021-09-11 10:00:00 | Sprint     | 2021-09-11 16:30:00+02:00 | 2021-09-11 14:30:00 | Race       | 2021-09-12 15:00:00+02:00 | 2021-09-12 13:00:00 | True           |
|     2021 |            19 | Brazil        | São Paulo   | FORMULA 1 HEINEKEN GRANDE PRÊMIO DE SÃO PAULO 2021                       | 2021-11-14 00:00:00 | São Paulo Grand Prix      | sprint        | Practice 1 | 2021-11-12 12:30:00-03:00 | 2021-11-12 15:30:00 | Qualifying | 2021-11-12 16:00:00-03:00 | 2021-11-12 19:00:00 | Practice 2 | 2021-11-13 12:00:00-03:00 | 2021-11-13 15:00:00 | Sprint     | 2021-11-13 16:30:00-03:00 | 2021-11-13 19:30:00 | Race       | 2021-11-14 14:00:00-03:00 | 2021-11-14 17:00:00 | True           |
|     2022 |             4 | Italy         | Imola       | FORMULA 1 ROLEX GRAN PREMIO DEL MADE IN ITALY E DELL'EMILIA-ROMAGNA 2022 | 2022-04-24 00:00:00 | Emilia Romagna Grand Prix | sprint        | Practice 1 | 2022-04-22 13:30:00+02:00 | 2022-04-22 11:30:00 | Qualifying | 2022-04-22 17:00:00+02:00 | 2022-04-22 15:00:00 | Practice 2 | 2022-04-23 12:30:00+02:00 | 2022-04-23 10:30:00 | Sprint     | 2022-04-23 16:30:00+02:00 | 2022-04-23 14:30:00 | Race       | 2022-04-24 15:00:00+02:00 | 2022-04-24 13:00:00 | True           |
|     2022 |            11 | Austria       | Spielberg   | FORMULA 1 ROLEX GROSSER PREIS VON ÖSTERREICH 2022                        | 2022-07-10 00:00:00 | Austrian Grand Prix       | sprint        | Practice 1 | 2022-07-08 13:30:00+02:00 | 2022-07-08 11:30:00 | Qualifying | 2022-07-08 17:00:00+02:00 | 2022-07-08 15:00:00 | Practice 2 | 2022-07-09 12:30:00+02:00 | 2022-07-09 10:30:00 | Sprint     | 2022-07-09 16:30:00+02:00 | 2022-07-09 14:30:00 | Race       | 2022-07-10 15:00:00+02:00 | 2022-07-10 13:00:00 | True           |

<div align="center">
    <i>Table 1.4: Dataset of sprint races collected from FastF1 API.</i>
</div>
<br>

|   season |   RoundNumber |   DriverNumber | BroadcastName   | Abbreviation   |   DriverId | TeamName        | TeamColor   |   TeamId | FirstName   | LastName   | FullName        | HeadshotUrl                                                                                                               | CountryCode   |   Position |   ClassifiedPosition |   GridPosition | Q1                     | Q2                     | Q3                     |   Time |   Status |   Points |
|---------:|--------------:|---------------:|:----------------|:---------------|-----------:|:----------------|:------------|---------:|:------------|:-----------|:----------------|:--------------------------------------------------------------------------------------------------------------------------|:--------------|-----------:|---------------------:|---------------:|:-----------------------|:-----------------------|:-----------------------|-------:|---------:|---------:|
|     2023 |             4 |             16 | C LECLERC       | LEC            |        nan | Ferrari         | F91536      |      nan | Charles     | Leclerc    | Charles Leclerc | https://www.formula1.com/content/dam/fom-website/drivers/C/CHALEC01_Charles_Leclerc/chalec01.png.transform/1col/image.png | MON           |          1 |                  nan |            nan | 0 days 00:01:42.820000 | 0 days 00:01:42.500000 | 0 days 00:01:41.697000 |    nan |      nan |      nan |
|     2023 |             4 |             11 | S PEREZ         | PER            |        nan | Red Bull Racing | 3671C6      |      nan | Sergio      | Perez      | Sergio Perez    | https://www.formula1.com/content/dam/fom-website/drivers/S/SERPER01_Sergio_Perez/serper01.png.transform/1col/image.png    | MEX           |          2 |                  nan |            nan | 0 days 00:01:43.858000 | 0 days 00:01:42.925000 | 0 days 00:01:41.844000 |    nan |      nan |      nan |
|     2023 |             4 |              1 | M VERSTAPPEN    | VER            |        nan | Red Bull Racing | 3671C6      |      nan | Max         | Verstappen | Max Verstappen  | https://www.formula1.com/content/dam/fom-website/drivers/M/MAXVER01_Max_Verstappen/maxver01.png.transform/1col/image.png  | NED           |          3 |                  nan |            nan | 0 days 00:01:43.288000 | 0 days 00:01:42.417000 | 0 days 00:01:41.987000 |    nan |      nan |      nan |
|     2023 |             4 |             63 | G RUSSELL       | RUS            |        nan | Mercedes        | 6CD3BF      |      nan | George      | Russell    | George Russell  | https://www.formula1.com/content/dam/fom-website/drivers/G/GEORUS01_George_Russell/georus01.png.transform/1col/image.png  | GBR           |          4 |                  nan |            nan | 0 days 00:01:43.763000 | 0 days 00:01:43.112000 | 0 days 00:01:42.252000 |    nan |      nan |      nan |
|     2023 |             4 |             55 | C SAINZ         | SAI            |        nan | Ferrari         | F91536      |      nan | Carlos      | Sainz      | Carlos Sainz    | https://www.formula1.com/content/dam/fom-website/drivers/C/CARSAI01_Carlos_Sainz/carsai01.png.transform/1col/image.png    | ESP           |          5 |                  nan |            nan | 0 days 00:01:43.622000 | 0 days 00:01:42.909000 | 0 days 00:01:42.287000 |    nan |      nan |      nan |

<div align="center">
    <i>Table 1.5: Raw sprint qualifying data collected from FastF1 API.</i>
</div>
<br>

|   season |   RoundNumber |   DriverNumber | BroadcastName   | Abbreviation   | DriverId       | TeamName        | TeamColor   | TeamId   | FirstName   | LastName   | FullName        | HeadshotUrl                                                                                                               |   CountryCode |   Position |   ClassifiedPosition |   GridPosition |   Q1 |   Q2 |   Q3 | Time                   | Status   |   Points |
|---------:|--------------:|---------------:|:----------------|:---------------|:---------------|:----------------|:------------|:---------|:------------|:-----------|:----------------|:--------------------------------------------------------------------------------------------------------------------------|--------------:|-----------:|---------------------:|---------------:|-----:|-----:|-----:|:-----------------------|:---------|---------:|
|     2021 |            10 |             33 | M VERSTAPPEN    | VER            | max_verstappen | Red Bull Racing | 0600EF      | red_bull | Max         | Verstappen | Max Verstappen  | https://www.formula1.com/content/dam/fom-website/drivers/M/MAXVER01_Max_Verstappen/maxver01.png.transform/1col/image.png  |           nan |          1 |                    1 |              2 |  nan |  nan |  nan | 0 days 00:25:38.426000 | Finished |        3 |
|     2021 |            10 |             44 | L HAMILTON      | HAM            | hamilton       | Mercedes        | 00D2BE      | mercedes | Lewis       | Hamilton   | Lewis Hamilton  | https://www.formula1.com/content/dam/fom-website/drivers/L/LEWHAM01_Lewis_Hamilton/lewham01.png.transform/1col/image.png  |           nan |          2 |                    2 |              1 |  nan |  nan |  nan | 0 days 00:00:01.430000 | Finished |        2 |
|     2021 |            10 |             77 | V BOTTAS        | BOT            | bottas         | Mercedes        | 00D2BE      | mercedes | Valtteri    | Bottas     | Valtteri Bottas | https://www.formula1.com/content/dam/fom-website/drivers/V/VALBOT01_Valtteri_Bottas/valbot01.png.transform/1col/image.png |           nan |          3 |                    3 |              3 |  nan |  nan |  nan | 0 days 00:00:07.502000 | Finished |        1 |
|     2021 |            10 |             16 | C LECLERC       | LEC            | leclerc        | Ferrari         | DC0004      | ferrari  | Charles     | Leclerc    | Charles Leclerc | https://www.formula1.com/content/dam/fom-website/drivers/C/CHALEC01_Charles_Leclerc/chalec01.png.transform/1col/image.png |           nan |          4 |                    4 |              4 |  nan |  nan |  nan | 0 days 00:00:11.278000 | Finished |        0 |
|     2021 |            10 |              4 | L NORRIS        | NOR            | norris         | McLaren         | FF9800      | mclaren  | Lando       | Norris     | Lando Norris    | https://www.formula1.com/content/dam/fom-website/drivers/L/LANNOR01_Lando_Norris/lannor01.png.transform/1col/image.png    |           nan |          5 |                    5 |              6 |  nan |  nan |  nan | 0 days 00:00:24.111000 | Finished |        0 |

<div align="center">
    <i>Table 1.6: Raw sprint qualifying results data collected from FastF1 API.</i>
</div>
