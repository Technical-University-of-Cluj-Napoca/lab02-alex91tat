def multiply_all(*args: int) -> int:
    rez = 1
    for num in args:
        rez *= num

    return rez

# if __name__ == "__main__":
#     print(f"multiply_all(1, 2, 3, 4, 5) => {multiply_all(1, 2, 3, 4, 5)}") 
#     print(f"multiply_all() => {multiply_all()}")  
#     print(f"multiply_all(7) => {multiply_all(7)}")