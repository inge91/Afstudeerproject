import csv

def main():
    # opens the csv file
    t = open('map4.txt', 'a')
    with open('MapInfo.csv', 'rb') as f:
        for row in f:
            l = row.split(", ")
            #in case of new x coord create newline
            if l[1] == "0":
                t.write("\n")
            # in case walkable draw a 1
            if l[2] == "1":
                t.write("0 ")
            else:
                t.write("1 ")


if __name__ == "__main__":
    main()
