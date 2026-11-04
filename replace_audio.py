import subprocess
import os

def replace_audio_in_video(input_video_path, input_audio_path, output_video_path):
    """
    Substitui o áudio de um vídeo pelo áudio de um arquivo separado usando FFmpeg.

    Args:
        input_video_path (str): O caminho para o arquivo de vídeo original (ex: .mp4, .mkv).
        input_audio_path (str): O caminho para o arquivo de áudio gerado (ex: .mp3).
        output_video_path (str): O caminho para o novo arquivo de vídeo com o áudio substituído.
    """
    if not os.path.exists(input_video_path):
        print(f"Erro: O arquivo de vídeo de entrada '{input_video_path}' não foi encontrado.")
        return
    if not os.path.exists(input_audio_path):
        print(f"Erro: O arquivo de áudio de entrada '{input_audio_path}' não foi encontrado.")
        return

    # Comando FFmpeg para substituir o áudio
    # -i: especifica o arquivo de entrada
    # -map 0:v:0: seleciona a primeira trilha de vídeo do primeiro arquivo de entrada
    # -map 1:a:0: seleciona a primeira trilha de áudio do segundo arquivo de entrada (seu novo áudio)
    # -c:v copy: copia o codec de vídeo original sem re-codificar (mantém a qualidade e é mais rápido)
    # -c:a aac: re-codifica o novo áudio para AAC (formato comum para vídeo, pode mudar se preferir)
    # -b:a 192k: define o bitrate do áudio para 192 kbps (boa qualidade, ajuste conforme necessário)
    # -shortest: garante que o vídeo final não seja mais longo que a duração do á áudio mais curto
    #            (útil se o áudio gerado for mais curto que o vídeo original)
    command = [
        "ffmpeg",
        "-i", input_video_path,
        "-i", input_audio_path,
        "-map", "0:v:0",  # Seleciona a primeira stream de vídeo do primeiro input (o vídeo original)
        "-map", "1:a:0",  # Seleciona a primeira stream de áudio do segundo input (seu novo áudio)
        "-c:v", "copy",   # Copia o vídeo sem re-codificar (muito mais rápido e sem perda de qualidade)
        "-c:a", "aac",    # Re-codifica o áudio para AAC (codec comum para vídeo)
        "-b:a", "192k",   # Bitrate do áudio (ajuste conforme a qualidade desejada)
        "-shortest",      # Garante que o vídeo de saída tenha a duração da stream mais curta (áudio ou vídeo)
        "-y",             # Sobrescreve o arquivo de saída se ele já existir sem perguntar
        output_video_path
    ]

    print(f"Executando comando FFmpeg:\n{' '.join(command)}\n")

    try:
        # Executa o comando FFmpeg
        # capture_output=True: captura stdout e stderr
        # text=True: decodifica stdout e stderr como texto
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Áudio substituído com sucesso! Novo vídeo salvo em: {output_video_path}")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar FFmpeg:")
        print(f"Comando: {e.cmd}")
        print(f"Código de retorno: {e.returncode}")
        print(f"Saída padrão (stdout): {e.stdout}")
        print(f"Saída de erro (stderr): {e.stderr}")
    except FileNotFoundError:
        print("Erro: FFmpeg não encontrado. Certifique-se de que o FFmpeg está instalado e no seu PATH.")
        print("Se você já instalou, tente fechar e reabrir seu terminal ou IDE.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

# --- Exemplo de Uso ---
if __name__ == "__main__":
    # Certifique-se de ter um arquivo de vídeo de exemplo e o áudio gerado anteriormente
    # Crie um vídeo dummy para teste se não tiver um real
    # Exemplo: um vídeo MP4 simples chamado "video_original.mp4"
    # e o áudio gerado pelo script anterior "audio_sincronizado.mp3"

    # --- Criação de arquivos dummy para teste (opcional) ---
    # Para testar este script sem ter um vídeo real:
    # 1. Certifique-se que o FFmpeg está instalado e no PATH.
    # 2. Descomente as linhas abaixo para criar um vídeo dummy e um áudio dummy.
    # Isso simula a existência dos arquivos necessários.

    # Cria um vídeo dummy de 10 segundos
    dummy_video_path = "video_original.mp4"
    if not os.path.exists(dummy_video_path):
        print(f"Criando vídeo dummy '{dummy_video_path}' para teste...")
        dummy_video_command = [
            "ffmpeg", "-f", "lavfi", "-i", "color=c=blue:s=1280x720:d=10",
            "-f", "lavfi", "-i", "sine=frequency=1000:duration=10",
            "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "libx264", "-c:a", "aac", "-b:a", "128k", "-pix_fmt", "yuv420p",
            dummy_video_path, "-y"
        ]
        try:
            subprocess.run(dummy_video_command, check=True, capture_output=True, text=True)
            print(f"Vídeo dummy '{dummy_video_path}' criado com sucesso.")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao criar vídeo dummy: {e.stderr}")
            exit()
        except FileNotFoundError:
            print("FFmpeg não encontrado. Não foi possível criar vídeo dummy.")
            exit()

    # Cria um áudio dummy de 8 segundos (para mostrar o efeito de -shortest)
    dummy_audio_path = "audio_sincronizado.mp3"
    if not os.path.exists(dummy_audio_path):
        print(f"Criando áudio dummy '{dummy_audio_path}' para teste...")
        dummy_audio_command = [
            "ffmpeg", "-f", "lavfi", "-i", "sine=frequency=440:duration=8",
            "-c:a", "mp3", "-b:a", "192k", dummy_audio_path, "-y"
        ]
        try:
            subprocess.run(dummy_audio_command, check=True, capture_output=True, text=True)
            print(f"Áudio dummy '{dummy_audio_path}' criado com sucesso.")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao criar áudio dummy: {e.stderr}")
            exit()
        except FileNotFoundError:
            print("FFmpeg não encontrado. Não foi possível criar áudio dummy.")
            exit()
    # --- Fim da criação de arquivos dummy ---

    video_input = "output.mp4"     # Seu vídeo original
    audio_input = "output_audio.mp3"     # O áudio gerado a partir do SRT
    video_output = "video_com_novo_audio.mp4" # O novo vídeo com o áudio substituído

    replace_audio_in_video(video_input, audio_input, video_output)

    # Opcional: Limpar arquivos dummy após o teste
    # os.remove(dummy_video_path)
    # os.remove(dummy_audio_path)