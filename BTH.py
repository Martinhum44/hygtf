import cv2

def hexifyImage(path) -> list:
  try:
    with open(path, "rb") as b:
      return [hex(byte) for byte in b.read()]
  except FileNotFoundError:
    print(f"file {path} not found")
    return []

def getSize(path):
  with open(path, "rb") as b:
    bytes = [byte for byte in b.read()]
    return len(bytes)

def getBinary(path) -> list:
  try:
    with open(path, "rb") as b:
      return [byte for byte in b.read()]
  except FileNotFoundError:
    print(f"file {path} not found")
    return []



