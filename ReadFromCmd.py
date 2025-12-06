
import subprocess

def _safe_decode(byte_data: bytes) -> str:
  """Try decoding bytes with several encodings and fall back safely.

  Preference order: utf-8 (strict), utf-8 (replace), cp1252 (replace).
  """
  if not byte_data:
    return ""
  try:
    return byte_data.decode('utf-8')
  except UnicodeDecodeError:
    # try utf-8 with replacement to preserve as much as possible (emojis, unicode)
    try:
      return byte_data.decode('utf-8', errors='replace')
    except Exception:
      # final fallback to cp1252 with replacement
      return byte_data.decode('cp1252', errors='replace')


def read_data_from_cmd(command):
  # Use shell=True because some commands include pipes/filters (Windows cmd/powershell)
  p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  stdout_bytes = p.stdout.read()
  stderr_bytes = p.stderr.read()
  p.communicate()

  out = _safe_decode(stdout_bytes).strip()
  # Normalize non-breaking spaces and line endings
  out = out.replace('\u00A0', ' ')
  out = out.replace('\r\n', '\n').replace('\r', '\n')

  # If there's stderr, include it for debugging (decoded safely)
  stderr_text = _safe_decode(stderr_bytes).strip()
  if stderr_text:
    # append stderr on a new line so callers can see errors
    out = out + ('\n' + stderr_text)

  print(out)
  return out