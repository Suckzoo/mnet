import os


runners = ['traditional', 'mnet_bd_sum', 'mnet_bd_wg_sum', 'mnet_branch_no', 'mnet_relation']
sum_gen = [0, 0, 0, 0]

def get_row(trial, runner):
    global sum_gen
    gens = []
    for i, deepness in enumerate((5, 10, 15, 20)):
        fname = f'manual_3_{deepness}.txt'
        out_file = f'trial_{trial}/{runner}/{fname}/stdout'
        filesize = os.stat(out_file).st_size
        with open(out_file, 'r') as f:
            f.seek(filesize - 200)
            result = f.read()
            gen = result.split('generation : ')[1].strip()
            sum_gen[i] += int(gen)
            gens.append(gen)
    return ', '.join(gens)

def main():
    global runners
    global sum_gen
    with open('report.out', 'w') as fw:
        for runner in runners:
            sum_gen = [0, 0, 0, 0]
            for trial in range(1,21):
                fw.write(f'{runner}\n')
                fw.write(get_row(trial, runner))
                fw.write('\n')
            ave_gen = [gen / 20 for gen in sum_gen]
            fw.write(f'average for {runner}: {ave_gen}')

if __name__ == '__main__':
    main()
