#!/bin/bash

sed -r 's/\t+/,/g' tcp_ids_and_dates.txt > tcp_ids_and_dates.csv
