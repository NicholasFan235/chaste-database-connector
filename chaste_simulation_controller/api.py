import itertools


def all_parameter_combinations(variations:dict)->list[dict]:
    return [{k:v for k,v in zip(variations, parameter_set)} for parameter_set in itertools.product(*variations.values())]

def latin_hypercube_parameter_combinations(n_parameter_sets:int, parameter_options:dict, plot_distributions:bool=True)->list[dict]:
    from scipy.stats.qmc import LatinHypercube
    import scipy.stats
    import numpy as np
    import math

    if plot_distributions: import matplotlib.pyplot as plt

    sampler = LatinHypercube(len(parameter_options), scramble=False, strength=1, seed=0)
    samples = sampler.random(n=n_parameter_sets)
    for j, (key, opts) in enumerate(parameter_options.items()):
        if plot_distributions: fig, ax = plt.subplots(1,1, figsize=(8,8))
        if opts['distribution'] == 'linear':
            samples[:,j] = samples[:,j] * (opts['max'] - opts['min']) + opts['min']
            if plot_distributions: ax.set_title(f"Uniform [{opts['min']},{opts['max']})")
        elif opts['distribution'] == 'log':
            samples[:,j] = np.power(10, samples[:,j]*math.log10(opts['max']/opts['min']) + math.log10(opts['min']))
            if plot_distributions: ax.set_title(f"Log [{opts['min']},{opts['max']})")
        elif opts['distribution'] == 'normal':
            dist = scipy.stats.norm(loc=opts['mean'], scale=opts['std'])
            a,b = dist.cdf(opts['min']), dist.cdf(opts['max'])
            samples[:,j] = samples[:,j] * (b - a) + a
            samples[:,j] = dist.ppf(samples[:,j])
            samples[samples[:,j] > opts['max'],j] = opts['max']
            samples[samples[:,j] < opts['min'],j] = opts['min']
            if plot_distributions: ax.set_title(rf"Truncated Normal ($\mu=${opts['mean']},$\sigma=${opts['std']}) [{opts['min']},{opts['max']})")
        else:
            raise NotImplementedError(f"Variable Distribution {opts['distribution']} is not defined.")
        
        if plot_distributions:
            s = samples[:,j]
            if 'dtype' in opts: s = s.astype(opts['dtype'])
            ax.hist(s, bins=20)
            ax.set_xlabel(key)
            ax.set_ylabel('Frequency')
            fig.savefig(f'Distribution {key}.png')
            plt.close(fig)

    parameter_combinations = []
    for i in range(samples.shape[0]):
        parameter_set = dict()
        for j, (key, opts) in enumerate(parameter_options.items()):
            parameter_set[key] = samples[i,j]
            if 'dtype' in opts:
                if opts['dtype'] == "int":
                    parameter_set[key] = int(parameter_set[key])
        parameter_combinations.append(parameter_set)
    return parameter_combinations

def args_from_params_dict(params:dict)->str:
    return ' '.join([f'--{name.lstrip('--')}={value}' for name, value in params.items()])
