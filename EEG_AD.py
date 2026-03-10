# Imports
import os
from pathlib import Path
import pandas as pd
import mne
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Dataset root
DATASET_ROOT = Path("Data/COGS118C_Final_Project")
print("Dataset root:", DATASET_ROOT.resolve())
print("Root exists:", DATASET_ROOT.exists())
print("participants exists:", (DATASET_ROOT / "participants.tsv").exists())

if not DATASET_ROOT.exists():
    raise FileNotFoundError("Dataset root folder not found.")

if not (DATASET_ROOT / "participants.tsv").exists():
    raise FileNotFoundError("participants.tsv not found in dataset root.")

# Load participants
participants = pd.read_csv(DATASET_ROOT / "participants.tsv", sep="\t")

print(participants.columns)
print(participants["Group"].value_counts())

# Separate groups
ad_subjects = participants[participants["Group"] == "A"]
hc_subjects = participants[participants["Group"] == "C"]

print("Alzheimer Subjects:", len(ad_subjects))
print("Healthy Subjects:", len(hc_subjects))

# Sample 20 from each
ad_sample = ad_subjects.sample(20, random_state=42)#random_state included so that it produces same random result so that results can become reproducible
hc_sample = hc_subjects.sample(20, random_state=42)

selected_subjects = pd.concat([ad_sample, hc_sample])
subject_ids = selected_subjects["participant_id"].tolist()

print(subject_ids[:10])

results = []
all_psd = []
all_groups = []
freqs_saved = None

# Making sure everything is in the folders
for subject in subject_ids:
    try:
        eeg_folder = DATASET_ROOT / "derivatives" / subject / "eeg"
        print("Checking folder:", eeg_folder)

        if not eeg_folder.exists():
            print("Folder not found:", eeg_folder)
            continue

        eeg_files = [f for f in os.listdir(eeg_folder) if f.endswith(".set")]
        print("Found files:", eeg_files)

        if len(eeg_files) == 0:
            print("No .set file found for", subject)
            continue

        file_path = eeg_folder / eeg_files[0]

        raw = mne.io.read_raw_eeglab(file_path, preload=True)
        print("Loaded:", subject)
        print(raw)

        # Preprocess
        raw.filter(0.5, 40.0)
        raw.notch_filter(50.0)
        raw.set_eeg_reference("average")

        # Compute PSD with Welch
        data = raw.get_data()
        sfreq = raw.info["sfreq"]

        psd, freqs = mne.time_frequency.psd_array_welch(
            data,
            sfreq=sfreq,
            fmin=0.5,
            fmax=40.0,
            n_fft=1024
        )

        subject_psd = psd.mean(axis=0)
        all_psd.append(subject_psd)
        freqs_saved = freqs

        # Average PSD across channels and frequencies in each band
        delta = psd[:, (freqs >= 1) & (freqs < 4)].mean()
        theta = psd[:, (freqs >= 4) & (freqs < 8)].mean()
        alpha = psd[:, (freqs >= 8) & (freqs < 13)].mean()
        beta = psd[:, (freqs >= 13) & (freqs < 30)].mean()

        group = participants.loc[
            participants["participant_id"] == subject, "Group"
        ].values[0]

        all_groups.append(group)

        results.append({
            "participant_id": subject,
            "group": group,
            "delta": delta,
            "theta": theta,
            "alpha": alpha,
            "beta": beta
        })

        print("Processed:", subject)
    #double checking if something is missing or failed to run
    except Exception as e:
        print(f"Skipping {subject} due to error: {e}")
        continue

# Convert to dataframe
results_df = pd.DataFrame(results)

print(results_df.head())
if results_df.empty:
    raise ValueError("No subjects were processed successfully. Check dataset folder structure.")

print(results_df.groupby("group")[["delta", "theta", "alpha", "beta"]].mean())

#Creating Vizualization 1 - Bar Plot

bands = ['delta','theta','alpha','beta']
#using the melt function so that we can just easily plot mulitple frequency bands in one graph without doing multiple so that its cleaner 
#the melt function will reshape the df from a wide format to long so seaborn can easily compare the categories
results_melt = results_df.melt(
    id_vars = 'group',
    value_vars = bands,
    var_name = 'band',
    value_name = 'power',
)

sns.barplot(
    data = results_melt,
    x='band',
    y = 'power',
    hue='group',
    palette = {'A': '#384860','C':'#97A6C4'},
    errorbar='se' #Chose error bar of standard error instead of standard deviation because se looked cleaner and also because I wanted to measure the uncertainty in the mean estimate rather than distribution variability
)

plt.title('Average EEG Band Power AD vs Healthy')
plt.xlabel('Frequency Band')
plt.ylabel('Power')
plt.show()

# Creating Visualization #2 - A Power Spectrum Overlay
psd_array = np.array(all_psd)
group_array = np.array(all_groups)

if np.any(group_array == 'A'):
    ad_psd = psd_array[group_array == 'A'].mean(axis=0)
    plt.plot(freqs_saved, ad_psd, label='Alzheimers')

if np.any(group_array == 'C'):
    hc_psd = psd_array[group_array == 'C'].mean(axis=0)
    plt.plot(freqs_saved, hc_psd, label='Healthy')

plt.xlabel('Frequency in Hz')
plt.ylabel('Power')
plt.title('Average Power Spectrum')
plt.legend()
plt.show()