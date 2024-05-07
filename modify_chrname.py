import argparse
import gzip
import subprocess
import sys


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--fasta', dest='f', type=str, required=False)
    parser.add_argument('-g', '--gff', dest='g', type=str, required=False)
    parser.add_argument('-t', '--tsv', dest='t', type=str, required=False)
    parser.add_argument('-m', '--mode', dest='m', type=str, required=False)
    parser.add_argument('-of', '--out_fasta', dest='of', type=str,
                        required=False)
    parser.add_argument('-og', '--out_gff', dest='og', type=str,
                        required=False)
    parser.add_argument('-ot', '--out_txt', dest='ot', type=str,
                        required=False)
    parser.add_argument('-bgzip', '--bgzip', dest='bgzip', type=str,
                        default='/home/tools/bgzip', required=False)
    args = parser.parse_args()
    return args


class modify_chrname:
    def chromname_dict(self, args):
        self.chrom_dict = {}
        if args.t.endswith('.gz'):
            itsv = gzip.open(args.t, mode='rt')
            line = itsv.readline()
        else:
            itsv = open(args.t, mode='rt')
            line = itsv.readline()
            while line:
                if args.t.endswith(('.csv', '.csv.gz')):
                    chrom_names = line.split(',')
                else:
                    chrom_names = line.split('\t')
                print(chrom_names)
                self.chrom_dict[chrom_names[0].strip().strip('"')] =\
                    chrom_names[1].strip()
                line = itsv.readline()
                if len(line) > 0:
                    continue
        print(self.chrom_dict)
        return

    def modify_fasta(self, args):
        write_per = 1000
        if args.f.endswith('.gz'):
            ifasta = gzip.open(args.f, mode='rt')
        else:
            ifasta = open(args.f, mode='rt')
        if args.of.endswith('.gz'):
            ofasta = open(args.of[:-3], mode='w')
        else:
            ofasta = open(args.of, mode='w')
        line = ifasta.readline()
        self.tmp_lines_fasta = []
        self.ovnum = 0
        while line:
            self.ovnum += 1
            if line.startswith('>'):
                chrom_name_bf = line.strip('>').strip()
                chrom_name_af = self.chrom_dict[chrom_name_bf]
                self.tmp_lines_fasta.append('>' + chrom_name_af)
            else:
                self.tmp_lines_fasta.append(line.strip())
            if self.ovnum % write_per == 0:
                if self.ovnum - write_per == 0:
                    outtxt_fasta = '\n'.join(self.tmp_lines_fasta)
                else:
                    outtxt_fasta = '\n' + '\n'.join(self.tmp_lines_fasta)
                print(f'{self.ovnum} done')
                ofasta.write(outtxt_fasta)
                self.tmp_lines_fasta = []
            line = ifasta.readline()
            if len(line) > 0:
                continue
        outtxt_fasta = '\n' + '\n'.join(self.tmp_lines_fasta)
        ofasta.write(outtxt_fasta)
        ofasta.close()
        if args.of.endswith('.gz'):
            subprocess.run(f"{args.bgzip} {args.of[:-3]}", shell=True)

    def modify_gff(self, args):
        write_per = 10000
        if args.g.endswith('.gz'):
            igff = gzip.open(args.g, mode='rt')
        else:
            igff = open(args.g, mode='rt')
        if args.og.endswith('.gz'):
            ogff = open(args.og[:-3], mode='w')
        else:
            ogff = open(args.og, mode='w')
        line = igff.readline()
        headers = []
        self.tmp_lines_gff = []
        self.ovnum = 0
        while line:
            if line.startswith('#'):
                headers.append(line.strip())
                line = igff.readline()
                continue
            elif self.ovnum == 0:
                ogff.write('\n'.join(headers))
            self.ovnum += 1
            data = line.strip().split(sep='\t')
            chrom_name_bf = data[0]
            chrom_name_af = self.chrom_dict[chrom_name_bf]
            data[0] = chrom_name_af
            self.tmp_lines_gff.append('\t'.join(data))
            line = igff.readline()
            if self.ovnum % write_per == 0:
                outtxt_gff = '\n' + '\n'.join(self.tmp_lines_gff)
                print(f'{self.ovnum} done')
                ogff.write(outtxt_gff)
                self.tmp_lines_gff = []
            if len(line) > 0:
                continue
        outtxt_gff = '\n' + '\n'.join(self.tmp_lines_gff)
        ogff.write(outtxt_gff)
        igff.close()
        ogff.close()
        if args.og.endswith('.gz'):
            subprocess.run(f"gzip {args.og[:-3]}", shell=True)

    def create_tsv_fasta(self, args):
        if args.f.endswith('.gz'):
            cmd = f"zgrep -i '>' {args.f} > {args.ot}"
        else:
            cmd = f"grep -i '>' {args.f} > {args.ot}"
        subprocess.run(cmd, shell=True)
        cmd = f"sed -i s/'>'//g {args.ot}"
        subprocess.run(cmd, shell=True)

    def create_tsv_gff(self, args):
        if args.g.endswith('.gz'):
            igff = gzip.open(args.g, mode='rt')
        else:
            igff = open(args.g, mode='rt')
        line = igff.readline()
        chrom_set = set()
        self.ovnum = 0
        while line:
            if line.startswith('#'):
                line = igff.readline()
                continue
            data = line.strip().split(sep='\t')
            chrom_set.add(data[0])
            line = igff.readline()
            if len(line) > 0:
                continue
        chrom_list = list(chrom_set)
        outtxt = '\n'.join(chrom_list)
        otxt = open(args.ot, mode='w')
        otxt.write(outtxt)
        igff.close()
        otxt.close()

    def run(self, args):
        if args.m == 'txt_fasta':
            self.create_tsv_fasta(args)
            sys.exit(0)
        if args.m == 'txt_gff':
            self.create_tsv_gff(args)
            sys.exit(0)
        if args.t is not None:
            self.chromname_dict(args)
        if args.f is not None:
            self.modify_fasta(args)
        if args.g is not None:
            self.modify_gff(args)


def main():
    args = argument_parser()
    mc = modify_chrname()
    mc.run(args)
    sys.exit(0)


if __name__ == '__main__':
    main()
