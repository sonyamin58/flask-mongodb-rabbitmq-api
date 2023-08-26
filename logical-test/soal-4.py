from datetime import datetime, timedelta
import math


class SoalEmpat:
    def __init__(self):
        self.OKGREEN = '\033[92m'
        self.OKBLUE = '\033[94m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'
        self.CUTI_KANTOR = int(14)
        self.CUTI_BERSAMA = int(0)
        self.HARI_JOIN = int(180)  # 180 hari bisa ambil cuti
        self.HARI_SETAHUN = int(365)
        self.TGL_JOIN = "2023-01-01"
        self.TGL_CUTI = "2023-06-01"
        self.DURASI_CUTI = int(1)
        self.TOLAK_CUTI = None

    def is_date_matching(self, date_str):
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return False

    def input_jumlah_cuti_bersama(self):
        error = True
        while (error):
            cuti_bersama = input("Jumlah cuti bersama = ")
            if (cuti_bersama.isnumeric() > 0):
                error = False
                self.CUTI_BERSAMA = int(cuti_bersama)
            else:
                print(self.FAIL, "inputan (harus angka!)", self.ENDC)
        return self

    def input_tgl_join(self):
        error = True
        while (error):
            tgl_join = input("Tanggal join karyawan (Y-m-d) = ")
            if (self.is_date_matching(tgl_join)):
                tgl_join = datetime.strptime(tgl_join, '%Y-%m-%d')
                error = False
                self.TGL_JOIN = tgl_join
            else:
                print(self.FAIL, "inputan (harus sesuai format!)", self.ENDC)
        return self

    def input_tgl_cuti(self):
        error = True
        while (error):
            tgl_cuti = input("Tanggal cuti karyawan (Y-m-d) = ")
            if (self.is_date_matching(tgl_cuti)):
                tgl_cuti = datetime.strptime(tgl_cuti, '%Y-%m-%d')
                error = False
                self.TGL_CUTI = tgl_cuti
            else:
                print(self.FAIL, "inputan (harus sesuai format!)", self.ENDC)
        return self

    def input_durasi_cuti(self):
        error = True
        while (error):
            durasi_cuti = input("Durasi cuti (hari) = ")
            if (durasi_cuti.isnumeric() > 0):
                if (int(durasi_cuti) > 3):
                    print(self.FAIL, "cuti maksimal 3 hari!)", self.ENDC)
                else:
                    error = False
                    self.DURASI_CUTI = int(durasi_cuti)
            else:
                print(self.FAIL, "inputan (harus angka!)", self.ENDC)
        return self

    def handle(self):
        print(self.OKBLUE)
        print("cuti kantor :", self.CUTI_KANTOR)
        print("cuti bersama :", self.CUTI_BERSAMA)
        jumlah_cuti_pribadi = int(self.CUTI_KANTOR - self.CUTI_BERSAMA)
        print("jatah cuti :", jumlah_cuti_pribadi)

        tgl_bisa_cuti = (self.TGL_JOIN + timedelta(days=180)).date()
        print("tanggal bisa cuti :", tgl_bisa_cuti)

        tahun_bisa_cuti = int(tgl_bisa_cuti.strftime("%Y"))
        tgl_berakhir_cuti = datetime.now().date().replace(
            year=tahun_bisa_cuti, month=12, day=31)
        print("tanggal berakhir cuti :", tgl_berakhir_cuti)

        jumlah_hari = tgl_berakhir_cuti - tgl_bisa_cuti
        jumlah_hari = int(jumlah_hari.days)
        print("jumlah hari :", jumlah_hari)

        total_kuota_cuti = math.floor(
            int(jumlah_hari) / 365 * jumlah_cuti_pribadi)
        print("total kuota cuti :", total_kuota_cuti)
        print(self.ENDC)

        if self.DURASI_CUTI > total_kuota_cuti:
            self.TOLAK_CUTI = "hanya boleh mengambil " + \
                str(total_kuota_cuti)+" hari cuti"

        if self.TGL_CUTI.date() < tgl_bisa_cuti:
            self.TOLAK_CUTI = "belum 180 hari sejak tanggal join karyawan"

    def result(self):
        if self.TOLAK_CUTI is not None:
            print(False)
            print(self.FAIL, self.TOLAK_CUTI, self.ENDC)
        else:
            print(True)


blueprint = SoalEmpat()
blueprint.input_jumlah_cuti_bersama()
blueprint.input_tgl_join()
blueprint.input_tgl_cuti()
blueprint.input_durasi_cuti()
blueprint.handle()
blueprint.result()
