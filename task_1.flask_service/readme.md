### Задание 1.

<details>
 <summary>Описание</summary>
  <p> 
    Напишите web-сервис на python, у которого будет html страничка с кнопкой upload mp3. Web-сервис должен преобразовать аудиозапись в изображение её частотного спектра и показать на странице.
  </p>
</details>


**1. Установка необходимых библиотек**

1. <code>pip install -r requirements.txt</code>
2. Install [FFmpeg](https://github.com/BtbN/FFmpeg-Builds/releases)
    1. Add path to FFmpeg/bin to glopal environment PATH 

Или

1. <code>conda install flask werkzeug librosa matplotlib numpy ffmpeg</code>

Через Anaconda ffmpeg ставится и работает без проблем, а напрямую через pip нет.

**2. Запуск демо**

- <code>python main.py</code>

- Или запустить main.py через IDEA

**3. Использование**

Открыть в браузере страницу:
- http://127.0.0.1:8000/

