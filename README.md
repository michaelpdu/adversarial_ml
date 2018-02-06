# Adversary-Machine-Learning
Adversary Machine Learning project for experiment

## Interface Description

### automation tool
In startup.py, it supports JavaScript and PE adversary process. More detailed information, please refer to following Usage.

```
Usage:
    (a) find bypassed script sample
        >> python startup.py --file-type JS --file-path malicious_script --dna DNA_dir --start start_index --step DNA_size
        e.g.
        >> python startup.py --file-type JS --file-path samples/mal_script/0a0b692133dbba549c81dec49e1ba2ccf1b2bfea --dna DNA_JS/function_snippets --start 0 --step 32
      OR
    (b) find bypassed PE sample
        >> python3 startup.py --file-type PE --file-path malicious_pe --dna DNA_dir --start start_index --step DNA_size --tool housecallx_dir
        e.g.
        >> python3 startup.py --file-type PE --file-path samples/mal_pe/6d3e5e56984a7e91c7a8c434224b73886d413d1d1f435358f40bf78c71c1932d --dna DNA_PE/section_add --start 64 --step 32 --tool housecallx
```
### function analyzer

This tool could analyze JavaScript files and dump all of function snippets.

#### Usage

``` python
python function_analyzer.py target dest_dir
```

This function will analyze target(folder or file), and generate many function files.


### how to generate new sample

#### Usage

```python
Usage:
    python concat_files.py ori_file fun_code_dir output_dir
```

### how to use TrendX tool?

In trendx_tool folder, execute following command.
```python
python run.py target
```

