from time import sleep
import cProfile
import sys

def main():
    child_a()
    child_a()
    child_b()


def child_a():
    print('In A')
    sleep(1)


def child_b():
    print('In B')
    sleep(1)
    grandchild_c()
    grandchild_d()


def grandchild_c():
    print('In C')
    sleep(1)


def grandchild_d():
    print('In D')
    sleep(1)


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '--self-profile':

        profiler = cProfile.Profile()
        output_file = 'output.prof'

        print('Starting self-profiling...')

        profiler.enable()
        main()
        profiler.disable()

        profiler.dump_stats(output_file)
        print(f'...finished, wrote output to "{output_file}"')

    else:
        main()
