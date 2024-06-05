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
            y.append(float(row[column]) if row[column] != 'T' else 0)

    plt.plot(x, y, color = 'g', linestyle = 'dashed', 
            marker = 'o',label = "Weather Data")

    plt.xticks(ticks=range(0, len(x), 3), labels=[x[i] for i in range(0, len(x), 3)], rotation=45) 
    plt.xlabel('Dates') 
    plt.ylabel(column_indices[column]) 
    plt.title(f'{column_indices[column]} For Spring 2024', fontsize = 20) 
    plt.grid() 
    plt.legend() 
    plt.show() 

def cumulative_graph():

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

        curr = 0
        for row in plots: 
            curr += float(row[column]) if row[column] != 'T' else 0
            x.append(row[0])
            y.append(curr)

    plt.plot(x, y, color = 'g', linestyle = 'dashed', 
            marker = 'o',label = "Cumulative Weather Data")

    plt.xticks(ticks=range(0, len(x), 3), labels=[x[i] for i in range(0, len(x), 3)], rotation=45) 
    plt.xlabel('Dates') 
    plt.ylabel(column_indices[column]) 
    plt.title(f'Cumulative {column_indices[column]} For Spring 2024', fontsize = 20) 
    plt.grid() 
    plt.legend() 
    plt.show() 

def find_avg():

    choice = int(input("Are you looking into data or variance? input 1 for data or 2 for variance: "))

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

        data = {
            'index': column,
            'name' : column_indices[column],
            'info' : [],
            'avg' : 0
        }

        curr = 0
        count = 0

        for row in plots: 
            value = float(row[column]) if row[column] != 'T' else 0
            
            
            data['info'].append(value)
            curr += value
            
            count += 1

        print(f'sum = {curr}')
        data['avg'] = (curr/count)

        pprint.pp(data)

def find_record_days():
    choice = int(input("1 for max temp, 2 for min temp, 3 for precip, 4 for snow: "))

    filename = 'data.csv'
    
    with open(filename, 'r') as csvfile: 
        plots = csv.reader(csvfile, delimiter=',') 
        column_names = next(plots)
        column_indices = {name: idx for idx, name in enumerate(column_names)}

        record_column = ''
        daily_info_column = ''
        record_breaks = []

        # Max temp
        if choice == 1:
            daily_info_column = 'daily_maxt'
            record_column = 'record_high_maxt'
        # Min temp
        elif choice == 2:
            daily_info_column = 'daily_mint'
            record_column = 'record_low_mint'
        # Precipitation
        elif choice == 3:
            daily_info_column = 'daily_precip'
            record_column = 'record_high_precip'
        # Snow
        elif choice == 4:
            daily_info_column = 'daily_snow'
            record_column = 'record_high_snow'
        else:
            raise ValueError("You put in the wrong number, brother")
            return

        # Ensure columns exist
        if daily_info_column not in column_indices or record_column not in column_indices:
            raise ValueError("Column not found in data")

        daily_info_index = column_indices[daily_info_column]
        record_index = column_indices[record_column]

        for row in plots:
            daily_value = float(row[daily_info_index]) if row[daily_info_index] != 'T' else 0
            record_value = float(row[record_index])
            if daily_value >= record_value:
                difference = daily_value - record_value
                record_breaks.append({
                    'date': row[0],
                    'daily_value': daily_value,
                    'record_value': record_value,
                    'difference': difference
                })

        print(f"Days with record-breaking {daily_info_column}:")
        for record in record_breaks:
            print(f"Date: {record['date']}, New Value: {record['daily_value']}, Old Record: {record['record_value']}, Difference: {record['difference']}")


            
        


if __name__ == '__main__':
    choice = int(input("1 for graph, 2 for cumulative graph, 3 for avg, 4 for record breaking days: "))

    if choice == 1:
        graph()

    elif choice == 2:
        cumulative_graph()

    elif choice == 3:
        find_avg()

    elif choice == 4:
        find_record_days()


    else:
        ValueError("You dun put in the wrong number, brÖther")