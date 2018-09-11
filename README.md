# gaitgmm

## Performance Evaluation of GMMs for Inertial Sensor-based Gait Biometrics

### Context

Code repository of paper submitted for CINTI 2018, Informatics section.

### Dataset

The ZJU-GaitAcc dataset can be obtained [here](http://www.cs.zju.edu.cn/~gpan/database/gaitacc.html). Feature extraction has been already performed on the data with a [Java application](https://github.com/nemesszili/gaitgmm/tree/javafeat) and the results are in the features [directory](https://github.com/nemesszili/gaitgmm/tree/master/features).

The dataset contains walking data captured by 5 accelerometers (Wii Remote, ADXL330) fastened at five different body locations. The data obtained from the accelerometers were resampled with a frequency of 100 Hz. The dataset contains walking data of 175 subjects recorded in two sessions. 22 subjects participated in only one session (their recordings were grouped into a separate session, named **session0**), and 153 subjects participated in both sessions (**session1** and **session2**). There are 6 records per subject in one session. The time interval between the two sessions is at least one week and at most half a year. The subjects were tasked with walking on a 20m long floor. The recording lengths are 7-15s containing 7-14 full step cycles. One advantage of this dataset is that the authors also provided a manual annotation of the step cycles. In this paper, we used only the data from a single accelerometer, the one fastened to the right hip.

### Evaluation

Performances are reported using widely used metrics used for biometric systems, such as **Equal Error Rate (EER)** and **Area Under Curve (AUC)**.
We considered the following baseline evaluation protocol:

|                      | Same-day                       | Cross-day |
|----------------------|--------------------------------|-----------|
| **Training**         | session1 (50% - first half)    | session1 (50% - first half)|
| **Testing positive** | session1 (50% - second half)   | session2 (all samples) |
| **Testing negative** | sampled session0 (u012 - u022) | sampled session0 (u012 - u022)|

### How it works

Install [pipenv](https://pipenv.readthedocs.io/en/latest/) before proceeding.

`pip install --user pipenv`

After installation, enter the cloned project and run:

`pipenv install`

This will install all project dependencies. Next, create the virtual environment:

`pipenv shell`

Run the script with:

`python main.py`

There are two ways to define evaluation parameters:
- set them accordingly in [util/settings.py](https://github.com/nemesszili/gaitgmm/blob/master/util/settings.py)
- use command line arguments (options) and specify `--no-config` to override `settings.py`

#### Options

The options below can be used to generate plots or to explicitly specify
arguments.

| Plots         | Description |
|:-------------:|-------------|
| `--plot`      | Generate figure 3 from the paper |
| `--plot-auc`  | Plot system AUC for current settings |
| `--plot-hist` | Plot system histogram for current settings |

| Settings                            | Description |
|:-----------------------------------:|-------------|
| `--no-config`                       | Override `settings.py` with command-line options |
| `--cross-session/--same-session`    | Evaluate with data from session 2 **OR** Evaluate with data from session 1 (test data from the same session as training) |
| `--cycle/--fixed`                   | Use annotations from the dataset **OR** Use fixed frames of 128 samples |
| `--num-cycles`                      | Number of consecutive cycles used for evaluation |
| `--adapted-gmm/--classic-gmm`       | Use MAP adapted GMMs **OR** Train GMMs from scratch |
| `--reg-negatives/--unreg-negatives` | Use negative data from users that the model has already encountered **OR** Use unencountered data from unregistered users |
