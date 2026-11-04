# TV2

Ferramentas em Python para transcrever, traduzir e dublar vídeos.

## Funcionalidades

- **`app.py`** — Aplicação Streamlit que recebe um vídeo, extrai o áudio, transcreve a fala com Faster Whisper e gera um arquivo de legenda `.srt`, traduzindo o texto para o idioma escolhido (en, es, fr, de, it, pt).
- **`generate_audio.py`** — Gera um áudio narrado (texto-para-fala com gTTS) a partir de um arquivo `.srt`, ajustando a duração de cada trecho para casar com os tempos das legendas.
- **`replace_audio.py`** — Usa o FFmpeg para substituir a trilha de áudio original de um vídeo por um novo áudio (ex: o gerado por `generate_audio.py`), mantendo o vídeo sem recodificação.

## Fluxo de uso

1. Rode `app.py` para transcrever e traduzir o vídeo, gerando o `.srt`.
2. Rode `generate_audio.py` para transformar o `.srt` traduzido em áudio dublado.
3. Rode `replace_audio.py` para substituir o áudio do vídeo original pelo áudio dublado.

## Como executar

```
streamlit run app.py
```

(comando também disponível em `command.txt`)

## Dependências

- streamlit
- faster-whisper
- moviepy
- translate
- pysrt
- gTTS
- pydub
- tqdm
- FFmpeg (instalado e disponível no PATH)

## Estrutura

- `files/` e `side/` — pastas de saída/temporárias (ignoradas pelo Git).
