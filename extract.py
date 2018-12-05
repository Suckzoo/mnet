import os


runners = ['traditional', 'mnet_bd_sum', 'mnet_bd_wg_sum', 'mnet_branch_no', 'mnet_relation']

def get_row(trial, runner):
    gens = []
    for deepness in (5, 10, 15, 20):
        fname = f'manual_3_{deepness}.txt'
        out_file = f'trial_{trial}/{runner}/{fname}/stdout'
        filesize = os.stat(out_file).st_size
        with open(out_file, 'r') as f:
            f.seek(filesize - 200)
            result = f.read()
            gen = result.split('generation : ')[1]
            gens.append(gen)
    return ', '.join(gens)

def main():
    global runners
    with open('report.out', 'w') as fw:
        for runner in runners:
            for trial in range(1, 2):
            # for trial in range(1,21):
                fw.write(f'{runner}\n')
                fw.write(get_row(trial, runner))
                fw.write('\n')

if __name__ == '__main__':
    main()