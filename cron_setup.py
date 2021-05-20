from crontab import CronTab
import subprocess
import os



if __name__ == "__main__":

    #init cron
    cron   = CronTab(user='eldiablo')
    

    pwd = os.getcwd()
    cron_comm = "{pwd}/hellfire.sh {pwd} >> {pwd}/stdout.log 2>&1".format(pwd=pwd)
    
    #add new cron job
    job  = cron.new(command=cron_comm, comment='cowin_api')

    #job settings
    job.minute.every(5)

    cron.write()

    '''
    result = subprocess.run(['/media/eldiablo/P3/groundzero/vaccine-availability/hellfire.sh', '>>', '/media/eldiablo/P3/groundzero/vaccine-availability/stdout.log'], stdout=subprocess.PIPE)
    print("Result: [{}]".format(result))
    '''

