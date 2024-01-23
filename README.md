# loader_stat_gibdd_ru

This is a simple loader statistics from site stat.gibdd.ru (traffic accidents in Russia). 

Usage: python3 loader.py year region

Region is internal number of region in project stat.gibdd.ru (for Moscow - 45). 

After starting this script downloads statistics of all traffic accidents with dead and wounded people and store it in current directory. Each month statistics is storing in file with pattern year_month.xml


