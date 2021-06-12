import sys

def check(arr):
    for x in range(1, arr[0]+1):
        i = 0
        while i < len(arr):

            if arr[i] == x:
                interval = arr[(i+1):(i+arr[i]+1)]

                if len(interval) == x and sum(interval) == x-1:
                    del arr[(i+1):(i+arr[i]+1)]
                else:
                    return 0

            i += 1
    return int(len(arr) == 1)
            
def main():
    for line in sys.stdin:
        d = [int(x) for x in line.split()]
        print(check(d))

if __name__ == "__main__":
    main()