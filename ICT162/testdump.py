
def num_digits(n):
    n = str(n)
    count = 0
    for i in n:
        count += 1
    print(count)



def main():
    while True:
        try:
            test = int(input("enter numbers"))
            break
        except:
            print("Please input integers only!")

    
    num_digits(test)

main()