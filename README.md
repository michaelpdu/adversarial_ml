# Adversarial-Machine-Learning

Adversarial Machine Learning project for experiment

## Install packages

This project is based on python3, so please install following packages in pip3.

```
sudo pip3 install numpy
sudo pip3 install xgboost
sudo pip3 install lief
```

If you want to run Windows tool(such as, HouseCallX) in Linux, please install Wine. You could refer to [https://wiki.winehq.org/Ubuntu](https://wiki.winehq.org/Ubuntu)

## Description

### Automation Tool

In terminal, type following command:

```python
Usage:
    python3 start.py
```

There is no parameters here, but we could modify config file to support different settings.

### Configuration File

please refer to [config.json](./config.json)

Common config:

```json
    "common": {
        "enable_system_cpu": false,
        "use_cpu_count": 1,
        "free_disk": 4096,
        "samples": "samples/coinminer",
        "generated_dir": "new_generated_samples",
        "remove_not_bypassed": false,

        "__algorithm_comments__": "ga|bruteforce",
        "algorithm": "ga",

        "__target_comments__": "trendx_script|trendx_pe|tlsh_html|tlsh_pe",
        "target": "tlsh_pe"
    }, 
```

- `enable_system_cpu`: if there're 4 CPU in machine, it will use 4 processes to run automation tool
- `use_cpu_count`: if enable_system_cpu is true, this value is omited, or there will be `use_cpu_count` processes
- `samples`: target sample path, it supports file path and directory path
- `generated_dir`: where do the new generated samples saved
- `remove_not_bypassed`: remove not bypassed samples or not
- `algorithm`: it supports `ga` and `bruteforce`
- `target`: target tool here, it only supports `trendx_pe` and `tlsh_pe` now

Give an example here, if we want to try to bypass TrendX for PE detection in Genetic Algorithm. We could set common config item below:

```json
    ...
    "algorithm": "ga",
    "target": "trendx_pe"
    ...
```

### Cuckoo Sandbox

```json
    "cuckoo": {
        "enable": false,
        "scan_in_file_proc": false
    }
```

- `cuckoo.enable`: if it's true, automation tool will use Cuckoo Sandbox to run generated PE
- `cuckoo.scan_in_file_proc`: if it's true, run generated PE in Sandbox after generating PE, or check all of PE at the end of PE generation.

Before PE adversarial process, it's necessary to startup cuckoo sandbox if you enable cuckoo in configuration file. Please refer to following instructions:

- startup VirtualBox and VMs
- startup Cuckoo Sandbox (use command 'cuckoo community' to load Cuckoo Signatures)

For more details, please refer to Cuckoo Sandbox: https://cuckoo.sh/docs/index.html

### Genetic Algorithm

```json
    "genetic_algorithm" : {
        "dna_size": 20,
        "population_size": 30,
        "mating_prob": 0.8,
        "mutation_prob": 0.03,
        "generations": 40,
        "start_index": 0
    },
```

- `dna_size`: how many DNA files would be used in Genetic Algorithm
- `population_size`: population size
- `generations`: how many generations in GA
- `start_index`: specify DNA start index, if start_index is 5 and dna_size is 7, DNA indexes are [5, 6, 7, 8, 9, 10, 11]. Make sure total DNA size >= start_index+dna_size 

### Brute force

```json
    "dna_manager": {
        "random_section_count": 16
    },
    "pe_generator_random": {
        "count": 20,
        "round": 10
    },
```

- `dna_manager.random_section_count`: how many random section DNA files would be used
- `pe_generator_random.count`: count of random generated PE in one round
- `pe_generator_random.round`: how many round in PE generation

Give an example here: 

if dna_manager.random_section_count is 5, there are 5 random sections would be inserted into new PE.

if pe_generator_random.count is 20 and pe_generator_random.round is 10, there would be 200(=20*10) new PE generated.

### Target Tools

We place target tools in `./tools/`folder, and config them in configuration file.

```json
    "trendx": {
        "scan_type": 1,
        "housecallx": "tools/housecallx"
    },
    "tlsh": {
        "scan_type": 1,
        "tlsh_tool": "tools/tlsh"
    },
```

Before TLSH evasion, please install TLSH firstly. More details, please refer to Jon's Github: [https://github.trendmicro.com/CoreTech-ERS/Library-tlsh](https://github.trendmicro.com/CoreTech-ERS/Library-tlsh)

### Unit Test

**Anytime before submiting code, please run UT firstly!!!**

```
Usage:
    python3 ut.py
```

## Utility Tools

### generate JS function DNA files

This tool could analyze JavaScript files and dump all of function snippets.

``` python
Usage:
    python function_analyzer.py target dest_dir
```

This function will analyze target(folder or file), and generate many function files.

### generate PE section DNA files

In pe_modifier folder, there is a script to generate PE section DNA files.

```
Usage:
    python create_sections_dna.py PE_target_path dest_path
```

