# MatchingEngine

This project acts as a "Trading Simulation".

It is a simulation of how a simple financial exchange works. A user can submit a trade via the UI, and their order is processed 
in a price-time priority exchange. Other traders / users are simulated via datasets.

Through the UI (Flask backend, HTML/CSS/JS frontend), you can access multiple different stocks and trade with them. Each stock has its own inidividual wallet, and you can purchase shares for each one.

## Benchmarking Library

This project includes a lightweight benchmarking library that I used to test the effect of using Python3.13.7t (free-threaded Python).

I wrote a report on the tests in ```/benchmarking```, please do have a read!

## Project Purpose

The purpose of this project was to make a makeshift trading platform from scratch; I've implemented the logic for matching buy vs sell trades, as well as enabling user input so that they can trade on the app, making the graphs load the current and previous trade data, and more.

I originally created this in 2024, and since then I have a much stronger understanding of exchanges and I definitely write better Python code now! At the time, it was good fun trying to work all of it out without much prior knowledge!

## How to run

- Create a .venv with your chosen interpreter (recommended Python3.13)
- Run these commands:
```shell
pip install flask
pip install numpy
python app.py
```
- To run the benchmarking:
```shell
python -m benchmarking.test_csv_data
```

