import sys
import numpy as np
from os.path import isfile, join as opj
from umap import UMAP
from embedding_config import config
from embedding_helpers import distance_funcs


order, seed = [int(i) for i in sys.argv[1:]]
trajs_dir = opj(config['datadir'], 'trajectories')
embeddings_dir = opj(config['datadir'], 'embeddings')
models_dir = opj(config['datadir'], 'fit_reducers')

ff_traj = np.load(opj(trajs_dir, 'forces_lecture.npy'))
bos_traj = np.load(opj(trajs_dir, 'bos_lecture.npy'))
questions = np.load(opj(trajs_dir, 'all_questions.npy'))

ff_len = len(ff_traj)
bos_len = len(bos_traj)

if order == 1:
    to_reduce = [ff_traj] + [bos_traj] + list(questions)
elif order == 2:
    to_reduce = [ff_traj] + list(questions) + [bos_traj]
elif order == 3:
    to_reduce = [bos_traj] + [ff_traj] + list(questions)
elif order == 4:
    to_reduce = [bos_traj] + list(questions) + [ff_traj]
elif order == 5:
    to_reduce = list(questions) + [ff_traj] + [bos_traj]
else:
    to_reduce = list(questions) + [bos_traj] + [ff_traj]

split_inds = np.cumsum([np.atleast_2d(vec).shape[0] for vec in to_reduce])[:-1]
stacked_vecs = np.log(np.vstack(to_reduce))

for n_neighbors in [5, 10, 15] + list(range(20, 201, 20)):
    for min_dist in (.1, .3, .5, .7, .9):
        for spread in range(1, 10, 2):
            for met, dist_func in distance_funcs.items():
                fname = f"seed{seed}_nn{n_neighbors}_md{min_dist}_sp{spread}_{met}.npy"
                embpath = opj(embeddings_dir, f'order{order}', fname)
                modpath = opj(models_dir, f'order{order}', fname)
                if isfile(embpath) and isfile(modpath):
                    continue

                params = {
                    'n_components': 2,
                    'init': 'spectral',
                    'metric': dist_func,
                    'random_state': seed,
                    'n_neighbors': n_neighbors,
                    'min_dist': min_dist,
                    'spread': spread
                }
                np.random.seed(seed)
                reducer = UMAP(**params).fit(stacked_vecs)

                stacked_embeddings = reducer.transform(stacked_vecs)
                embeddings = np.vsplit(stacked_embeddings, split_inds)

                ff_emb = next(i for i in embeddings if len(i) == ff_len)
                bos_emb = next(i for i in embeddings if len(i) == bos_len)
                qs_embs = np.squeeze([i for i in embeddings if len(i) == 1])
                embs_ordered = [ff_emb, bos_emb, qs_embs]

                np.save(embpath, embs_ordered)
                np.save(modpath, reducer)
