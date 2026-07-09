def mono(arr):
    a=ab=True
    for i in range(1,len(arr)):
        if arr[i-1]>arr[i-1]:
            b=False
        elif arr[i]<arr[i-1]:
            a=False
        return a or b
    arr1=[1,2,2,3]
    arr2=[3,2,1]
    arr3=[1,3,2,4]
    print(mono(arr1))
    print(mono(arr2))
    print(mono(arr3))