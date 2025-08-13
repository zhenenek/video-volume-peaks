скрипт анализирует громкость аудио в видеофайле, находит пики громкости и сохраняет их в формате JSON.
при необходимости строит график RMS [dB] vs окно с отмеченными пиками и пороговой линией.

**требования:**

* Python 3.8+

* установленные библиотеки:

```pip install numpy librosa matplotlib```

* установленный FFmpeg

https://ffmpeg.org/download.html (после установки убедитесь, что FFmpeg добавлен в переменную окружения PATH)


**запуск:**

1.базовый (только поиск пиков и сохранение JSON):

  ```*python audio_peaks.py hard_09.mp4*```

2. с построением графика:

  ```*python audio_peaks.py hard_09.mp4 --plot myplot.png*```


hard_09.mp4 — путь к видеофайлу

myplot.png — имя или путь для сохранения графика 

<ins>оба файла должны находиться в одной папке с audio_peaks.py</ins>



**пример графика:**

<img width="1291" height="408" alt="image" src="https://github.com/user-attachments/assets/e0026349-349c-4b0e-b29f-7a4fc8b427f4" />
