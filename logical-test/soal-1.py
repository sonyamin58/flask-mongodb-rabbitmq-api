class SoalSatu:
    def __init__(self):
        self.OKGREEN = '\033[92m'
        self.OKBLUE = '\033[94m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'

    def input_total_kata(self):
        error = True
        while (error):
            input_total_kata = input("Input jumlah kata = ")
            if (input_total_kata.isnumeric() > 0):
                error = False
                return input_total_kata
            else:
                print(self.FAIL, "inputan (harus angka!)", self.ENDC)

    def input_kata(self, total_kata):
        list_kata_arr = []
        for key in range(int(total_kata)):
            input_kata = input("Input kata %d = " % (key+1))
            list_kata_arr.append(str(input_kata).lower())

        return list_kata_arr

    def handle(self, list_kata_arr):
        duplicate_kata = {
            "kata": "",
            "baris": []
        }
        for i, check in enumerate(list_kata_arr):
            for j, kata in enumerate(list_kata_arr):
                if (i != j) and (check == kata) and (len(duplicate_kata["baris"]) == 0 or duplicate_kata["kata"] == check):
                    duplicate_kata["kata"] = check
                    duplicate_kata["baris"].append(i+1)
                    break
        return duplicate_kata

    def output(self, duplicate_kata):
        if len(duplicate_kata["baris"]) > 0:
            print(self.OKBLUE)
            print("kata =", duplicate_kata["kata"])
            print(self.OKGREEN)
            print(duplicate_kata["baris"])
        else:
            print(self.FAIL)
            print(False)

        print(self.ENDC)


blueprint = SoalSatu()
input_total_kata = blueprint.input_total_kata()
input_kata_arr = blueprint.input_kata(input_total_kata)
result = blueprint.handle(input_kata_arr)
blueprint.output(result)
