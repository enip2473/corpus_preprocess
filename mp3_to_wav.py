from glob import glob
import subprocess

def transfer():
    for audio in glob("clips/*.mp3"):
        name = audio.split(".")[0].split("/")[1]
        subprocess.run(f"ffmpeg -i clips/{name}.mp3 clips_wav/pre_{name}.wav", shell=True)

def check_sample_rate():
    for audio in glob("clips_wav/pre_*.wav"):
        new_name = audio.replace("pre_", "")
        subprocess.run(f"ffmpeg -y -i {audio} -ar 32000 {new_name}", shell=True)
    subprocess.run(f"rm -f clips_wav/pre_*.wav", shell=True)

def check_corruption():
    for audio in glob("clips_wav/*.wav"):
        subprocess.run(f"ffmpeg -v error -i {audio} -f null - 2>error.log", shell=True)

def get_statistics():
    total_files = len(glob("clips_wav/*.wav"))
    total_length = 0
    for audio in glob("clips_wav/*.wav"):
        process = subprocess.Popen(f"ffprobe -show_entries format=duration -i {audio} 2>/dev/null", stdout=subprocess.PIPE, shell=True)
        process.wait()
        output = process.stdout.readlines()[1].decode('utf-8')
        length = float(output.split("=")[-1])
        total_length += length
    return total_files, total_length


if __name__ == "__main__":
    # transfer()
    # check_sample_rate()
    # check_corruption()
    files, length = get_statistics()
    print(files, length)