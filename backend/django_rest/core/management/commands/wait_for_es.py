"""Configuration of wait for elasticsearch django helper command"""


from django.core.management.base import BaseCommand
import subprocess
import time
import os

# Note: everytime you update your project (Django) related .sh files, you need
#       to re-build the docker service of Django and other ones use same image
#       like celery worker.


def is_service_up(host, username, password):
    """Method to return True if service is up"""

    # Info: 1-  The recommended approach to invoking subprocesses is to use the
    #           run() function for all use cases it can handle, not call().
    #
    #       2-  You can think of each entry in the list that we pass to
    #           subprocess.run as being separated by a space. For example:
    #
    #           subprocess.run([sys.executable, "-c", "print('ocean')"])
    #
    #           translates roughly to:
    #
    #           >> /usr/local/bin/python -c "print('ocean')"
    #
    #       3-  Subprocess automatically quotes the components of the command
    #           before trying to run them on the underlying operating system so
    #           that, for example, you can pass a filename that has spaces in
    #           it.
    #
    #       4-  subprocess.run() returns a 'subprocess.CompletedProcess' object
    #           that is bound to the variable you define to store response.
    #           The 'subprocess.CompletedProcess' object includes details about
    #           the external program’s exit code and its output.
    #
    #       5-  You can capture output from subprocess by providing extra
    #           arguments, like:
    #
    #           1- stdout=subprocess.PIPE
    #           2- stderr=subprocess.PIPE
    #
    #           By default, the output of subprocess is sent to the terminal.
    #           However, if you don’t want to dump a large output onto the
    #           terminal, you can use subprocess.PIPE to send the output of one
    #           command to the next. This corresponds to the | option in Linux.
    #           Also, it's possible to capture the output (errors or response)
    #           without need to use the arguments above by using:
    #
    #           capture=True
    #
    #       6-  By default, result of 'stdout' and 'stderr' are bound as bytes,
    #           but passing the bellow keyword argument into subprocess :
    #
    #           text=True
    #
    #           instructs Python to instead decode the bytes into strings,
    #           without need to decode it by yourself using decode() method.
    #
    #       7-  the result of 'stdout' is containing trailing newline that adds
    #           implicitly.
    #
    #       8-  By default Python writes the Traceback of the unhandled
    #           exception to 'stderr'.
    #
    #       9-  It’s useful to raise an exception if a program we run exits
    #           with a bad exit code. Programs that exit with a zero code are
    #           considered successful, but programs that exit with a non-zero
    #           code are considered to have encountered an error.
    #           We can pass the bellow keyword argument to subprocess.run():
    #
    #           check=True
    #
    #           to have an exception raised if the external program returns
    #           a non-zero exit code, which is printed in 'stderr' in our
    #           terminal, then subprocess.run dutifully raised
    #           a 'subprocess.CalledProcessError' exception on our behalf in
    #           our main Python program.
    #           Alternatively, the subprocess module also includes the
    #           following method:
    #
    #           subprocess.CompletedProcess.check_returncode
    #
    #           which we can invoke for similar effect (raising exception):
    #
    #           result = subprocess.run(
    #                       [sys.executable, "-c", "raise ValueError('oops')"]
    #                   )
    #           result.check_returncode()
    #
    #       10- subprocess.run() includes the 'timeout' argument to allow you
    #           to stop an external program if it is taking too long to
    #           execute, which lead to raise the exception:
    #
    #           subprocess.TimeoutExpired
    #
    #       11- Sometimes programs expect input to be passed to them via
    #           'stdin', The 'input' keyword argument to subprocess.run()
    #           allows you to pass data (should be Byte type) to the 'stdin' of
    #           the subprocess. For example:
    #
    #           result = subprocess.run(
    #                         [
    #                           sys.executable,
    #                           "-c",
    #                           "import sys; print(sys.stdin.read())"
    #                          ],
    #                          input=b"underwater"
    #                    )
    #           We’ll receive output like the following after running this
    #           code.

    # The command is consisting of multiple commands:
    # 1- curl -Is <url> -> outputs just the headers, the response:
    #
    #    HTTP/1.1 200 OK
    #    X-elastic-product: Elasticsearch
    #    content-type: application/json
    #    content-length: 541
    #
    # 2- grep HTTP -> filters to the HTTP response header, will grep:
    #
    #    HTTP/1.1 200 OK
    #
    # 3- cut -d ' ' -f2 -> trims the output to the second "word", in this case
    #                      the status code.
    #
    cmd = f"curl -Is -u {username}:{password} {host} " \
          f"| grep HTTP | cut -d ' ' -f2"

    service_up = False

    while service_up is False:
        # call the command
        result = subprocess.run(
            ["sh", "-c", cmd],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # return output of the powershell command
        # Note: alternatively you can use: result.returncode()
        out = result.stdout.decode().strip()

        if out == '200':
            service_up = True
        else:
            time.sleep(3)

    return True


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        """Entrypoint for command."""

        self.stdout.write(
            'Waiting for elasticsearch cluster to be up and ready...'
        )

        elasticsearch_host = os.getenv('ELASTICSEARCH_HOSTS')
        host_username = os.getenv('ELASTIC_USERNAME')
        host_password = os.getenv('ELASTIC_PASSWORD')

        self.stdout.write('Trying to connect to elasticsearch service...')

        is_service_up(elasticsearch_host, host_username, host_password)

        self.stdout.write(f'{elasticsearch_host} cluster is up...')

        cmd = f'curl -u {host_username}:{host_password} ' \
              f'{elasticsearch_host}/_cluster/health?pretty | ' \
              f'grep -E "green" || exit 1'

        es_ready = False

        while es_ready is False:
            result = subprocess.run(
                ["sh", "-c", cmd],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # return system-exit code of the command
            res = str(result.returncode).strip()

            # exit code 1 means the current status of elasticsearch is not
            # green (red or yellow).
            if res == '1':
                self.stdout.write(
                    f'{elasticsearch_host} cluster not ready yet, '
                    f'waiting 3 seconds...'
                )
                time.sleep(3)
            else:
                # if there is no exit code or 0, means elasticsearch is ready.
                es_ready = True

        self.stdout.write(
            self.style.SUCCESS(f'{elasticsearch_host} cluster is up and ready')
        )
