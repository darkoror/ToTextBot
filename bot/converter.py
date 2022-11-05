from io import BytesIO

import ffmpeg


class ConvertingError(Exception):
    """
    FFMPEG error during converting file type (.oga -> .wav)
    """
    def __init__(self, message: str, *args):
        self.message = message
        super().__init__(*args)

    def __str__(self):
        return self.message


def oga_2_wav_bytesio(file: BytesIO) -> BytesIO:
    """
    Convert .oga file to .wav
    """
    process = (
        ffmpeg
        .input('pipe:')
        .output('pipe:', format='wav')
        .run_async(pipe_stdin=True, pipe_stdout=True, quiet=True)
    )
    output_data = process.communicate(input=file.getbuffer())[0]
    if process.returncode != 0:
        raise ConvertingError(f'Something went wrong. FFMPEG return code != 0. Error: {process.errors}')

    return BytesIO(output_data)
