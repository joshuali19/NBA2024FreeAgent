# Predicting NBA 2024 Free Agent Salaries in Python

This project predicts the value of NBA Free Agents in 2024 by a machine learning (ML) model trained on the player's previous year basic and advanced statistics.

## File Organization

Here is how to navigate through the project:

```
|-finance
   |---advanced_stats
     |---CSV files of player stats from 2014-23
   |---cleaned_data
     |---CSV files of cleaned datasets
   |---finance
     |---Spyders for scraping
   |---intermediate_data
     |---CSV files of intermediate datasets
   |---models
     |---.pkl objects of trained models
   |---output
     |---CSV files of final predictions
   |---raw_data
     |---Raw CSV data sources
   |---.ipynb notebooks for ETL and Modeling
   |---SQL DB
```

## Abstract

NBA Free Agency is one of the most critical periods of the year for many organizations. With all the moving parts during the offseason, deciding on which players to sign and how much to pay them is difficult to identify quickly. The objective of this project answers this conundrum by building a model to streamline the process of deciding how much a player is worth based on their previous stats, accolades, and contracts. This model is pipelined into a financial dashboard of each NBA team’s payroll for the 24-25 season.These two components work in tandem to identify the positions that are lacking for each team, and identify potential free agents who would fit in their 2024-25 payroll situation.

Our **objective** is to build NBA offseason dashboards to be used by GMs to evaluate potential offseason moves and initiatives for their respective teams.

## References

Basketball-Reference was used to make this project viable, with various data sources from [depth charts](https://www.basketball-reference.com/teams/ATL/2024_depth.html), to player regular and [advanced statistics](https://www.basketball-reference.com/leagues/NBA_2024_per_game.html).