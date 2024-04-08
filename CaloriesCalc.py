def calcul_calorii(proteine, carbohidrati, grasimi):
    calorii = proteine * 4 + carbohidrati * 4 + grasimi * 9
    return calorii


def main():
    print("Calculator de calorii din alimente")
    proteine = float(input("Introdu cantitatea de proteine (în grame): "))
    carbohidrati = float(input("Introdu cantitatea de carbohidrați (în grame): "))
    grasimi = float(input("Introdu cantitatea de grăsimi (în grame): "))

    total_calorii = calcul_calorii(proteine, carbohidrati, grasimi)

    print("Total calorii: ", total_calorii)


if __name__ == "__main__":
    main()
