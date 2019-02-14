import servicemanager
import socket
import sys, os
import win32event
import win32service
import win32serviceutil

def installsvc(service):
    win32serviceutil.InstallService(
        service._svc_reg_class_,
        service._svc_name_,
        service._svc_display_name_,
        startType = win32service.SERVICE_AUTO_START,
        description = service._svc_description_
        )

def removesvc(service):
    win32serviceutil.RemoveService(service._svc_name_)
    
class WinService(win32serviceutil.ServiceFramework):
    _svc_name_ = "ServiceName"
    _svc_display_name_ = "Windows Service"
    _svc_reg_class_ = '%s.%s' % ("WinService", _svc_name_)
    _svc_description_ = "Windows Service Description"
    
    def __init__(self, args):             
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        rc = None
        
        while rc != win32event.WAIT_OBJECT_0:
            pass        
            rc = win32event.WaitForSingleObject(self.hWaitStop, 5000)
			
if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(WinService)
        servicemanager.StartServiceCtrlDispatcher()
    elif sys.argv[1] == 'install':
        try:
            installsvc(WinService)
        except:
            removesvc(WinService)
            installsvc(WinService)
            print("Service " + WinService._svc_name_ + " reinstalled.")
        else:
            print("Service " + WinService._svc_name_ + " installed.")
    elif sys.argv[1] == 'remove':
        removesvc(WinService)
        print("Service " + WinService._svc_name_ + " removed.")
    else:
        print("Please, use only 'install' or 'remove' keys")
