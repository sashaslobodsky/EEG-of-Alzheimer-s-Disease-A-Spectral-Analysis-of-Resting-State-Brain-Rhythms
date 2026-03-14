# EEG Spectral Analysis of Alzheimer’s Disease
### Resting-State Brain Rhythms and Functional Connectivity


## Overview

This project investigates **differences in resting-state EEG activity between Alzheimer’s disease (AD) patients and healthy controls** using spectral signal processing methods.

Using EEG recordings, we analyze:

- **Power Spectral Density (PSD)**
- **Frequency band power**
- **Alpha-band functional connectivity (coherence)**

The goal is to understand how **neural oscillations and network synchronization change in Alzheimer’s disease**.


---

# Project Goals

The analysis aims to answer the research question:

> **How does resting-state EEG activity differ between Alzheimer’s disease patients and healthy controls?**

To address this question, the project analyzes EEG signals using:

- Spectral analysis
- Frequency band comparisons
- Functional connectivity measures


# Repository Structure
EEG-of-Alzheimer-s-Disease-A-Spectral-Analysis-of-Resting-State-Brain-Rhythms/

├── EEG_AD.py
│ Main analysis script

│
├── README.md
│ Project documentation

│
├── .gitignore
│ Files excluded from version control

│
└── Data/

└── COGS118C_FINALPRJ/

EEG dataset (downloaded separately)


# Dataset

This project uses the public EEG dataset described in:

**Miltiadous, A. et al. (2023)**  
*A Dataset of Scalp EEG Recordings of Alzheimer’s Disease, Frontotemporal Dementia and Healthy Subjects from Routine EEG.*

Dataset link:

https://openneuro.org/datasets/ds004504

The dataset includes:

- Alzheimer’s disease subjects
- Healthy control subjects
- Frontotemporal dementia subjects

For this project we analyze **Alzheimer’s vs healthy controls**.

---

# Downloading the Dataset

1. Go to the dataset page:

https://openneuro.org/datasets/ds004504

2. Download the dataset.

3. Extract the downloaded files.

4. Rename dataset folder to: COGS118C_FINALPRJ
   
5. Place the dataset inside the repository's `Data` folder.

Final directory structure should look like:
Data/

└── COGS118C_FINALPRJ/

├── participants.tsv

├── dataset_description.json

└── derivatives/

├── sub-001/

│ └── eeg/

│ └── sub-001_task-eyesclosed_eeg.set

├── sub-002/

└── ...


If the dataset is not placed in this exact location, the script will not be able to load the EEG data.

---

# Installation

Clone the repository:

```bash
git clone <REPOSITORY_URL>
cd EEG-of-Alzheimer-s-Disease-A-Spectral-Analysis-of-Resting-State-Brain-Rhythms
