import math


class SoalDua:
    def __init__(self):
        self.OKGREEN = '\033[92m'
        self.OKBLUE = '\033[94m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'
        self.PECAHAN = [
            {"nominal": 100000, "jenis": "lembar"},
            {"nominal": 50000, "jenis": "lembar"},
            {"nominal": 20000, "jenis": "lembar"},
            {"nominal": 10000, "jenis": "lembar"},
            {"nominal": 5000, "jenis": "lembar"},
            {"nominal": 2000, "jenis": "lembar"},
            {"nominal": 2000, "jenis": "lembar"},
            {"nominal": 1000, "jenis": "lembar"},
            {"nominal": 500, "jenis": "koin"},
            {"nominal": 200, "jenis": "koin"},
            {"nominal": 100, "jenis": "koin"}
        ]

    def total_belanja_customer(self):
        error = True
        while (error):
            total_belanja = input("Total belanja seorang customer Rp ")
            # print("total_belanja ===", total_belanja)
            if (total_belanja.isnumeric() > 0):
                error = False
                return total_belanja
            else:
                print(self.FAIL, "inputan (harus angka)!", self.ENDC)

    def total_bayar_customer(self, total_belanja):
        error = True
        while (error):
            uang_pembeli = input("Pembeli membayar Rp ")
            # print("uang_pembeli ===", uang_pembeli)
            if (uang_pembeli.isnumeric() > 0):
                if (int(uang_pembeli) < int(total_belanja)):
                    print(self.FAIL, "Uang pembeli, kurang bayar", self.ENDC)
                else:
                    error = False
                    return uang_pembeli
            else:
                print(self.FAIL, "inputan (harus angka!)", self.ENDC)

    def total_kembalian(self, total_belanja, uang_pembeli):
        kembalian = int(uang_pembeli) - int(total_belanja)
        kembalian_bulat = int(math.floor(kembalian / 100)) * 100

        print(self.OKBLUE)
        print("Kembalian yang harus diberikan kasir Rp", kembalian,
              ",dibulatkan menjadi Rp", kembalian_bulat, self.ENDC)
        return kembalian_bulat

    def handle(self, kembalian_fix):
        result_arr = []
        temp = kembalian_fix
        for i, pecahan in enumerate(self.PECAHAN):
            if temp >= pecahan['nominal']:
                total = int(temp / pecahan['nominal'])
                result_arr.append({
                    "pecahan": pecahan,
                    "total": total
                })
                temp = temp - (int(pecahan['nominal'] * total))
        return result_arr

    def output(self, result_arr):
        total_pecahan = 0
        print(self.OKGREEN)
        print('Pecahan uang:')
        for i, val in enumerate(result_arr):
            total = val['pecahan']['nominal'] * val['total']
            print(val['total'], val['pecahan']['jenis'],
                  val['pecahan']['nominal'], ":", total)
            total_pecahan += total

        print("total (", total_pecahan, ")")
        print(self.ENDC)


blueprint = SoalDua()
total_belanja_customer = blueprint.total_belanja_customer()
total_bayar_customer = blueprint.total_bayar_customer(total_belanja_customer)
total_kembalian = blueprint.total_kembalian(
    total_belanja_customer,
    total_bayar_customer
)
result = blueprint.handle(total_kembalian)
blueprint.output(result)
