import matplotlib.pyplot as plt 
import csv 
import pprint

def graph():

    choice = int(input("Are you looking into data or variance? input 1 for data or 2 for variance: "))

    x = [] 
    y = [] 
    filename = ''
    if choice == 1:
        filename = 'data.csv' 

    elif choice == 2:
        filename = 'variance.csv'

    else:
        ValueError("You dun put in the wrong number, brÖther")
        return

    
    with open(filename,'r') as csvfile: 
        plots = csv.reader(csvfile, delimiter = ',') 
        column_names = next(plots)
        column_indices = {idx: name for idx, name in enumerate(column_names)}

        print("Column Names and Indices: ")
        pprint.pp(column_indices)

        column = int(input("Which would you like to have be your y-axis? Enter the number or else I'm gunna cry: "))        

        
        for row in plots: 
            x.append(row[0]) 
            y.append(float(row[column]))

    plt.plot(x, y, color = 'g', linestyle = 'dashed', 
            marker = 'o',label = "Weather Data")

    plt.xticks(ticks=range(0, len(x), 3), labels=[x[i] for i in range(0, len(x), 3)], rotation=45) 
    plt.xlabel('Dates') 
    plt.ylabel(column_indices[column]) 
    plt.title(f'{column_indices[column]} For Spring 2024', fontsize = 20) 
    plt.grid() 
    plt.legend() 
    plt.show() 

graph()
