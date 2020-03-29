import tempfile

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import numpy as np
import librosa
import matplotlib.pyplot as plt
import librosa.display
import soundfile as sf
from os import path
from pydub import AudioSegment
# files

from pydub.utils import which

AudioSegment.converter = which("ffmpeg")

from urllib.request import urlopen

src = "files/media/little-big_-_uno.mp3"
dst = "files/media/test.wav"

spectrogram = "spectrogram.png"
context = {
    'spectrogram': 'files/media/spectrogram.png'
}


def home(request):
    if request.method == 'POST' and request.FILES['document']:
        uploaded_file = request.FILES['document']
        print(uploaded_file.name)
        fs = FileSystemStorage(location='files/media')
        fs.save(uploaded_file.name, uploaded_file)

        sound = AudioSegment.from_mp3(src)
        sound.export(dst, format="wav")

        # data = open('media/little-big_-_uno_DWciZv1.mp3').read()
        # # urlopen('media/little-big_-_uno_DWciZv1.mp3').read()
        # f = tempfile.NamedTemporaryFile(delete=False)
        # f.write(data)
        # AudioSegment.from_mp3(src).export('result.ogg', format='ogg')
        # data = urlopen('https://sample-videos.com/audio/mp3/crowd-cheering.mp3').read()
        # f = tempfile.NamedTemporaryFile(delete=False)
        # f.write(data)
        # AudioSegment.from_mp3(f).export('files/media/test.ogg', format='ogg')
        # f.close()

        # AudioSegment.from_file(src).export('files/media/test.wav', format='wav')
        # f.close()

        # filename = "files/media/test.ogg"
        # data = sf.read('test.wav')

        # 2. Load the audio as a waveform `y`и
        #    Store the sampling rate as `sr`
        X, sample_rate = sf.read('files/media/test.wav')
        X = X.mean(axis=1)

        y, sr = librosa.load(X)

        # balyys
        D = np.abs(librosa.stft(y))
        print(D)

        # D_left = np.abs(librosa.stft(y, center=False))
        # D_short = np.abs(librosa.stft(y, hop_length=64))

        plt.switch_backend('agg')
        librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max), y_axis='log', x_axis='time')
        plt.title('Power spectrogram')
        plt.colorbar(format='%+2.0f dB')
        plt.tight_layout()
        plt.savefig('files/media/spectrogram.png')
        # plt.show()

        # # 3. Run the default beat tracker
        # tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        # print('Estimated tempo: {:.2f} beats per minute'.format(tempo))
        # # 4. Convert the frame indices of beat events into timestamps
        # beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    # return render(request, 'music_conversion/music_conversion.html', context)
    return render(request, 'music_conversion/music_conversion.html')


def about(request):
    return render(request, 'music_conversion/about.html')
