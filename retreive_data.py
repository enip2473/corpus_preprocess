import csv, os

def readfile(filename):
    with open(filename, 'r') as file:
        datas = list(csv.DictReader(file, delimiter="\t"))
    for data in datas:
        data["path"] = data["path"][:-4] + ".wav"
        data["id"] = data["path"][19:-4]
    return datas

def retrieve_text(datas):
    utt_text = [(data["id"], data["sentence"]) for data in datas]
    with open("text", "w+") as file:
        for utt, text in utt_text:
            print(utt, text, file=file)
    return utt_text

def file_path(datas):
    absolute_path = os.path.dirname(os.path.abspath(__file__)) + "/clips_wav/"

    paths = [(data["id"], data["path"]) for data in datas]
    with open("wav.scp", "w+") as file:
        for utt, filepath in paths:
            print(utt, absolute_path + filepath, file=file)
    return paths

def utt_to_speaker(datas):
    speakers = [(data["id"], data["client_id"]) for data in datas]
    with open("utt2spk", "w+") as file:
        for utt, spk in speakers:
            print(utt, spk, file=file)
    return speakers

def speaker_to_utt(datas):
    speakers = [(data["id"], data["client_id"]) for data in datas]
    speakers_utt = dict()
    for utt, speaker in speakers:
        if speaker not in speakers_utt:
            speakers_utt[speaker] = list()
        speakers_utt[speaker].append(utt)
    with open("spk2utt", "w+") as file:
        for spk in speakers_utt:
            print(spk, " ".join(speakers_utt[spk]), file=file)
    return speakers_utt

if __name__ == "__main__":
    datas = readfile("other.tsv") + readfile("validated.tsv")
    text = retrieve_text(datas)
    wav_scp = file_path(datas)
    utt2spk = utt_to_speaker(datas)
    spk2utt = speaker_to_utt(datas)


