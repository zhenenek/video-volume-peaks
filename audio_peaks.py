import argparse
import json
import subprocess
import tempfile
import numpy as np
import librosa
import matplotlib.pyplot as plt
import os


def extract_audio(input_video_path, target_sr=16000):
    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    temp_wav_path = temp_file.name
    temp_file.close()

    cmd = [
        "ffmpeg", "-y",
        "-i", input_video_path,
        "-ac", "1",
        "-ar", str(target_sr),
        temp_wav_path
    ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode("utf-8"))

    return temp_wav_path


def compute_rms_db(wav_path, window_duration_ms=50):
    y, sr = librosa.load(wav_path, sr=None, mono=True)
    frame_length = int(sr * window_duration_ms / 1000)
    hop_length = frame_length

    rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
    rms_db = librosa.amplitude_to_db(rms, ref=np.max)

    return rms_db


def find_peaks(rms_db):
    median_db = np.median(rms_db)
    threshold_db = median_db + 6

    peaks = []
    for i, val in enumerate(rms_db):
        if val > threshold_db:
            score = min((val - threshold_db) / 20, 1.0)
            peaks.append((i, score))

    return peaks, threshold_db


def peaks_to_frames(peaks, fps=25):
    frames = []
    for idx, score in peaks:
        frames.append({"frame": int(idx * fps), "score": round(float(score), 2)})
    return frames


def save_json(data, output_path="peaks.json"):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def plot_graph(rms_db, threshold_db, peaks, output_path):
    plt.figure(figsize=(12, 4))
    plt.plot(rms_db, label="RMS [dB]")
    plt.axhline(threshold_db, color="red", linestyle="--", label="Threshold")

    peak_indices = [i for i, _ in peaks]
    peak_values = [rms_db[i] for i in peak_indices]
    plt.scatter(peak_indices, peak_values, color="red", label="Peaks")

    plt.xlabel("Window (50 ms)")
    plt.ylabel("Volume [dB]")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="detect volume peaks in video")
    parser.add_argument("input", help="path to .mp4 video file")
    parser.add_argument("--plot", help="path to save PNG plot")
    args = parser.parse_args()

    wav_path = None
    try:
        wav_path = extract_audio(args.input)
        rms_db = compute_rms_db(wav_path)
        peaks, threshold_db = find_peaks(rms_db)
        frames = peaks_to_frames(peaks)

        save_json(frames)
        print(f"[OK] found peaks: {len(frames)}. saved to peaks.json")

        if args.plot:
            plot_graph(rms_db, threshold_db, peaks, args.plot)
            print(f"[OK] plot saved: {args.plot}")

    except Exception as e:
        print(f"[error] {e}")

    finally:
        if wav_path and os.path.exists(wav_path):
            os.remove(wav_path)


if __name__ == "__main__":
    main()
