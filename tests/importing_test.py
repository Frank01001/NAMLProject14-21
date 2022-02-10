from feat_ext.sample_processing import *
from nearest_centroid.nearest_centroid_classifier import NearestCentroidClassifier

genre_names = ['blues', 'classical', 'country', 'disco', 'hipop', 'jazz', 'metal', 'pop', 'reggae', 'rock']

path = 'C:\\Users\\frapa\\Music\\Fall of Arcana (New Era Version) Looped.wav'
signal = load_audio_signal(path, 'int32')
signal = select_30sec_extract(signal, sampling_rate=44100)

zcr, avg_eng, sr = get_feature_triplet(signal)
sample = np.array([zcr, avg_eng, sr])

data = pd.read_csv('C:\\Users\\frapa\\PycharmProjects\\namlProject14-21\\extracted_dataset.csv')

training_set, training_labels, valid_set, valid_labels = get_normalized_train_valid_sets(data)

ncc = NearestCentroidClassifier()
ncc.train(training_set, training_labels)

predicted = ncc.classify(sample, genres_to_classify=genre_names)

print('Classified %s as %s' % (path, predicted))

