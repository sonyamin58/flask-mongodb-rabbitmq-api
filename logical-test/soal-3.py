class SoalTiga:
    def __init__(self):
        self.OKGREEN = '\033[92m'
        self.OKBLUE = '\033[94m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'
        self.PEMBUKA = ["<", "{", "["]
        self.PENUTUP = [">", "}", "]"]
        self.MAX = 4096
        self.RESULT = self.OKGREEN

    def input_syntax(self):
        error = True
        while (error):
            syntax = input("Masukan syntax = ")
            if (len(syntax) > self.MAX):
                print(self.FAIL, "inputan (maksimal",
                      self.MAX, "karakter)", self.ENDC)
            else:
                error = False
                return syntax

    def check(self, syntax):
        valid = True
        temp = []
        for i, char in enumerate(syntax):
            if char in self.PEMBUKA:
                temp.append(char)

            if char in self.PENUTUP:
                if (len(temp) > 0):
                    index_penutup = self.PENUTUP.index(char)
                    pasangan_penutup = self.PEMBUKA[index_penutup]
                    pembuka_sebelumnya = temp[len(temp)-1]
                    if (pasangan_penutup == pembuka_sebelumnya):
                        temp.pop()
                else:
                    valid = False
                    self.RESULT = self.FAIL
                    break

            if (i == len(syntax) - 1) and (len(temp) > 0):
                valid = False
                self.RESULT = self.FAIL
                break

        return valid


blueprint = SoalTiga()
syntax = blueprint.input_syntax()
valid = blueprint.check(syntax)
print(blueprint.RESULT, valid, blueprint.ENDC)
