

""" 
문제 기록 

Traceback (most recent call last):
  File "D:\AI\Multimodal\src\sense\proto_py\proto_stt.py", line 35, in <module>
    from path import model_download_root
ModuleNotFoundError: No module named 'path'

해결 방법 서치: 
pip install -e .
(.venv) PS D:\AI\Multimodal> pip install -e .                            
Obtaining file:///D:/AI/Multimodal
  Installing build dependencies ... done
  Checking if build backend supports build_editable ... done
  Getting requirements to build editable ... done
  Preparing editable metadata (pyproject.toml) ... done
Building wheels for collected packages: multimodal
  Building editable for multimodal (pyproject.toml) ... done
  Created wheel for multimodal: filename=multimodal-0.0.0-0.editable-py3-none-any.whl size=1186 sha256=c9e9765c4ae820c8fe20f35ff2414f10c6433472fc2d0bcd4733b9c7f42e0802
  Stored in directory: C:\Users\funny\AppData\Local\Temp\pip-ephem-wheel-cache-nclqw9kz\wheels\4f\16\e3\5a1918f2d9f8f995fedd951d76da73e9e4c7fb2909c0d246bc
Successfully built multimodal
Installing collected packages: multimodal
Successfully installed multimodal-0.0.0

[notice] A new release of pip is available: 24.0 -> 26.2.1
[notice] To update, run: python.exe -m pip install --upgrade pip
(.venv) PS D:\AI\Multimodal> 
"""
"""

Traceback (most recent call last):
  File "D:\AI\Multimodal\src\sense\proto_py\proto_stt.py", line 35, in <module>
    from path import model_download_root
ModuleNotFoundError: No module named 'path'

"""


# import sys
# import os
# print(os.path.dirname(os.path.abspath(__file__)))
# print(os.path.abspath(__file__))
# print(sys.path)


# import os
# import sys
# # 현재 이 파일의 상위 디렉토리
# # current_dir = os.path.dirname(os.path.abspath(__file__))
# # parent_dir = os.path.dirname(current_dir)
# current_dir = os.path.dirname(__file__)
# print(current_dir)


# import sys
# for p in sys.path:
#     print(p)

from pathlib  import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

print(PROJECT_ROOT)