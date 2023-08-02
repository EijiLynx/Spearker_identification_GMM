import os
import warnings
import numpy as np
import _pickle as pik
import extractor
from scipy.io.wavfile import read
from sklearn.mixture import GaussianMixture as GMM

warnings.filterwarnings("ignore")
source = "sounds/"
taker = []

dest = "speaker-models/"


# train_file = "sounds.txt"
# file_paths = open(train_file, 'r')


# path to training data
# source = "SampleData/"
def testing(testing):
    # path where training speakers will be saved
    # modelpath = "speaker-models/"
    modelpath = testing
    outlet = "testing.wav"

    gmm_files = [os.path.join(modelpath, fname) for fname in
                 os.listdir(modelpath) if fname.endswith('.gmm')]

    # Load the Gaussian gender Models
    models = [pik.load(open(fname, 'rb')) for fname in gmm_files]
    speakers = [fname.split("/")[-1].split(".gmm")[0] for fname
                in gmm_files]

    # sr, audio = read(source + path)
    sr, audio = read(outlet)

    vector = extractor.extract_features(audio, sr)

    log_likelihood = np.zeros(len(models))

    for i in range(len(models)):
        gmm = models[i]  # checking with each model one by one
        scores = np.array(gmm.score(vector))
        log_likelihood[i] = scores.sum()

    winner = np.argmax(log_likelihood)
    print(winner)
    print(log_likelihood[winner])
    print("\tdetected as - ", speakers[winner])
    return speakers[winner]


def create_model():
    train_file = "names.txt"
    file_paths = open(train_file, 'r')
    count = 1
    features = np.asarray(())
    print(features)
    for path in file_paths:
        path = path.strip()
        print(path)
        taker.append(path)

        # read the audio
        sr, audio = read(source + path)

        # extract 40 dimensional MFCC & delta MFCC features
        vector = extractor.extract_features(audio, sr)

        if features.size == 0:
            features = vector
        else:
            features = np.vstack((features, vector))
        # when features of 5 files of speaker are concatenated, then do model training
        # -> if count == 5: --> edited below
        if count == 5:
            gmm = GMM(n_components=16, max_iter=200, covariance_type='diag', n_init=3)
            gmm.fit(features)

            # dumping the trained gaussian model
            picklefile = path.split("-")[0] + ".gmm"
            kl = path.split("-")[0]
            pik.dump(gmm, open(dest + picklefile, 'wb'))
            print('+ modeling completed for speaker:', picklefile, " with data point = ", features.shape)
            kt = '+ completed for speaker:' + str(kl) + " with data point = " + str(features.shape)
            taker.append(kt)
            features = np.asarray(())
            count = 0
        count = count + 1

    return taker
