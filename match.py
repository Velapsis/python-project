# Comparer un record par rapport un son de la base de données
# Format: hash(fréquence1, fréquence2, anchor_t, delta_t)
def TryMatch(record, song):
    for recordHash in record:
        for songHash in song:
            if (recordHash[0] > songHash[0]+40 | recordHash[0] < songHash[0]+40):
                return False
            if (recordHash[1] > songHash[1]+40 | recordHash[1] < songHash[1]+40):
                return False
            if (recordHash[2] > songHash[2]+10 | recordHash[2]-10):
                return False
            if (recordHash[3] > songHash[3]+15 | recordHash[3] > songHash[3]+15):
                return False
            else:
                return True